"""Imports the subprocess module, which allows for external commands
 and programs (like flake8) and interact with their input/output."""
import subprocess


# flake8-report.txt is the file in which the contents of flake8 will be outputted.
def run_flake8(output_file="flake8-report.txt"):
    # 2nd argument, "w", creates the file if not exists, over-write if it does.
    # This helps to avoid any errors if the file is already present.
    with open(output_file, "w") as f:
        """Run flake8 and redirect both stdout and stderr to the file
        stderr=subprocess.STDOUT redirects the standard error output (errors and warnings)
        to the same place as standard output — in this case, the same file f.
        """
        result = subprocess.run(["flake8"], stdout=f, stderr=subprocess.STDOUT)

    """ Command-line programs use an exit code of 0 for successful operations.
    Here, we mean that issues relate to linting and formatting issues."""
    if result.returncode == 0:
        print("✅ flake8 finished with no issues.")
    else:
        print(f"⚠️ flake8 completed with issues. See {output_file} for details.")


if __name__ == "__main__":
    run_flake8()
