import pandas as pd
import numpy as np
from scipy.optimize import linprog

# Load your original file
df = pd.read_csv("Podatki/SLO.csv")

# Define input and output columns
input_cols = ["javna_na_prebivalca_usd_adj", "zdravstveno_osebje_na_1000", "zdravniki_na_1000"]
output_cols = ["pricakovana_zivljenjska_doba", "infant_mortality_rate"]
bad_outputs = ["infant_mortality_rate"]

def add_malmquist_index(df, input_cols, output_cols, bad_outputs=None):
    data = df.copy()

    # Invert bad output(s)
    if bad_outputs:
        for col in bad_outputs:
            max_val = data[col].max()
            data[col + "_inv"] = max_val - data[col]
        output_cols_mod = [col + "_inv" if col in bad_outputs else col for col in output_cols]
    else:
        output_cols_mod = output_cols

    inputs = data[input_cols].values
    outputs = data[output_cols_mod].values
    n = len(data)

    def dea_output_oriented(input_data, output_data, x0, y0):
        num_dmus = input_data.shape[0]
        num_inputs = input_data.shape[1]
        num_outputs = output_data.shape[1]

        c = np.zeros(num_dmus + 1)
        c[-1] = -1

        A_ub_inputs = np.hstack([input_data.T, np.zeros((num_inputs, 1))])
        b_ub_inputs = x0

        A_ub_outputs = []
        b_ub_outputs = []
        for j in range(num_outputs):
            row = np.zeros(num_dmus + 1)
            row[:num_dmus] = -output_data[:, j]
            row[-1] = y0[j]
            A_ub_outputs.append(row)
            b_ub_outputs.append(0)
        A_ub_outputs = np.array(A_ub_outputs)
        b_ub_outputs = np.array(b_ub_outputs)

        A_ub = np.vstack([A_ub_inputs, A_ub_outputs])
        b_ub = np.concatenate([b_ub_inputs, b_ub_outputs])

        bounds = [(0, None)] * num_dmus + [(None, None)]

        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

        return res.x[-1] if res.success else np.nan

    malmquist_indices = [np.nan]  # First year has no previous reference

    for t in range(n - 1):
        x_t = inputs[t]
        y_t = outputs[t]
        x_tp1 = inputs[t + 1]
        y_tp1 = outputs[t + 1]

        D_t_xt_yt = dea_output_oriented(inputs, outputs, x_t, y_t)
        D_t_xtp1_ytp1 = dea_output_oriented(inputs, outputs, x_tp1, y_tp1)
        D_tp1_xt_yt = dea_output_oriented(inputs, outputs, x_t, y_t)
        D_tp1_xtp1_ytp1 = dea_output_oriented(inputs, outputs, x_tp1, y_tp1)

        if all(val is not None and val > 0 for val in [D_t_xt_yt, D_t_xtp1_ytp1, D_tp1_xt_yt, D_tp1_xtp1_ytp1]):
            malmquist = np.sqrt((D_t_xt_yt / D_t_xtp1_ytp1) * (D_tp1_xt_yt / D_tp1_xtp1_ytp1))
        else:
            malmquist = np.nan

        malmquist_indices.append(malmquist)

    # Add or replace the column
    df["malmquist_indeks"] = malmquist_indices
    return df

# Run the function and save the result back to the original file
df = add_malmquist_index(df, input_cols, output_cols, bad_outputs)
df.to_csv("Podatki/SLO.csv", index=False)  # Overwrite the original file
