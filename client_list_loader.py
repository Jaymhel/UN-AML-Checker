import os
import pandas as pd
import re
from datetime import datetime

def find_latest_client_file():
    """
    Find the latest client CSV file in the clients_data folder based on the filename date.
    Returns the path to the latest file and its date.
    """
    clients_dir = "clients_data"
    
    # Check if clients_data directory exists
    if not os.path.exists(clients_dir):
        return None, None
    
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(clients_dir) if f.endswith('.csv')]
    
    if not csv_files:
        return None, None
    
    # Extract dates from filenames and find the latest one
    dated_files = []
    for csv_file in csv_files:
        # Try to extract date from filename (format: YYYYMMDD_clients.csv)
        match = re.match(r'(\d{8})_clients\.csv$', csv_file)
        if match:
            date_str = match.group(1)
            try:
                file_date = datetime.strptime(date_str, "%Y%m%d")
                dated_files.append((file_date, csv_file))
            except ValueError:
                continue
            
    if not dated_files:
        return None, None
    
    # Find the file with the latest date
    latest_date, latest_file = max(dated_files, key=lambda x: x[0])
    latest_file_path = os.path.join(clients_dir, latest_file)
    
    return latest_file_path, latest_date

def load_client_data(file_path):
    """
    Load client data from a CSV file with the new format.
    The CSV should have headers: SN, File_no, BRN, Company, Officer, Role
    Returns the client data as a DataFrame.
    """
    try:
        # Read the CSV file
        client_data = pd.read_csv(file_path)
        
        # Validate required columns
        required_columns = ['SN', 'File_no', 'BRN', 'Company', 'Officer', 'Role']
        missing_columns = [col for col in required_columns if col not in client_data.columns]
        
        if missing_columns:
            print(f"Error: Missing required columns: {missing_columns}")
            return None
        
        return client_data
        
    except Exception as e:
        print(f"Error processing client data: {e}")
        return None
