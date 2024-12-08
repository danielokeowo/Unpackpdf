import pdfplumber
import pandas as pd
import os

def extract_tables_from_pdf(pdf_path):
    """
    Extracts tables from a PDF file and returns them as a list of DataFrames.

    Arguements:
        pdf_path (str): The file path to the PDF file.

    Returns:
        list: A list of pandas DataFrames, each representing a table from the PDF.
    """
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Look for tables on this page
            page_tables = page.extract_tables()
            for table in page_tables:
                if table:
                    # Convert the raw table into a DataFrame
                    df = pd.DataFrame(table)
                    tables.append(df)
    return tables

def clean_extracted_data(tables):
    """
    Cleans up the raw table data and makes it more useful.

    Arguments:
        tables (list): A list of DataFrames with the raw table data.

    Returns:
        list: A list of all Cleaned-up DataFrames.
    """
    cleaned_data = []
    for table in tables:
        # Assuming the first row has the column names
        table.columns = table.iloc[0]  # Set the first row as headers
        table = table[1:]  # Drop the header row from the data
        table = table.dropna(how='all')  # Get rid of any rows that are completely empty
        cleaned_data.append(table)
    return cleaned_data

def process_pdfs_in_directory(directory_path, output_file):
    """
    Goes through all the PDFs in a folder, extracts tables, cleans them up,
    and saves everything into one Excel or CSV file.

    Args:
        directory_path (str): The folder where your PDF files are stored.
        output_file (str): The file where you want the combined data saved (Excel or CSV).
    """
    all_data = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(directory_path, file_name)
            print(f"Processing {file_name}...")

            # Extract tables and clean them up
            tables = extract_tables_from_pdf(pdf_path)
            cleaned_tables = clean_extracted_data(tables)

            # Add a column to keep track of which file this table came from
            for table in cleaned_tables:
                table['Source_File'] = file_name
                all_data.append(table)

    # Combine all the cleaned tables into one big DataFrame
    final_df = pd.concat(all_data, ignore_index=True)

    # Save the results to a file
    if output_file.endswith('.csv'):
        final_df.to_csv(output_file, index=False)
    else:
        final_df.to_excel(output_file, index=False)

    print(f'94All Done! Your data is saved in {output_file}")

# Run the script
if __name__ == "__main__":
    # Ask the user for the directory with PDFs and where to save the output
    input_directory = input("Enter the path to the folder containing your PDF files: ").strip()
    output_file = input("Enter the full path for the output file (Excel or CSV): ").strip()

    # Validates user input
    if not os.path.isdir(input_directory):
        print("The directory you entered does not exist. Please try again.")
    elif not output_file.endswith(('.xlsx', '.csv')):
        print("The output file must end with .xlsx or .csv. Please try again.")
    else:
        # Starts the process
        process_pdfs_in_directory(input_directory, output_file)
}