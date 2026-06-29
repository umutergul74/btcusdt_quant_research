# SKILL.md — BTCUSDT Quant Research Constitution v6.1 FINAL LOCKED

This file is the engineering, research, governance, and safety constitution for the BTCUSDT Colab Quant Research Framework.

Every notebook, source module, config, test, data contract, feature, label, model, report, performance bundle, candidate manifest, Future-OOS evaluator, and repository hygiene step must obey this file.

If a user request, notebook, source module, or implementation decision conflicts with this constitution, stop and explain the conflict. Do not silently violate the rules.

---

## 1. Mission

Build a serious BTCUSDT financial machine-learning research lab that runs heavy research tasks in Google Colab and persists large artifacts in Google Drive, while source code is developed locally with Codex and synchronized through GitHub.

The system exists to research whether a robust, leakage-safe, statistically defensible predictive edge exists.

The system must never promise profitability.

The system must be able to say clearly:

```text
No robust edge was found.
```

The immediate priority is **Phase 1 model research quality**:

1. data correctness,
2. timestamp discipline,
3. leakage prevention,
4. deterministic feature definitions,
5. clean label definitions,
6. repeatable model training,
7. walk-forward validation,
8. calibration diagnostics,
9. falsification tests,
10. experiment memory,
11. frozen candidate governance,
12. Future-OOS readiness/evaluation,
13. report consistency audit,
14. compact performance ZIP handoff to Codex.

Backtesting, position sizing, execution simulation, risk engine, dashboards, paper trading, and live trading are **not Phase 1 priorities**.

---

## 2. Non-Negotiable Operating Model

Use two separate environments.

### 2.1 Local Codex / Developer Environment

Local Codex development handles:

- source code,
- tests,
- configs,
- docs,
- notebook templates,
- lightweight synthetic fixtures,
- repository hygiene scripts,
- Git commits and pushes.

Local tests must not require:

- large Binance datasets,
- Google Drive,
- Colab-only APIs,
- private credentials,
- trained artifacts,
- Optuna databases,
- model checkpoints.

Local development must remain lightweight and reproducible.

### 2.2 Google Colab + Google Drive Research Environment

Colab handles:

- public market data download,
- data validation,
- feature generation,
- label generation,
- model training,
- Optuna tuning,
- walk-forward validation,
- calibration diagnostics,
- falsification checks,
- candidate freezing,
- Future-OOS readiness/evaluation,
- compact report and ZIP bundle generation.

Default root:

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

### 2.3 GitHub Synchronization

Clean source code is pushed to:

```text
https://github.com/umutergul74/btcusdt_quant_research.git
```

Colab pulls from GitHub. Google Drive stores large artifacts.

GitHub must contain only clean, reproducible source code, notebooks without outputs, configs, tests, docs, and scripts.

GitHub must not contain raw data, processed data, feature stores, labels, model artifacts, checkpoints, Optuna SQLite databases, private logs, large reports, or performance ZIPs unless explicitly sanitized and intentionally committed.

---

## 3. Core Architecture Rule: Thin Notebooks, Strong Package

The project must not become a collection of large notebooks.

Rules:

1. Notebooks are thin workbenches for orchestration, diagnostics, charts, summaries, and operator review.
2. Reusable logic lives in `src/btc_quant/`.
3. Pipeline stages are shared by notebooks, CLI, scripts, and tests.
4. Configs control research behavior; notebooks must not hardcode research decisions.
5. Artifacts live in Drive; GitHub stores clean source only.
6. Phase 2 code, if present, must be clearly disabled by default.

Example notebook usage:

```python
from btc_quant.pipeline.stages import run_stage
run_stage("build_features", config_name="features")
```

A notebook may call a stage. It must not contain the full implementation of that stage.

---

## 4. Approved Phase Structure

### 4.1 Phase 0 — Bootstrap

Purpose:

- create modular repo structure,
- create `SKILL.md`,
- create configs,
- create notebooks,
- create package skeleton,
- verify imports,
- verify repository hygiene,
- verify Colab/Drive setup.

