import pandas as pd

def generate_name_combinations(full_name):
    """
    Generate all possible name combinations from a full name string.
    
    Args:
        full_name (str): The full name with parts separated by spaces
        
    Returns:
        list: A list of all possible name combinations
    """
    if not full_name or not isinstance(full_name, str):
        return []
    
    # Split the name into parts
    name_parts = full_name.strip().split()
    
    if not name_parts:
        return []
    
    # Remove empty strings and duplicates
    name_parts = list(set(part for part in name_parts if part))
    
    # If only one part, return it
    if len(name_parts) == 1:
        return name_parts
    
    combinations = set()
    
    # Add all individual parts
    for part in name_parts:
        combinations.add(part)
    
    # Generate all possible combinations of parts
    from itertools import permutations
    for r in range(2, len(name_parts) + 1):
        for perm in permutations(name_parts, r):
            combinations.add(" ".join(perm))
    
    # Add common variations (last name, first name) etc.
    if len(name_parts) >= 2:
        # First name + last name
        combinations.add(f"{name_parts[0]} {name_parts[-1]}")
        # Last name + first name
        combinations.add(f"{name_parts[-1]} {name_parts[0]}")
        
        # If we have a middle name
        if len(name_parts) >= 3:
            # First + middle
            combinations.add(f"{name_parts[0]} {name_parts[1]}")
            # Middle + last
            combinations.add(f"{name_parts[1]} {name_parts[-1]}")
            # First + middle + last
            combinations.add(f"{name_parts[0]} {name_parts[1]} {name_parts[-1]}")
            # Last + first + middle
            combinations.add(f"{name_parts[-1]} {name_parts[0]} {name_parts[1]}")
            # Last + middle + first
            combinations.add(f"{name_parts[-1]} {name_parts[1]} {name_parts[0]}")
    
    return sorted(list(combinations), key=lambda x: (-len(x), x))

def process_client_data(client_data):
    """
    Process client data to generate name combinations for all officers.
    Removes duplicate officer names before processing.
    
    Args:
        client_data (DataFrame): Client data with 'SN' and 'Officer' columns
        
    Returns:
        dict: A dictionary mapping client SN to name and combinations
    """
    if client_data is None or 'Officer' not in client_data.columns or 'SN' not in client_data.columns:
        return {}
    
    # Create a mapping of SN to officer name (handling duplicates)
    sn_to_officer = {}
    
    for _, row in client_data.iterrows():
        sn = row['SN']
        officer_name = row['Officer']
        
        if officer_name and isinstance(officer_name, str) and pd.notna(sn):
            # Use SN as key to handle duplicate officer names
            sn_to_officer[sn] = officer_name.strip()
    
    client_combinations = {}
    
    # Generate combinations for each unique officer (by SN)
    for sn, officer_name in sn_to_officer.items():
        combinations = generate_name_combinations(officer_name)
        client_combinations[sn] = {
            'name': officer_name,
            'combinations': combinations
        }
    
    return client_combinations
