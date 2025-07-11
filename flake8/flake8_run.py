import subprocess
import sys
from pathlib import Path
from datetime import datetime
from colorama import init, Fore, Style
"""colorama.init() at the top for cross-platform color support.
Fore.GREEN for success messages.
Fore.YELLOW for warnings (linting issues).
Fore.RED for errors and exceptions.
Resetting color with Style.RESET_ALL after each print to avoid bleeding colors.
Comprehensive exception handling with colored feedback.
"""
init()

TIMEOUT_IN_SECONDS = 40 # 40 second timeout

def ensure_flake8_installed():
    """Checks if flake8 is available, and optionally installs it if missing."""
    try:
        subprocess.run(["flake8", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except FileNotFoundError:
        print(Fore.RED + f"❌ flake8 is not installed." + Style.RESET_ALL)
        user_input = input(Fore.CYAN +"👉 Would you like to install flake8 now? (y/n): " + Style.RESET_ALL).strip().lower()
        if user_input == 'y':
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "flake8"], check=True)
                print(Fore.GREEN +f"✅ flake8 successfully installed." + Style.RESET_ALL)
            except subprocess.CalledProcessError:
                print(Fore.RED + f"❌ Failed to install flake8. Please install it manually: pip install flake8" + Style.RESET_ALL)
                sys.exit(1)
        else:
            print(Fore.RED + "❌ flake8 is required. Exiting." + Style.RESET_ALL)
            sys.exit(1)




def run_flake8(output_dir="reports", output_file="flake8-report.txt"):
    """output_dir: the folder where the report will be saved (default is "reports").
    output_file: the filename of the flake8 report (default is "flake8-report.txt").
    """

    """
    run_flake8() returns an int exit code representing the flake8 result or error condition.
    The main script exits with that code, so it can be used directly in CI pipelines or other automation tools.
    I added custom return codes for various error conditions to differentiate issues beyond just flake8 exit codes.
    """

    print(Fore.CYAN + "🔍 Running flake8 linting..." + Style.RESET_ALL)
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create the directory if it doesn't exist (including parents)
        output_dir_path = Path(output_dir)
        # Creates the folder (and any missing parent folders).
        # Doesn't raise an error if the folder already exists.
        output_dir_path.mkdir(parents=True, exist_ok=True)
        base = Path(output_file).stem
        output_filename = f"{base}_{timestamp}.txt"

        # Construct full output file path inside the directory
        output_path = output_dir_path / output_filename

        """Open the file for writing AFTER creating the directory.
        The with block ensures that the file is properly closed after usage.
        """

        with output_path.open("w") as f:
            """Run flake8, redirect stdout and stderr to the file
            check=False: don’t raise an exception 
            even if flake8 returns a non-zero exit code."""
            result = subprocess.run(
            ["flake8"],
            stdout=f,
            stderr=subprocess.STDOUT,
            check=False,
            timeout = TIMEOUT_IN_SECONDS
            )

        # Check the exit code and print status
        if result.returncode == 0:

            if output_path.stat().st_size == 0:
                print(Fore.GREEN + f"✅ flake8 finished with no issues. "
                      f"Report is empty, this is normal: {output_path}."+ Style.RESET_ALL)
            else:
                print(Fore.GREEN + f"✅ flake8 finished with no issues. "
                      f"Report saved to: {output_path}." + Style.RESET_ALL)

        elif result.returncode == 1:
            print(Fore.YELLOW + f"⚠️ flake8 has finished with linting issues. See {output_path}"
                  f"for further details." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"❌ flake8 failed (exit code {result.returncode}).")
            print(f"    Check {output_path} for possible runtime errors or misconfigurations." + Style.RESET_ALL)

    except subprocess.TimeoutExpired:
        print(Fore.RED + f"❌ flake8 timed out after {TIMEOUT_IN_SECONDS} seconds. Process was terminated." + Style.RESET_ALL)
        return 2
    except FileNotFoundError:
        """This happens if the 'flake8' executable is not found. 
        This will because flake8 is not installed OR
        not found within the system PATH."""
        print(Fore.RED + f"❌ Error: 'flake8' is not installed or not found in your PATH." + Style.RESET_ALL)
        return 3
    except PermissionError:
        """Happens if the script doesn't have write permission for the directory
        or file"""
        print(Fore.RED + f"❌ Error: Permission denied when writing to {output_path}." + Style.RESET_ALL)
        return 4
    except IsADirectoryError: #invoked if a folder instead of file is found.
        print(Fore.RED + f"❌ Expected a file but got a directory: {output_path}" + Style.RESET_ALL)
        return 5
    except NotADirectoryError:
        print(Fore.RED + f"❌ Part of the specified path is not a directory: {output_dir}" + Style.RESET_ALL)
        return 6
    except OSError as e: #Catch-all for general system-related errors
        # (e.g., disk full, invalid filename, I/O failure).
        if "No space left" in str(e):
            print(Fore.RED + "❌ Disk is full. Unable to write report." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"❌ OS error: {e}" + Style.RESET_ALL)
        return 7
    except KeyboardInterrupt:
        # Gracefully exits if the user presses Ctrl+C during the process.
        print(Fore.RED + f"❌ Process interrupted by user (Ctrl+C)." + Style.RESET_ALL)
        return 8
    except Exception as e:
        # Catches any other unanticipated exceptions
        # and prints the exception type and message.
        print(Fore.RED + f"❌ Unexpected error: {type(e).__name__}: {e}" + Style.RESET_ALL)
        return 9

def main():
    ensure_flake8_installed()
    exit_code = run_flake8()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()


