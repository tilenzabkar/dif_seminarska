import csv

def update_or_insert_column_from_file(target_csv, source_csv, insert_position, output_file=None):
    output_file = output_file or target_csv

    # Read the source column (assumes 1 column in source)
    with open(source_csv, 'r', newline='', encoding='utf-8') as f:
        source_reader = list(csv.reader(f))
        if not source_reader:
            raise ValueError("Source CSV is empty.")
        source_header = source_reader[0]
        source_col_name = source_header[0]
        source_values = [row[0] if row else '' for row in source_reader[1:]]

    # Read the target CSV
    with open(target_csv, 'r', newline='', encoding='utf-8') as f:
        target_reader = list(csv.reader(f))
        if not target_reader:
            raise ValueError("Target CSV is empty.")
        target_header = target_reader[0]
        target_rows = target_reader[1:]

    # Pad source values to match target rows
    while len(source_values) < len(target_rows):
        source_values.append("")
    source_values = source_values[:len(target_rows)]

    if source_col_name in target_header:
        # Overwrite existing column
        col_index = target_header.index(source_col_name)
        for i, row in enumerate(target_rows):
            # Ensure row has enough columns to update existing column
            while len(row) <= col_index:
                row.append('')
            row[col_index] = source_values[i]
    else:
        # Insert new column at the specified index
        insert_position = max(0, min(insert_position, len(target_header)))  # clip within bounds
        target_header.insert(insert_position, source_col_name)
        for i, row in enumerate(target_rows):
            # Ensure row is long enough to insert at position
            while len(row) < insert_position:
                row.append('')
            row.insert(insert_position, source_values[i])

    # Write updated CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(target_header)
        writer.writerows(target_rows)

    print(f"Column '{source_col_name}' inserted/updated in '{output_file}'.")


# === Example Usage ===
update_or_insert_column_from_file('Podatki/SLO.csv', 'Podatki/insert.csv', insert_position=1)
