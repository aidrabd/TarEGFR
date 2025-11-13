# 🧬 TarEGFR (Targeting EGFR Resistance in NSCLC)
A **Machine Learning–Aided Drug Repurposing Tool** for predicting and screening potential **EGFR inhibitors** to overcome resistance in **non-small cell lung cancer (NSCLC)**.  

---

## 🎯 Overview
**TarEGFR** accelerates the discovery of novel therapeutics against **EGFR-driven NSCLC**, where resistance to existing EGFR inhibitors poses a major clinical challenge.  
This tool enables **rapid virtual screening** of approved anticancer drugs, natural compounds, or novel molecules by predicting their **EGFR inhibitory activity (pIC₅₀)** through a validated **Random Forest–based machine learning model**, integrated with **molecular docking and dynamics validation pipelines**.  

---

## 🚀 Key Applications
- **Drug Repurposing:** Identify existing anticancer drugs with potential EGFR inhibitory activity  
- **Virtual Screening:** Rapidly assess compound libraries for EGFR inhibition potential  
- **Lead Optimization:** Predict activity and guide structural modifications  
- **Resistance Management:** Discover inhibitors effective against resistant EGFR variants  
- **Decision Support:** Prioritize candidates for *in vitro* and *in vivo* testing  

---

## 📊 Model Performance
Our **Random Forest regression model** demonstrated strong predictive performance with excellent generalization ability:  

| Dataset | R² Score |
|----------|-----------|
| Training Set | 0.979 |
| Validation Set | 0.866 |
| Overall | **0.9017** |

The high overall R² highlights the robustness of the model in predicting EGFR inhibitory activity (pIC₅₀).  

---

## 🔬 Key Findings
Among the screened FDA-approved anticancer drugs:  

| Compound | Predicted IC₅₀ (nM) | Docking Energy (kcal/mol) | RMSD (Å) | H-bond (Key Residue) |
|-----------|--------------------|----------------------------|-----------|----------------------|
| **Idarubicin** | 184.65 | -9.98 | 1.49 ± 0.24 | MET793 |
| **Larotrectinib** | 296.64 | -9.42 | 1.34 ± 0.29 | MET793 |
| *Reference (Erlotinib)* | — | -8.91 | — | MET793 |

- Both **Idarubicin** and **Larotrectinib** exhibited higher binding affinities and more stable EGFR complexes than Erlotinib.  
- **Molecular dynamics simulations (100 ns)** confirmed stable binding conformations.  
- Predicted **cytotoxicity profiles** suggested strong activity against NSCLC cell lines.  
- Binding free energy and H-bond persistence analysis indicated consistent **interaction with MET793**, crucial for inhibitory action.  

---

## ⚙️ Installation

### Prerequisites
- Python ≥ 3.8  
- `pip` or `conda` package manager  

### Quick Install
```bash
git clone https://github.com/aidrabd/TarEGFR.git
cd TarEGFR
pip install -r requirements.txt
```

---

## 🏃‍♂️ Simple Start

### Command Line Usage
```bash
python predict.py
# Provide input file name (e.g., sample.csv) containing:
# Columns: SMILES, pIC50 (Leave pIC50 empty for prediction)
```

### 🧾 Input Format
| Column | Description |
|---------|--------------|
| **SMILES** | Simplified Molecular Input Line Entry System notation |
| **pIC50** | Predicted biological activity (keep empty for prediction) |

---

## 📖 Scientific Background
The **epidermal growth factor receptor (EGFR)** is a key regulator of tumor growth and survival.  
Abnormal EGFR signaling is a hallmark of various cancers, notably **NSCLC**, where drug resistance commonly develops against first- and second-generation inhibitors.  

**TarEGFR** was designed to accelerate *in silico* screening and repurposing of anticancer agents targeting EGFR by integrating:  
- **Machine Learning (Random Forest)** for predictive modeling  
- **Molecular Docking** for binding affinity evaluation  
- **Molecular Dynamics Simulations (100 ns)** for stability validation  
- **Bioactivity & Cytotoxicity Prediction** for biological relevance assessment  

---

## 💡 Highlights
- High model reliability (**R² = 0.9017**) with minimal overfitting  
- Identified **Idarubicin** and **Larotrectinib** as potent EGFR inhibitors  
- Stable EGFR–ligand complexes with favorable bioactivity and cytotoxicity  
- Effective in addressing **EGFR mutation–driven resistance mechanisms**  
- Ready-to-use tool for **rapid computational repurposing and screening**  

---

## ⚠️ Disclaimer
**TarEGFR** is developed for **research purposes only**.  
All predictions should be validated experimentally before any clinical or commercial application.  

---

## 📄 License
This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.  

---

## 📚 Citation
If you use **TarEGFR** in your research, please cite:  

> *Al Ashik S.A.A. et al. (2025). TarEGFR: Machine Learning–Aided Drug Repurposing Tool for EGFR Inhibition and Resistance Management in NSCLC.*

---

## 🙏 Acknowledgments
- Training data curated from **ChEMBL** and published literature  
- Molecular descriptors generated using **RDKit**  
- Molecular docking and dynamics simulations performed using **AutoDock Vina** and **GROMACS**  
- Special thanks to the **open-source bioinformatics and cheminformatics communities**
