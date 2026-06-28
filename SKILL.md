# SKILL.md — Professional Colab Quant Trading Research Framework Rules

You are building a professional-grade BTCUSDT quantitative trading research system in Google Colab and Google Drive.

This file defines the mandatory engineering, research, backtesting, feature engineering, validation, risk management, reporting, and GitHub publishing standards for the project.

You must follow these rules before writing any notebook, Python module, configuration file, model training code, backtest engine, report, or GitHub delivery workflow.

---

## 1. Core Mission

Build a robust, leakage-safe, restart-safe, Colab-compatible BTCUSDT trading research framework.

The system must focus on:

* Advanced market structure
* Price action
* ICT concepts
* Smart Money Concepts
* Liquidity behavior
* Fair Value Gaps
* Order Blocks
* Breaker Blocks
* Mitigation logic
* Order flow
* CVD
* Futures metrics
* Volatility regimes
* Session behavior
* Risk management
* Realistic backtesting
* Walk-forward validation
* Explainable ML decisions
* Professional GitHub delivery

This is a research framework, not a gambling bot.

Do not promise profitability.

Do not build live trading execution in the first version.

---

## 2. Mandatory Environment

Everything must run inside Google Colab.

There must be no dependency on:

* Local terminal
* Local files outside Google Drive
* Docker
* Local database server
* Manual command line execution except optional GitHub push commands
* Background services
* Live trading infrastructure

Use this project root:

```python
PROJECT_ROOT = "/content/drive/MyDrive/btcusdt_quant_research"
```

Every notebook must begin with:

```python
from google.colab import drive
drive.mount("/content/drive")
```

Then:

```python
import sys
PROJECT_ROOT = "/content/drive/MyDrive/btcusdt_quant_research"
sys.path.append(f"{PROJECT_ROOT}/src")
```

All artifacts must be saved under `PROJECT_ROOT`.

---

## 3. Colab Restart-Safety Rules

Colab sessions can disconnect. Therefore every expensive step must be restart-safe.

Every notebook must:

* Save intermediate results to Google Drive
* Check whether output files already exist
* Skip completed steps unless `FORCE_REBUILD=True`
* Save logs
* Save model checkpoints
* Save Optuna studies to persistent SQLite storage
* Save feature matrices
* Save labels
* Save split definitions
* Save trained models
* Save backtest results
* Save reports
* Resume incomplete folds where possible

Never rely on in-memory state across notebooks.

---

## 4. Project Folder Standard

Create and maintain this structure:

```text
btcusdt_quant_research/
  SKILL.md
  README.md
  requirements.txt
  pyproject.toml
  .gitignore
  .env.example

  configs/
    data_config.yaml
    feature_config.yaml
    labeling_config.yaml
    model_config.yaml
    validation_config.yaml
    backtest_config.yaml
    risk_config.yaml
    github_config.yaml

  notebooks/
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

  src/
    data/
    features/
    labeling/
    models/
    validation/
    backtesting/
    risk/
    explainability/
    visualization/
    utils/

  data/
    raw/
    processed/
    feature_store/
    labels/
    events/

  models/
    checkpoints/
    trained_models/
    calibration/
    feature_importance/

  reports/
    data_quality/
    feature_analysis/
    labeling/
    validation/
    backtests/
    explainability/
    dashboards/
    github/

  logs/
  cache/
```

Do not create random files outside this structure unless explicitly necessary.

Use `.gitkeep` files to preserve empty folder structure in GitHub.

---

## 5. Notebook Design Rules

Every notebook must be executable top-to-bottom.

Every notebook must contain:

1. Title and purpose
2. Drive mount
3. Imports
4. Configuration loading
5. Reproducibility seed
6. Input file checks
7. Main computation
8. Validation checks
9. Saved outputs
10. Summary of generated artifacts
11. Clear next-step instruction

Use markdown cells to explain what each major section does.

Do not hide important logic inside unexplained cells.

Do not produce notebooks that only work once.

---

## 6. Coding Standards

All reusable logic must go into `src/`.

Notebook cells should orchestrate the workflow, not contain large duplicated functions.

Python code must use:

* Type hints where practical
* Small functions
* Clear names
* Docstrings for important functions
* Logging
* Config-driven parameters
* Deterministic seeds
* Explicit input/output paths
* Reasonable exception handling
* Vectorized operations where possible
* Parquet for large data

