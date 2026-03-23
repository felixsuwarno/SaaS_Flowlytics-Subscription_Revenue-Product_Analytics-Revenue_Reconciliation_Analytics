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

summary_path    = os.path.join(data_dir, "01_1_Monthly_Recurring_Revenue.csv")

df              = pd.read_csv(summary_path)

# -----------------------------------------------------------
# Prep data
# -----------------------------------------------------------

df["mrr_month"]                 = pd.to_datetime(df["mrr_month"])
df                              = df.sort_values("mrr_month").reset_index(drop=True)

df["month_label"]               = df["mrr_month"].dt.strftime("%b")

df["starting_mrr_position"]     = df["total_mrr"].cumsum().shift(fill_value=0)
df["ending_mrr_position"]       = df["starting_mrr_position"] + df["total_mrr"]

df["bar_base"]                  = df[["starting_mrr_position","ending_mrr_position"]].min(axis=1)
df["bar_height"]                = df["total_mrr"].abs()

x                               = np.arange(len(df))

# -----------------------------------------------------------
# Figure
# -----------------------------------------------------------

fig, (ax1, ax2)                 = plt.subplots(2, 1, figsize=(16, 16))

# -----------------------------------------------------------
# Chart 1 — Waterfall
# -----------------------------------------------------------

ax1.bar(
    x=df["month_label"],
    height=df["bar_height"],
    bottom=df["bar_base"],
    edgecolor="black",
    linewidth=1
)

for i in range(len(df) - 1):

    y = df.loc[i, "ending_mrr_position"]

    ax1.plot(
        [i + 0.4, i + 1 - 0.4],
        [y, y],
        linestyle="--",
        linewidth=1
    )

for i, row in df.iterrows():

    bar_center_y = row["bar_base"] + (row["bar_height"] / 2)

    ax1.text(
        i,
        bar_center_y,
        f"${row['total_mrr']:,.0f}",
        ha="center",
        va="center",
        color="white",
        fontsize=12,
        fontweight="bold"
    )

    ax1.text(
        i,
        row["ending_mrr_position"] + 100,
        f"${row['ending_mrr_position']:,.0f}",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold"
    )

ax1.set_title(
    "Flowlytics Monthly Recurring Revenue Waterfall (2025)",
    fontsize=22,
    fontweight="bold",
    pad=20
)

ax1.set_ylabel("Cumulative Net MRR", fontweight="bold")
ax1.set_ylim(0, df["ending_mrr_position"].max() * 1.2)
ax1.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

for label in ax1.get_xticklabels():
    label.set_fontweight("bold")

for label in ax1.get_yticklabels():
    label.set_fontweight("bold")

ax1.axhline(0, linewidth=1)
ax1.grid(axis="y", linestyle="--", alpha=0.4)

# -----------------------------------------------------------
# Chart 2 — MRR Movement by Component
# -----------------------------------------------------------

COLORS      = {
    "new":          "#2ecc71",
    "expansion":    "#3498db",
    "contraction":  "#e67e22",
    "churn":        "#e74c3c",
}

keys        = ["new_mrr", "expansion_mrr", "contraction_mrr", "churn_mrr"]
labels      = ["New MRR", "Expansion MRR", "Contraction MRR", "Churn MRR"]
clrs        = [COLORS["new"], COLORS["expansion"], COLORS["contraction"], COLORS["churn"]]
offsets     = [-1.5, -0.5, 0.5, 1.5]
group_w     = 0.2

for offset, key, color, label in zip(offsets, keys, clrs, labels):

    ax2.bar(
        x + offset * group_w,
        df[key].values,
        width=group_w,
        color=color,
        alpha=0.88,
        zorder=3,
        label=label
    )

ax2.set_xticks(x)
ax2.set_xticklabels(df["month_label"])

ax2.set_xlabel("Month", fontweight="bold")
ax2.set_ylabel("MRR Change (USD)", fontweight="bold")

ax2.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

for label in ax2.get_xticklabels():
    label.set_fontweight("bold")

for label in ax2.get_yticklabels():
    label.set_fontweight("bold")

ax2.axhline(0, linewidth=1)
ax2.grid(axis="y", linestyle="--", alpha=0.4)
ax2.legend(fontsize=10, framealpha=0.6)

plt.xticks(rotation=0)
plt.savefig(os.path.join(script_dir, "01_MRR_Movement.png"), dpi=150, bbox_inches='tight')
plt.show()