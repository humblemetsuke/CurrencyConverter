import matplotlib.pyplot as plt


"""This function plots the frequency of Flake8 errors using
 vertical bar chart. error_counts is a dictionary, where the keys are
 the error codes, and the values are the frequency of the error codes.
 plt.figure creates a canvas/figure of 10 inches by 6 inches. These dimensions
 chosen for readability.
 
 This function does NOT make use of a line of code present in the 
 plot_top_files_chart function and that is:
 sorted_data = sorted(zip(files, issue_counts), key=lambda x: -x[1])[:10]
 The reason why this function doesn't make use of sorted_data is 
 because Flake8 error codes like E501, F401, etc., 
 are not naturally ordered by importance. Users will want to see ALL of the errors.
 Sorting therefore is not as necessary or crucial, and visual order is not as relevant.
 """
def plot_error_code_chart(error_counts):
    codes = list(error_counts.keys())
    counts = list(error_counts.values())

    plt.figure(figsize=(10,6))
    # codes are the bars' labels on
    # the x-axis counts are the height of each bar
    # color='skyblue' makes the bars light blue.
    plt.bar(codes, counts, color='skyblue')

    plt.xlabel("Error Code")
    plt.ylabel("Occurrences")
    plt.title("Flake8 Error Code Frequency")
    plt.xticks(rotation=45) # used to rotate 45 degrees, to avoid overlap.
    plt.tight_layout() # Automatically adjusts the padding/margins
    # so everything fits nicely.
    plt.savefig("flake8_error_codes.png", dpi=300) # Save to file.
    plt.savefig("flake8_error_codes.pdf")
    plt.savefig("flake8_error_codes.svg")
    plt.show() # displays the plot window.

"""This function creates a horizontal bar chart of the top 10 files 
with the most Flake8 errors."""


def plot_top_files_chart(file_errors):
    files = list(file_errors.keys())
    issue_counts = [len(errors) for errors in file_errors.values()]
    sorted_data = sorted(zip(files, issue_counts), key=lambda x: -x[1])[:10]
    top_files, top_counts = zip(*sorted_data)
    plt.figure(figsize=(12,6))
    plt.barh(top_files, top_counts, color ='salmon')
    plt.title("Top 10 Files with Most Flake8 Issues")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("flake8_error_codes.png", dpi=300) # Save to file.
    plt.savefig("flake8_error_codes.pdf")
    plt.savefig("flake8_error_codes.svg")
    plt.show()