# BTCUSDT Colab Quant Research Framework — MASTER PROMPT v6.1 FINAL LOCKED Model-First Modular Lab

You are a senior Quant Researcher, Financial Machine Learning Engineer, Algorithmic Trading Architect, Market Microstructure Analyst, ICT/SMC/Price Action Researcher, Python Systems Engineer, Colab/Drive workflow architect, and GitHub delivery engineer.

Design and build a serious BTCUSDT trading research and machine-learning framework. This is not a simple indicator bot, not a get-rich-quick system, and not a live-trading executor. It is a leakage-safe, restart-safe, reproducible, scientific, experiment-driven research lab that runs data, feature generation, label generation, model training, model validation, diagnostics, reports, and checkpoints in Google Colab/Google Drive while source-code development is performed locally with Codex and synchronized through GitHub.

The immediate goal is **not** to build a full backtesting/risk engine. The immediate goal is to create the strongest possible **model research skeleton**: reliable data, strict timestamp discipline, leakage-safe feature and label factories, repeatable training loops, robust validation, calibration diagnostics, falsification tests, experiment registry, frozen candidate governance, Future-OOS readiness/evaluation, report consistency audit, and a Drive-saved performance ZIP that can be handed to Codex for the next iteration.

Backtesting, position sizing, execution simulation, dashboards, and risk management are **Phase 2**. Do not enter Phase 2 unless the historical Phase 1 evidence is strong enough, a candidate is frozen/pre-registered, enough mature Future-OOS rows exist, prediction-only Future-OOS evaluation has actually completed, the candidate passed, and the report consistency audit confirms the state.

Never simplify this into RSI/MACD/EMA toy code. Classical indicators may be auxiliary context only. The core must be market structure, liquidity, ICT/SMC definitions, order-flow proxies, volatility/regime features, futures positioning/pressure, session behavior, event labels, calibrated probabilities, and robust validation.

Do not promise profitability. The system must be able to report honestly that no robust edge was found.

---

## 0. Hard Corrections From Previous Drafts

Apply these corrections strictly:

1. **Do not create a GitHub publish notebook.** GitHub publishing is local Codex/developer workflow using scripts and normal Git commands.
2. **Do not put backtesting inside the Phase 1 notebook sequence.** Backtesting is Phase 2 only.
3. **Do not make the user run a Phase 1 notebook that performs backtesting.** The final Phase 1 notebook must create a model performance ZIP, not a backtest report.
4. **Do not spread the project across too many notebooks.** Use thin notebooks and strong package modules.
5. **Do not hide model weakness behind risk management, position sizing, or execution assumptions.** Model quality must be judged before Phase 2.
6. **Do not optimize for a pretty dashboard before the model skeleton is stable.** Visuals are diagnostics only in Phase 1.
7. **Do not tune on final test.** Final untouched test remains locked until a mature candidate exists.
8. **Do not push Drive artifacts to GitHub.** Only clean code, configs, notebooks, tests, and docs go to GitHub.

---

## 1. Operating Model: Codex Local Development → GitHub → Colab/Drive Research

This project has two separate environments.

### 1.1 Development Environment: Local Codex

Codex develops locally:

- source code
- configs
- tests
- docs
- notebook templates
- scripts
- CI helpers

Local development must not require large Binance datasets, Google Drive, private credentials, Colab-only APIs, or trained model artifacts.

Codex must keep modules testable with small synthetic fixtures.

### 1.2 Research Execution Environment: Google Colab + Google Drive

Colab runs:

- public market data download
- heavy feature generation
- label generation
- model training
- Optuna tuning
- walk-forward validation
- calibration diagnostics
- falsification tests
- model performance reports
- performance ZIP packaging
- checkpoints and artifact manifests

Use this root path:

```python
PROJECT_ROOT = "/content/drive/MyDrive/btcusdt_quant_research"
```

Every notebook must start with:

```python
from google.colab import drive
drive.mount("/content/drive")

import sys
from pathlib import Path
PROJECT_ROOT = "/content/drive/MyDrive/btcusdt_quant_research"
sys.path.append(f"{PROJECT_ROOT}/src")
Path(PROJECT_ROOT).mkdir(parents=True, exist_ok=True)
```

### 1.3 GitHub Sync

Clean code is pushed to:

```text
https://github.com/umutergul74/btcusdt_quant_research.git
```

Colab pulls from GitHub. Google Drive stores data, feature stores, labels, models, checkpoints, Optuna studies, reports, and performance ZIPs.

Recommended loop:

```text
Codex local edits
  ↓
local lightweight tests / static checks
  ↓
GitHub push
  ↓
Colab git pull
  ↓
run selected Phase 1 notebook/stage
  ↓
performance artifacts saved to Drive
  ↓
review ZIP / reports
  ↓
feed results to Codex
  ↓
improve code/configs
  ↓
repeat
```

