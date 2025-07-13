import subprocess
import sys
from pathlib import Path
from datetime import datetime
from colorama import init, Fore, Style
from collections import defaultdict

init()

TIMEOUT_IN_SECONDS = 40  # 40 second timeout


def ensure_flake8_installed():
    """Check if flake8 is installed; if not, offer to install it."""
    try:
        subprocess.run(
            ["flake8", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except FileNotFoundError:
        print(Fore.RED + f"❌ flake8 is not installed." + Style.RESET_ALL)
        user_input = input(
            Fore.CYAN + "👉 Would you like to install flake8 now? (y/n): " + Style.RESET_ALL
        ).strip().lower()
        if user_input == "y":
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "flake8"], check=True)
                print(Fore.GREEN + f"✅ flake8 successfully installed." + Style.RESET_ALL)
            except subprocess.CalledProcessError:
                print(
                    Fore.RED
                    + f"❌ Failed to install flake8. Please install it manually: pip install flake8"
                    + Style.RESET_ALL
                )
                sys.exit(1)
        else:
            print(Fore.RED + "❌ flake8 is required. Exiting." + Style.RESET_ALL)
            sys.exit(1)


def run_flake8(output_dir="reports", output_file="flake8-report.txt"):
    """Run flake8, save output report with timestamp, and return report file path."""
    print(Fore.CYAN + "🔍 Running flake8 linting..." + Style.RESET_ALL)
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

        base = Path(output_file).stem
        output_filename = f"{base}_{timestamp}.txt"
        output_path = output_dir_path / output_filename

        with output_path.open("w") as f:
            result = subprocess.run(
                ["flake8"],
                stdout=f,
                stderr=subprocess.STDOUT,
                check=False,
                timeout=TIMEOUT_IN_SECONDS,
            )

        if result.returncode == 0:
            if output_path.stat().st_size == 0:
                print(
                    Fore.GREEN
                    + f"✅ flake8 finished with no issues. Report is empty, this is normal: {output_path}."
                    + Style.RESET_ALL
                )
            else:
                print(
                    Fore.GREEN
                    + f"✅ flake8 finished with no issues. Report saved to: {output_path}."
                    + Style.RESET_ALL
                )
        elif result.returncode == 1:
            print(
                Fore.YELLOW
                + f"⚠️ flake8 has finished with linting issues. See {output_path} for further details."
                + Style.RESET_ALL
            )
        else:
            print(
                Fore.RED
                + f"❌ flake8 failed (exit code {result.returncode})."
                + f" Check {output_path} for possible runtime errors or misconfigurations."
                + Style.RESET_ALL
            )
        return output_path

    except subprocess.TimeoutExpired:
        print(
            Fore.RED
            + f"❌ flake8 timed out after {TIMEOUT_IN_SECONDS} seconds. Process was terminated."
            + Style.RESET_ALL
        )
        return None
    except FileNotFoundError:
        print(
            Fore.RED
            + f"❌ Error: 'flake8' is not installed or not found in your PATH."
            + Style.RESET_ALL
        )
        return None
    except PermissionError:
        print(
            Fore.RED
            + f"❌ Error: Permission denied when writing to {output_path}."
            + Style.RESET_ALL
        )
        return None
    except IsADirectoryError:
        print(Fore.RED + f"❌ Expected a file but got a directory: {output_path}" + Style.RESET_ALL)
        return None
    except NotADirectoryError:
        print(
            Fore.RED
            + f"❌ Part of the specified path is not a directory: {output_dir}"
            + Style.RESET_ALL
        )
        return None
    except Exception as e:
        print(Fore.RED + f"❌ Unexpected error: {type(e).__name__}: {e}" + Style.RESET_ALL)
        return None


def summarise_flake8_report(file_path):
    """Parse the flake8 report file and print error summary by code and by file."""
    error_counts = defaultdict(int)
    file_errors = defaultdict(list)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":")
                if len(parts) < 4:
                    continue
                filename = parts[0].strip()
                code = parts[3].strip().split()[0]

                error_counts[code] += 1
                file_errors[filename].append(code)

    except Exception as e:
        print(f"Failed to parse the report file {file_path}: {e}")
        return

    print("\n📌 Error Summary by Code:")
    for code, count in sorted(error_counts.items(), key=lambda x: -x[1]):
        print(f"{code}: {count} occurrences")

    print("\n📁 Top Files with Most Errors:")
    sorted_files = sorted(file_errors.items(), key=lambda x: -len(x[1]))
    for file, codes in sorted_files[:10]:  # Top 10 files
        print(f"{file}: {len(codes)} issues")


def main():
    ensure_flake8_installed()
    report_path = run_flake8()
    if report_path and Path(report_path).exists():
        summarise_flake8_report(report_path)
    else:
        print("⚠️ No flake8 report found to summarize.")
    sys.exit(0)


if __name__ == "__main__":
    main()
