Scripts for the experiments
===

Command to install dependencies:
```
pip install -r requirements.txt
```

If the `mcrl2` and `ltsmin` tools are not globally installed,
edit `config.json` to set the path where they can be found.

Command to generate LPS and PBES files for the experiments:
```
../../scripts/experiments.py config.json experiments.json prepare
```