---

## 2. Non-Negotiable Safety Rules

1. No live trading in v1.
2. No automatic order execution.
3. No Binance private endpoint requirement.
4. No hardcoded secrets.
5. No GitHub tokens, Binance credentials, Google credentials, API keys, passwords, or secrets in code, notebooks, configs, logs, reports, commits, or outputs.
6. No raw data, processed data, feature stores, labels, model checkpoints, trained models, Optuna SQLite databases, personal logs, or large reports in GitHub.
7. Every feature must be point-in-time safe.
8. Every label must be created after the decision timestamp and must never be used as a feature.
9. Validation must be chronological with purging/embargo when labels overlap.
10. The final test period must remain untouched until the correct gate is reached.
11. Backtest/risk/position sizing must not be used to make a weak model look strong.
12. Negative results must be reported clearly.

---

## 3. Professional Phase Plan

### Phase 1 — Model-First Research Foundation

Phase 1 is the main current focus.

Deliver:

- modular project architecture
- `SKILL.md` research constitution
- Colab/Drive/GitHub workflow
- data foundation
- feature factory
- label factory
- model training skeleton
- baseline models
- tabular ML models
- leakage checks
- walk-forward validation
- calibration diagnostics
- robustness/falsification tests
- experiment registry
- Drive-saved model performance ZIP
- Codex handoff file explaining what to improve next

Phase 1 does **not** include formal backtesting, realistic execution engine, position sizing optimization, dashboard productization, live trading, or GitHub publishing from Colab.

### Phase 2 — Backtest, Risk, Execution, Dashboard, Later

Phase 2 begins only after Phase 1 historical evidence passes, a candidate is frozen/pre-registered, Future-OOS readiness is satisfied with mature labeled rows, prediction-only Future-OOS evaluation is completed exactly as pre-registered, the candidate passes, and the report consistency audit passes.

Phase 2 may include:

- realistic out-of-sample backtesting
- execution simulator
- fees/slippage/spread/funding integration
- stop-loss/take-profit logic
- conservative intrabar assumptions
- position sizing
- risk engine
- paper-trading style simulation
- trade journal
- dashboard
- final research report

Phase 2 must not be created as a default notebook in the Phase 1 workflow. It may exist as a separate later template only after the gate is passed.


---

## 3.1 Phase 1A — Frozen Candidate + Future-OOS Gate

Historical walk-forward success is not enough to start Phase 2.

When Phase 1 identifies a promising candidate, the system must:

1. freeze the candidate,
2. save an immutable manifest,
3. hash model/config/feature/label/split/preprocessing artifacts,
4. pin the expected manifest hash in config,
5. record candidate activation state separately from immutable manifest text,
6. start a Future-OOS anchor at `anchor_data_end`,
7. wait until enough new unseen rows mature into labels,
8. run prediction-only Future-OOS evaluation without refit,
9. permit promotion only if the actual evaluation completed and passed.

Important:

```text
Data window ready != candidate passed.
Historical holdout pass != Future-OOS pass.
Candidate frozen != Phase2 allowed.
```

Phase 2 is blocked until prediction-only Future-OOS evaluation passes.

Required frozen candidate artifacts:

```text
reports/experiments/<run_id>/frozen_candidate_manifest.json
reports/experiments/<run_id>/frozen_candidate_index.csv
configs/candidate_activation.yaml
configs/future_oos.yaml
```

The manifest must include:

```yaml
candidate_id:
source_run_id:
model_profile:
feature_list_hash:
label_definition_hash:
split_definition_hash:
preprocessing_hash:
model_artifact_hash:
threshold_policy_hash:
selection_evidence_hash:
anchor_data_end:
created_at_utc:
manifest_hash:
```

The immutable manifest must not be edited after creation. Mutable activation state belongs in config/index files.

---

## 3.2 Future-OOS Readiness and Evaluation Protocol

Future-OOS means truly unseen data after the frozen candidate anchor.

Readiness must be based on mature labeled rows, not elapsed calendar time guesses.

Required fields:

```yaml
anchor_data_end:
latest_available_data_end:
new_labeled_rows:
min_rows:
min_rows_remaining:
preferred_rows:
preferred_rows_remaining:
window_data_ready:
ready_for_evaluation:
min_ready_time_utc:
min_raw_data_ready_time_utc:
preferred_ready_time_utc:
preferred_raw_data_ready_time_utc:
primary_candidate_id:
candidate_activation_valid:
evaluation_completed:
primary_candidate_passed:
promotion_allowed:
promotion_block_reason:
```

Promotion rule:

```text
promotion_allowed =
  evaluation_completed
  AND primary_candidate_passed
  AND candidate_activation_valid
  AND report_consistency_passed
  AND no_required_errors
```

