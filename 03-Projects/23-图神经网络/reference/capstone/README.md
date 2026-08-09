# Capstone reference submission

This directory is an executable reference implementation for `GNN-CAPSTONE`.
It is evidence that the assignment contract can be executed, not a learner
submission and not a claim that the course has produced a general-purpose GNN.

## Run

From `03-Projects/23-图神经网络/`:

```powershell
python reference/capstone/run.py --config reference/capstone/config.json --output artifacts/capstone-reference
python -m pytest -q reference/capstone/tests
```

The run creates a manifest with the exact split indices and environment,
`runs.csv` with every seed and failure field, `summary.json`, and
`error_nodes.json`. Validation loss is the only model-selection signal; test
labels are never used for early stopping or configuration selection.

## Scope

The reference uses a locally generated 120-node contextual stochastic block
model so the full protocol runs on CPU without downloading a dataset. Results
are limited to this synthetic transductive task. They must not be presented as
OGB, CS224W, inductive, production, or online A/B evidence.
