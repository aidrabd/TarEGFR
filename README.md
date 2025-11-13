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

| Compound | Predicted IC₅₀ (nM) | Docking Energy (kcal/mol) | H-bond (Key Residue) |
|-----------|--------------------|----------------------------|----------------------|
| **Idarubicin** | 184.65 | -9.98 | MET793 |
| **Larotrectinib** | 296.64 | -9.42 | MET793 |
| *Reference (Erlotinib)* | 385.58 | -8.91 | MET793 |

- Both **Idarubicin** and **Larotrectinib** exhibited higher binding affinities and more stable EGFR complexes than Erlotinib.  
- **Molecular dynamics simulations (100 ns)** confirmed stable binding conformations.  
- Predicted **cytotoxicity profiles** suggested strong activity against NSCLC cell lines.  
- Binding free energy and H-bond persistence analysis indicated consistent **interaction with MET793**, crucial for inhibitory action.  

---

## ⚙️ Installation

### Prerequisites
- Python ≥ 3.8  
- `conda` package manager  

### Install
### Prerequisites

- Ubuntu/Linux terminal/Window Command Line

### Installation

```bash
# Clone and setup
git clone https://github.com/aidrabd/TarEGFR.git
cd TarEGFR

# Make prediction script executable
chmod +x predict.py
```

First, make sure you have conda installed:

```bash
1. Install  Miniconda (if not installed)

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

2. Activate conda base environment

Type "conda init"

Then, restart your terminal

After that, activate the base environment with:

conda activate
```

Second, make sure you have Python specific version installed:

```bash
conda create -n py312 python=3.12.9
conda activate py312
python --version
```

---

## 🏃‍♂️ Simple Start

### Command Line Usage
```bash
python predict.py
# Provide input file name (e.g., sample.csv)
# Columns required in File: SMILES, pIC50 (Leave pIC50 empty for prediction)
```

### 🧾 Input Format
| Column | Description |
|---------|--------------|
| **SMILES** | Simplified Molecular Input Line Entry System notation |
| **pIC50** | Predicted biological activity (keep empty for prediction) |
# See sample.csv file to prepare your own file.
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

---

## 🙏 Acknowledgments
- Training data curated from **ChEMBL** and published literature  
- Molecular descriptors generated using **RDKit**  
- Molecular docking and dynamics simulations performed using **AutoDock Vina** and **Schrodinger's DESMOND**  
- Special thanks to the **open-source bioinformatics and cheminformatics communities**