Never promote from stale config state, mutable report text, unpinned manifest, historical holdout alone, or a readiness flag without actual evaluation.

---

## 3.3 Phase 1.5 — Safe Phase 2 Preparation While Waiting

While waiting for Future-OOS rows, Codex may prepare only non-influential Phase 2 scaffolding.

Allowed:

- Phase 2 design docs
- disabled guardrail modules
- runbook docs
- risk policy notes
- paper-trading skeleton clearly disabled by default
- readiness monitor code that cannot influence candidate selection

Not allowed:

- using Future-OOS data to tune
- changing the frozen candidate after anchor
- building a backtest to justify promotion
- enabling execution
- using Phase 2 results to select Phase 1 candidates

---

## 4. Approved Phase 1 Notebook Sequence

The user should run the notebooks in this order.

```text
notebooks/
  00_colab_bootstrap_and_git_sync.ipynb
  01_data_foundation_lab.ipynb
  02_feature_label_factory_lab.ipynb
  03_model_training_lab.ipynb
  04_model_validation_diagnostics_lab.ipynb
  05_phase1_performance_package_lab.ipynb
```

These are the only Phase 1 notebooks.

### 00_colab_bootstrap_and_git_sync.ipynb

Purpose:

- mount Drive
- create project folder
- install packages
- clone or pull GitHub repo
- create configs if missing
- create folder structure
- verify imports
- verify GPU
- run smoke tests
- print project status

This notebook does not push to GitHub.

### 01_data_foundation_lab.ipynb

Purpose:

- run OHLCV download stage
- run data cleaning stage
- run resampling stage
- run futures metrics stage when enabled
- run optional aggTrades/order-flow pre-aggregation when enabled
- generate data quality report

### 02_feature_label_factory_lab.ipynb

Purpose:

- run feature factory for selected feature groups
- build feature store
- validate feature availability timestamps
- run leakage checks
- build labels
- generate feature and label reports
- save feature/label metadata

### 03_model_training_lab.ipynb

Purpose:

- select experiment config
- load feature matrix and labels
- run baselines
- train tabular ML models
- run fold-local Optuna tuning when enabled
- save models/checkpoints/predictions
- save model cards and experiment registry artifacts

This is the main repeated notebook during Phase 1.

### 04_model_validation_diagnostics_lab.ipynb

Purpose:

- run chronological and walk-forward validation
- run purged/embargoed validation where labels overlap
- evaluate calibration
- confidence decile analysis
- regime/setup/session breakdown
- long/short/no-trade breakdown
- random-label sanity check
- shuffled-feature sanity check
- drift checks
- overfitting diagnostics
- Phase 1 gate evaluation

This notebook does not perform formal backtesting.

### 05_phase1_performance_package_lab.ipynb

Purpose:

- collect all Phase 1 outputs for the selected run
- build a compact performance review folder
- create a ZIP saved to Drive
- create a Codex handoff summary
- create a Phase 1 gate decision
- list exact next improvements for Codex

This notebook is the replacement for the previous backtest notebook in the Phase 1 sequence.

It must generate:

```text
reports/experiments/<run_id>/phase1_performance_bundle/
reports/experiments/<run_id>/phase1_performance_bundle_<run_id>.zip
```

The ZIP must be designed so the user can download it from Drive and give it to Codex for the next improvement cycle.

---

## 5. Phase 2 Notebook Policy

Do not create Phase 2 notebooks by default in the initial Phase 1 workflow.

After Phase 1 gate passes, Codex may create:

```text
notebooks_phase2/
  10_backtest_risk_dashboard_lab.ipynb
```

or:

```text
notebooks/
  phase2_10_backtest_risk_dashboard_lab.ipynb
```

But this must be explicitly marked as Phase 2 and not included in the normal six-notebook Phase 1 run sequence.

---

## 6. Required Project Structure

Create this structure under:

```text
/content/drive/MyDrive/btcusdt_quant_research/
```

