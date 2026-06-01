# Run DVC Full Pipeline Locally

## Setup

From repository root:

```bash
pip install -r requirements.txt
cd ml-pipeline
```

## Test Locally

Run full pipeline rebuild:

```bash
dvc repro
```

Push artifacts to configured remote (optional):

```bash
dvc push
```

Verify outputs generated:

```bash
ls -la data/processed/  # check train/test splits
ls -la models/          # check model.pkl
ls -la reports/         # check evaluation.json
```

## DVC Config

Pipeline pushes to SeaweedFS at `http://localhost:8333` bucket `dvc-storage` (pre-configured in `.dvc/config`).
