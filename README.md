# check-anonymity

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://gitlab.ifca.es/sainzj/check-anonymity/-/blob/main/LICENSE)

**Author:** Judith Sáinz-Pardo Díaz (IFCA - CSIC).

**Description:** Check if the following privacy-preserving techniques are verified and the value of the parameters associated with each of them:
- [x] **k-anonymity**
- [x] **(α, k)-anonymity**
- [x] **l-diversity**
- [x] **Entropy l-diversity**
- [ ] **Recursive (c,l)-diversity**
- [x] **Basic β-likeness**
- [x] **Enhanced β-likeness**
- [ ] **t-closness**
- [ ] **m-invariance**
- [x] **δ-disclosure privacy**
- [ ] **δ-presence**

## Usage (examples)
1. Example using the [_adult dataset_](https://archive.ics.uci.edu/ml/datasets/adult). First, note that in de the folder _Data_ there are 3 files in which the dataset adult has been anonymized in different ways. Running _check_adult_anonymity.py_, we obtain the values of _k_, _α_, _l_, _entropy-l_, _β_ (for basic β-likeness), _β_ (for enhanced β-likeness) and _δ_ (for δ-disclosure privacy) and associated to each of the 3 files, and a new file for each of them is saved, verifying now l-diversity with l=2.
2. Example using the [_drug type dataset_](https://www.kaggle.com/datasets/prathamtripathi/drug-classification), with the original data and with the data obtained after performing k-anonymization with k=5 with [ARX](https://arx.deidentifier.org/). Running _check_drug_data_anonymity.py_, we obtain the values of _k_, _α_, _l_, _entropy-l_, _β_ (for basic β-likeness), _β_ (for enhanced β-likeness) and _δ_ (for δ-disclosure privacy) associated to each of the 2 datasets, and a new file for each of them is saved, verifying now l-diversity with l=2 (original data) and l=3 (anonymized data).
3. Example using the [_stroke prediction dataset_](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset) with the original data and with the data obtained after performing k-anonymization with k=2, 4, 10, 25, 19, 20, 22 and 25 with [ARX](https://arx.deidentifier.org/). Running _check_drug_data_anonymity.py_, we obtain the values of _k_, _α_, _l_, _entropy-l_, _β_ (for basic β-likeness), _β_ (for enhanced β-likeness) and _δ_ (for δ-disclosure privacy) associated to each datset, and a new file for each of them is saved, verifying now l-diversity with l=2.

## About the data
As mentioned in the previous section, different datasets are used for testing purposes, and the quasi-identifiers (QI) and sensitive attribute(s) (SA) are, in each case, the following:
- [_Adult dataset_](https://archive.ics.uci.edu/ml/datasets/adult): **QI** = ['age', 'education', 'occupation', 'relationship', 'sex', 'native-country'], **SA** = ['salary-class'].
- [_Drug type dataset_](https://www.kaggle.com/datasets/prathamtripathi/drug-classification): **QI** = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K'], **SA** = ['Drug'].
- [_Stroke prediction dataset_](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset): **QI** = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'smoking_status'], **SA** = ['stroke'].
