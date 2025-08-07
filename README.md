# Scheme Calculator

This project provides a calculator for various government schemes such as Pension Scheme, Health Insurance, and Education Grant.  
It allows users to input relevant information (age, income, eligibility criteria) and calculates the benefit they may receive from different schemes.

## Features

- Calculate benefits for multiple schemes
- Easily extendable by updating `schemes.csv`
- Modular calculation logic in `scheme_calculator/calculator_logic.py`

## Files

- `scheme_calculator/calculator_logic.py`: Python logic for calculating benefits
- `scheme_calculator/schemes.csv`: CSV file containing scheme details and calculation formulas
- `README.md`: Project overview and usage instructions

## Usage

1. Add or modify schemes in `scheme_calculator/schemes.csv`
2. Use the functions in `scheme_calculator/calculator_logic.py` to calculate benefits by passing user data and schemes data

## Example

```python
from scheme_calculator.calculator_logic import calculate_benefit
import csv

# Load schemes from CSV
schemes_data = {}
with open('scheme_calculator/schemes.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        schemes_data[row['Scheme']] = row

# Calculate benefit
benefit = calculate_benefit('Pension Scheme', age=65, income=400000, additional=None, schemes_data=schemes_data)
print(f"Pension Scheme Benefit: {benefit}")
```

## Extending

To add new schemes:
- Add a row to `schemes.csv` with appropriate calculation formula.
- Update logic in `calculator_logic.py` if custom rules are needed.

## License

MIT
