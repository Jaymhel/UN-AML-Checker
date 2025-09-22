import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import hashlib
import json

def download_un_sc_list():
    """
    Download the UN Security Council Consolidated List in XML format
    and save it to the local machine with metadata.
    Returns the path to the downloaded XML file and metadata.
    """
    # URL for the UN SC Consolidated List (XML format)
    url = "https://scsanctions.un.org/resources/xml/en/consolidated.xml"
    
    # Headers to simulate a legitimate browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    try:
        # Make the request to download the XML file
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Get the current timestamp for filename
        current_time = datetime.now()
        timestamp_str = current_time.strftime("%Y%m%d_%H%M%S")
        
        # Create data directory if it doesn't exist
        data_dir = "un_data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Define file paths
        xml_filename = f"un_sc_consolidated_{timestamp_str}.xml"
        xml_filepath = os.path.join(data_dir, xml_filename)
        
        # Save the XML file
        with open(xml_filepath, 'wb') as f:
            f.write(response.content)
        
        # Calculate file hash for verification
        file_hash = hashlib.sha256(response.content).hexdigest()
        
        # Parse the XML to extract basic information
        root = ET.fromstring(response.content)
        
        # Extract some metadata from the XML
        date_of_issue = root.find('.//DATE_OF_ISSUE')
        date_of_issue = date_of_issue.text if date_of_issue is not None else "Unknown"
        
        # Count the number of entries
        individual_entries = root.findall('.//INDIVIDUAL')
        entity_entries = root.findall('.//ENTITY')
        total_entries = len(individual_entries) + len(entity_entries)
        
        # Create metadata
        metadata = {
            'download_date': current_time.isoformat(),
            'original_url': url,
            'file_name': xml_filename,
            'file_size': len(response.content),
            'file_hash_sha256': file_hash,
            'un_list_date_of_issue': date_of_issue,
            'individual_entries': len(individual_entries),
            'entity_entries': len(entity_entries),
            'total_entries': total_entries
        }
        
        # Save metadata to JSON file
        metadata_filename = f"metadata_{timestamp_str}.json"
        metadata_filepath = os.path.join(data_dir, metadata_filename)
        
        with open(metadata_filepath, 'w') as f:
            json.dump(metadata, f, indent=4)
        
        return xml_filepath, metadata
        
    except Exception as e:
        return None, None
