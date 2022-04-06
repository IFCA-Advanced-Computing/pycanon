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
- [ ] **Basic β-likeness**
- [ ] **Enhanced β-likeness**
- [ ] **t-closness**
- [ ] **m-invariance**
- [ ] **δ-disclosure privacy**
- [ ] **δ-presence**


## Usage (examples)
1. Example using th adult dataset. First, note that in de the folder _Data_ there are 3 files in which the dataset adult has been anonymized in different ways. Running _check_adult_anonymity.py_, we obtain the values of _k_, _alpha_, _l_, _entropy-l_, _beta_ (for basic beta) and _beta_ (for enhanced beta) associated to each of the 3 files, and a new file for each of them isa saved, verifying now l-diversity with l=2.
