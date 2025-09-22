from un_data_parser import get_un_names_for_matching

def find_suspicious_persons(client_combinations, un_name_mapping):
    """
    Compare client name combinations against UN list names.
    
    Args:
        client_combinations (dict): Dictionary of client names, SNs, and their combinations
        un_name_mapping (dict): Dictionary mapping UN names to DATAIDs
        
    Returns:
        tuple: (suspicious_dataids, suspicious_matches) where:
            - suspicious_dataids: Set of DATAIDs for suspicious persons
            - suspicious_matches: List of matches with client SN and matched name
    """
    suspicious_dataids = set()
    suspicious_matches = []
    
    for client_sn, client_info in client_combinations.items():
        client_name = client_info['name']
        combinations = client_info['combinations']
        
        for combo in combinations:
            # Check if this combination matches any UN name
            if combo.lower() in un_name_mapping:
                # Add all DATAIDs associated with this name
                for dataid in un_name_mapping[combo.lower()]:
                    suspicious_dataids.add(dataid)
                    suspicious_matches.append({
                        'client_sn': client_sn,
                        'client_name': client_name,
                        'matched_combo': combo,
                        'un_dataid': dataid
                    })
    
    return suspicious_dataids, suspicious_matches