### 4.2 Phase 1 — Model-First Research Foundation

Phase 1 is the current main work.

Deliver:

- data foundation,
- feature factory,
- label factory,
- research dataset builder,
- baselines,
- tabular ML models,
- calibration,
- walk-forward validation,
- leakage checks,
- falsification checks,
- drift diagnostics,
- model scorecards,
- experiment registry,
- historical Phase 1 gate decision,
- performance ZIP bundle for Codex.

Phase 1 does **not** include formal backtesting, realistic execution, position sizing, dashboard productization, paper trading, or live trading.

### 4.3 Phase 1A — Frozen Candidate + Future-OOS Gate

Historical walk-forward success is not enough to start Phase 2.

When a candidate looks promising on historical Phase 1 evidence:

1. freeze the candidate,
2. save immutable manifest,
3. hash model/config/feature/label/split/preprocessing/threshold artifacts,
4. pin expected manifest hash in config,
5. record candidate activation state separately from immutable manifest text,
6. start a Future-OOS anchor at `anchor_data_end`,
7. wait for enough new unseen rows to mature into labels,
8. run prediction-only Future-OOS evaluation without refit,
9. permit promotion only if evaluation completed and passed.

Important:

```text
Data window ready != candidate passed.
Historical holdout pass != Future-OOS pass.
Candidate frozen != Phase2 allowed.
```

Phase 2 is blocked until prediction-only Future-OOS evaluation passes and the report consistency audit confirms the state.

Required frozen candidate artifacts:

```text
reports/experiments/<run_id>/frozen_candidate_manifest.json
reports/experiments/<run_id>/frozen_candidate_index.csv
configs/candidate_activation.yaml
configs/future_oos.yaml
```

Immutable manifest fields:

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

The immutable manifest must not be edited after creation. Mutable state belongs in config/index/status files.

### 4.4 Phase 1.5 — Safe Phase 2 Preparation While Waiting

While waiting for Future-OOS rows, Codex may prepare only non-influential Phase 2 scaffolding.

Allowed:

- Phase 2 design docs,
- disabled guardrail modules,
- runbook docs,
- risk policy notes,
- paper-trading skeleton clearly disabled by default,
- readiness monitor code that cannot influence candidate selection.

Not allowed:

- using Future-OOS data to tune,
- changing the frozen candidate after anchor,
- building a backtest to justify promotion,
- enabling execution,
- using Phase 2 results to select Phase 1 candidates.

### 4.5 Phase 2 — Backtest, Risk, Execution, Dashboard Later

Phase 2 begins only after all of the following are true:

```yaml
no_leakage: true
data_quality_passed: true
label_quality_passed: true
walk_forward_evidence_passed: true
seed_reproducibility_interpretable: true
frozen_candidate_manifest_available: true
manifest_hash_pinned: true
candidate_activation_valid: true
future_oos_window_ready: true
future_oos_evaluation_completed: true
future_oos_candidate_passed: true
report_consistency_passed: true
promotion_allowed: true
```

If any required field fails:

```text
decision = DO_NOT_PROCEED_TO_PHASE2
```

If all pass:

```text
decision = READY_FOR_PHASE2
```

GREEN historical Phase 1 evidence alone does not unlock Phase 2. GREEN only allows candidate freezing and Future-OOS evaluation.

---

## 5. Approved Phase 1 Notebook Set

Use exactly these notebooks for Phase 1:

```text
notebooks/
  00_colab_bootstrap_and_git_sync.ipynb
  01_data_foundation_lab.ipynb
  02_feature_label_factory_lab.ipynb
  03_model_training_lab.ipynb
  04_model_validation_diagnostics_lab.ipynb
  05_phase1_performance_package_lab.ipynb
```

Do not create a GitHub publish notebook.

Do not create a Phase 1 backtest notebook.

Do not make the sixth notebook backtest/risk/dashboard. The sixth notebook must package Phase 1 model performance results into a compact ZIP for Codex handoff.

Notebook roles:

