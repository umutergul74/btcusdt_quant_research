import os
import shutil
import zipfile
import pandas as pd
from utils.logging_utils import setup_logger

logger = setup_logger("colab_utils")

def generate_pipeline_summary_and_zip(project_root: str, symbol: str):
    """Aggregates all validation and backtesting reports into a single text summary and zips the reports directory."""
    logger.info("Generating pipeline summary report...")
    
    reports_dir = os.path.join(project_root, "reports")
    summary_path = os.path.join(reports_dir, "summary_report.txt")
    
    summary_lines = []
    summary_lines.append("==================================================")
    summary_lines.append("   BTCUSDT QUANT RESEARCH PIPELINE SUMMARY   ")
    summary_lines.append("==================================================\n")
    
    # 1. Load Walk-Forward Validation Metrics
    val_path = os.path.join(reports_dir, "validation", f"{symbol}_walk_forward_metrics.parquet")
    if os.path.exists(val_path):
        try:
            df_val = pd.read_parquet(val_path)
            summary_lines.append("--- Walk-Forward Validation Metrics (Averages) ---")
            for col in df_val.columns:
                if col != "fold":
                    summary_lines.append(f"  {col.upper():<15}: {df_val[col].mean():.4f}")
            summary_lines.append("\n")
        except Exception as e:
            summary_lines.append(f"Error reading validation metrics: {e}\n")
    else:
        summary_lines.append("[-] Walk-Forward validation metrics not found.\n")
        
    # 2. Load Backtest Trade Journal
    backtest_path = os.path.join(reports_dir, "backtests", f"{symbol}_trade_journal.parquet")
    if os.path.exists(backtest_path):
        try:
            df_trades = pd.read_parquet(backtest_path)
            summary_lines.append("--- Backtesting Trade Journal Summary ---")
            total_trades = len(df_trades)
            summary_lines.append(f"  Total Trades   : {total_trades}")
            
            if total_trades > 0:
                # Calculate basic stats
                wins = df_trades[df_trades["pnl"] > 0]
                win_rate = len(wins) / total_trades
                total_profit = df_trades[df_trades["pnl"] > 0]["pnl"].sum()
                total_loss = abs(df_trades[df_trades["pnl"] < 0]["pnl"].sum())
                profit_factor = total_profit / total_loss if total_loss > 0 else float("inf")
                
                summary_lines.append(f"  Win Rate       : {win_rate:.2%}")
                summary_lines.append(f"  Profit Factor  : {profit_factor:.2f}")
                summary_lines.append(f"  Total PnL ($)  : {df_trades['pnl'].sum():.2f}")
            summary_lines.append("\n")
        except Exception as e:
            summary_lines.append(f"Error reading backtest trade journal: {e}\n")
    else:
        summary_lines.append("[-] No trades executed or backtest trade journal not found.\n")
        
    # Write summary report
    os.makedirs(reports_dir, exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))
    
    logger.info(f"Summary report written to {summary_path}")
    
    # Print the summary to the console so the user can see it in Colab
    print("\n" + "\n".join(summary_lines) + "\n")
    
    # 3. Create ZIP archive of the reports directory
    zip_path = os.path.join(project_root, "reports_archive.zip")
    logger.info(f"Creating ZIP archive of reports at {zip_path}...")
    
    try:
        if os.path.exists(zip_path):
            os.remove(zip_path)
            
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(reports_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calculate relative path to keep the zip structure clean
                    arcname = os.path.relpath(file_path, project_root)
                    zipf.write(file_path, arcname)
                    
        logger.info("ZIP archive created successfully!")
        print(f"=== SUCCESS: Download your reports archive from Drive: {zip_path} ===\n")
    except Exception as e:
        logger.error(f"Failed to create ZIP archive: {e}")
        print(f"Error creating ZIP archive: {e}\n")
