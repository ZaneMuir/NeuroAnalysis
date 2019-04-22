Spike

<!--
[![Build Status](https://travis-ci.org/ZaneMuir/NeuroAnalysis.svg?branch=master)](https://travis-ci.org/ZaneMuir/NeuroAnalysis)
[![Coverage Status](https://coveralls.io/repos/github/ZaneMuir/NeuroAnalysis/badge.svg?branch=master)](https://coveralls.io/github/ZaneMuir/NeuroAnalysis?branch=master)
[![Documentation Status](https://readthedocs.org/projects/neuroanalsys/badge/?version=latest)](http://neuroanalsys.readthedocs.io/en/latest/?badge=latest)
-->

---

- readin MATLAB format spike train data and csv format stimulus marker file.
- apply linear filter with a gaussian, causal or rectangular kernel.
- simple single unit and multi unit analysis, including:
    - neuroanslysis.spike.PSTH
    - neuroanslysis.spike.crosscorrelogram

### requirements
- numpy
- pandas
- h5py
- matplotlib
- scipy

### todo
- package structure
    - [x] uniform data structure
    - [ ] reusable API and protocols
- multi unit
    - [ ] optimize crosscorrelogram and further statistical test
    - [ ] Joint PSTH
- single unit
    - [ ] inter-spike interval
    - [ ] auto-correlation
- documentations
    - [ ] references for analysis methods
    - [ ] `readthedocs` documentation
