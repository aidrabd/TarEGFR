#!/usr/bin/env python3
import argparse
import os
import sys
import pickle
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, AllChem, MACCSkeys
from rdkit.ML.Descriptors import MoleculeDescriptors

def load_rf_pickle_and_meta_from_model_path(model_path):
    rf_model = None
    meta = None
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    with open(model_path, 'rb') as fh:
        rf_model = pickle.load(fh)
    model_dir = os.path.dirname(os.path.abspath(model_path)) or '.'
    meta_path = os.path.join(model_dir, 'egfr_rf_scaler_and_selector.pkl')
    if os.path.exists(meta_path):
        try:
            with open(meta_path, 'rb') as fh:
                meta = pickle.load(fh)
        except Exception:
            meta = None
    return rf_model, meta

def compute_descriptors_for_smiles_list(smiles_list):
    desc_calc = MoleculeDescriptors.MolecularDescriptorCalculator([x[0] for x in Descriptors._descList])
    descriptors_list = []
    morgan_fps_list = []
    maccs_fps_list = []
    for smi in smiles_list:
        try:
            mol = Chem.MolFromSmiles(smi)
            if mol is None:
                d = [np.nan] * (len(desc_calc.GetDescriptorNames()) + 7)
                descriptors_list.append(d)
                morgan_fps_list.append([0]*1024)
                maccs_fps_list.append([0]*167)
                continue
            desc = desc_calc.CalcDescriptors(mol)
            desc = [float(x) if x is not None else np.nan for x in desc]
            lip = [
                float(Lipinski.NumHDonors(mol)),
                float(Lipinski.NumHAcceptors(mol)),
                float(Lipinski.NumRotatableBonds(mol)),
                float(Lipinski.NumAromaticRings(mol)),
                float(Lipinski.NumAliphaticRings(mol)),
                float(Lipinski.NumSaturatedRings(mol)),
                float(Lipinski.NumHeteroatoms(mol))
            ]
            descriptors_list.append(list(desc)+lip)
            morgan_fps_list.append(list(AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)))
            maccs_fps_list.append(list(MACCSkeys.GenMACCSKeys(mol)))
        except Exception:
            descriptors_list.append([np.nan] * (len(desc_calc.GetDescriptorNames()) + 7))
            morgan_fps_list.append([0]*1024)
            maccs_fps_list.append([0]*167)
    parts = []
    if descriptors_list:
        parts.append(np.array(descriptors_list, dtype=np.float64))
    if morgan_fps_list:
        parts.append(np.array(morgan_fps_list, dtype=np.float64))
    if maccs_fps_list:
        parts.append(np.array(maccs_fps_list, dtype=np.float64))
    if parts:
        X = np.hstack(parts)
    else:
        X = np.empty((len(smiles_list), 0))
    X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    return X

def extract_meta_objects(meta):
    variance_selector = None
    selector = None
    if isinstance(meta, dict):
        for k in ('variance_selector','var_selector','variance_select'):
            if k in meta:
                variance_selector = meta[k]; break
        for k in ('feature_selector','selector','select_k_best','SelectKBest'):
            if k in meta:
                selector = meta[k]; break
        for v in meta.values():
            if selector is None and hasattr(v, 'transform') and hasattr(v, 'get_support'):
                selector = v
            if variance_selector is None and hasattr(v, 'get_support') and not hasattr(v, 'mean_'):
                variance_selector = v
    else:
        if hasattr(meta, 'transform') and hasattr(meta, 'get_support'):
            selector = meta
        elif hasattr(meta, 'get_support') and not hasattr(meta, 'mean_'):
            variance_selector = meta
    return variance_selector, selector

