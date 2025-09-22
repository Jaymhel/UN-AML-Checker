import xml.etree.ElementTree as ET

def parse_un_xml(xml_path):
    """
    Parse the UN SC Consolidated List XML file to extract individual data.
    
    Args:
        xml_path (str): Path to the UN SC XML file
        
    Returns:
        list: A list of dictionaries containing individual data
    """
    individuals = []
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Find all INDIVIDUAL elements
        for individual in root.findall('.//INDIVIDUAL'):
            dataid = individual.find('DATAID').text if individual.find('DATAID') is not None else 'N/A'
            
            # Get name information
            first_name = get_element_text(individual, 'FIRST_NAME')
            second_name = get_element_text(individual, 'SECOND_NAME')
            third_name = get_element_text(individual, 'THIRD_NAME')
            fourth_name = get_element_text(individual, 'FOURTH_NAME')
            
            # Get all alias names
            alias_names = []
            for alias in individual.findall('INDIVIDUAL_ALIAS'):
                alias_name = get_element_text(alias, 'ALIAS_NAME')
                if alias_name:
                    alias_names.append(alias_name)
            
            # Get additional details
            designation = get_element_text(individual, 'DESIGNATION')
            title = get_element_text(individual, 'TITLE')
            nationality = get_element_text(individual, 'NATIONALITY')
            listed_on = get_element_text(individual, 'LISTED_ON')
            comments = get_element_text(individual, 'COMMENTS1')
            
            individuals.append({
                'DATAID': dataid,
                'FIRST_NAME': first_name,
                'SECOND_NAME': second_name,
                'THIRD_NAME': third_name,
                'FOURTH_NAME': fourth_name,
                'FULL_NAME': ' '.join(filter(None, [first_name, second_name, third_name, fourth_name])),
                'ALIAS_NAMES': alias_names,
                'DESIGNATION': designation,
                'TITLE': title,
                'NATIONALITY': nationality,
                'LISTED_ON': listed_on,
                'COMMENTS': comments
            })
            
    except Exception as e:
        print(f"Error parsing XML file: {e}")
    
    return individuals

def get_element_text(element, tag_name):
    """
    Safely get text from an XML element.
    
    Args:
        element: XML element
        tag_name (str): Name of the tag to find
        
    Returns:
        str: Text content of the element, or empty string if not found
    """
    elem = element.find(tag_name)
    return elem.text if elem is not None else ''

def get_un_names_for_matching(un_individuals):
    """
    Extract all names from UN individual data for matching.
    
    Args:
        un_individuals (list): List of individual dictionaries
        
    Returns:
        dict: A dictionary mapping names to DATAIDs
    """
    name_to_dataid = {}
    
    for individual in un_individuals:
        dataid = individual['DATAID']
        
        # Add first name if exists
        if individual['FIRST_NAME']:
            name = individual['FIRST_NAME'].lower()
            if name not in name_to_dataid:
                name_to_dataid[name] = []
            name_to_dataid[name].append(dataid)
        
        # Add second name if exists
        if individual['SECOND_NAME']:
            name = individual['SECOND_NAME'].lower()
            if name not in name_to_dataid:
                name_to_dataid[name] = []
            name_to_dataid[name].append(dataid)
        
        # Add full name if exists
        if individual['FULL_NAME']:
            name = individual['FULL_NAME'].lower()
            if name not in name_to_dataid:
                name_to_dataid[name] = []
            name_to_dataid[name].append(dataid)
        
        # Add all alias names
        for alias in individual['ALIAS_NAMES']:
            if alias:
                name = alias.lower()
                if name not in name_to_dataid:
                    name_to_dataid[name] = []
                name_to_dataid[name].append(dataid)
    
    return name_to_dataid

def get_individuals_by_dataids(un_individuals, dataids):
    """
    Get complete information for individuals by their DATAIDs.
    
    Args:
        un_individuals (list): List of individual dictionaries
        dataids (list): List of DATAIDs to retrieve
        
    Returns:
        list: List of individual dictionaries matching the DATAIDs
    """
    return [ind for ind in un_individuals if ind['DATAID'] in dataids]