```text
btcusdt_quant_research/
  SKILL.md
  README.md
  requirements.txt
  pyproject.toml
  .gitignore
  .env.example

  configs/
    project.yaml
    paths.yaml
    data.yaml
    features.yaml
    labels.yaml
    models.yaml
    validation.yaml
    performance_gate.yaml
    future_oos.yaml
    candidate_activation.yaml
    reports.yaml
    github.yaml
    experiments/
      debug_baseline.yaml
      full_research_template.yaml
      feature_ablation_template.yaml
      model_candidate_template.yaml

  notebooks/
    00_colab_bootstrap_and_git_sync.ipynb
    01_data_foundation_lab.ipynb
    02_feature_label_factory_lab.ipynb
    03_model_training_lab.ipynb
    04_model_validation_diagnostics_lab.ipynb
    05_phase1_performance_package_lab.ipynb

  notebooks_phase2/
    .gitkeep

  scripts/
    dev/
      colab_pull_latest.sh
      local_push_clean.sh
    quality/
      strip_notebook_outputs.py
      secret_scan.py
      check_large_files.py
      repo_preflight.py
    release/
      prepare_github_release.py
    research/
      run_stage.py
      package_phase1_performance.py

  src/
    btc_quant/
      __init__.py
      cli.py

      core/
        config.py
        paths.py
        logging.py
        seed.py
        time.py
        io.py
        memory.py
        exceptions.py

      pipeline/
        run_context.py
        stages.py
        stage_registry.py
        artifact_manifest.py
        pipeline_state.py
        checkpoints.py
        experiment_tracker.py
        schemas.py

      data/
        clients/
          binance_futures.py
          binance_spot.py
        ingestion.py
        downloader.py
        futures_metrics.py
        trades_agg.py
        cleaning.py
        resampling.py
        quality.py
        contracts.py
        parquet_store.py

      features/
        base.py
        registry.py
        metadata.py
        availability.py
        quality.py
        market_structure.py
        ict_smc.py
        fvg.py
        order_blocks.py
        liquidity.py
        candle_quality.py
        order_flow.py
        volatility.py
        futures_pressure.py
        sessions.py
        classical_context.py
        confluence.py
        matrix_builder.py

      labels/
        base.py
        forward_returns.py
        triple_barrier.py
        events.py
        meta_labeling.py
        mae_mfe.py
        quality.py
        label_store.py

      models/
        baselines.py
        preprocessing.py
        tabular.py
        calibration.py
        ensemble.py
        training.py
        prediction_schema.py
        model_registry.py
        sequence_later.py

      validation/
        splits.py
        purged_cv.py
        walk_forward.py
        leakage.py
        metrics.py
        calibration.py
        robustness.py
        overfitting.py
        drift.py
        gate.py

      performance/
        gate.py
        scorecard.py
        leaderboard.py
        bundle.py
        codex_handoff.py

      backtest_phase2/
        README_PHASE2_ONLY.md
        execution.py
        costs.py
        portfolio.py
        risk_engine.py
        metrics.py
        journal.py
        conservative_intrabar.py

      explainability/
        feature_importance.py
        shap_tools.py
        decision_explainer.py
        failure_analysis.py

      reports/
        data_quality_report.py
        feature_report.py
        label_report.py
        model_report.py
        validation_report.py
        robustness_report.py
        performance_bundle_report.py
        final_phase1_report.py

      github/
        secret_scan.py
        git_safety.py
        notebook_strip.py

  tests/
    conftest.py
    fixtures/
    test_data_contracts.py
    test_time_alignment.py
    test_feature_availability.py
    test_leakage.py
    test_labeling.py
    test_splits.py
    test_model_smoke.py
    test_metrics.py
    test_performance_gate.py
    test_secret_scan.py

  docs/
    architecture.md
    codex_local_development_workflow.md
    colab_research_workflow.md
    data_contracts.md
    feature_dictionary.md
    labeling_dictionary.md
    validation_protocol.md
    model_research_protocol.md
    phase1_performance_gate.md
    phase1_to_phase2_transition.md
    github_delivery.md

  data/
    raw/
      klines/
      trades/
      agg_trades/
      futures_metrics/
      orderbook/
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
    model_training/
    validation/
    calibration/
    robustness/
    performance_bundles/
    explainability/
    experiments/
    final/

  logs/
  cache/
```

Use `.gitkeep` files where required.

---

## 7. Pipeline Stage Registry

Implement a stage registry so notebooks and CLI use the same backend.

Approved Phase 1 stage names:

```text
bootstrap
sync_repo
data_ohlcv
data_quality
futures_metrics
aggtrades_optional
build_features
build_labels
build_research_dataset
train_baselines
train_tabular
calibrate_models
validate_walk_forward
run_falsification
run_drift_checks
evaluate_phase1_gate
package_phase1_performance
generate_phase1_reports
```

Phase 2 stage names must be clearly marked and disabled by default:

```text
backtest_phase2_later
risk_phase2_later
dashboard_phase2_later
```

Each stage must define:

- name
- phase
- inputs
- outputs
- config dependencies
- artifact manifest entries
- restart policy
- force rebuild behavior
- expected runtime class: light / medium / heavy
- leakage sensitivity level
- validation checks
- failure behavior

CLI examples:

```bash
python -m btc_quant.cli run-stage data_ohlcv --config configs/data.yaml
python -m btc_quant.cli run-stage build_features --config configs/features.yaml
python -m btc_quant.cli run-experiment --config configs/experiments/debug_baseline.yaml
python -m btc_quant.cli package-phase1 --run-id <run_id>
```

In Colab, a notebook may call:

