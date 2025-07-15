import subprocess

from datetime import datetime
from pathlib import Path
from logger_setup import setup_logger

logger = setup_logger()




# Create directories if they don't exist
FLAKE8_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
FLAKE8_GRAPHS_DIR.mkdir(parents=True, exist_ok=True)

# --- Plotting functions ---




# --- Find latest flake8 report ---

def get_latest_flake8_report():
    files = list(FLAKE8_REPORTS_DIR.glob("flake8-report_*.txt"))
    if not files:
        return None
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return files[0]

# --- Parse and summarize flake8 report ---


            except Exception as e:
                print(f"Failed to parse line: {line}\n{e}")

    print("\n📌 Error Summary by Code:")
    for code, count in sorted(error_counts.items(), key=lambda x: -x[1]):
        print(f"{code}: {count} occurrences")

    print("\n📁 Top Files with Most Errors:")
    sorted_files = sorted(file_errors.items(), key=lambda x: -len(x[1]))
    for file, codes in sorted_files[:10]:
        print(f"{file}: {len(codes)} issues")

    plot_error_code_chart(error_counts)
    plot_top_files_chart(file_errors)

# --- Main ---

if __name__ == "__main__":
    report_path = run_flake8_report()
    if report_path.exists():
        summarise_flake8_report(report_path)
    else:
        print("❌ Failed to create flake8 report.")