Avoid:

* Hardcoded magic numbers
* Silent failures
* Hidden global state
* Repeated copy-paste logic
* Dataframe mutation that is hard to trace
* Unexplained assumptions
* Massive cells with mixed responsibilities

---

## 7. Data Rules

Default symbol:

```text
BTCUSDT
```

Default market:

```text
Binance USD-M Futures
```

Fallback:

```text
Binance Spot
```

Required OHLCV timeframes:

* 1m
* 3m
* 5m
* 15m
* 30m
* 1h
* 4h
* 1d

The system should also support, when possible:

* aggTrades
* taker buy/sell volume
* funding rate
* open interest
* long/short ratio
* mark price
* liquidation data or liquidation proxies
* order book snapshots as optional data

Raw data must be saved before processing.

Processed data must never overwrite raw data.

---

## 8. Data Quality Rules

Every downloaded dataset must be validated for:

* Missing timestamps
* Duplicate rows
* Invalid OHLC relationships
* Zero or negative prices
* Negative volume
* Extreme outliers
* Unexpected gaps
* Timezone inconsistency
* Sorting errors
* Incomplete last candle
* Coverage period

For every dataset, generate a data quality report under:

```text
reports/data_quality/
```

If data quality is poor, do not continue silently. Report the issue and either fix it or mark the dataset as unreliable.

---

## 9. Absolute No-Leakage Rules

Data leakage is the most dangerous failure mode.

The project must strictly prevent look-ahead bias.

Forbidden:

* Using future candles to create current features
* Using future-confirmed swing highs/lows as real-time signals
* Using centered rolling windows
* Fitting scalers on the full dataset
* Selecting features using final test data
* Tuning thresholds using final test data
* Using labels or future returns inside feature generation
* Executing trades on the same close that generated the signal
* Using higher timeframe candle values before that candle is closed
* Using future FVG/OB/sweep information in past decisions
* Resampling higher timeframe data incorrectly
* Backtesting with impossible intrabar assumptions

Required:

* Signal generated after candle close
* Trade entry no earlier than next candle open or realistic simulated price
* Scalers fit only on train data
* Validation/test transformed only using train-fitted scalers
* Chronological splits
* Walk-forward validation
* Final untouched test set
* Explicit leakage tests

Implement leakage checks in:

```text
src/validation/leakage_checks.py
```

Every major notebook must include a leakage-safety section.

---

## 10. Multi-Timeframe Safety Rules

Higher timeframe features must only be available after the higher timeframe candle closes.

Example:

A 1h candle covering 09:00–10:00 must not be used by 5m candles before 10:00.

When aligning higher timeframe data to lower timeframe data:

* Use closed higher timeframe candles only
* Shift higher timeframe features if necessary
* Validate timestamps
* Document the alignment rule
* Add tests for availability timing

Never forward-fill an unfinished higher timeframe candle into lower timeframe rows.

---

## 11. Feature Engineering Standards

Build many features, but treat all features skeptically.

Each feature must have:

* Name
* Family
* Description
* Required input data
* Timeframe
* Availability timestamp
* Parameters
* Leakage risk level
* Missing-value behavior
* Expected interpretation

Save feature metadata to:

```text
data/feature_store/feature_metadata.json
```

Feature families must include:

* Market structure
* ICT/SMC
* Fair Value Gap
* Order Block
* Breaker Block
* Liquidity
* Displacement
* Candle quality
* Order flow
* CVD
* Futures metrics
* Liquidation proxies
* Sessions
* Volatility
* Regime
* Classical indicators as auxiliary context only
* Confluence

---

## 12. Market Structure Rules

Implement:

* Swing high
* Swing low
* Real-time swing candidate
* Confirmed swing
* Higher high
* Higher low
* Lower high
* Lower low
* BOS
* CHOCH
* MSS
* Internal structure
* External structure
* Range high
* Range low
* Premium zone
* Discount zone
* Equilibrium
* Trend leg
* Pullback leg
* Multi-timeframe alignment

Important:

Separate real-time swing candidates from confirmed swings.

Confirmed swings are useful for analysis but can easily create leakage if used incorrectly.

---

## 13. ICT / SMC Feature Rules

ICT and SMC concepts are often subjective. In this project they must be converted into strict, testable, configurable rules.