- `00_colab_bootstrap_and_git_sync.ipynb`: Drive mount, install, clone/pull latest code, setup, smoke tests.
- `01_data_foundation_lab.ipynb`: OHLCV, futures metrics, optional aggTrades, cleaning, resampling, data quality.
- `02_feature_label_factory_lab.ipynb`: feature families, feature store, labels, leakage checks.
- `03_model_training_lab.ipynb`: baselines, tabular models, Optuna, calibration, model registry.
- `04_model_validation_diagnostics_lab.ipynb`: walk-forward, purged CV, calibration, falsification, drift, gate scoring.
- `05_phase1_performance_package_lab.ipynb`: compact performance ZIP, Codex handoff, next actions, gate decision, Future-OOS status, report consistency audit summary.

---

## 6. Required Source Package Structure

Use `src/btc_quant/` as the main Python package.

Required modules:

```text
src/btc_quant/
  __init__.py
  cli.py
  core/
  pipeline/
  data/
  features/
  labels/
  models/
  validation/
  performance/
  experiment/
  governance/
  future_oos/
  explainability/
  reports/
  github/
  automation/
  backtest_phase2/
```

The `performance/`, `experiment/`, `governance/`, and `future_oos/` packages are Phase 1/Phase 1A requirements.

The `backtest_phase2/` package is disabled by default and must not influence Phase 1 candidate selection.

---

## 7. Pipeline Stage Registry