def apply_preprocessing_without_scaler(X, variance_selector, selector):
    Xc = X
    try:
        if variance_selector is not None and hasattr(variance_selector, 'get_support'):
            idx = variance_selector.get_support(indices=True)
            if Xc.shape[1] >= len(idx):
                Xc = Xc[:, idx]
    except Exception:
        pass
    try:
        if selector is not None:
            if hasattr(selector, 'transform'):
                Xc = selector.transform(Xc)
            elif hasattr(selector, 'get_support'):
                idx = selector.get_support(indices=True)
                if Xc.shape[1] >= len(idx):
                    Xc = Xc[:, idx]
    except Exception:
        pass
    return np.asarray(Xc, dtype=np.float64)

def attempt_prediction_without_scaler(model, X_raw, variance_selector=None, selector=None):
    try:
        if hasattr(model, 'named_steps'):
            try:
                preds = np.array(model.predict(X_raw)).flatten()
                return preds, 'pipeline_raw'
            except Exception:
                pass
    except Exception:
        pass
    X_meta = apply_preprocessing_without_scaler(X_raw, variance_selector, selector)
    try:
        preds = np.array(model.predict(X_meta)).flatten()
        return preds, 'selectors_only'
    except Exception:
        pass
    expected = None
    if hasattr(model, 'n_features_in_'):
        try:
            expected = int(model.n_features_in_)
        except Exception:
            expected = None
    if expected is not None:
        try:
            if selector is not None and hasattr(selector, 'get_support'):
                idx = selector.get_support(indices=True)
                if len(idx) == expected:
                    X_sel = X_raw[:, idx]
                    try:
                        preds = np.array(model.predict(X_sel)).flatten()
                        return preds, 'sliced_by_selector'
                    except Exception:
                        pass
        except Exception:
            pass
        if X_raw.shape[1] >= expected:
            try:
                preds = np.array(model.predict(X_raw[:, :expected])).flatten()
                return preds, 'first_k_columns'
            except Exception:
                pass
    return None, 'failed'

def main():
    parser = argparse.ArgumentParser(description='Predict using RF model without applying scalers from meta.')
    parser.add_argument('--model', '-m', required=True, help='Path to RF model pickle')
    parser.add_argument('--input', '-i', required=True, help='CSV with SMILES column')
    parser.add_argument('--output', '-o', required=False, help='Output CSV file path')
    parser.add_argument('--output_dir', required=False, help='If --output not given, write test_output.csv into this dir')
    args = parser.parse_args()
    model_path = args.model
    input_csv = args.input
    output_file = args.output
    output_dir = args.output_dir
    if not os.path.exists(input_csv):
        print("Input CSV not found:", input_csv, file=sys.stderr)
        return 1
    if output_file is None:
        if output_dir is None:
            print("Either --output or --output_dir must be specified.", file=sys.stderr)
            return 1
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                print("Failed to create output_dir:", e, file=sys.stderr)
                return 1
        output_file = os.path.join(output_dir, 'test_output.csv')
    try:
        rf_model, meta = load_rf_pickle_and_meta_from_model_path(model_path)
    except Exception as e:
        print("Failed to load model:", e, file=sys.stderr)
        return 2
    if rf_model is None:
        print("Model failed to load for unknown reason.", file=sys.stderr)
        return 2
    df = pd.read_csv(input_csv)
    if 'SMILES' not in df.columns:
        print("Input CSV must contain 'SMILES' column.", file=sys.stderr)
        return 1
    smiles = df['SMILES'].astype(str).tolist()
    vsel_meta, selector_meta = extract_meta_objects(meta)
    variance_selector = vsel_meta
    selector = selector_meta
    X_raw = compute_descriptors_for_smiles_list(smiles)
    preds, used = attempt_prediction_without_scaler(rf_model, X_raw, variance_selector, selector)
    if preds is None:
        print(f"Random forest model failed to produce predictions (last method tried: {used}).", file=sys.stderr)
        return 3
    out_df = df.copy()
    out_df['Pred_RandomForest'] = preds
    out_df['pIC50'] = preds
    try:
        out_df.to_csv(output_file, index=False)
    except Exception as e:
        print("Failed to save output CSV:", e, file=sys.stderr)
        return 4
    return 0

if __name__ == '__main__':
    sys.exit(main())