
import eacal

cal = eacal.EACal()
year = 2023

print(f"--- Inspecting eacal.EACal().get_annual_solar_terms({year}) ---")

try:
    solar_terms = cal.get_annual_solar_terms(year)
    print(f"Successfully called function.")
    print("Return type:", type(solar_terms))
    if isinstance(solar_terms, list) and len(solar_terms) > 0:
        print("Length of list:", len(solar_terms))
        first_term = solar_terms[0]
        print("First element type:", type(first_term))
        print("First element value:", first_term)
        if isinstance(first_term, tuple) and len(first_term) > 1:
            print("Second item in first element (the date part):")
            print("  - Type:", type(first_term[1]))
            print("  - Value:", first_term[1])

except Exception as e:
    print(f"An error occurred: {e}")
