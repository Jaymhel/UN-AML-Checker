from un_list_loader import download_un_sc_list
from client_list_loader import find_latest_client_file, load_client_data
from name_combinations import process_client_data
from un_data_parser import parse_un_xml, get_un_names_for_matching
from comparison_tool import find_suspicious_persons
from un_data_retriever import get_suspicious_persons_info, generate_complete_suspicious_persons_report
from client_data_retriever import get_client_data_by_sn
import os
from datetime import datetime

def main():
    # Load UN SC list
    print("Loading UN SC Consolidated List...")
    xml_path, un_metadata = download_un_sc_list()
    
    if xml_path:
        print(f"✓ UN List loaded: {xml_path}")
        print(f"  Total entries: {un_metadata['total_entries']}")
        
        # Parse UN XML data for basic matching
        print("Parsing UN XML data for matching...")
        un_individuals = parse_un_xml(xml_path)
        print(f"  Parsed {len(un_individuals)} individuals from UN list")
        
        # Create name mapping for matching
        print("Creating UN name mapping...")
        un_name_mapping = get_un_names_for_matching(un_individuals)
        print(f"  Created mapping with {len(un_name_mapping)} unique names")
    else:
        print("✗ Failed to load UN List")
        return
    
    # Load client data
    print("\nLoading client data...")
    client_file_path, client_file_date = find_latest_client_file()
    
    if client_file_path:
        print(f"✓ Latest client file: {client_file_path}")
        print(f"  File date: {client_file_date.strftime('%Y-%m-%d')}")
        
        client_data = load_client_data(client_file_path)
        
        if client_data is not None:
            print(f"✓ Client data loaded: {len(client_data)} records")
            
            # Generate name combinations
            print("\nGenerating name combinations for officers...")
            client_combinations = process_client_data(client_data)
            
            print(f"  Generated combinations for {len(client_combinations)} unique officers (by SN)")
            total_combinations = sum(len(info['combinations']) for info in client_combinations.values())
            print(f"  Total name combinations: {total_combinations}")
            
            # Find suspicious persons
            print("\nComparing names against UN SC list...")
            suspicious_dataids, suspicious_matches = find_suspicious_persons(client_combinations, un_name_mapping)
            print(f"  Found {len(suspicious_dataids)} suspicious DATAIDs")
            print(f"  Found {len(suspicious_matches)} individual matches")
            
            # Get complete information for suspicious persons
            print("Retrieving complete information for suspicious persons...")
            suspicious_individuals = get_suspicious_persons_info(
                un_individuals, suspicious_dataids, suspicious_matches, xml_path
            )
            
            # Get suspicious client SNs
            suspicious_sns = list(set([match['client_sn'] for match in suspicious_matches]))
            
            # Get client data for suspicious SNs
            print("Retrieving client data for suspicious persons...")
            suspicious_client_data = get_client_data_by_sn(client_data, suspicious_sns)
            
            # Generate complete report
            print("Generating complete suspicious persons report...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create reports directory if it doesn't exist
            os.makedirs("reports", exist_ok=True)
            
            # Generate complete report with all data
            complete_report_filename = f"complete_suspicious_report_{timestamp}.txt"
            complete_report_path = os.path.join("reports", complete_report_filename)
            complete_report = generate_complete_suspicious_persons_report(
                suspicious_individuals, suspicious_client_data, complete_report_path
            )
            
            # Display summary
            print("\n" + "="*80)
            print("COMPREHENSIVE COMPARISON RESULTS")
            print("="*80)
            print(f"Total suspicious UN individuals: {len(suspicious_individuals)}")
            print(f"Total suspicious client records: {len(suspicious_client_data)}")
            print(f"Total unique client SNs with matches: {len(suspicious_sns)}")
            
            if suspicious_individuals:
                print(f"\nComplete report generated: {complete_report_path}")
                
                # Display summary of first match
                print("\nSUMMARY OF FIRST MATCH:")
                first_individual = suspicious_individuals[0]
                client_sns = [match['client_sn'] for match in first_individual['client_matches']]
                
                print(f"UN Individual: {first_individual['FULL_NAME']} (ID: {first_individual['DATAID']})")
                print(f"Designation: {first_individual.get('DESIGNATION', 'N/A')}")
                
                # Show client details for the first SN
                if client_sns:
                    first_sn = client_sns[0]
                    client_row = suspicious_client_data[suspicious_client_data['SN'] == first_sn]
                    if not client_row.empty:
                        print(f"Client SN {first_sn}: {client_row.iloc[0]['Company']} - {client_row.iloc[0]['Officer']}")
                
                if len(suspicious_individuals) > 1:
                    print(f"\n... and {len(suspicious_individuals) - 1} more suspicious UN individuals")
            else:
                print("No suspicious persons found.")
            
        else:
            print("✗ Failed to load client data")
            return
    else:
        print("✗ No client files found")
        return
    
    # Next steps
    print("\n" + "="*50)
    print("NEXT STEPS:")
    print("1. Review the complete suspicious report for detailed information")
    print("2. Conduct manual verification of all matches")
    print("3. Document the screening process for compliance purposes")
    print("4. Implement regular screening schedule")

if __name__ == "__main__":
    main()