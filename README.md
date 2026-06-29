# BTCUSDT Quant Research Framework

Phase 1 model-first BTCUSDT research framework for local Codex
development and Google Colab/Drive research execution.

Phase 1 includes data, feature, label, model, validation, diagnostics,
report consistency, and performance-bundle scaffolding. Formal
backtesting, position sizing, execution simulation, dashboards, paper
trading, and live trading are Phase 2 and blocked by default.

## Approved Phase 1 Notebooks

1. `notebooks/00_colab_bootstrap_and_git_sync.ipynb`
2. `notebooks/01_data_foundation_lab.ipynb`
3. `notebooks/02_feature_label_factory_lab.ipynb`
4. `notebooks/03_model_training_lab.ipynb`
5. `notebooks/04_model_validation_diagnostics_lab.ipynb`
6. `notebooks/05_phase1_performance_package_lab.ipynb`

The sixth notebook creates a compact Phase 1 model-performance ZIP. It
does not run a backtest.

## Local Smoke Run

```bash
python -m btc_quant.cli run-experiment --config configs/experiments/debug_baseline.yaml --project-root .
```

