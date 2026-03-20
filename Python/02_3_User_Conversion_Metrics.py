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

activation_path = os.path.join(data_dir, "02_3a_User_Activation_Metrics.csv")
quartile_path   = os.path.join(data_dir, "02_3b_User_Conversion_Rate.csv")

df_activation   = pd.read_csv(activation_path)
df_quartile     = pd.read_csv(quartile_path)

# -----------------------------------------------------------
# Prep data — Output 1: Activation Metrics
# -----------------------------------------------------------

feature_labels = {
    "days_active_during_trial" : "Days Active\nDuring Trial",
    "templates_used"           : "Templates\nUsed",
    "workflows_created"        : "Workflows\nCreated",
    "integrations_connected"   : "Integrations\nConnected"
}

df_activation["feature_label"] = df_activation["feature"].map(feature_labels)

x         = np.arange(len(df_activation))
bar_width  = 0.35

# -----------------------------------------------------------
# Prep data — Output 2: Conversion Rate by Quartile
# -----------------------------------------------------------

df_quartile["feature_label"] = df_quartile["feature"].map(feature_labels)
df_quartile = df_quartile.sort_values(["feature", "quartile"])

features_ordered = [
    "days_active_during_trial",
    "templates_used",
    "workflows_created",
    "integrations_connected"
]

colors = {
    "days_active_during_trial" : "#1D9E75",
    "templates_used"           : "#D4537E",
    "workflows_created"        : "#BA7517",
    "integrations_connected"   : "#378ADD"
}

# -----------------------------------------------------------
# Figure layout
# -----------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle(
    "Flowlytics — 2025 \n Trial Users — What Characteristics Are Associated with Conversion?",
    fontsize=20,
    fontweight="bold",
    y=0.9,
    ha="center"
)

# -----------------------------------------------------------
# Output 1 — Activation Metrics by Conversion Status
# -----------------------------------------------------------

ax1 = axes[0]

bars_converted     = ax1.bar(
    x - bar_width / 2,
    df_activation["avg_converted"],
    width=bar_width,
    color="#1D9E75",
    label="Converted",
    zorder=3
)

bars_not_converted = ax1.bar(
    x + bar_width / 2,
    df_activation["avg_not_converted"],
    width=bar_width,
    color="#D3D1C7",
    label="Not Converted",
    zorder=3
)

for i, (converted_val, not_converted_val, ratio) in enumerate(zip(
    df_activation["avg_converted"],
    df_activation["avg_not_converted"],
    df_activation["separation_ratio"]
)):
    ax1.text(
        x[i],
        max(converted_val, not_converted_val) + 0.15,
        f"{ratio:.2f}x",
        ha="center",
        va="bottom",
        fontsize=9,
        color="#444441",
        fontweight="bold"
    )

ax1.set_xticks(x)
ax1.set_xticklabels(df_activation["feature_label"], fontsize=10)
ax1.set_ylabel("Average Value", fontsize=10)
ax1.set_title("Trial Users Activation Metrics by Conversion Status", fontsize=16, pad=12)
ax1.legend(fontsize=9)
ax1.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax1.set_axisbelow(True)
ax1.spines[["top", "right"]].set_visible(False)

ax1.text(
    0.5, -0.18,
    "Numbers above bars show separation ratio (converted avg ÷ not converted avg)",
    transform=ax1.transAxes,
    ha="center",
    fontsize=16,
    color="#888780"
)

# -----------------------------------------------------------
# Output 2 — Conversion Rate by Engagement Quartile
# -----------------------------------------------------------

ax2 = axes[1]

for feature in features_ordered:
    df_feature = df_quartile[df_quartile["feature"] == feature]
    label      = feature_labels[feature].replace("\n", " ")
    ax2.plot(
        df_feature["quartile"],
        df_feature["conversion_rate"],
        marker="o",
        markersize=6,
        linewidth=2,
        color=colors[feature],
        label=label
    )

ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
ax2.set_xticks([1, 2, 3, 4])
ax2.set_xticklabels(["Q1", "Q2", "Q3", "Q4"], fontsize=10)
ax2.set_xlabel("Engagement Quartile  (Q1 = lowest 25%  ·  Q4 = highest 25%)", fontsize=9)
ax2.set_ylabel("Conversion Rate", fontsize=10)
ax2.set_title("Trial Users Conversion Rate by Engagement Quartile", fontsize=16, pad=12)
ax2.legend(fontsize=9)
ax2.grid(axis="y", linestyle="--", alpha=0.4)
ax2.set_axisbelow(True)
ax2.spines[["top", "right"]].set_visible(False)
ax2.set_ylim(0, 0.75)

ax2.text(
    0.5, -0.18,
    "n = 12,500 customers per quartile per feature  ·  population = all trial users",
    transform=ax2.transAxes,
    ha="center",
    fontsize=16,
    color="#888780"
)

# -----------------------------------------------------------
# Save
# -----------------------------------------------------------

plt.tight_layout()

output_path = os.path.join(script_dir, "..", "Charts", "02_3_Trial_User_Conversion_Analysis.png")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=150, bbox_inches="tight")

plt.show()
