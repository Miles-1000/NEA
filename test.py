from trading_ig import IGService
import pandas as pd

# Initialize IGService
username = "davidvorster_ig_demo"
password = "OPGEST44n"
api_key = "a51cf907e8a52d08f68fc1d452f87dbef61927fe"

ig_service = IGService(username, password, api_key, acc_type="DEMO")

# Log in
ig_service.create_session()

# Search for the S&P 500 epic
search_results = ig_service.search_markets("US 500")

# Print results to inspect the structure
print(search_results)

# Handle different structures
try:
    for index, row in search_results.iterrows():  # If it's a DataFrame
        print(f"Epic: {row['epic']}, Name: {row['instrumentName']}")
except KeyError:
    print("KeyError: The DataFrame does not have the expected keys.")
except AttributeError:
    print("The search results are not a DataFrame or iterable.")