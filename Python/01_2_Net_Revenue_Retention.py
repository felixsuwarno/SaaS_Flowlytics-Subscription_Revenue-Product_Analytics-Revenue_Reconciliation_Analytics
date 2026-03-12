import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

# -----------------------------------------------------------
# Load data
# -----------------------------------------------------------

script_dir      = os.path.dirname(os.path.abspath(__file__))
data_dir        = os.path.join(script_dir, "..", "Data_Generated")

summary_path    = os.path.join(data_dir, "01_2b_Net_Revenue_Retention.csv")

df              = pd.read_csv(summary_path)

# -----------------------------------------------------------
# Prep data
# -----------------------------------------------------------

df["mrr_month"]     = pd.to_datetime(df["mrr_month"])
df                  = df.sort_values("mrr_month").reset_index(drop=True)
df["month_label"]   = df["mrr_month"].dt.strftime("%b")

x                   = np.arange(len(df))

# -----------------------------------------------------------
# Plot
# -----------------------------------------------------------

fig, ax             = plt.subplots(figsize=(14, 6))

ax.plot(
    x,
    df["nrr_pct"],
    color       = "#2c3e50",
    linewidth   = 2.5,
    marker      = "o",
    markersize  = 7,
    zorder      = 3
)

# -----------------------------------------------------------
# 100% reference line
# -----------------------------------------------------------

ax.axhline(
    100,
    color       = "#e74c3c",
    linewidth   = 1.5,
    linestyle   = "--",
    zorder      = 2,
    label       = "100% Retention Threshold"
)

# -----------------------------------------------------------
# Labels
# -----------------------------------------------------------

for i, row in df.iterrows():
    ax.text(
        i,
        row["nrr_pct"] + 0.3,
        f"{row['nrr_pct']}%",
        ha          = "center",
        va          = "bottom",
        fontsize    = 10,
        fontweight  = "bold"
    )

# -----------------------------------------------------------
# Formatting
# -----------------------------------------------------------

ax.set_xticks(x)
ax.set_xticklabels(df["month_label"])

ax.set_title(
    "Flowlytics - Net Revenue Retention (NRR) — 2025",
    fontsize    = 22,
    fontweight  = "bold"
)

ax.set_xlabel("Month", fontweight="bold")
ax.set_ylabel("NRR (%)", fontweight="bold")

ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:.1f}%'))

for label in ax.get_xticklabels():
    label.set_fontweight("bold")

for label in ax.get_yticklabels():
    label.set_fontweight("bold")

ax.legend(fontsize=10, framealpha=0.6)
ax.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.show()