```python
from btc_quant.pipeline.stages import run_stage
run_stage("data_ohlcv", config_name="data")
```

---

## 8. Configuration System

Use YAML configs for everything. Do not hardcode symbol, timeframes, fees, model parameters, validation splits, feature groups, artifact paths, or gate thresholds.

Default `configs/project.yaml`:

```yaml
project_name: btcusdt_quant_research
project_root: /content/drive/MyDrive/btcusdt_quant_research
mode: phase1_model_research
live_trading: false
phase2_enabled: false
debug_mode: true
full_mode: false
force_rebuild: false
max_rows_debug: 200000
random_seed: 42
timezone: UTC
```

Default `configs/data.yaml`:

```yaml
symbol: BTCUSDT
exchange: Binance
market_type: USD-M Futures
fallback_market_type: Spot
start_date: "2019-01-01"
end_date: null
lower_timeframe: 1m
execution_timeframe: 5m
secondary_execution_timeframe: 15m
higher_timeframes: [1h, 4h, 1d]
all_timeframes: [1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d]
incremental_download: true
save_format: parquet
rate_limit_safe: true
include_futures_metrics: true
include_aggtrades: false
include_orderbook: false
optional_external_context: false
```

Default `configs/features.yaml`:

```yaml
feature_groups:
  market_structure: true
  ict_smc: true
  fvg: true
  order_blocks: true
  liquidity: true
  candle_quality: true
  order_flow: true
  volatility: true
  futures_pressure: true
  sessions: true
  classical_context: true
feature_store_version: v1
require_feature_available_time: true
run_leakage_checks: true
remove_high_missing_features: true
max_missing_ratio: 0.40
correlation_report: true
```

Default `configs/models.yaml`:

```yaml
models:
  baselines: true
  logistic_regression: true
  hist_gradient_boosting: true
  random_forest: true
  extra_trees: true
  lightgbm: true
  xgboost: true
  catboost: true
  calibrated_ensemble: true
  sequence_models_later: false
selection_metric: validation_score_composite
optuna:
  enabled: true
  storage: sqlite_drive
  n_trials_debug: 20
  n_trials_full: 200
  tune_inside_folds_only: true
calibration:
  enabled: true
  methods: [platt, isotonic]
```

Default `configs/performance_gate.yaml`:

```yaml
phase1_gate:
  require_no_leakage: true
  require_data_quality_pass: true
  require_label_quality_pass: true
  require_train_only_preprocessing: true
  require_walk_forward: true
  require_calibration_report: true
  require_falsification_pass: true
  require_drift_report: true
  require_baseline_comparison: true
  require_confidence_decile_monotonicity_check: true
  require_out_of_sample_predictions: true
  allow_phase2_if_gate_status: GREEN
  manual_override_allowed: false

minimum_evidence:
  min_walk_forward_folds_debug: 3
  min_walk_forward_folds_full: 5
  min_positive_folds_ratio: 0.60
  min_baseline_improvement_ratio: 0.02
  max_calibration_ece: 0.08
  max_brier_vs_baseline_ratio: 0.98
  require_random_label_failure: true
  require_shuffled_feature_failure: true
  require_no_single_regime_dependency: true
  require_long_short_breakdown: true
  require_cost_proxy_sensitivity: true

reporting:
  gate_status_values: [RED, YELLOW, GREEN]
  default_status_if_any_required_check_fails: RED
  default_status_if_results_are_mixed: YELLOW
```

The threshold defaults are starting points, not promises of profitability. Codex may adjust them only with documented reasoning and never using the final test set or Future-OOS evaluation window.

---

## 9. Data Plan

Default market:

```yaml
symbol: BTCUSDT
exchange: Binance
market_type: USD-M Futures
fallback_market_type: Spot
```

Required OHLCV fields:

- open time UTC
- close time UTC
- open
- high
- low
- close
- volume
- quote volume
- number of trades
- taker buy base volume
- taker buy quote volume
- taker sell base volume if derivable
- taker sell quote volume if derivable
- source
- symbol
- timeframe

Futures metrics:

- funding rate
- mark price
- index price
- premium index
- open interest
- open interest statistics
- global long/short account ratio
- top trader account ratio
- top trader position ratio
- taker buy/sell volume

Trades/aggTrades optional phase:

- aggregate to 1m
- compute taker buy/sell proxy
- delta
- cumulative volume delta
- large trade proxy
- absorption proxy

Data quality checks:

- missing timestamps
- duplicate candles
- invalid OHLC
- zero volume
- incomplete latest candle
- gaps by timeframe
- timezone errors
- outliers
- volume spikes
- coverage report

Raw data must be immutable once saved. Corrections create processed outputs.

---

## 10. Timestamp and Leakage Rules

Every dataset or feature table must preserve relevant timestamps:

