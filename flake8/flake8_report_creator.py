
"""subprocess is used to run flake8 as if from the command line.
datetime class is used for timestamping the generated flake8 reports.
Path is imported to provide an object-oriented way to handle filesystem paths
for directories and files.
Chosen because more robust and cross-platform than plain strings.
logger is the custom logging function used in place of print statements for more
robust and informative debugging.
FLAKE8_REPORTS_DIR is a pre-defined constant imported to avoid usage of hard-coded
strings."""

import subprocess
from datetime import datetime
from pathlib import Path
from logger_setup import setup_logger
from constants import FLAKE8_REPORTS_DIR
logger = setup_logger()

# --- Run flake8 and create report, storing to specified directory ---

# path argument is optional, with the default being "." which is the current
# directory.
def run_flake8(path=".") -> Path:

    # gets the current date and time
    # this ensures that there is duplication of the generated files.
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = FLAKE8_REPORTS_DIR / f"flake8-report_{timestamp}.txt"

    # Informational message to user to confirm that analysis being undertaken
    # with specified directory.
    logger.info(f"Running flake8 on path {path}...")

    # Open report file in write mode, with ensures the file is closed properly.
    with report_path.open("w", encoding="utf-8") as f:

        """flake8 command is ran as a subprocess, targeting the specified path.
        Entirety of this block runs the actual linting."""
        result = subprocess.run(["flake8", path],
                                stdout=f, # sends output to the report file
                                stderr=subprocess.PIPE, # capture error messages
                                text=True) # ensure the output is treated as text.
    # Checks if there is a severe error with the linting.
    # Return code 0 means no issues
    # Return code 1 means linting issues (normal)
    # Return 2 means there has been an internal/fatal error.
    if result.returncode > 1:
        # logs error message if flake8 crashed or returned unexpected status.
        logger.error(f"flake8 failed with exit code {result.returncode}")
    elif result.stderr:
        logger.warning(f"flake8 stderr: {result.stderr}")
        # If stderr has any output but the return code is acceptable
        # (likely 1), this line catches and logs it.
    else:
        logger.info(f"✅ Flake8 report saved to: {report_path}")
        # If no errors generated, then document success.
    return report_path
