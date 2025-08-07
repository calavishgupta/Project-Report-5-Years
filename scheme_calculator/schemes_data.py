import csv
import os

def get_scheme_data(csv_file):
    # Make path relative to this file's location
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, csv_file)
    schemes = {}
    try:
        with open(csv_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                scheme_name = row.get('Scheme', '').strip()
                schemes[scheme_name] = {
                    "Description": row.get('Description', '').strip(),
                    "Eligibility": row.get('Eligibility', '').strip(),
                    "Calculation": row.get('Calculation', '').strip()
                }
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at {csv_path}. Please ensure schemes.csv exists in scheme_calculator directory.")
    return schemes