- `bar_open_time`
- `bar_close_time`
- `event_time`
- `feature_available_time`
- `decision_time`
- `label_start_time`
- `label_end_time`
- `created_at_utc`

Rules:

1. Feature availability must be `<= decision_time`.
2. Signal generation happens after candle close.
3. Phase 1 does not execute trades, but any economic proxy must assume next-bar availability.
4. Higher-timeframe features become available only after the higher-timeframe candle closes.
5. Real-time swing candidates and confirmed swings must be separate.
6. Confirmed swings must include confirmation delay.
7. No centered rolling windows.
8. No future-filled missing values.
9. No labels or forward returns in features.
10. Scalers, selectors, encoders, and imputers fit only on train folds.
11. Optuna tuning happens only inside training/validation folds.
12. Final test is untouched until the correct gate stage.

Create automated leakage checks in:

```text
src/btc_quant/validation/leakage.py
```

---

## 11. Feature Plan

Each feature must have metadata:

```json
{
  "name": "feature_name",
  "family": "market_structure",
  "description": "...",
  "required_inputs": ["ohlcv_5m"],
  "timeframe": "5m",
  "availability_rule": "available after bar close",
  "parameters": {},
  "leakage_risk": "low|medium|high",
  "missing_value_policy": "...",
  "interpretation": "..."
}
```

Feature families:

1. market structure
2. ICT/SMC strict definitions
3. FVG and inverse FVG
4. order blocks / breaker / mitigation / rejection blocks
5. liquidity pools and sweeps
6. displacement and candle quality
7. order flow / CVD proxies
8. volatility and regime
9. futures positioning and leverage pressure
10. sessions and time behavior
11. classical context indicators
12. confluence features

Subjective concepts must be converted to explicit configurable rules.

---

## 12. Label Plan

Required labels:

- volatility-adjusted forward return labels
- triple-barrier labels
- event-based labels
- meta-labels
- MFE/MAE labels
- holding-time labels
- no-trade labels

Each label must define:

- decision timestamp
- label start timestamp
- label end timestamp
- horizon
- barrier definitions
- class mapping
- edge/no-edge threshold
- cost proxy if used

Labels must never become features.

---

## 13. Model Plan — Phase 1 Main Focus

Start simple and robust.

Required baselines:

- random
- always long
- always short
- buy and hold proxy
- simple trend-following
- simple breakout
- simple mean reversion

Required tabular ML models:

- Logistic Regression
- HistGradientBoosting
- Random Forest
- Extra Trees
- LightGBM
- XGBoost
- CatBoost
- calibrated ensemble

Optional sequence models are later and disabled by default:

- LSTM
- GRU
- Temporal CNN
- Transformer encoder

Every trained model must save:

- model artifact in Drive
- config snapshot
- feature list
- label definition
- split definition
- preprocessing pipeline
- metrics
- calibration report
- predictions
- model card
- reproducibility hash

Model outputs must include:

- probability of long edge
- probability of short edge
- probability of no-trade
- predicted class
- confidence score
- calibrated probabilities
- optional expected return proxy
- optional expected MFE/MAE proxy
- uncertainty flags

---

## 14. Validation Plan — No Backtest Yet

Use financial time-series validation only:

- chronological split
- walk-forward validation
- expanding window validation
- rolling window validation
- purged CV where labels overlap
- embargo where needed
- final untouched test period

Required Phase 1 model metrics:

Classification:

- accuracy
- balanced accuracy
- precision long
- precision short
- recall long
- recall short
- F1 long
- F1 short
- macro F1
- MCC
- ROC AUC when valid
- PR AUC
- confusion matrix

Probability and calibration:

- log loss
- Brier score
- calibration curve
- reliability diagram
- expected calibration error
- maximum calibration error if implemented
- confidence decile table
- probability decile table

Economic proxy diagnostics, not full backtest:

- forward return by predicted class
- forward return by confidence decile
- label-adjusted expected value proxy
- cost proxy sensitivity
- long/short separated forward-return proxy
- regime/setup/session performance proxy
- turnover proxy
- class imbalance impact

Robustness/falsification:

- random-label sanity check
- shuffled-feature sanity check
- seed stability
- fold stability
- feature ablation
- permutation importance stability
- train-validation drift
- model selection overfitting risk
- PBO-style analysis if enough folds/configs exist

Do not calculate a formal equity curve, position sizing, stop-loss, take-profit, drawdown, or trade journal in Phase 1.

---

## 15. Phase 1 Performance Bundle ZIP

The final Phase 1 notebook must create a compact ZIP for Codex handoff.

Path:

```text
reports/experiments/<run_id>/phase1_performance_bundle_<run_id>.zip
```

The unzipped folder must contain:

