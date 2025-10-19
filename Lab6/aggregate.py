import pandas as pd
try:
    df = pd.read_csv('consolidated_cpp.csv')
    aggregated_df = df.groupby(['Project_name', 'Tool_name', 'CWE_ID'])['Number_of_Findings'].sum().reset_index()
    print("Aggregated Findings:")
    print(aggregated_df.head())
    aggregated_df.to_csv('aggregated_findings.csv', index=False)
    print("\nAggregated data saved to 'aggregated_findings.csv'")

except FileNotFoundError:
    print("Error: 'consolidated_cpp.csv' not found. Please make sure the file is in the same directory as the script.")
except Exception as e:
    print(f"An error occurred: {e}")