Implement mathematical definitions for:

* Fair Value Gap
* Inverse Fair Value Gap
* Balanced Price Range
* Order Block
* Breaker Block
* Mitigation Block
* Rejection Block
* Liquidity Void
* Displacement
* Dealing Range
* Premium/Discount Array
* Optimal Trade Entry approximation
* Judas Swing approximation
* Accumulation/Manipulation/Distribution proxy

Every definition must be configurable.

Never rely on vague statements like “looks like an order block.”

---

## 14. Fair Value Gap Rules

Bullish FVG baseline definition:

* Three-candle structure
* Candle 1 high < Candle 3 low
* Middle candle should show displacement
* Gap size normalized by ATR

Bearish FVG baseline definition:

* Candle 1 low > Candle 3 high
* Middle candle should show displacement
* Gap size normalized by ATR

For each FVG, compute:

* Direction
* Upper boundary
* Lower boundary
* Midpoint
* Size
* ATR-normalized size
* Percent filled
* Fully filled flag
* Partially filled flag
* Age
* Time to mitigation
* First-touch reaction
* Displacement score
* Volume confirmation
* CVD confirmation
* Premium/discount location
* Higher timeframe alignment
* Conversion into inverse FVG
* Overlap with OB
* Overlap with liquidity sweep

---

## 15. Order Block Rules

Create multiple order block definitions and compare them.

Bullish OB baseline:

* Last bearish candle before bullish displacement
* Followed by BOS/MSS or strong impulse
* Displacement exceeds ATR threshold
* Body/range ratio exceeds threshold

Bearish OB baseline:

* Last bullish candle before bearish displacement
* Followed by BOS/MSS or strong impulse

For every OB, compute:

* Direction
* High/low boundaries
* Open/close boundaries
* Midpoint
* Age
* Mitigation status
* First mitigation reaction
* Invalidation
* Displacement strength
* Volume
* CVD behavior
* Higher timeframe alignment
* Distance from price
* Overlap with FVG
* Breaker conversion
* Success/failure after mitigation

Test high-low and open-close definitions separately.

---

## 16. Liquidity Feature Rules

Implement:

* Equal highs
* Equal lows
* Relative equal highs
* Relative equal lows
* Previous day high/low
* Previous week high/low
* Previous month high/low
* Session high/low
* Asia range
* London range
* New York range
* Buy-side liquidity
* Sell-side liquidity
* Liquidity sweep
* Liquidity grab
* Stop hunt
* Sweep and reclaim
* Failed breakout
* Range deviation
* Range reclaim
* Turtle soup style reversal approximation

For each liquidity sweep, compute:

* Direction
* Swept level type
* Wick depth
* Close reclaim flag
* Reclaim speed
* Post-sweep displacement
* Post-sweep FVG creation
* Post-sweep CVD divergence
* Post-sweep volume spike
* MFE
* MAE
* Time to reaction

---

## 17. Order Flow and CVD Rules

When trade or taker data is available, compute:

* Taker buy volume
* Taker sell volume
* Delta
* Cumulative Volume Delta
* Rolling CVD slope
* CVD divergence
* Absorption proxy
* Aggressive buyer imbalance
* Aggressive seller imbalance
* Volume imbalance
* Trade count imbalance
* Large trade detection
* VWAP
* Anchored VWAP
* VWAP deviation

If raw trade data is too large:

* Aggregate to 1m
* Save compressed Parquet
* Process in chunks
* Cache results
* Avoid loading all raw trades at once

---

## 18. Volatility and Regime Rules

Implement:

* ATR
* Realized volatility
* Parkinson volatility
* Garman-Klass volatility if possible
* Rolling return volatility
* Volatility percentile
* Bollinger bandwidth
* Compression score
* Expansion score
* Range efficiency
* Trend strength
* Choppiness
* Hurst exponent optional
* ADX optional
* Volume volatility
* Regime clustering optional

Every model and backtest must report performance by regime.

---

## 19. Session Feature Rules

BTC trades 24/7, but session behavior can still matter.

Implement:

* Hour of day
* Day of week
* Weekend flag
* Daily open
* Weekly open
* Monthly open
* Asia session
* London session
* New York session
* London open
* New York open
* London/New York overlap
* Asia high/low
* London high/low
* New York high/low
* Session sweeps
* Kill zone approximation