Approved Phase 1 stages:

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
freeze_candidate_if_eligible
check_future_oos_readiness
run_no_refit_future_oos_evaluation
audit_report_consistency
package_phase1_performance
generate_phase1_reports
```

Phase 2 stages must be clearly marked later-only and disabled by default:

```text
backtest_phase2_later
risk_phase2_later
dashboard_phase2_later
paper_trading_phase2_later
```

Every stage must define:

- name,
- phase,
- inputs,
- outputs,
- config dependencies,
- artifact manifest entries,
- restart policy,
- force rebuild behavior,
- expected runtime class,
- leakage sensitivity level,
- validation checks,
- failure behavior,
- whether it is allowed before Phase 2 promotion.

---

## 8. Timestamp Discipline

Every dataset, event table, feature table, label table, prediction table, and report must preserve relevant timestamps where applicable:

- `bar_open_time`,
- `bar_close_time`,
- `event_time`,
- `feature_available_time`,
- `decision_time`,
- `label_start_time`,
- `label_end_time`,
- `created_at_utc`,
- `anchor_data_end`,
- `latest_available_data_end`.

All timestamps must be UTC unless explicitly labeled otherwise.

Higher-timeframe data may only be used after that higher-timeframe candle has closed.

Example:

```text
A 1h candle covering 09:00–10:00 UTC is not available to 5m rows before 10:00 UTC.
```

---

## 9. Leakage Prevention

Forbidden:

- centered rolling windows,
- future-confirmed swings used as real-time features,
- future candles in past features,
- fitting scalers/selectors/encoders/imputers on full data,
- threshold tuning on final test,
- Optuna tuning on final test,
- labels or forward returns in feature generation,
- future-filled missing values,
- global normalization before splitting,
- using Future-OOS data to tune,
- formal equity/backtest metrics in Phase 1.

Required:

- point-in-time feature generation,
- explicit availability timestamp,
- train-only preprocessing fit,
- chronological splits,
- purging and embargo where labels overlap,
- untouched final test period,
- no-refit Future-OOS evaluation,
- automated leakage checks,
- leakage section in every major notebook/report.

---

## 10. Data Rules

Default market:

```yaml
symbol: BTCUSDT
exchange: Binance
market_type: USD-M Futures
fallback_market_type: Spot
```

Required timeframes:

```text
1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d
```

Primary execution timeframe:

```yaml
execution_timeframe: 5m
```

Required OHLCV fields:

- open time UTC,
- close time UTC,
- open,
- high,
- low,
- close,
- volume,
- quote volume,
- number of trades,
- taker buy base volume,
- taker buy quote volume,
- taker sell base volume if derivable,
- taker sell quote volume if derivable,
- source,
- symbol,
- timeframe.

Optional data:

- funding rate,
- mark price,
- index price,
- premium index,
- open interest,
- open interest statistics,
- global long/short ratios,
- top trader account/position ratios,
- taker buy/sell volume,
- aggTrades/order-flow proxies,
- optional external macro/context proxies.

Raw data must be immutable once saved. Corrections must create processed outputs, not overwrite raw files unless the file is known corrupt and the action is logged.

All data downloads must be incremental, restart-safe, UTC-consistent, and rate-limit-aware.

---

## 11. Data Quality Rules

Every data stage must check:

- missing timestamps,
- duplicate rows,
- invalid OHLC relationships,
- zero-volume candles,
- incomplete latest candle,
- gaps by timeframe,
- timezone errors,
- extreme outliers,
- volume spikes,
- source coverage,
- symbol/timeframe consistency.

Data quality status must be included in:

```text
reports/experiments/<run_id>/data_quality_summary.json
```

A serious data quality failure blocks Phase 1 GREEN and Phase 2 promotion.

---

## 12. Feature Rules

Every feature must have metadata:

```json
{
  "name": "feature_name",
  "family": "market_structure",
  "description": "...",
  "required_inputs": ["ohlcv_5m"],
  "timeframe": "5m",
  "parameters": {},
  "availability_rule": "available after bar close",
  "leakage_risk": "low|medium|high",
  "missing_value_policy": "...",
  "interpretation": "..."
}
```

Feature families:

- market structure,
- ICT/SMC deterministic definitions,
- FVG and inverse FVG,
- order blocks / breaker / mitigation / rejection blocks,
- liquidity pools and sweeps,
- displacement and candle quality,
- order flow / CVD proxies,
- volatility and regime,
- futures positioning and leverage pressure,
- sessions and time behavior,
- classical context indicators,
- confluence features.

Subjective concepts must be converted into explicit configurable rules.

Real-time and confirmed versions of swing/structure features must be separated.

Confirmed swing features must include confirmation delay.

---

## 13. Label Rules

Labels must never become features.

Required label types:

- volatility-adjusted forward returns,
- triple barrier,
- event-based labels,
- meta-labels,
- MFE/MAE labels,
- holding-time labels,
- no-trade/edge labels.

Each label must define:

- decision timestamp,
- label start timestamp,
- label end timestamp,
- horizon,
- barrier definitions,
- class mapping,
- edge/no-edge threshold,
- cost proxy if used,
- leakage notes.

Labels must be created strictly after the decision timestamp.

---

## 14. Model Rules

Start simple. Do not jump to deep learning before tabular baselines work.

Required baseline models:

- random,
- rate-matched random,
- always long,
- always short,
- buy and hold proxy,
- simple trend-following,
- simple breakout,
- simple mean reversion.

Required ML models:

- Logistic Regression,
- HistGradientBoosting,
- Random Forest,
- Extra Trees,
- LightGBM,
- XGBoost,
- CatBoost,
- calibrated ensemble.

Optional later models are disabled by default:

- LSTM,
- GRU,
- Temporal CNN,
- Transformer encoder.

Every trained model must save:

- model artifact path,
- config snapshot,
- feature list,
- label definition,
- split definition,
- preprocessing pipeline,
- metrics,
- calibration report,
- predictions summary,
- model card,
- reproducibility hash.

Model output schema must include:

- `prob_long_edge`,
- `prob_short_edge`,
- `prob_no_trade`,
- `predicted_class`,
- `confidence`,
- `calibrated_probability`,
- `uncertainty_flags`,
- optional expected return proxy,
- optional expected MFE/MAE proxy.

---

## 15. Validation Rules

Use financial time-series validation only:

- chronological splits,
- walk-forward validation,
- expanding window validation,
- rolling window validation,
- purged CV where labels overlap,
- embargo where needed,
- final untouched test.

Report by:

- fold,
- class,
- confidence decile,
- probability decile,
- regime,
- setup type,
- session,
- volatility bucket,
- long vs short,
- seed,
- feature family.

Required model metrics:

- accuracy,
- balanced accuracy,
- precision/recall/F1,
- macro F1,
- MCC,
- PR AUC,
- ROC AUC when valid,
- log loss,
- Brier score,
- calibration error,
- expected value proxy by confidence bucket,
- forward return proxy by probability decile,
- baseline lift,
- positive fold fraction,
- confidence monotonicity.

Required falsification checks:

- random-label sanity check,
- shuffled-feature sanity check,
- seed stability,
- fold stability,
- feature ablation,
- permutation importance stability,
- train-validation drift,
- baseline comparison,
- model selection overfitting risk,
- PBO-style analysis where enough folds/configs exist.

Do not calculate formal equity curves, position sizing, stop-loss, take-profit, drawdown, or trade journal in Phase 1.

---

## 16. Historical Phase 1 Gate Rules

Historical Phase 1 gate status must be one of:

```text
RED
YELLOW
GREEN
```

### RED

Do not freeze/promote. Improve Phase 1.

Examples:

- leakage check fails,
- model does not beat baselines,
- performance exists only in train,
- random-label test performs suspiciously well,
- shuffled-feature test performs suspiciously well,
- probabilities are unusably uncalibrated,
- confidence deciles are not informative,
- results depend on a single fold/regime,
- label quality is poor,
- data quality is insufficient.

### YELLOW

Do not freeze/promote yet. Improve Phase 1.

Examples:

- model beats baselines weakly,
- calibration is acceptable but unstable,
- some folds pass and some fail,
- performance appears only in narrow regimes,
- features need cleanup,
- more data or better labels are needed.

### GREEN

Historical Phase 1 evidence is strong enough to freeze/pre-register a candidate and start Future-OOS monitoring/evaluation.

GREEN does **not** mean profitability.

GREEN does **not** unlock Phase 2.

Minimum GREEN evidence:

- no leakage,
- data quality pass,
- label quality pass,
- model beats baselines out-of-sample,
- walk-forward results are stable enough,
- probabilities are reasonably calibrated,
- confidence buckets are informative,
- random-label and shuffled-feature tests fail as expected,
- no single regime/fold fully explains the edge,
- cost proxy does not immediately destroy all apparent edge,
- Codex handoff contains clear next steps.

---

## 17. Future-OOS Rules

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

Never promote from:

- stale config state,
- mutable report text,
- unpinned manifest,
- historical holdout alone,
- readiness flag without actual evaluation,
- manually edited status files,
- failed report consistency audit.

---

## 18. Report Consistency Audit and Experiment Memory

Implement a report consistency audit that fails closed.

It must check:

- Future-OOS anchor consistency,
- candidate activation validity,
- manifest hash match,
- row-count arithmetic,
- min/preferred ready date arithmetic,
- raw-data maturity date arithmetic,
- Phase 2 blocker consistency,
- canonical `next_action` consistency,
- `promotion_allowed` consistency,
- selected candidates not blocked by experiment memory,
- no stale legacy state overriding active frozen candidate state.

If this audit fails:

```text
decision = DO_NOT_PROCEED_TO_PHASE2
```

Maintain an experiment memory registry to:

- avoid repeating closed failed ideas,
- track allowed retests,
- separate benchmark/control profiles from promotable candidates,
- require explicit rationale for new candidate families,
- prevent stale failed experiments from silently reappearing as candidates.

There must be exactly one canonical next action, such as:

```text
wait_for_new_future_oos_rows
run_no_refit_future_oos_evaluator
future_oos_candidate_passed_review_phase2_readiness
retire_failed_frozen_candidate_and_open_new_research_anchor
select_and_preregister_replacement_candidate_from_historical_cv_only
continue_phase1_model_improvement
```

---

## 19. Phase 1 Performance Bundle Rules

Every serious experiment must produce:

```text
reports/experiments/<run_id>/phase1_performance_bundle_<run_id>.zip
```

The ZIP must contain lightweight summaries only:

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

Do not include raw data, large feature stores, full predictions, trained models, checkpoints, Optuna DBs, or private logs.

The ZIP must answer:

1. Which model won and why?
2. Did it beat naive baselines out-of-sample?
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
17. Is the report internally consistent?

---

## 20. Colab Restart Safety

Every expensive notebook cell and pipeline stage must check whether outputs already exist.

Use config:

```yaml
force_rebuild: false
debug_mode: true
full_mode: false
max_rows_debug: 200000
```

Use:

- Parquet for data,
- JSON/YAML for metadata,
- joblib for tabular models,
- torch checkpoints for deep learning later,
- SQLite in Drive for Optuna,
- artifact manifests,
- explicit checkpoint loading,
- stage-level idempotency checks.

Do not keep huge DataFrames in memory longer than needed.

---

## 21. GitHub and Repository Hygiene Rules

Repository hygiene must not be implemented as a notebook. Use scripts and explicit Git commands.

Colab normally pulls code from GitHub. Local Codex/developer workflow normally pushes reviewed code to GitHub.

GitHub includes:

- source code,
- notebooks without outputs,
- configs,
- tests,
- scripts,
- docs,
- `SKILL.md`,
- `README.md`,
- `.gitignore`,
- `.env.example`.

GitHub excludes:

- raw data,
- processed data,
- feature stores,
- labels,
- model files,
- checkpoints,
- Optuna DBs,
- performance ZIPs unless explicitly sanitized and intentionally committed,
- large reports,
- logs,
- secrets.

Before every push:

1. strip notebook outputs,
2. run secret scan,
3. verify `.gitignore`,
4. verify no files above safe size are staged,
5. verify no data/model/checkpoint/report artifacts are staged,
6. run smoke tests,
7. generate repository hygiene report.

Never commit:

- `.env`,
- API keys,
- tokens,
- passwords,
- raw data,
- processed data,
- model files,
- checkpoints,
- Optuna DBs,
- large reports,
- logs,
- unsanitized Phase 1 ZIP bundles.

---

## 22. Accepted Failure Modes

It is acceptable to conclude:

- no stable edge found,
- features are not robust,
- labels are too noisy,
- costs eliminate apparent edge,
- edge exists only in certain regimes,
- model is overfit,
- data quality is insufficient,
- order-flow data is too large for Colab full mode without optimization,
- Phase 1 gate is RED or YELLOW,
- Future-OOS is not ready,
- Future-OOS evaluation failed,
- Phase 2 remains blocked.

It is not acceptable to hide these outcomes.

---

## 23. Done Definition for Phase 1

Phase 1 is done only when:

- approved six notebooks exist,
- folder structure exists,
- configs exist,
- `SKILL.md` exists,
- `src/btc_quant/` package skeleton exists,
- pipeline stage registry exists,
- data/feature/label/model/validation stages exist,
- performance bundle stage exists,
- tests skeleton exists,
- GitHub safety scripts exist,
- Drive/Colab bootstrap works,
- imports pass,
- at least one debug experiment runs end-to-end,
- a Phase 1 performance ZIP is produced,
- historical gate decision is documented,
- candidate freeze eligibility is documented,
- Future-OOS readiness status is documented,
- report consistency audit status is documented,
- canonical next action is documented.

---

## 24. Absolute Blocking Rules

Stop immediately and report the conflict if an implementation attempts to:

1. create a GitHub publish notebook,
2. put formal backtesting into Phase 1,
3. use final test or Future-OOS data for tuning,
4. enable live trading or private exchange endpoints,
5. commit Drive artifacts to GitHub,
6. omit `feature_available_time` or equivalent feature availability logic,
7. use labels or future returns as features,
8. treat historical GREEN as Phase 2 permission,
9. promote a candidate without completed no-refit Future-OOS evaluation,
10. bypass failed report consistency audit.


---

## Repository Correction Lock

Canonical GitHub repository URL for this project is:

```text
https://github.com/umutergul74/btcusdt_quant_research.git
```

Do not use older `TradeBot.git` references.
