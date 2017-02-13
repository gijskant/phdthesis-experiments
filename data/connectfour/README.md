The Connect Four model, originally from the mCRL2 example directory.
===

The original process is in `mcrl2/four_in_a_row5.mcrl2`.
An adapted version is in `mcrl2/four5.mcrl2`.

Make sure to have the correct paths configured in `config.json`.

Command to generate LPS and PBES files for the experiments:
```
mkdir -p output
../../scripts/experiments.py config.json experiments.json prepare
```