Do not assume session features work. Test them statistically.

---

## 20. Labeling Rules

Use multiple labeling methods.

Required:

1. Forward return labels
2. Triple barrier labels
3. Event-based labels
4. Meta-labeling

Forward return labels:

* Multiple horizons
* Volatility-adjusted thresholds
* Long edge / short edge / no edge

Triple barrier labels:

* Dynamic TP
* Dynamic SL
* Time barrier
* ATR-based or structure-based barriers

Event-based labels:

Create labels only after meaningful events such as:

* Liquidity sweep
* FVG creation
* FVG mitigation
* OB mitigation
* BOS
* CHOCH
* MSS
* CVD divergence
* Session sweep
* Liquidation proxy

Meta-labeling:

* Stage 1 detects setups
* Stage 2 decides trade or skip

Labels must never be used as features.

---

## 21. Modeling Rules

Start simple.

Required baselines:

* Random signal
* Always long
* Always short
* Buy and hold
* Simple trend-following
* Simple breakout
* Simple mean reversion

Required ML models:

* Logistic Regression
* Random Forest
* Extra Trees
* HistGradientBoosting
* XGBoost
* LightGBM
* CatBoost
* Calibrated ensemble

Optional sequence models:

* LSTM
* GRU
* Temporal CNN
* Transformer encoder

Do not start with deep learning before the tabular pipeline is stable.

Every model must be compared against baselines.

---

## 22. Model Output Rules

The model should output more than direction.

Required outputs:

* Long probability
* Short probability
* No-trade probability
* Expected return
* Expected adverse excursion
* Expected favorable excursion
* Confidence score
* Suggested stop distance
* Suggested take-profit distance
* Expected holding time
* Setup type
* Trade/no-trade decision
* Regime-adjusted confidence

Use probability calibration:

* Platt scaling
* Isotonic regression
* Calibration curve
* Brier score

---

## 23. Feature Selection Rules

Because the feature set may become large, apply disciplined feature selection.

Required checks:

* Constant features
* Near-constant features
* Excessive missing values
* Obvious leakage
* Correlation clustering
* Permutation importance
* SHAP analysis
* Walk-forward feature stability
* Feature ablation
* Drift analysis optional

Never perform feature selection using the final test set.

---

## 24. Validation Rules

Never use random train/test split for financial time series.

Required validation:

* Chronological split
* Walk-forward validation
* Expanding window validation
* Rolling window validation
* Purged cross-validation where applicable
* Embargo period
* Untouched final test set

Final test data must not influence:

* Feature selection
* Threshold selection
* Hyperparameter tuning
* Model selection
* Calibration
* Risk settings

---

## 25. Backtesting Rules

Backtests must be realistic.

Mandatory assumptions:

* Signal known only after candle close
* Entry no earlier than next candle open
* Fees included
* Slippage included
* Spread proxy included
* Funding included for futures when available
* Conservative intrabar SL/TP handling
* Position sizing included
* Risk limits included
* One-position-at-a-time mode by default
* Pyramiding disabled by default
* No look-ahead bias
* No impossible fills

If both stop-loss and take-profit are touched in the same candle, assume the worse outcome by default unless using lower timeframe intrabar data.

Backtest only out-of-sample predictions.

---

## 26. Backtest Metrics

Report:

* Gross return
* Net return
* CAGR if appropriate
* Sharpe
* Sortino
* Calmar
* Max drawdown
* Profit factor
* Expectancy
* Win rate
* Average win
* Average loss
* Payoff ratio
* Exposure time
* Turnover
* Number of trades
* Average holding time
* Median holding time
* MFE
* MAE
* Fee impact
* Slippage impact
* Funding impact
* Long-only performance
* Short-only performance
* Setup-level performance
* Regime-level performance
* Session-level performance

Accuracy alone is not a trading metric.

---

## 27. Risk Management Rules

Implement a professional risk engine.

Defaults:

* Risk per trade: 0.5%
* Maximum risk per trade: 1%
* Maximum leverage: 1x initially
* Daily max loss: configurable
* Weekly max loss: configurable
* Maximum drawdown stop: configurable
* Maximum consecutive losses: configurable
* Reduce risk during drawdown
* Reduce risk during high volatility
* Skip trade if confidence is low
* Skip trade if expected value after costs is negative
* Skip trade if risk/reward is too low