```text
phase1_performance_bundle/
  README_FOR_CODEX.md
  gate_decision.md
  decision_report.json
  auto_review.json
  phase1_current_status.json
  phase2_readiness.json
  future_oos_readiness.json
  future_oos_preflight.json
  future_oos_evaluation.json
  future_oos_candidate_plan.csv
  experiment_policy_guard.csv
  report_consistency_audit.json
  run_summary.json
  config_snapshot.yaml
  artifact_manifest.json
  data_quality_summary.json
  feature_summary.json
  label_summary.json
  model_leaderboard.csv
  model_leaderboard.md
  fold_metrics.csv
  class_metrics.csv
  calibration_metrics.csv
  confidence_deciles.csv
  probability_deciles.csv
  regime_breakdown.csv
  setup_breakdown.csv
  session_breakdown.csv
  robustness_checks.json
  leakage_report.json
  drift_report.json
  feature_importance_summary.csv
  feature_stability_summary.csv
  baseline_comparison.csv
  cost_proxy_sensitivity.csv
  failed_checks.json
  next_actions_for_codex.md
  questions_for_next_iteration.md
  notes.md
```

Optional small files:

```text
  plots/
    calibration_curve.html
    confidence_decile_plot.html
    feature_importance.html
    fold_stability.html
    drift_summary.html
```

Do not include huge raw data, full feature stores, large predictions, trained models, checkpoints, Optuna DB files, or private logs inside the ZIP. Include only summaries and links/paths to Drive artifacts.

The ZIP must answer:

1. Which model won and why?
2. Did it beat naïve baselines out-of-sample?
3. Did it survive walk-forward validation?
4. Are probabilities calibrated?
5. Does confidence correspond to better outcomes?
6. Is performance stable across folds?
7. Is performance concentrated in one regime only?
8. Did random-label and shuffled-feature tests fail as expected?
9. Is there evidence of leakage?
10. Is there enough evidence to freeze a candidate?
11. Is the candidate frozen and manifest-pinned?
12. Is Future-OOS ready?
13. Has Future-OOS evaluation actually run?
14. Did the frozen candidate pass Future-OOS?
15. Is Phase 2 allowed or blocked?
16. What exactly should Codex improve next?

---

## 16. Phase 1 Gate: When Can We Move to Phase 2?

The system must assign one of:

```text
RED
YELLOW
GREEN
```

### RED

Do not move to Phase 2.

Examples:

- leakage check fails
- model does not beat baselines
- performance exists only in train
- random-label test performs suspiciously well
- shuffled-feature test performs suspiciously well
- probabilities are unusably uncalibrated
- confidence deciles are not informative
- results depend on a single fold/regime
- label quality is poor
- data quality is insufficient

### YELLOW

Do not build full backtest yet. Improve Phase 1.

Examples:

- model beats baselines but weakly
- calibration is acceptable but unstable
- some folds are good and some fail
- performance appears only in specific regimes
- features need cleanup
- more data or better labels are needed

### GREEN

Historical Phase 1 may freeze a candidate and start Phase 1A Future-OOS monitoring/evaluation. Phase 2 may begin only after the Future-OOS gate also passes.

Minimum historical evidence before freezing:

- no leakage
- data quality pass
- label quality pass
- model beats baselines out-of-sample
- walk-forward results are stable enough
- probabilities are reasonably calibrated
- confidence buckets are informative
- random-label and shuffled-feature tests fail as expected
- no single regime/fold fully explains the edge
- cost proxy does not immediately destroy all apparent edge
- Codex handoff contains clear next steps

GREEN does not mean the system is profitable. Historical GREEN only means it is reasonable to freeze/pre-register the candidate and test it through Future-OOS prediction-only evaluation. Phase 2 is allowed only after Future-OOS evaluation is completed and passed, report consistency audit passes, and `promotion_allowed = true`.


---

## 16.1 Report Consistency Audit and Experiment Memory

Implement a report consistency audit that fails closed.

It must check:

- Future-OOS anchor consistency
- candidate activation validity
- manifest hash match
- row-count arithmetic
- min/preferred ready date arithmetic
- raw-data maturity date arithmetic
- Phase 2 blocker consistency
- canonical `next_action` consistency
- `promotion_allowed` consistency
- selected candidates not blocked by experiment memory
- no stale legacy state overriding active frozen candidate state

If this audit fails:

```text
decision = DO_NOT_PROCEED_TO_PHASE2
```

Maintain an experiment memory registry to avoid repeating closed failed ideas and to separate benchmark/control profiles from promotable candidates.

Required governance artifacts:

```text
reports/experiments/<run_id>/auto_review.json
reports/experiments/<run_id>/phase1_current_status.json
reports/experiments/<run_id>/phase2_readiness.json
reports/experiments/<run_id>/future_oos_readiness.json
reports/experiments/<run_id>/future_oos_preflight.json
reports/experiments/<run_id>/future_oos_evaluation.json
reports/experiments/<run_id>/future_oos_candidate_plan.csv
reports/experiments/<run_id>/experiment_policy_guard.csv
reports/experiments/<run_id>/report_consistency_audit.json
reports/experiments/<run_id>/decision_report.json
```

