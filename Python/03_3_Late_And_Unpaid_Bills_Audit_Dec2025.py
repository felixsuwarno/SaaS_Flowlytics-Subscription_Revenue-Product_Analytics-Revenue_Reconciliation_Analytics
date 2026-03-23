import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# -----------------------------------------------------------
# Load data
# -----------------------------------------------------------

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir   = os.path.join(script_dir, "..", "Data_Generated")

path_03_3b = os.path.join(data_dir, "03_3b_How_Much_Are_The_Unpaid_Bills.csv")
df         = pd.read_csv(path_03_3b)

# -----------------------------------------------------------
# Prep
# -----------------------------------------------------------

TIER_ORDER   = ["Starter", "Growth", "Business"]
ISSUE_ORDER  = ["Unpaid", "Late Payment"]
ISSUE_COLORS = {
    "Unpaid":       "#F5A623",
    "Late Payment": "#4A90D9",
}

df["plan_tier"] = pd.Categorical(df["plan_tier"], categories=TIER_ORDER, ordered=True)
df = df.sort_values("plan_tier").reset_index(drop=True)

total_invoices  = df["invoice_count"].sum()
total_uncollect = df["total_uncollected"].sum()

df_count  = df.pivot(index="plan_tier", columns="payment_issue_type", values="invoice_count").reindex(TIER_ORDER)
df_amount = df.pivot(index="plan_tier", columns="payment_issue_type", values="total_uncollected").reindex(TIER_ORDER)

x     = np.arange(len(TIER_ORDER))
width = 0.35

# -----------------------------------------------------------
# Canvas
# -----------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(13, 7))
fig.patch.set_facecolor("#F7F8FA")

fig.suptitle(
    "Flowlytics — December 2025 — Payment Collection Audit",
    fontsize=18, fontweight="bold", color="#1A1A2E", y=0.97
)
fig.text(
    0.5, 0.89,
    f"{total_invoices:,} invoices with payment issues  ·  ${total_uncollect:,.0f} in uncollected revenue",
    ha="center", fontsize=10, color="#555577"
)

# -----------------------------------------------------------
# Panel A — Invoice Count
# -----------------------------------------------------------

ax1 = axes[0]
ax1.set_facecolor("#F7F8FA")

for i, issue in enumerate(ISSUE_ORDER):
    vals = df_count[issue].values
    bars = ax1.bar(x + (i - 0.5) * width, vals, width=width,
                   color=ISSUE_COLORS[issue], label=issue, zorder=3)
    for bar, val in zip(bars, vals):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
                 f"{val:,}", ha="center", va="bottom",
                 fontsize=9, fontweight="bold", color="#1A1A2E")

ax1.set_title("Invoice Count by Plan Tier & Issue Type", fontsize=12, fontweight="bold",
              color="#1A1A2E", pad=12)
ax1.set_ylabel("Number of Invoices", fontsize=10, color="#555577")
ax1.set_xticks(x)
ax1.set_xticklabels(TIER_ORDER, fontsize=10, color="#1A1A2E")
ax1.set_ylim(0, df_count.values.max() * 1.22)
ax1.tick_params(axis="y", labelsize=9, colors="#888888")
ax1.yaxis.grid(True, linestyle="--", alpha=0.5, color="#CCCCDD", zorder=0)
ax1.set_axisbelow(True)
for spine in ax1.spines.values():
    spine.set_visible(False)
ax1.legend(fontsize=9, frameon=False)
ax1.text(0.98, 0.97, f"Total: {total_invoices:,} invoices",
         transform=ax1.transAxes, ha="right", va="top",
         fontsize=9, color="#555577", style="italic")

# -----------------------------------------------------------
# Panel B — Uncollected Revenue
# -----------------------------------------------------------

ax2 = axes[1]
ax2.set_facecolor("#F7F8FA")

for i, issue in enumerate(ISSUE_ORDER):
    vals = df_amount[issue].values
    bars = ax2.bar(x + (i - 0.5) * width, vals, width=width,
                   color=ISSUE_COLORS[issue], label=issue, zorder=3)
    for bar, val in zip(bars, vals):
        offset = df_amount.values.max() * 0.02
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 max(bar.get_height(), 0) + offset,
                 f"${val:,.0f}", ha="center", va="bottom",
                 fontsize=9, fontweight="bold", color="#1A1A2E")

ax2.set_title("Uncollected Revenue by Plan Tier & Issue Type", fontsize=12, fontweight="bold",
              color="#1A1A2E", pad=12)
ax2.set_ylabel("Amount Uncollected ($)", fontsize=10, color="#555577")
ax2.set_xticks(x)
ax2.set_xticklabels(TIER_ORDER, fontsize=10, color="#1A1A2E")
ax2.set_ylim(bottom=min(df_amount.values.min() * 1.3, -500),
             top=df_amount.values.max() * 1.22)
ax2.yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))
ax2.tick_params(axis="y", labelsize=9, colors="#888888")
ax2.yaxis.grid(True, linestyle="--", alpha=0.5, color="#CCCCDD", zorder=0)
ax2.set_axisbelow(True)
for spine in ax2.spines.values():
    spine.set_visible(False)
ax2.legend(fontsize=9, frameon=False)
ax2.text(0.98, 0.97, f"Total: ${total_uncollect:,.0f}",
         transform=ax2.transAxes, ha="right", va="top",
         fontsize=9, color="#555577", style="italic")

# -----------------------------------------------------------
# Save & Show
# -----------------------------------------------------------

plt.tight_layout(rect=[0, 0.02, 1, 0.86])

out_path = os.path.join(script_dir, "03_3_Payment_Collection_Audit_Dec2025.png")
plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.show()
plt.close()