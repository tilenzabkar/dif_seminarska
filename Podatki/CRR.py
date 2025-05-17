import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import os

# === 1. Naloži podatke ===
input_csv = "Podatki/SLO.csv"  # zamenjaj s svojo potjo
df = pd.read_csv(input_csv)

# === 2. Izberi inpute in outpute ===
inputs = df[["javna_na_prebivalca_usd_adj", "zdravniki_na_1000", "zdravstveno_osebje_na_1000"]]
outputs = df[["pricakovana_zivljenjska_doba", "infant_mortality_rate"]]

# === 3. Normalizacija inputov (opcijsko, pomaga pri stabilnosti modela) ===
scaler = MinMaxScaler()
X = scaler.fit_transform(inputs)

# === 4. Izhodna metrika za regresijo ===
# Višja pričakovana doba → boljše; višja umrljivost → slabše
y = outputs["pricakovana_zivljenjska_doba"] - outputs["infant_mortality_rate"]

# === 5. Linearna regresija ===
model = LinearRegression()
model.fit(X, y)
eff_scores = model.predict(X)

# === 6. Normalizacija učinkovitosti na [0, 1] ===
eff_scores_normalized = (eff_scores - np.min(eff_scores)) / (np.max(eff_scores) - np.min(eff_scores))

# === 7. Dodaj ali posodobi stolpec CRR_efficiency ===
df["CRR_efficiency"] = eff_scores_normalized

# === 8. Shrani v CSV (prepiši original ali v novo datoteko) ===
output_csv = input_csv  # ali: "podatki_crr.csv"
df.to_csv(output_csv, index=False)

print(f"Rezultati CRR uspešno shranjeni v: {output_csv}")
