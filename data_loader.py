import pandas as pd
import sys

class DataLoader:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.data = {}

    def load_data(self):
        try:
            xlsx = pd.ExcelFile(self.excel_file)
            for sheet_name in xlsx.sheet_names:
                self.data[sheet_name] = pd.read_excel(xlsx, sheet_name)
            print(f"Loaded {len(self.data)} tables from Excel file.")
        except ImportError as e:
            print("Error: Missing required dependency.")
            print(str(e))
            print("\nTo fix this, please install the required dependency by running:")
            print("pip install openpyxl")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred while loading the data: {str(e)}")
            sys.exit(1)

    def get_data(self):
        return self.data

if __name__ == "__main__":
    loader = DataLoader("data.xlsx")
    loader.load_data()
    loaded_data = loader.get_data()
    
    # Print some information about the loaded data
    for table_name, df in loaded_data.items():
        print(f"\nTable: {table_name}")
        print(f"Shape: {df.shape}")
        print("Columns:")
        for column in df.columns:
            print(f"  - {column}")