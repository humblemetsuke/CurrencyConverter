import matplotlib.pyplot as plt
import textwrap
import seaborn as sns
from constants import FLAKE8_GRAPHS_DIR
from logger_setup import setup_logger
from datetime import datetime
from pathlib import Path
sns.set_theme(style="whitegrid")
logger = setup_logger()


def save_plot(name: str,
              output_dir: Path = FLAKE8_GRAPHS_DIR,
              formats: list = None,
              add_timestamp: bool = False):

    """
    Saves the current Matplotlib figure in multiple formats.

    Parameters:
        name (str): Base name of the file (no extension).
        output_dir (Path): Output directory (default: FLAKE8_GRAPHS_DIR).
        formats (list): List of file extensions to save (e.g., ['png', 'svg']).
        add_timestamp (bool): Whether to append a timestamp to the filename.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    if formats is None:
        formats = ['png', 'pdf', 'svg']

    if add_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"{name}_{timestamp}"


    for ext in formats:
        filename = output_dir / f"{name}.{ext}"
        try:
            plt.savefig(filename, dpi=300)
            logger.info(f"Saved plot: {filename}")
        except Exception as e:
            logger.error(f"Failed to save plot '{filename}': {e}")



def wrap_labels(labels, width=40):
    """Wraps long strings into multiple lines for better readability."""
    return ['\n'.join(textwrap.wrap(label, width)) for label in labels]


def plot_error_code_chart(error_counts: dict, show: bool = False,
                          filter_codes: set = None):
    """
    Plots a bar chart showing the frequency of each Flake8 error code.

    Parameters:
        error_counts (dict): Mapping of error codes to their occurrence counts.
        show (bool): If True, displays the plot interactively.
        filter_codes (set or None): Optional set of error codes to include.
    """
    if not error_counts:
        logger.warning("No error counts to plot.")
        return

    # Apply filtering if specified
    filtered = {code: count for code, count in error_counts.items()
                if (filter_codes is None or code in filter_codes)}

    if not filtered:
        logger.warning("No error counts match the filter criteria.")
        return

    try:
        codes, counts = zip(*sorted(filtered.items()))

        plt.figure(figsize=(10, 6))
        plt.bar(codes, counts, color='skyblue')
        plt.xlabel("Error Code")
        plt.ylabel("Occurrences")
        plt.title("Flake8 Error Code Frequency")
        plt.xticks(rotation=45)
        plt.tight_layout()

        save_plot("flake8_error_codes")

        if show:
            plt.show()
        plt.close()
    except Exception as e:
        logger.error(f"Failed to plot error codes: {e}")

def plot_top_files_chart(file_errors: dict, show: bool = False,
                         filter_files: set = None, min_issues: int = 1):
    """
    Plots a horizontal bar chart of the top 10 files with the most Flake8 issues.

    Parameters:
        file_errors (dict): Mapping of file names to lists of error messages.
        show (bool): If True, displays the plot interactively.
        filter_files (set or None): Optional set of filenames to include.
        min_issues (int): Minimum number of issues a file must have to be included.
    """
    if not file_errors:
        logger.warning("No data to plot for top files.")
        return

    # Filter files by name and issue count
    filtered = {
        f: errs for f, errs in file_errors.items()
        if (filter_files is None or f in filter_files) and len(errs) >= min_issues
    }

    if not filtered:
        logger.warning("No files meet the filter criteria.")
        return

    sorted_data = sorted(
        ((f, len(errs)) for f, errs in filtered.items()),
        key=lambda x: -x[1]
    )[:10]

    if not sorted_data:
        logger.warning("No data to plot for top files after sorting.")
        return

    try:
        top_files, top_counts = zip(*sorted_data)
        wrapped_files = wrap_labels(top_files, width=50)

        plt.figure(figsize=(12, 6))
        plt.barh(wrapped_files, top_counts, color='salmon')
        plt.title("Top 10 Files with Most Flake8 Issues")
        plt.xlabel("Number of Issues")
        plt.gca().invert_yaxis()
        plt.tight_layout()

        save_plot("flake8_top_files")

        if show:
            plt.show()
        plt.close()
    except Exception as e:
        logger.error(f"Failed to plot top files chart: {e}")
