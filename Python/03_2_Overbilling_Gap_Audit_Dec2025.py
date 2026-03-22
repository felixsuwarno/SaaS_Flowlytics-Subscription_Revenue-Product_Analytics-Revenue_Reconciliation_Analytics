import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# -----------------------------------------------------------
# Load data
# -----------------------------------------------------------

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "Data_Generated")

path_03_2b = os.path.join(data_dir, "03_2b_How_Much_Was_the_Overbill.csv")

df_03_2b = pd.read_csv(path_03_2b)

# -----------------------------------------------------------
# Prep
# -----------------------------------------------------------

lst_tier_order = ["Starter", "Growth", "Business"]
dct_tier_colors = {
    "Starter": "#4A90D9",
    "Growth": "#F5A623",
    "Business": "#E84545"
}

df_plot = df_03_2b.copy()

df_plot["plan_tier"] = pd.Categorical(
    df_plot["plan_tier"],
    categories=lst_tier_order,
    ordered=True
)

df_plot = df_plot.sort_values("plan_tier").reset_index(drop=True)

lst_colors = [dct_tier_colors[tier] for tier in df_plot["plan_tier"]]

total_overbilled_subs = df_plot["overbilled_subscription_count"].sum()
total_overbilled_amount = df_plot["overbilled_amount"].sum()

df_plot["subs_pct"] = (
    df_plot["overbilled_subscription_count"] / total_overbilled_subs * 100
)
df_plot["amount_pct"] = (
    df_plot["overbilled_amount"] / total_overbilled_amount * 100
)

# -----------------------------------------------------------
# Figure
# -----------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(13, 7))
fig.patch.set_facecolor("#F7F8FA")

fig.suptitle(
    "Flowlytics — December 2025 — Overbilling Audit",
    fontsize=18,
    fontweight="bold",
    color="#1A1A2E",
    y=0.97
)

fig.text(
    0.5,
    0.89,
    f"{total_overbilled_subs:,.0f} inactive subscriptions billed  ·  ${total_overbilled_amount:,.0f} in overbilled revenue",
    ha="center",
    fontsize=10,
    color="#555577"
)

# -----------------------------------------------------------
# Left chart: Overbilled subscriptions by plan tier
# -----------------------------------------------------------

ax_left = axes[0]
ax_left.set_facecolor("#F7F8FA")

bars_left = ax_left.bar(
    df_plot["plan_tier"],
    df_plot["overbilled_subscription_count"],
    color=lst_colors,
    width=0.5,
    zorder=3
)

for bar, value in zip(bars_left, df_plot["overbilled_subscription_count"]):
    ax_left.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.8,
        f"{value:,.0f}",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        color="#1A1A2E"
    )

for bar, pct in zip(bars_left, df_plot["subs_pct"]):
    ax_left.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() / 2,
        f"{pct:.0f}%",
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="white"
    )

ax_left.set_title(
    "Billed Inactive Subscriptions by Plan Tier",
    fontsize=12,
    fontweight="bold",
    color="#1A1A2E",
    pad=12
)

ax_left.set_ylabel(
    "Number of Subscriptions",
    fontsize=10,
    color="#555577"
)

ax_left.set_ylim(0, df_plot["overbilled_subscription_count"].max() * 1.18)
ax_left.tick_params(axis="x", labelsize=10, colors="#1A1A2E")
ax_left.tick_params(axis="y", labelsize=9, colors="#888888")
ax_left.yaxis.grid(True, linestyle="--", alpha=0.5, color="#CCCCDD", zorder=0)
ax_left.set_axisbelow(True)

for spine in ax_left.spines.values():
    spine.set_visible(False)

ax_left.text(
    0.98,
    0.97,
    f"Total: {total_overbilled_subs:,.0f} subs",
    transform=ax_left.transAxes,
    ha="right",
    va="top",
    fontsize=9,
    color="#555577",
    style="italic"
)

# -----------------------------------------------------------
# Right chart: Overbilled revenue by plan tier
# -----------------------------------------------------------

ax_right = axes[1]
ax_right.set_facecolor("#F7F8FA")

bars_right = ax_right.bar(
    df_plot["plan_tier"],
    df_plot["overbilled_amount"],
    color=lst_colors,
    width=0.5,
    zorder=3
)

for bar, value in zip(bars_right, df_plot["overbilled_amount"]):
    ax_right.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 15,
        f"${value:,.0f}",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        color="#1A1A2E"
    )

for bar, pct in zip(bars_right, df_plot["amount_pct"]):
    ax_right.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() / 2,
        f"{pct:.0f}%",
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="white"
    )

ax_right.set_title(
    "Billed Inactive Subscription by Plan Tier",
    fontsize=12,
    fontweight="bold",
    color="#1A1A2E",
    pad=12
)

ax_right.set_ylabel(
    "Revenue Overbilled ($)",
    fontsize=10,
    color="#555577"
)

ax_right.set_ylim(0, df_plot["overbilled_amount"].max() * 1.22)
ax_right.yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))
ax_right.tick_params(axis="x", labelsize=10, colors="#1A1A2E")
ax_right.tick_params(axis="y", labelsize=9, colors="#888888")
ax_right.yaxis.grid(True, linestyle="--", alpha=0.5, color="#CCCCDD", zorder=0)
ax_right.set_axisbelow(True)

for spine in ax_right.spines.values():
    spine.set_visible(False)

ax_right.text(
    0.98,
    0.97,
    f"Total: ${total_overbilled_amount:,.0f}",
    transform=ax_right.transAxes,
    ha="right",
    va="top",
    fontsize=9,
    color="#555577",
    style="italic"
)

# -----------------------------------------------------------
# Bottom insight
# -----------------------------------------------------------

srs_largest_subs = df_plot.loc[df_plot["subs_pct"].idxmax()]
srs_largest_amount = df_plot.loc[df_plot["amount_pct"].idxmax()]

callout_text = (
    f"{srs_largest_subs['plan_tier']} tier accounts for "
    f"{srs_largest_subs['subs_pct']:.0f}% of overbilled subscriptions "
    f"but {srs_largest_subs['amount_pct']:.0f}% of overbilled revenue. "
    f"{srs_largest_amount['plan_tier']} tier drives "
    f"{srs_largest_amount['amount_pct']:.0f}% of overbilled revenue."
)

fig.text(
    0.5,
    -0.04,
    callout_text,
    ha="center",
    fontsize=9,
    color="#333355",
    style="italic"
)

plt.tight_layout(rect=[0, 0.02, 1, 0.86])

# -----------------------------------------------------------
# Save and show
# -----------------------------------------------------------

path_output = os.path.join(script_dir, "03_2_Overbilling_Audit_Dec2025.png")

plt.savefig(
    path_output,
    dpi=150,
    bbox_inches="tight",
    facecolor=fig.get_facecolor()
)

plt.show()
plt.close()