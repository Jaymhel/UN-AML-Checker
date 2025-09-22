# Setup Instructions

## Prerequisites
- Python 3.8 or higher
- pip package manager

## Installation
1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Create data directories: `mkdir un_data clients_data reports`

## Usage
1. Place client CSV files in `clients_data/` with naming format: `YYYYMMDD_clients.csv`
2. CSV format must include columns: SN, File_no, BRN, Company, Officer, Role
3. Run the main script: `python main.py`
4. Review reports in the `reports/` directory

## Data Security
- All processing occurs locally on your machine
- No data is transmitted to external servers
- You are responsible for securing client data

## Code Structure

UN-AML-Checker/
   --- main.py
   
   --- client_data_retriever.py
   
   --- client_list_loader.py
   
   --- comparision_tool.py
   
   --- name_combinations.py
   
   --- un_data_parser.py
   
   --- un_data_retriever.py
   
   --- unlist_loader.py
   
   ---/clients_data/YYYYMMDD_clients.csv   (prepare by you)
   
   ---/report/                             (report generated in here)
   
   ---/un_data/                            (save the un data in here) 

