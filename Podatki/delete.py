import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('Podatki/USA.csv')

# Specify the column name to delete
column_to_delete = 'malmquist_indeks'

# Check if the column exists before attempting to delete
if column_to_delete in df.columns:
    # Delete the column
    df.drop(columns=[column_to_delete], inplace=True)
    print(f"Column '{column_to_delete}' has been deleted.")
else:
    print(f"Column '{column_to_delete}' not found in the CSV file.")

# Save the modified DataFrame back to CSV
df.to_csv('Podatki/USA.csv', index=False)