Position sizing methods:

* Fixed fractional
* Volatility targeting
* Confidence-weighted sizing
* Capped Kelly fraction
* Regime-adjusted sizing

Risk management must be part of the backtest, not added afterward.

---

## 28. Confluence Engine Rules

Do not trade from a single feature.

Create a confluence engine using:

* Higher timeframe bias
* Market structure
* Liquidity sweep
* FVG
* Order block
* CVD
* Volume
* Session
* Volatility regime
* Premium/discount
* Risk/reward
* Expected value
* Model confidence

The confluence engine must output:

* Bullish score
* Bearish score
* Conflict score
* Final confluence score
* No-trade reason
* Human-readable explanation

Support both:

1. Rule-based confluence
2. ML-learned confluence

Compare both.

---

## 29. Explainability Rules

Every trade decision must be explainable.

For each trade, generate:

* Decision
* Confidence
* Setup type
* Entry
* Stop
* Take profits
* Risk/reward
* Expected value after costs
* Higher timeframe bias
* Regime
* Key bullish reasons
* Key bearish reasons
* Conflict reasons
* No-trade reason if skipped

Example:

```text
Decision: LONG
Confidence: 0.74
Setup: Sell-side liquidity sweep + bullish FVG mitigation + bullish CVD divergence
HTF Bias: Bullish
Entry: 64120
Stop: 63780
TP1: 64800
TP2: 65500
Risk/Reward: 2.1
Expected Value After Costs: Positive

Reasoning:
- Price swept previous Asia low and reclaimed the range.
- Bullish displacement created a 5m FVG.
- Price returned into the FVG midpoint while still in discount.
- CVD formed bullish divergence while price made a lower low.
- Higher timeframe structure remains bullish.
- Trade passes minimum expected value and risk/reward filters.
```

Use SHAP or permutation importance where practical.

Do not overstate explainability. Clearly mention uncertainty.

---

## 30. Reporting Rules

Generate reports under:

```text
reports/
```

Required reports:

* Data quality report
* Feature coverage report
* Feature correlation report
* Feature stability report
* Label distribution report
* Model validation report
* Walk-forward report
* Backtest report
* Regime performance report
* Setup performance report
* Cost impact report
* Overfitting risk report
* GitHub publishing report
* Final research summary

Reports may be:

* HTML
* Markdown
* CSV
* JSON
* PNG
* Interactive Plotly HTML

Every report must include enough information to judge whether the system is actually useful.

---

## 31. Robustness Rules

The system must try to falsify itself.

Required tests:

* Random label sanity check
* Shuffled feature sanity check
* Random strategy baseline
* Transaction cost stress test
* Slippage stress test
* Funding stress test
* Walk-forward degradation analysis
* Monte Carlo trade reshuffling
* Parameter sensitivity
* Feature ablation
* Bull/bear/chop period breakdown
* Long-only vs short-only breakdown
* Distribution drift report

If performance disappears after costs, say so.

If performance only works in one narrow period, say so.

If final test fails, report failure honestly.

---

## 32. Dashboard Rules

Create Colab-friendly visual analysis.

Use Plotly by default.

Required charts:

* Candlestick chart
* FVG zones
* Order block zones
* Liquidity levels
* Sweep markers
* BOS/CHOCH/MSS markers
* CVD panel
* Volume/delta panel
* Model signal markers
* Trade entries/exits
* Equity curve
* Drawdown curve
* Regime performance
* Setup performance
* Feature importance
* Latest prediction explanation

If Streamlit is impractical in Colab, save interactive Plotly HTML files to Drive.

---

## 33. Long Training Rules

For long model training:

* Save checkpoints
* Save fold results
* Save Optuna studies to SQLite
* Resume completed studies
* Resume incomplete folds
* Save best model per fold
* Save calibration objects
* Save feature list used by each model
* Save train/validation/test indices
* Save metrics after every fold

Never lose progress because of a Colab disconnect.

---

## 34. Memory Optimization Rules

Colab memory is limited.

Use:

* Parquet
* Chunked processing
* Polars where useful
* Downcast numeric columns safely
* Cached intermediate features
* Garbage collection
* Debug mode
* Full mode

Config must include:

```yaml
debug_mode: true
full_mode: false
max_rows_debug: 200000
force_rebuild: false
```

Allow switching to:

