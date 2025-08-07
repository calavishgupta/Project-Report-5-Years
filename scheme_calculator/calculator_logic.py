def calculate_benefit(scheme, age, income, additional, schemes_data):
    data = schemes_data.get(scheme)
    if not data:
        return "Scheme data not found."
    
    # Example calculation logic based on scheme name
    if scheme == "Pension Scheme":
        if age >= 60:
            benefit = 0.5 * income
        else:
            benefit = 0.1 * income
    elif scheme == "Health Insurance":
        if age < 18:
            benefit = 20000
        elif age < 60:
            benefit = 100000
        else:
            benefit = 150000
    elif scheme == "Education Grant":
        if age < 25 and income < 300000:
            benefit = 50000
        else:
            benefit = 0
    else:
        # Use custom calculation string if available
        calc_str = data.get("Calculation", "")
        try:
            # Basic string replacement for variables
            calc_str = calc_str.replace("age", str(age)).replace("income", str(income))
            benefit = eval(calc_str)
        except Exception:
            benefit = "Calculation error."
    
    return benefit
