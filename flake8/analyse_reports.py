from collections import defaultdict
from pathlib import Path
from charts import plot_error_code_chart, plot_top_files_chart


def get_latest_flake8_report(output_dir="reports", base_name='flake8-report'):
    report_path = Path(output_dir)
    files = list(report_path.glob(f"{base_name}_*.txt"))
    if not files:
        print(f"No flake8 report files were found in {output_dir}")
        return None
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return files[0]