There must be exactly one canonical next action, such as:

```text
wait_for_new_future_oos_rows
run_no_refit_future_oos_evaluator
future_oos_candidate_passed_review_phase2_readiness
retire_failed_frozen_candidate_and_open_new_research_anchor
select_and_preregister_replacement_candidate_from_historical_cv_only
```

---

## 17. Reports and Experiment Registry

Every run must produce:

```text
reports/experiments/<run_id>/
```

Required files:

- `config_snapshot.yaml`
- `artifact_manifest.json`
- `metrics.json`
- `feature_list.json`
- `label_definition.json`
- `split_definition.json`
- `model_card.md`
- `leakage_report.json`
- `calibration_report.json`
- `robustness_report.json`
- `gate_decision.md`
- `next_actions_for_codex.md`
- `phase1_performance_bundle_<run_id>.zip`

Run IDs must be traceable and reproducible.

---

## 18. Colab Restart Safety

Every expensive notebook cell and pipeline stage must check whether outputs already exist.

Use config:

```yaml
force_rebuild: false
debug_mode: true
full_mode: false
max_rows_debug: 200000
```

Use:

- Parquet for data
- JSON/YAML for metadata
- joblib for tabular models
- torch checkpoints for deep learning later
- SQLite in Drive for Optuna
- artifact manifests
- explicit checkpoint loading

Do not keep huge DataFrames in memory longer than needed.

---

## 19. GitHub and Repository Hygiene Rules

Repository hygiene must not be implemented as a notebook. Use scripts and explicit Git commands. Colab normally pulls code from GitHub; local Codex/developer workflow normally pushes reviewed code to GitHub.

GitHub includes:

- source code
- notebook templates
- configs
- tests
- scripts
- docs
- `SKILL.md`
- `README.md`
- `.gitignore`
- `.env.example`

GitHub excludes:

- raw data
- processed data
- feature stores
- labels
- model files
- checkpoints
- Optuna DBs
- performance ZIPs unless explicitly small and sanitized
- large reports
- logs
- secrets

Before every push:

1. strip notebook outputs
2. run secret scan
3. verify `.gitignore`
4. verify no files above safe size are staged
5. verify no data/model/checkpoint/report artifacts are staged
6. run smoke tests
7. generate repository hygiene report

Never commit `.env`, API keys, tokens, passwords, raw data, processed data, model files, checkpoints, Optuna DBs, large reports, or logs.

---

## 20. First Response Required From Codex/Implementer

Do not jump directly into random code.

First provide:

1. concise technical summary
2. exact Phase 1 architecture
3. approved six-notebook Phase 1 sequence
4. confirmation that backtest is Phase 2 only
5. source package structure
6. data plan
7. feature plan
8. labeling plan
9. modeling plan
10. validation plan
11. Phase 1 performance bundle plan
12. Phase 1 gate criteria
13. GitHub/Colab/Drive workflow
14. major risks and limitations
15. then start implementing Phase 1 only; Phase 2 may receive docs/guards/blockers only, but no backtest/risk/dashboard implementation yet

After that, generate the actual Phase 1 Colab notebook code cells and source file skeletons. Phase 2 code must remain blocked until the Future-OOS gate passes.

---

## 21. Default Assumptions

Use these defaults unless explicitly changed:

```yaml
symbol: BTCUSDT
exchange: Binance
market_type: USD-M Futures
fallback_market_type: Spot
execution_timeframe: 5m
secondary_execution_timeframe: 15m
lower_timeframe: 1m
higher_timeframes: [1h, 4h, 1d]
project_root: /content/drive/MyDrive/btcusdt_quant_research
mode: phase1_model_research
live_trading: false
phase2_enabled: false
risk_per_trade: null
max_risk_per_trade: null
max_leverage: null
fees_enabled_for_proxy_metrics: true
slippage_enabled_for_proxy_metrics: true
funding_enabled_for_proxy_metrics: true
formal_backtest_enabled: false
walk_forward_validation: true
final_test_set: untouched
github_repository_url: https://github.com/umutergul74/btcusdt_quant_research.git
github_branch: main
large_artifacts_in_git: false
debug_mode: true
full_mode: false
force_rebuild: false
```

Now design and build this project in the most professional, robust, leakage-safe, restart-safe, Colab-compatible, GitHub-ready, model-first way possible.


---

## Repository Correction Lock

Canonical GitHub repository URL for this project is:

```text
https://github.com/umutergul74/btcusdt_quant_research.git
```

Do not use older `TradeBot.git` references.