```yaml
debug_mode: false
full_mode: true
```

Do not load massive raw trade datasets into memory at once.

---

## 35. Configuration Rules

Everything important must be configurable in YAML.

Do not hardcode:

* Symbol
* Exchange
* Market type
* Timeframes
* Date ranges
* Fees
* Slippage
* Funding settings
* Risk limits
* Label horizons
* Barrier multipliers
* Feature toggles
* Model parameters
* Walk-forward windows
* Final test size
* Debug/full mode
* GitHub repository URL

Load configs through a shared utility:

```text
src/utils/config.py
```

---

## 36. Logging Rules

Every notebook and major module must log:

* Start time
* End time
* Inputs
* Outputs
* Row counts
* Date coverage
* Missing values
* File paths
* Warnings
* Errors
* Config used

Save logs to:

```text
logs/
```

Private or sensitive logs must not be pushed to GitHub.

---

## 37. Artifact Naming Rules

Use clear names.

Examples:

```text
data/raw/klines/BTCUSDT_5m_2023.parquet
data/processed/BTCUSDT_5m_clean.parquet
data/feature_store/BTCUSDT_5m_features.parquet
data/labels/BTCUSDT_5m_triple_barrier_labels.parquet
models/trained_models/lightgbm_fold_03.joblib
reports/backtests/backtest_walkforward_lightgbm.html
```

Every artifact should be traceable to:

* Symbol
* Timeframe
* Date range
* Config
* Model
* Fold
* Version if applicable

---

## 38. GitHub Repository Publishing Rules

The final project must be prepared for GitHub and pushed to:

```text
https://github.com/umutergul74/TradeBot.git
```

The GitHub repository is the canonical code repository for the project.

The repository must contain:

* Source code
* Colab notebooks
* Config files
* Documentation
* `SKILL.md`
* `README.md`
* `.gitignore`
* `.env.example`
* `requirements.txt`
* `pyproject.toml` if useful
* Reproducibility instructions
* Validation/test utilities
* Lightweight examples only when safe

The repository must not contain:

* API keys
* GitHub tokens
* Binance credentials
* Google credentials
* `.env` files
* Raw downloaded data
* Large processed datasets
* Feature stores
* Large model checkpoints
* Optuna SQLite databases
* Private logs
* Large reports
* Files containing secrets

Use Google Drive for large artifacts by default.

Use GitHub for reproducible code and documentation.

Create a professional `.gitignore` before the first commit.

Required `.gitignore` entries include:

```text
.env
.env.*
*.key
*.pem
*.sqlite
*.db
__pycache__/
.ipynb_checkpoints/
.cache/
logs/
data/raw/
data/processed/
data/feature_store/
data/labels/
data/events/
models/checkpoints/
models/trained_models/
models/calibration/
models/feature_importance/
reports/**/*.html
reports/**/*.png
reports/**/*.csv
reports/**/*.json
*.parquet
*.pkl
*.joblib
*.pt
*.pth
*.onnx
```

Use `.gitkeep` files to preserve empty folder structure where needed.

Before committing, run a safety checklist:

1. Verify `.gitignore`
2. Verify no secrets are present
3. Verify no large data files are staged
4. Verify notebooks do not contain credentials in outputs
5. Clear notebook outputs if needed
6. Run basic import tests
7. Run basic leakage tests
8. Run basic data pipeline smoke tests if feasible
9. Update README
10. Update project status

GitHub workflow:

```bash
cd /content/drive/MyDrive/btcusdt_quant_research

git init
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/umutergul74/TradeBot.git

git status
git add .
git commit -m "Initial Colab quant research framework"
git push -u origin main
```

Never hardcode GitHub tokens.

If a token is needed in Colab, request it securely using `getpass` or Colab secrets.

Example:

```python
import getpass
GITHUB_TOKEN = getpass.getpass("Enter GitHub token: ")
```

If using a temporary token-based remote URL, immediately reset the remote after pushing:

```bash
git remote set-url origin https://<TOKEN>@github.com/umutergul74/TradeBot.git
git push -u origin main
git remote set-url origin https://github.com/umutergul74/TradeBot.git
```

If GitHub authentication fails, stop and provide safe manual push instructions instead of exposing or logging credentials.

The final delivery is complete only when either:

1. The clean project has been successfully pushed to GitHub, or
2. The project is fully prepared and the exact safe manual push commands are provided because authentication is unavailable.

