import xml.etree.ElementTree as ET
from datetime import datetime

from un_data_parser import get_individuals_by_dataids

def get_complete_un_individual_info(xml_path, dataid):
    """
    Retrieve complete information for a UN individual by DATAID directly from XML.
    
    Args:
        xml_path (str): Path to the UN SC XML file
        dataid (str): DATAID of the individual to retrieve
        
    Returns:
        dict: Complete individual information
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Find the individual with the matching DATAID
        for individual in root.findall('.//INDIVIDUAL'):
            current_dataid = individual.find('DATAID')
            if current_dataid is not None and current_dataid.text == dataid:
                return extract_complete_individual_info(individual)
                
    except Exception as e:
        print(f"Error retrieving complete information for DATAID {dataid}: {e}")
    
    return None

def extract_complete_individual_info(individual):
    """
    Extract complete information from an INDIVIDUAL XML element.
    
    Args:
        individual: XML element for an individual
        
    Returns:
        dict: Complete individual information
    """
    def get_text(element, tag_name):
        elem = element.find(tag_name)
        return elem.text if elem is not None else ''
    
    def get_list(element, tag_name):
        return [elem.text for elem in element.findall(tag_name) if elem.text]
    
    dataid = get_text(individual, 'DATAID')
    
    # Basic information
    info = {
        'DATAID': dataid,
        'FIRST_NAME': get_text(individual, 'FIRST_NAME'),
        'SECOND_NAME': get_text(individual, 'SECOND_NAME'),
        'THIRD_NAME': get_text(individual, 'THIRD_NAME'),
        'FOURTH_NAME': get_text(individual, 'FOURTH_NAME'),
        'FULL_NAME': ' '.join(filter(None, [
            get_text(individual, 'FIRST_NAME'),
            get_text(individual, 'SECOND_NAME'),
            get_text(individual, 'THIRD_NAME'),
            get_text(individual, 'FOURTH_NAME')
        ])),
        'DESIGNATION': get_text(individual, 'DESIGNATION'),
        'TITLE': get_text(individual, 'TITLE'),
        'NATIONALITY': get_text(individual, 'NATIONALITY'),
        'LISTED_ON': get_text(individual, 'LISTED_ON'),
        'COMMENTS1': get_text(individual, 'COMMENTS1'),
        'COMMENTS2': get_text(individual, 'COMMENTS2'),
        'COMMENTS3': get_text(individual, 'COMMENTS3'),
        'COMMENTS4': get_text(individual, 'COMMENTS4'),
    }
    
    # Alias names
    info['ALIAS_NAMES'] = []
    for alias in individual.findall('INDIVIDUAL_ALIAS'):
        alias_name = get_text(alias, 'ALIAS_NAME')
        if alias_name:
            info['ALIAS_NAMES'].append(alias_name)
    
    # Dates of birth
    info['DATES_OF_BIRTH'] = []
    for dob in individual.findall('INDIVIDUAL_DATE_OF_BIRTH'):
        dob_type = get_text(dob, 'TYPE_OF_DATE')
        dob_date = get_text(dob, 'DATE')
        dob_year = get_text(dob, 'YEAR')
        dob_from = get_text(dob, 'FROM_YEAR')
        dob_to = get_text(dob, 'TO_YEAR')
        
        if dob_date:
            info['DATES_OF_BIRTH'].append(f"{dob_type}: {dob_date}" if dob_type else dob_date)
        elif dob_year:
            info['DATES_OF_BIRTH'].append(f"{dob_type}: {dob_year}" if dob_type else dob_year)
        elif dob_from and dob_to:
            info['DATES_OF_BIRTH'].append(f"{dob_type}: {dob_from}-{dob_to}" if dob_type else f"{dob_from}-{dob_to}")
    
    # Places of birth
    info['PLACES_OF_BIRTH'] = []
    for pob in individual.findall('INDIVIDUAL_PLACE_OF_BIRTH'):
        pob_city = get_text(pob, 'CITY')
        pob_state = get_text(pob, 'STATE_PROVINCE')
        pob_country = get_text(pob, 'COUNTRY')
        
        pob_parts = []
        if pob_city:
            pob_parts.append(pob_city)
        if pob_state:
            pob_parts.append(pob_state)
        if pob_country:
            pob_parts.append(pob_country)
        
        if pob_parts:
            info['PLACES_OF_BIRTH'].append(", ".join(pob_parts))
    
    # Addresses
    info['ADDRESSES'] = []
    for address in individual.findall('INDIVIDUAL_ADDRESS'):
        street = get_text(address, 'STREET')
        city = get_text(address, 'CITY')
        state = get_text(address, 'STATE_PROVINCE')
        country = get_text(address, 'COUNTRY')
        note = get_text(address, 'NOTE')
        
        address_parts = []
        if street:
            address_parts.append(street)
        if city:
            address_parts.append(city)
        if state:
            address_parts.append(state)
        if country:
            address_parts.append(country)
        
        address_str = ", ".join(address_parts)
        if note:
            address_str += f" ({note})"
        
        if address_str:
            info['ADDRESSES'].append(address_str)
    
    # Documents
    info['DOCUMENTS'] = []
    for doc in individual.findall('INDIVIDUAL_DOCUMENT'):
        doc_type = get_text(doc, 'TYPE_OF_DOCUMENT')
        doc_number = get_text(doc, 'NUMBER')
        doc_country = get_text(doc, 'ISSUING_COUNTRY')
        doc_date = get_text(doc, 'DATE_OF_ISSUE')
        note = get_text(doc, 'NOTE')
        
        doc_parts = []
        if doc_type:
            doc_parts.append(doc_type)
        if doc_number:
            doc_parts.append(f"Number: {doc_number}")
        if doc_country:
            doc_parts.append(f"Country: {doc_country}")
        if doc_date:
            doc_parts.append(f"Issue Date: {doc_date}")
        if note:
            doc_parts.append(f"Note: {note}")
        
        if doc_parts:
            info['DOCUMENTS'].append("; ".join(doc_parts))
    
    return info

def get_suspicious_persons_info(un_individuals, suspicious_dataids, suspicious_matches, xml_path):
    """
    Get complete information for suspicious persons and link with client matches.
    
    Args:
        un_individuals (list): List of all UN individual data
        suspicious_dataids (set): Set of DATAIDs for suspicious persons
        suspicious_matches (list): List of matches with client SN and matched name
        xml_path (str): Path to the UN XML file for complete data retrieval
        
    Returns:
        list: List of dictionaries with combined UN and client information
    """
    # Get basic information from parsed data
    suspicious_individuals = get_individuals_by_dataids(un_individuals, suspicious_dataids)
    
    # Enhance with complete information from XML
    enhanced_individuals = []
    for individual in suspicious_individuals:
        dataid = individual['DATAID']
        
        # Get complete information directly from XML
        complete_info = get_complete_un_individual_info(xml_path, dataid)
        if complete_info:
            individual.update(complete_info)
        
        # Find all client matches for this DATAID
        client_matches = [match for match in suspicious_matches if match['un_dataid'] == dataid]
        
        enhanced_individuals.append({
            **individual,
            'client_matches': client_matches
        })
    
    return enhanced_individuals

def format_complete_individual_info(individual, suspicious_client_data):
    """
    Format complete individual information for display including full client data.
    
    Args:
        individual (dict): Individual data dictionary with client matches
        suspicious_client_data (DataFrame): Client data for suspicious persons
        
    Returns:
        str: Formatted information string
    """
    lines = []
    
    # Basic information
    lines.append(f"UN DATAID: {individual['DATAID']}")
    lines.append(f"Full Name: {individual['FULL_NAME']}")
    
    if individual['DESIGNATION']:
        lines.append(f"Designation: {individual['DESIGNATION']}")
    
    if individual['TITLE']:
        lines.append(f"Title: {individual['TITLE']}")
    
    if individual['NATIONALITY']:
        lines.append(f"Nationality: {individual['NATIONALITY']}")
    
    if individual['LISTED_ON']:
        lines.append(f"Listed On: {individual['LISTED_ON']}")
    
    # Name details
    name_parts = []
    if individual['FIRST_NAME']:
        name_parts.append(f"First: {individual['FIRST_NAME']}")
    if individual['SECOND_NAME']:
        name_parts.append(f"Second: {individual['SECOND_NAME']}")
    if individual['THIRD_NAME']:
        name_parts.append(f"Third: {individual['THIRD_NAME']}")
    if individual['FOURTH_NAME']:
        name_parts.append(f"Fourth: {individual['FOURTH_NAME']}")
    
    if name_parts:
        lines.append("Name Details: " + ", ".join(name_parts))
    
    # Dates of birth
    if individual['DATES_OF_BIRTH']:
        lines.append(f"Dates of Birth: {', '.join(individual['DATES_OF_BIRTH'])}")
    
    # Places of birth
    if individual['PLACES_OF_BIRTH']:
        lines.append(f"Places of Birth: {', '.join(individual['PLACES_OF_BIRTH'])}")
    
    # Alias names
    if individual['ALIAS_NAMES']:
        lines.append(f"Alias Names: {', '.join(individual['ALIAS_NAMES'])}")
    
    # Addresses
    if individual['ADDRESSES']:
        lines.append("Addresses:")
        for address in individual['ADDRESSES']:
            lines.append(f"  - {address}")
    
    # Documents
    if individual['DOCUMENTS']:
        lines.append("Documents:")
        for doc in individual['DOCUMENTS']:
            lines.append(f"  - {doc}")
    
    # Comments
    comments = []
    for i in range(1, 5):
        comment_key = f'COMMENTS{i}'
        if individual.get(comment_key):
            comments.append(individual[comment_key])
    
    if comments:
        lines.append("Comments:")
        for comment in comments:
            lines.append(f"  - {comment}")
    
    # Client matches with FULL client data
    if individual['client_matches']:
        lines.append("")
        lines.append("CLIENT MATCHES WITH FULL DATA:")
        lines.append("=" * 50)
        
        for match in individual['client_matches']:
            client_sn = match['client_sn']
            
            # Find the client data for this SN
            client_row = suspicious_client_data[suspicious_client_data['SN'] == client_sn]
            
            if not client_row.empty:
                client_info = client_row.iloc[0]
                lines.append(f"CLIENT SN: {client_sn}")
                lines.append(f"  File No: {client_info['File_no']}")
                lines.append(f"  BRN: {client_info['BRN']}")
                lines.append(f"  Company: {client_info['Company']}")
                lines.append(f"  Officer: {client_info['Officer']}")
                lines.append(f"  Role: {client_info['Role']}")
                lines.append(f"  Matched Combination: {match['matched_combo']}")
                lines.append("-" * 40)
            else:
                lines.append(f"CLIENT SN: {client_sn} - DATA NOT FOUND")
                lines.append(f"  Matched Combination: {match['matched_combo']}")
                lines.append("-" * 40)
    
    return "\n".join(lines)

def safe_file_write(content, file_path, encoding='utf-8'):
    """
    Safely write content to a file with proper encoding handling.
    
    Args:
        content (str): Content to write to the file
        file_path (str): Path to the output file
        encoding (str): Encoding to use (default: utf-8)
    """
    try:
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except UnicodeEncodeError as e:
        print(f"Unicode encoding error: {e}")
        # Fallback: replace problematic characters
        with open(file_path, 'w', encoding=encoding, errors='replace') as f:
            f.write(content)
        print(f"Used character replacement for problematic Unicode characters")
        return True
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")
        return False
def generate_complete_suspicious_persons_report(suspicious_individuals, suspicious_client_data, output_path=None):
    """
    Generate a complete report of suspicious persons with all information including full client data.
    
    Args:
        suspicious_individuals (list): List of suspicious individual dictionaries
        suspicious_client_data (DataFrame): Client data for suspicious persons
        output_path (str): Path to save the report (optional)
        
    Returns:
        str: The report content
    """
    if not suspicious_individuals:
        report = "No suspicious persons found."
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
        return report
    
    report_lines = []
    report_lines.append("COMPLETE SUSPICIOUS PERSONS REPORT WITH FULL CLIENT DATA")
    report_lines.append("=" * 80)
    report_lines.append(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"Total suspicious UN individuals: {len(suspicious_individuals)}")
    report_lines.append(f"Total suspicious client records: {len(suspicious_client_data)}")
    report_lines.append("")
    
    for i, individual in enumerate(suspicious_individuals, 1):
        report_lines.append(f"SUSPICIOUS PERSON #{i}:")
        report_lines.append("=" * 80)
        report_lines.append(format_complete_individual_info(individual, suspicious_client_data))
        report_lines.append("")
        report_lines.append("=" * 80)
        report_lines.append("")
    
    # Add summary of all suspicious client data
    report_lines.append("SUMMARY OF ALL SUSPICIOUS CLIENT DATA")
    report_lines.append("=" * 80)
    
    if not suspicious_client_data.empty:
        for _, row in suspicious_client_data.iterrows():
            report_lines.append(f"SN: {row['SN']}")
            report_lines.append(f"  File No: {row['File_no']}")
            report_lines.append(f"  BRN: {row['BRN']}")
            report_lines.append(f"  Company: {row['Company']}")
            report_lines.append(f"  Officer: {row['Officer']}")
            report_lines.append(f"  Role: {row['Role']}")
            report_lines.append("-" * 40)
    else:
        report_lines.append("No suspicious client data found.")
    
    report = "\n".join(report_lines)
    
    if output_path:
        safe_file_write(report, output_path)
    
    return report