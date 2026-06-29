import argparse
import json
from btc_quant.performance.bundle import build_phase1_bundle
from btc_quant.pipeline.run_context import create_run_context
from btc_quant.pipeline.stage_registry import list_stage_specs
from btc_quant.pipeline.stages import run_experiment, run_stage

def main(argv=None):
    parser = argparse.ArgumentParser(prog="btc_quant")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("run-stage"); p.add_argument("stage"); p.add_argument("--config"); p.add_argument("--project-root"); p.add_argument("--run-id")
    p = sub.add_parser("run-experiment"); p.add_argument("--config", required=True); p.add_argument("--project-root"); p.add_argument("--run-id")
    p = sub.add_parser("package-phase1"); p.add_argument("--project-root"); p.add_argument("--run-id", default="debug_local")
    sub.add_parser("list-stages")
    args = parser.parse_args(argv)
    if args.command == "run-stage":
        result = run_stage(args.stage, args.config, args.project_root, args.run_id)
    elif args.command == "run-experiment":
        result = run_experiment(args.config, args.project_root, args.run_id)
    elif args.command == "package-phase1":
        ctx = create_run_context(project_root=args.project_root, run_id=args.run_id)
        result = {"zip_path": str(build_phase1_bundle(ctx.experiment_dir, ctx.run_id))}
    else:
        result = [spec.__dict__ for spec in list_stage_specs()]
    print(json.dumps(result, indent=2, default=str))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