---

## 39. Acceptance Criteria

The project is acceptable only if it produces:

1. Runnable Colab notebooks
2. Persistent Google Drive project structure
3. `SKILL.md`
4. BTCUSDT data pipeline
5. Cleaned multi-timeframe data
6. Advanced feature store
7. Leakage-safe labels
8. Baseline models
9. ML models
10. Walk-forward validation
11. Realistic backtest
12. Risk engine
13. Trade journal
14. Explainability report
15. Interactive visual reports
16. Robustness tests
17. Final honest research report
18. Clean GitHub repository pushed to `https://github.com/umutergul74/TradeBot.git` or safely prepared with manual push instructions

---

## 40. Forbidden Behavior

Do not:

* Build a fake profitable strategy
* Hide bad results
* Ignore fees
* Ignore slippage
* Ignore funding
* Use random train/test split as final validation
* Use future data in features
* Use final test data for tuning
* Claim institutional-grade profitability without proof
* Add live trading execution
* Produce untested notebooks
* Skip data quality checks
* Skip leakage checks
* Skip baselines
* Report accuracy as the main success metric
* Overfit parameters to one historical period
* Push secrets to GitHub
* Push raw data or large model artifacts to GitHub
* Hardcode GitHub tokens
* Hardcode API keys
* Expose credentials in notebook outputs

---

## 41. Required First Implementation Order

Before implementing advanced models, complete these in order:

1. `00_colab_setup.ipynb`
2. Drive folder creation
3. `SKILL.md`
4. Config files
5. `.gitignore`
6. `.env.example`
7. Basic data downloader
8. OHLCV data quality checks
9. Cleaned/resampled OHLCV data
10. Basic market structure features
11. Basic FVG/liquidity features
12. Basic labels
13. Baseline backtest
14. Leakage checks

Only after these are working should you add:

* Order flow
* CVD
* Futures metrics
* Advanced ICT/SMC
* ML models
* Walk-forward validation
* Explainability
* Dashboard
* GitHub publishing

---

## 42. Development Style

When building the project, proceed incrementally.

For each phase:

1. Explain what will be built
2. Write the code
3. Save artifacts
4. Validate outputs
5. Report what was created
6. Mention limitations
7. Move to the next phase

Do not jump randomly between unrelated parts.

Do not create a huge unvalidated system all at once.

---

## 43. Final Research Standard

The final result must answer:

* Is there any real edge?
* Does the edge survive costs?
* Does the edge survive walk-forward validation?
* Which setups work best?
* Which setups fail?
* Which regimes are favorable?
* Which regimes are dangerous?
* Which features matter?
* Which features are unstable?
* Is the result likely overfit?
* What should be improved next?

If the answer is “no reliable edge found,” report that honestly.

A failed but honest research system is better than a fake profitable backtest.

---

## 44. Default Project Settings

Unless changed by the user, use:

```yaml
symbol: BTCUSDT
exchange: Binance
market_type: USD-M Futures
fallback_market_type: Spot
project_root: /content/drive/MyDrive/btcusdt_quant_research

lower_timeframe: 1m
execution_timeframe: 5m
secondary_execution_timeframe: 15m
higher_timeframes:
  - 1h
  - 4h
  - 1d

mode: research_backtest_only
live_trading: false

risk_per_trade: 0.005
max_risk_per_trade: 0.01
max_leverage: 1

fees_enabled: true
slippage_enabled: true
funding_enabled: true

walk_forward_validation: true
final_test_set: untouched

debug_mode: true
full_mode: false
force_rebuild: false

github_repository_url: https://github.com/umutergul74/TradeBot.git
github_branch: main
large_artifacts_in_git: false
```

---

## 45. Final Instruction to the Coding Agent

Before writing implementation code, read this file carefully.

Every notebook, module, feature, model, backtest, report, risk rule, validation method, and GitHub publishing step must comply with this `SKILL.md`.

If a requested implementation conflicts with this file, prefer the safer, more robust, more leakage-resistant, more reproducible, and more scientifically honest approach.

Build the project as if it will be reviewed by professional quant researchers, ML engineers, experienced discretionary traders, and senior software engineers.

Do not optimize for looking impressive.

Optimize for correctness, robustness, realism, reproducibility, clean GitHub delivery, and truth.
