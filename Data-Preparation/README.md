### Overview
This Python script performs data preparation tasks for the NSCLC-ICI-Biomarkers project. It reads clinical, sample, and mutation data from various data folders, performs data filtering, and harmonizes column names. The processed dataset is exported to a text file.

### Prerequisites
- Python 3
- pandas
- matplotlib
- seaborn

### Instructions
1. Ensure the required libraries are installed.
2. Set the appropriate file paths and parameters in the script.
3. Run the script to perform data preparation.

### Script Details
1. The script imports necessary libraries, sets working directories, and defines parameters.
2. It defines several functions for data handling, such as removing commented lines from data files, reading data into dictionaries of DataFrames, and harmonizing column names.
3. The script executes the defined functions to prepare the dataset.
4. It waits for user confirmation at specific steps to ensure correct execution.
5. The final dataset is exported to a tab-separated values (TSV) text file named `output_file.txt`.

### Important Files
- `mutations.txt`: Contains mutations of interest specified in the file.
- `column_names_config.txt`: Contains configuration for column names to be harmonized.
- `Data` Folder: Contains clinical, sample, and mutations data in separate directories.
- `output_file.txt`: The final processed dataset exported as a TSV file.

### Instructions for Use
1. Clone the repository to your local machine.
2. Ensure the required libraries are installed by running `pip install -r requirements.txt`.
3. Navigate to the project directory and execute the data preparation script with `python data_preparation.py`.
4. Follow the instructions provided by the script and provide input when prompted.
5. The processed dataset will be saved as `output_file.txt`.

### Notes
- Before proceeding with the data preparation, ensure that the `columns_of_interest.txt` file includes only the columns of interest.
- Review the generated visualizations (`na_bar_plot.png` and `na_heatmap.png`) to check for missing data.
- The `column_name_harmonization.txt` file allows you to define columns that represent the same information.
