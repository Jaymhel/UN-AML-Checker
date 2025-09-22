# UN-AML-Chekcer
This software tool ("UN AML Checker") is provided as a free, open-source utility to assist Hong Kong Certified Public Accountants (CPAs) with preliminary screening requirements under AFRC guidelines.

A Python-based tool for Hong Kong CPA practices to screen client lists against the United Nations Security Council Consolidated List for AFRC compliance requirements.

## Features

- Automated download of UN SC Consolidated List
- Client data processing with name combination generation
- Comprehensive matching against UN list data
- Detailed reporting of potential matches
- Secure local processing (no data sent to external servers)

## Disclaimer

**Important:** This software is provided for informational purposes only. Users are solely responsible for:
- Verifying all matches against official UN sources
- Ensuring compliance with all regulatory requirements
- Proper handling and security of client data
- Any decisions made based on the software output

The author provides no warranties regarding accuracy or completeness of results. See [LICENSE](LICENSE) for complete terms.

## Installation

```bash
git clone https://github.com/yourusername/un-sc-checker.git
cd un-sc-checker
pip install -r requirements.txt
