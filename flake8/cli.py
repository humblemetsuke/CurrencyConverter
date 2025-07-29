import argparse
import sys

from flake8_report_creator import run_flake8
from parser import parse_flake8_report
from visualizer import plot_error_code_chart, plot_top_files_chart


def main() -> None:

    """
    Run Flake8 on specified path, parse the report,
    prints error summaries and  displays visual charts of the reports.
    """
    parser = argparse.ArgumentParser(description="Run Flake8 and analyze results.")
    parser.add_argument("path", nargs="?", default=".", help="Directory or file to lint")
    args = parser.parse_args()

    try:
        report_path = run_flake8(args.path)
        error_counts, file_errors = parse_flake8_report(report_path)
    except FileNotFoundError:
        print(f"❌ The path '{args.path}' does not exist.")
        sys.exit(1)
    except Exception as e:
        print(f"⚠️ An error occurred: {e}")
        sys.exit(2)

    print("\n📌 Error Summary by Code:")
    for code, count in sorted(error_counts.items(), key=lambda x: -x[1]):
        print(f"{code}: {count} occurrences")

    print("\n📁 Top Files with Most Errors:")
    for file, codes in sorted(file_errors.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"{file}: {len(codes)} issues")

    plot_error_code_chart(error_counts)
    plot_top_files_chart(file_errors)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"fatal error {e}")
        sys.exit(99)
