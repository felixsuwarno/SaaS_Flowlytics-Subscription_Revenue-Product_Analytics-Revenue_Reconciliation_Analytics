import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from scipy.stats import chi2_contingency

# -----------------------------------------------------------
# Load data
# -----------------------------------------------------------

script_dir      = os.path.dirname(os.path.abspath(__file__))
data_dir        = os.path.join(script_dir, "..", "Data_Generated")

summary_path    = os.path.join(data_dir, "02_1_Trial_To_Paid_Conversion.csv")

df              = pd.read_csv(summary_path)

# -----------------------------------------------------------
# Extract counts
# -----------------------------------------------------------

control                 = df[df['variant'] == 'control'].iloc[0]
treatment               = df[df['variant'] == 'treatment'].iloc[0]

control_converted       = int(control['converted'])
control_not_converted   = int(control['total_trials']) - control_converted

treatment_converted     = int(treatment['converted'])
treatment_not_converted = int(treatment['total_trials']) - treatment_converted

# -----------------------------------------------------------
# Build contingency table
# -----------------------------------------------------------

contingency_table = np.array([
    [control_converted,   control_not_converted],
    [treatment_converted, treatment_not_converted]
])

# -----------------------------------------------------------
# Run chi-square test
# -----------------------------------------------------------

chi2, p_value, dof, expected = chi2_contingency(contingency_table)

# -----------------------------------------------------------
# Evaluate significance
# -----------------------------------------------------------

alpha           = 0.05
is_significant  = p_value < alpha
conclusion      = "statistically significant" if is_significant else "not statistically significant"

# -----------------------------------------------------------
# Print results
# -----------------------------------------------------------

print("=" * 55)
print("Chi-Square Test — Trial-to-Paid Conversion")
print("=" * 55)
print(f"Chi-Square Statistic : {chi2:.4f}")
print(f"P-Value              : {p_value:.6f}")
print(f"Degrees of Freedom   : {dof}")
print(f"Significance Level   : {alpha}")
print(f"Result               : The difference is {conclusion}")
print("=" * 55)