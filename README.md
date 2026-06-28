# BTCUSDT Quantitative Trading Research & Machine Learning System

A professional-grade quantitative trading research and machine learning framework for BTCUSDT, designed to run entirely within Google Colab and Google Drive, with a clean and reproducible codebase prepared for GitHub.

This system is built to identify market regimes, estimate higher-timeframe biases, classify advanced price action setups (Smart Money Concepts, ICT, Fair Value Gaps, Order Blocks, Liquidity Sweeps), integrate order flow and CVD analysis, and train calibrated machine learning models to evaluate trading setups under strict risk management.

**This is a research and simulation framework. It does not support live trading and does not promise profitability.**

---

## Repository Structure

```text
btcusdt_quant_research/
  SKILL.md               # Engineering & Research Constitution (Rules)
  README.md              # Project overview & guide
  requirements.txt       # Python dependencies
  pyproject.toml         # Package configuration
  .gitignore             # Standard git exclusions for data, models, and secrets
  .env.example           # Template for local environment variables

  configs/               # YAML configuration files
    data_config.yaml
    feature_config.yaml
    labeling_config.yaml
    model_config.yaml
    validation_config.yaml
    backtest_config.yaml
    risk_config.yaml
    github_config.yaml

  notebooks/             # 14 Sequential Google Colab Notebooks
    00_colab_setup.ipynb
    01_data_download_binance.ipynb
    02_data_cleaning_and_resampling.ipynb
    03_feature_engineering_market_structure.ipynb
    04_feature_engineering_liquidity_ict_smc.ipynb
    05_feature_engineering_orderflow_volatility_sessions.ipynb
    06_labeling_and_event_generation.ipynb
    07_model_training_baselines_and_ml.ipynb
    08_walk_forward_validation.ipynb
    09_backtesting_and_risk_management.ipynb
    10_explainability_and_trade_journal.ipynb
    11_dashboard_and_visual_analysis.ipynb
    12_master_pipeline_runner.ipynb
    13_github_publish.ipynb

  src/                   # Reusable Python Source Code Modules
    data/                # Data downloading, cleaning, and resampling
    features/            # Market structure, ICT, SMC, FVG, OBs, CVD, sessions
    labeling/            # Triple-barrier, forward returns, meta-labeling
    models/              # Baseline and ML models, probability calibration
    validation/          # Walk-forward, purged cross-validation, leakage checks
    backtesting/         # Backtest execution, cost tracking, portfolio simulation
    risk/                # Position sizing, risk limits, drawdown controls
    explainability/      # SHAP tools, signal explainer, trade journaling
    visualization/       # Plotly charting, dashboard layouts
    utils/               # Configurations, logging, and Colab/GitHub utilities
```

---

## Getting Started in Google Colab

1. Create a folder in your Google Drive: `MyDrive/btcusdt_quant_research`.
2. Upload the `notebooks/` and `src/` directories, and the `configs/` folder to that path.
3. Open `notebooks/00_colab_setup.ipynb` in Google Colab.
4. Run the cells to mount Google Drive, install dependencies, and verify your environment.
5. Follow the notebook sequence from `00` to `13` to download data, engineer features, train models, backtest, and publish to GitHub.

---

## Core Engineering & Research Principles (`SKILL.md`)

This project is governed by the rules in `SKILL.md` (the Project Constitution). It enforces:
* **Zero Data Leakage**: No look-ahead bias, point-in-time features, training-fitted scalers only, and chronological validation.
* **Restart-Safety**: All intermediate states are persisted in Google Drive as Parquet, SQLite, or model checkpoints, enabling seamless resumption after Colab disconnects.
* **Realistic Backtesting**: Fills are executed at the open of the next candle after signal generation. Backtests incorporate trading fees, slippage, and funding rates.
* **Calibrated Explainability**: Predictions are calibrated (Platt scaling/Isotonic regression) to output true probabilities and are accompanied by human-readable trade decision cards.
