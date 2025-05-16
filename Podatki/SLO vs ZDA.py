import pandas as pd

# Load data
usa = pd.read_csv("Podatki/USA.csv")
slo = pd.read_csv("Podatki/SLO.csv")

# Calculate relative efficiency
def calculate_efficiency(row_slo, row_usa):
    input_usa = row_usa["javna_na_prebivalca_usd_adj"] + row_usa["zdravstveno_osebje_na_1000"] + row_usa["zdravniki_na_1000"] + row_usa["infant_mortality_rate"]
    input_slo = row_slo["javna_na_prebivalca_usd_adj"] + row_slo["zdravstveno_osebje_na_1000"] + row_slo["zdravniki_na_1000"] + row_slo["infant_mortality_rate"]
    ratio_usa = row_usa["pricakovana_zivljenjska_doba"] / input_usa
    ratio_slo = row_slo["pricakovana_zivljenjska_doba"] / input_slo
    return ratio_slo / ratio_usa

results = []
for year in range(2000, 2023):
    usa_row = usa[usa["leto"] == year].iloc[0]
    slo_row = slo[slo["leto"] == year].iloc[0]
    efficiency = calculate_efficiency(slo_row, usa_row)
    results.append({"Year": year, "Relative Efficiency": efficiency})

efficiency_df = pd.DataFrame(results)
print(efficiency_df)