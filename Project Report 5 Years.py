# You will make changes to:
# 1. Cell E14 formula (based on E13's new row)
# 2. Cell E33 formula: =SUM(E27:E30) --> adjust range based on added rows
# 3. Cell E34 formula: =E33/10^5 --> shift row of reference
# 4. Merge cells A{17+n} to E{17+n} and A{18+n} to E{18+n} dynamically
# 5. Sheet 'Cost': adjust references in B13 and B15 to new PM-MFA cell locations

from openpyxl.utils import range_boundaries

# In PM-MFA sheet
if "PM-MFA" in wb.sheetnames:
    sheet = wb["PM-MFA"]
    base_row = 10
    default_rows = 1
    n = len(st.session_state.pm_items)

    if n > default_rows:
        sheet.insert_rows(base_row + 1, n - default_rows)

    merged_ranges = list(sheet.merged_cells.ranges)
    for merge in merged_ranges:
        sheet.merge_cells(str(merge))

    for i, item in enumerate(st.session_state.pm_items):
        row = base_row + i
        copy_row_formatting(sheet, base_row, row)
        sheet[f"A{row}"] = i + 1
        sheet[f"B{row}"] = item["name"]
        sheet[f"C{row}"] = item["qty"]
        sheet[f"D{row}"] = item["rate"]
        sheet[f"E{row}"] = f"=C{row}*D{row}"

    # Remove total row in Cxx (we no longer want it)

    # Add formula in E13+n: =SUM(E10:E{10+n-1})
    pm_sum_row = base_row + n
    sheet[f"E{pm_sum_row}"] = f"=SUM(E{base_row}:E{base_row + n - 1})"

    # Cell E14 or E(13+n+1) = previous row / 10^5
    sheet[f"E{pm_sum_row + 1}"] = f"=E{pm_sum_row}/10^5"

    # Furniture and Electrical value rows
    f_row = 27 + (n - 1)
    e_row = 30 + (n - 1)
    sheet[f"E{f_row}"] = furniture_value
    sheet[f"E{e_row}"] = electrical_value

    # Cell E33 = SUM(E{f_row}:E{e_row})
    total_fixed_assets_row = e_row + 3
    sheet[f"E{total_fixed_assets_row}"] = f"=SUM(E{f_row}:E{e_row})"

    # Cell E34 = E33 / 10^5 --> new E(row)
    sheet[f"E{total_fixed_assets_row + 1}"] = f"=E{total_fixed_assets_row}/10^5"

    # Merge new footer rows
    sheet.merge_cells(f"A{pm_sum_row + 2}:E{pm_sum_row + 2}")
    sheet.merge_cells(f"A{pm_sum_row + 3}:E{pm_sum_row + 3}")

# Update dependent links in 'Cost' sheet
if "Cost" in wb.sheetnames:
    cost = wb["Cost"]
    # B13: = 'PM-MFA'!E13 --> now E{pm_sum_row}
    cost["B13"] = f"='PM-MFA'!E{pm_sum_row}/10^5"
    # B15: = 'PM-MFA'!E33 --> now E{total_fixed_assets_row}
    cost["B15"] = f"='PM-MFA'!E{total_fixed_assets_row}/10^5"
