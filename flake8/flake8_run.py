import subprocess
import sys
from pathlib import Path
from datetime import datetime
from colorama import init, Fore, Style
from collections import defaultdict

init()

TIMEOUT_IN_SECONDS = 40  # Timeout for flake8

def ensure_flake8_installed():
    try:
        subprocess.run(["flake8", "--version"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL,
                       check=True)
    except FileNotFoundError:
        print(Fore.RED + "❌ flake8 is not installed." + Style.RESET_ALL)
        user_input = input(Fore.CYAN + "👉 Install flake8 now? (y/n): "
                           + Style.RESET_ALL).strip().lower()
        if user_input == 'y':
            try:
                subprocess.run([sys.executable, "-m",
                                "pip",
                                "install",
                                "flake8"],
                               check=True)
                print(Fore.GREEN + "✅ flake8 installed."
                                 + Style.RESET_ALL)
            except subprocess.CalledProcessError:
                print(Fore.RED + "❌ Failed to install flake8. "
                                 "Install manually with: "
                                 "`pip install flake8`."
                                 + Style.RESET_ALL)
                sys.exit(1)
        else:
            print(Fore.RED + "❌ flake8 is required. "
                             "Exiting."
                             + Style.RESET_ALL)
            sys.exit(1)

def run_flake8(output_dir="reports", output_file="flake8-report.txt"):
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
                timeout=TIMEOUT_IN_SECONDS
            )

        if result.returncode == 0:
            if output_path.stat().st_size == 0:
                print(Fore.GREEN + f"✅ No issues found. "
                                   f"Empty report saved: "
                                   f"{output_path}"
                                   + Style.RESET_ALL)
            else:
                print(Fore.GREEN + f"✅ flake8 finished successfully. "
                                   f"Report saved: {output_path}"
                                   + Style.RESET_ALL)
        elif result.returncode == 1:
            print(Fore.YELLOW + f"⚠️ flake8 found issues. See report: {output_path}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"❌ flake8 failed with exit code {result.returncode}. See: {output_path}" + Style.RESET_ALL)

        return result.returncode, output_path

    except subprocess.TimeoutExpired:
        print(Fore.RED + "❌ flake8 timed out." + Style.RESET_ALL)
        return 2, None
    except FileNotFoundError:
        print(Fore.RED + "❌ flake8 not found in PATH." + Style.RESET_ALL)
        return 3, None
    except PermissionError:
        print(Fore.RED + f"❌ Permission denied when writing to {output_path}" + Style.RESET_ALL)
        return 4, None
    except IsADirectoryError:
        print(Fore.RED + f"❌ Expected a file but got a directory: {output_path}" + Style.RESET_ALL)
        return 5, None
    except NotADirectoryError:
        print(Fore.RED + f"❌ Part of path is not a directory: {output_dir}" + Style.RESET_ALL)
        return 6, None
    except OSError as e:
        if "No space left" in str(e):
            print(Fore.RED + "❌ Disk is full. Cannot write report." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"❌ OS error: {e}" + Style.RESET_ALL)
        return 7, None
    except KeyboardInterrupt:
        print(Fore.RED + "❌ Process interrupted by user (Ctrl+C)." + Style.RESET_ALL)
        return 8, None
    except Exception as e:
        print(Fore.RED + f"❌ Unexpected error: {type(e).__name__}: {e}" + Style.RESET_ALL)
        return 9, None

def summarise_flake8_report(file_path):
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
        print(f"❌ Failed to parse report: {e}")
        return

    print("\n📌 Error Summary by Code:")
    for code, count in sorted(error_counts.items(), key=lambda x: -x[1]):
        print(f"{code}: {count} occurrences")

    print("\n📁 Top Files with Most Errors:")
    for file, codes in sorted(file_errors.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"{file}: {len(codes)} issues")

def main():
    ensure_flake8_installed()
    exit_code, report_path = run_flake8()

    if report_path and Path(report_path).exists():
        summarise_flake8_report(report_path)
    else:
        print("⚠️ No report available to summarize.")

    sys.exit(exit_code if exit_code is not None else 1)

if __name__ == "__main__":
    main()
