The CMS wheel model
===

Analysis of the _wheel_ subsystem of the control software of the [CMS experiment](https://home.cern/about/experiments/cms) at the Large Hadron Collider of CERN.
The model and the properties used here are based on the verification approach described in
Y.-L. Hwong, J.J.A. Keiren, V.J J. Kusters, S. Leemans and T.A.C. Willemse (2013), 
[Formalising and analysing the control software of the Compact Muon Solenoid Experiment at the Large Hadron Collider](https://dx.doi.org/10.1016/j.scico.2012.11.009),
SCP 78(12).
A detailed description of the system and generated models are in
[arXiv:1101.5324v1](https://arxiv.org/abs/1101.5324v1).

Make sure to have the correct paths configured in `config.json`.

Command to generate LPS and PBES files for the experiments:
```
mkdir -p output
../../scripts/experiments.py config.json experiments.json prepare
```
