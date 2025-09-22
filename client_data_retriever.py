import pandas as pd

def get_client_data_by_sn(client_data, suspicious_sns):
    """
    Retrieve client data for suspicious serial numbers.
    
    Args:
        client_data (DataFrame): The complete client data
        suspicious_sns (list): List of suspicious SNs
        
    Returns:
        DataFrame: Client data for the suspicious SNs
    """
    if client_data is None or not suspicious_sns:
        return pd.DataFrame()
    
    # Filter client data for suspicious SNs
    suspicious_client_data = client_data[client_data['SN'].isin(suspicious_sns)]
    
    return suspicious_client_data

def format_client_data(client_data):
    """
    Format client data for display in reports.
    
    Args:
        client_data (DataFrame): Client data to format
        
    Returns:
        str: Formatted client data string
    """
    if client_data.empty:
        return "No client data available."
    
    lines = []
    
    for _, row in client_data.iterrows():
        lines.append(f"SN: {row['SN']}")
        lines.append(f"File No: {row['File_no']}")
        lines.append(f"BRN: {row['BRN']}")
        lines.append(f"Company: {row['Company']}")
        lines.append(f"Officer: {row['Officer']}")
        lines.append(f"Role: {row['Role']}")
        lines.append("-" * 40)
    
    return "\n".join(lines)

def generate_client_report(suspicious_client_data, output_path=None):
    """
    Generate a report of suspicious client data.
    
    Args:
        suspicious_client_data (DataFrame): Client data for suspicious persons
        output_path (str): Path to save the report (optional)
        
    Returns:
        str: The report content
    """
    if suspicious_client_data.empty:
        report = "No suspicious client data found."
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
        return report
    
    report_lines = []
    report_lines.append("SUSPICIOUS CLIENT DATA REPORT")
    report_lines.append("=" * 50)
    report_lines.append(f"Total suspicious clients found: {len(suspicious_client_data)}")
    report_lines.append("")
    
    report_lines.append(format_client_data(suspicious_client_data))
    
    report = "\n".join(report_lines)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(report)
    
    return report
