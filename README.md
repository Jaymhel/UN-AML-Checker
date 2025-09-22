# UN AML Checker for Hong Kong CPAs

A comprehensive Python tool for screening client lists against the United Nations Security Council Consolidated List to meet AFRC compliance requirements.

## Features

- Automated download of UN SC Consolidated List
- Client data processing with intelligent name matching
- Comprehensive comparison against UN sanctions data
- Detailed reporting with full client and UN individual information
- Local processing - no data leaves your computer

## Quick Start

```bash
# Clone the repository
git clone https://github.com/helmetWong/UN-AML-Checker.git
cd UN-AML-Checker

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir un_data clients_data reports

# Place your client CSV files in clients_data/
# Run the screening
python main.py

File Format
Client CSV files should be named YYYYMMDD_clients.csv (prepare by the user) and contain these columns:

SN, File_no, BRN, Company, Officer, Role

## Disclaimer

Important Disclaimer
This tool is for preliminary screening only. Always verify results against official UN sources. See DISCLAIMER.md for complete terms.

- Verifying all matches against official UN sources
- Ensuring compliance with all regulatory requirements
- Proper handling and security of client data
- Any decisions made based on the software output

The author provides no warranties regarding accuracy or completeness of results. See [LICENSE](LICENSE) for complete terms.

# Disclaimer and Terms of Use

## Important Notice

This software tool ("UN AML Checker") is provided as a free, open-source utility to assist Hong Kong Certified Public Accountants (CPAs) with preliminary screening requirements under AFRC guidelines. By using this software, you acknowledge and agree to the following terms:

## 1. No Warranty

The software is provided "AS IS" without any warranties, express or implied. The author makes no representations or warranties of any kind concerning:
- The accuracy, completeness, or reliability of screening results
- The fitness of the software for any particular purpose
- The continuous availability or error-free operation of the software

## 2. User Responsibility

You, as the user, assume full responsibility for:
- Verifying all potential matches against the official UN Security Council Consolidated List
- Ensuring compliance with all applicable laws and regulations
- Implementing appropriate data security measures for client information
- Making final determinations regarding client screening outcomes

## 3. Limitation of Liability

In no event shall the author be liable for any direct, indirect, incidental, special, exemplary, or consequential damages arising from:
- The use of or inability to use the software
- Any errors, omissions, or inaccuracies in the screening results
- Any decisions made or actions taken based on the software output
- Any regulatory non-compliance resulting from use of the software

## 4. Data Privacy and Security

You are solely responsible for:
- Securing client data during processing
- Complying with all applicable data protection laws
- Implementing appropriate access controls and security measures
- Ensuring proper data retention and disposal practices

## 5. Regulatory Compliance

This tool is intended to assist with preliminary screening only. You must:
- Verify all results against official UN sources
- Maintain proper documentation of your screening process
- Follow all AFRC and other regulatory requirements
- Consult with legal counsel for compliance assurance

## 6. Third-Party Services

While third-party IT providers may charge for installation and support services:
- They may not charge for the software itself
- They may not create derivative works for resale
- All support services are provided separately from the software author

## 7. Copyright Notice

Copyright (c) 2025 Micheal Wong . All rights reserved.

The software remains the intellectual property of the author. While free to use and modify, users must maintain this copyright notice and disclaimer in all distributions.


## Installation

```bash
git clone https://github.com/yourusername/un-sc-checker.git
cd un-sc-checker

pip install -r requirements.txt

