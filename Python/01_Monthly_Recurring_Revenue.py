import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# -----------------------------------------------------------
# Load data
# -----------------------------------------------------------

script_dir      = os.path.dirname(os.path.abspath(__file__))
data_dir        = os.path.join(script_dir, "..", "Data_Generated")

summary_path    = os.path.join(data_dir, "01_Monthly_Recurring_Revenue.csv")

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

# -----------------------------------------------------------
# Plot waterfall
# -----------------------------------------------------------

fig, ax                         = plt.subplots(figsize=(14,7))

bars = ax.bar(
    x=df["month_label"],
    height=df["bar_height"],
    bottom=df["bar_base"],
    edgecolor="black",
    linewidth=1
)

# -----------------------------------------------------------
# Connector lines
# -----------------------------------------------------------

for i in range(len(df)-1):

    y = df.loc[i, "ending_mrr_position"]

    ax.plot(
        [i + 0.4, i + 1 - 0.4],
        [y, y],
        linestyle="--",
        linewidth=1
    )

# -----------------------------------------------------------
# Labels
# -----------------------------------------------------------

for i, row in df.iterrows():

    bar_center_y = row["bar_base"] + (row["bar_height"] / 2)

    ax.text(
        i,
        bar_center_y,
        f"${row['total_mrr']:,.0f}",
        ha="center",
        va="center",
        color="white",
        fontsize=12,
        fontweight="bold"
    )

    ax.text(
        i,
        row["ending_mrr_position"] + 300,
        f"${row['ending_mrr_position']:,.0f}",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold"
    )

# -----------------------------------------------------------
# Formatting
# -----------------------------------------------------------

ax.set_title(
    "Flowlytics Monthly Recurring Revenue Waterfall (2025)",
    fontsize=28,
    fontweight="bold"
)

ax.set_xlabel("Month", fontweight="bold")
ax.set_ylabel("Cumulative Net MRR", fontweight="bold")

ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

for label in ax.get_xticklabels():
    label.set_fontweight("bold")

for label in ax.get_yticklabels():
    label.set_fontweight("bold")

ax.axhline(0, linewidth=1)
ax.grid(axis="y", linestyle="--", alpha=0.4)

plt.xticks(rotation=0)
plt.tight_layout()
plt.show()