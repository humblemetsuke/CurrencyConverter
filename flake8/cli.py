import argparse
from flake8_report_creator import run_flake8
from parser import parse_flake8_report
from visualizer import plot_error_code_chart, plot_top_files_chart
from logger_setup import

def main():
    parser = argparse.ArgumentParser(description="Run Flake8 and analyze results.")
    parser.add_argument("path", nargs="?", default=".", help="Directory or file to lint")
    args = parser.parse_args()

    report_path = run_flake8(args.path)
    error_counts, file_errors = parse_flake8_report(report_path)

    print("\n📌 Error Summary by Code:")
    for code, count in sorted(error_counts.items(), key=lambda x: -x[1]):
        print(f"{code}: {count} occurrences")

    print("\n📁 Top Files with Most Errors:")
    for file, codes in sorted(file_errors.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"{file}: {len(codes)} issues")

    plot_error_code_chart(error_counts)
    plot_top_files_chart(file_errors)

if __name__ == "__main__":
    main()
