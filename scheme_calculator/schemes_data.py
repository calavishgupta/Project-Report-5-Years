import csv

def get_scheme_data(csv_file):
    schemes = {}
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            scheme_name = row["Scheme"]
            schemes[scheme_name] = {
                "Description": row["Description"],
                "Eligibility": row["Eligibility"],
                "Calculation": row["Calculation"]
            }
    return schemes
