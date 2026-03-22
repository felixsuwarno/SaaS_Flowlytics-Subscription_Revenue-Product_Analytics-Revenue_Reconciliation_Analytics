import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# -----------------------------------------------------------
# Load data
# -----------------------------------------------------------

script_dir      = os.path.dirname(os.path.abspath(__file__))
data_dir        = os.path.join(script_dir, "..", "Data_Generated")

Subs_Not_Billed         = os.path.join(data_dir, "03_1a_Which_Active_Subs_Not_Billed.csv")
Total_Missing_Bill      = os.path.join(data_dir, "03_1b_How_Much_was_the_Missing_Bill.csv")

df_Subs_Not_Billed      = pd.read_csv(Subs_Not_Billed)
df_Total_Missing_Bill   = pd.read_csv(Total_Missing_Bill)

# -----------------------------------------------------------
# Prep
# -----------------------------------------------------------

TIER_ORDER  = ["Starter", "Growth", "Business"]
TIER_COLORS = {
    "Starter":  "#4A90D9",
    "Growth":   "#F5A623",
    "Business": "#E84545",
}

df_b = df_Total_Missing_Bill.copy()
df_b["plan_tier"] = pd.Categorical(df_b["plan_tier"], categories=TIER_ORDER, ordered=True)
df_b = df_b.sort_values("plan_tier")

colors      = [TIER_COLORS[t] for t in df_b["plan_tier"]]
total_subs  = df_b["subscription_count"].sum()
total_rev   = df_b["revenue_not_billed"].sum()

starter_sub_pct  = df_b.loc[df_b["plan_tier"] == "Starter",  "subscription_count"].values[0] / total_subs * 100
starter_rev_pct  = df_b.loc[df_b["plan_tier"] == "Starter",  "revenue_not_billed"].values[0] / total_rev * 100
business_rev_pct = df_b.loc[df_b["plan_tier"] == "Business", "revenue_not_billed"].values[0] / total_rev * 100
business_sub_pct = df_b.loc[df_b["plan_tier"] == "Business", "subscription_count"].values[0] / total_subs * 100

# -----------------------------------------------------------
# Canvas
# -----------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(13, 7))
fig.patch.set_facecolor("#F7F8FA")

fig.suptitle(
    "Flowlytics — December 2025 — Billing Gap Audit",
    fontsize=18, fontweight="bold", color="#1A1A2E",
    y=0.97
)
fig.text(
    0.5, 0.89,
    f"{total_subs} active subscriptions unbilled  ·  ${total_rev:,.0f} in uncaptured recurring revenue",
    ha="center", fontsize=10, color="#555577"
)

# -----------------------------------------------------------
# Panel A — Subscription Count by Tier
# -----------------------------------------------------------

ax1 = axes[0]
ax1.set_facecolor("#F7F8FA")

bars1 = ax1.bar(
    df_b["plan_tier"],
    df_b["subscription_count"],
    color=colors,
    width=0.5,
    zorder=3
)

for bar, val in zip(bars1, df_b["subscription_count"]):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.8,
        str(val),
        ha="center", va="bottom",
        fontsize=12, fontweight="bold", color="#1A1A2E"
    )

for bar, val in zip(bars1, df_b["subscription_count"]):
    pct = val / total_subs * 100
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() / 2,
        f"{pct:.0f}%",
        ha="center", va="center",
        fontsize=10, color="white", fontweight="bold"
    )

ax1.set_title("Unbilled Subscriptions by Plan Tier", fontsize=12, fontweight="bold",
              color="#1A1A2E", pad=12)
ax1.set_ylabel("Number of Subscriptions", fontsize=10, color="#555577")
ax1.set_ylim(0, df_b["subscription_count"].max() * 1.18)
ax1.tick_params(axis="x", labelsize=10, colors="#1A1A2E")
ax1.tick_params(axis="y", labelsize=9, colors="#888888")
ax1.yaxis.grid(True, linestyle="--", alpha=0.5, color="#CCCCDD", zorder=0)
ax1.set_axisbelow(True)
for spine in ax1.spines.values():
    spine.set_visible(False)
ax1.text(
    0.98, 0.97,
    f"Total: {total_subs} subs",
    transform=ax1.transAxes,
    ha="right", va="top",
    fontsize=9, color="#555577",
    style="italic"
)

# -----------------------------------------------------------
# Panel B — Revenue Not Billed by Tier
# -----------------------------------------------------------

ax2 = axes[1]
ax2.set_facecolor("#F7F8FA")

bars2 = ax2.bar(
    df_b["plan_tier"],
    df_b["revenue_not_billed"],
    color=colors,
    width=0.5,
    zorder=3
)

for bar, val in zip(bars2, df_b["revenue_not_billed"]):
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 15,
        f"${val:,.0f}",
        ha="center", va="bottom",
        fontsize=12, fontweight="bold", color="#1A1A2E"
    )

for bar, val in zip(bars2, df_b["revenue_not_billed"]):
    pct = val / total_rev * 100
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() / 2,
        f"{pct:.0f}%",
        ha="center", va="center",
        fontsize=10, color="white", fontweight="bold"
    )

ax2.set_title("Unbilled Revenue by Plan Tier", fontsize=12, fontweight="bold",
              color="#1A1A2E", pad=12)
ax2.set_ylabel("Revenue Not Billed ($)", fontsize=10, color="#555577")
ax2.set_ylim(0, df_b["revenue_not_billed"].max() * 1.22)
ax2.yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))
ax2.tick_params(axis="x", labelsize=10, colors="#1A1A2E")
ax2.tick_params(axis="y", labelsize=9, colors="#888888")
ax2.yaxis.grid(True, linestyle="--", alpha=0.5, color="#CCCCDD", zorder=0)
ax2.set_axisbelow(True)
for spine in ax2.spines.values():
    spine.set_visible(False)
ax2.text(
    0.98, 0.97,
    f"Total: ${total_rev:,.0f}",
    transform=ax2.transAxes,
    ha="right", va="top",
    fontsize=9, color="#555577",
    style="italic"
)

# -----------------------------------------------------------
# Insight callout at bottom
# -----------------------------------------------------------

fig.text(
    0.5, -0.04,
    f"⚠  Starter tier accounts for {starter_sub_pct:.0f}% of unbilled subscriptions but only {starter_rev_pct:.0f}% of unbilled revenue. "
    f"Business tier drives {business_rev_pct:.0f}% of unbilled revenue from just {business_sub_pct:.0f}% of affected subscriptions.",
    ha="center", fontsize=9, color="#333355",
    style="italic"
)

plt.tight_layout(rect=[0, 0.02, 1, 0.86])

# -----------------------------------------------------------
# Save & Show
# -----------------------------------------------------------

out_path = os.path.join(script_dir, "03_1_Billing_Gap_Audit_Dec2025.png")
plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.show()
plt.close()