WIP - Work in Progress - March 12 2026

# SaaS Flowlytics - Subscription Revenue - Product Analytics - Revenue Reconciliation Analytics
MRR Movement, Net Revenue Retention, Geographic Revenue Distribution, Onboarding Experiment Analysis, and Revenue & Billing Reconciliation

<br>

This project analyzes three years of synthetic SaaS subscription data from a simulated workflow automation platform, spanning January 2024 to June 2026. The dataset contains customer-level, trial-level, subscription lifecycle, billing, and engagement records, along with product experiment assignments and marketing acquisition data.

The analysis evaluates subscription revenue dynamics, customer activation behavior, product experimentation outcomes, and financial reconciliation across the subscription and billing systems. The full workflow is built end-to-end using SQL and Python across a dataset representing the entire SaaS customer lifecycle—from trial signup and onboarding to subscription activation, expansion, contraction, churn, billing, and payment events.

<br>

➤ Project Goal / Purpose:<br>

This project evaluates how a simulated SaaS subscription business generates and retains recurring revenue over time—examining whether subscription growth is stable, whether product onboarding improvements meaningfully increase activation, and whether billing operations accurately capture all expected revenue.

The analysis measures monthly recurring revenue (MRR) movement by identifying new subscriptions, expansion upgrades, contraction downgrades, and churn events. It evaluates Net Revenue Retention (NRR) trends to determine whether existing customers expand their subscription value over time or whether revenue growth relies primarily on new customer acquisition.

At the product level, the project evaluates a controlled onboarding experiment to determine whether a redesigned onboarding experience increases trial-to-paid conversion. The analysis compares conversion rates between control and treatment groups, tests statistical significance, and analyzes user engagement characteristics associated with successful activation.

At the financial operations level, the project performs revenue reconciliation between subscription records and billing invoices to identify operational discrepancies such as missing invoices, billing errors, or delayed billing events. The objective is to evaluate whether subscription activity and billing operations remain aligned, ensuring that expected recurring revenue is properly captured.

<br>

➤ Skills Demonstrated:<br>

Subscription revenue modeling (MRR movement and Net Revenue Retention), geographic revenue analysis, product experiment evaluation (A/B testing and statistical significance testing), trial-to-paid conversion analysis, behavioral feature analysis, and financial reconciliation between subscription and billing systems.

(SQL • Python • Pandas • SaaS Revenue Analytics • A/B Experiment Analysis • Revenue Reconciliation • Executive-Ready Analysis)

<br>

➤ Core Business Questions :<br>

**1. REVENUE & SUBSCRIPTION ECONOMICS**
   
  1. How does Monthly Recurring Revenue (MRR) change each month when broken into new, expansion, contraction, and churned MRR?
  2. How does Net Revenue Retention (NRR) change over time?
  3. How are customers and subscription revenue distributed across U.S. states?
   
**2. PRODUCT EXPERIMENTATION**
   
  1. Does the new onboarding experience increase trial-to-paid conversion?
  2. Is the difference in trial-to-paid conversion between the control and treatment groups statistically significant?
  3. What user characteristics are associated with trial-to-paid conversion?

**3. FINANCIAL DATA VALIDATION**

  1. Which active subscriptions did not generate a billing invoice in the expected billing month?
  2. Which billing invoices were generated for subscriptions that were not active in the billing period?
  3. Which billing invoices have not been fully paid, or were paid later than the expected payment window?

<br>

➤ Executive Summary :<br>
Work in Progress

<br>

➤ The Dataset :<br>
The raw dataset spans January 2024 through June 2026, and all reporting and conclusions in this project are intentionally scoped to this full analytical window to evaluate subscription revenue growth, customer activation behavior, product experimentation outcomes, and financial reconciliation across the subscription lifecycle.

The analysis uses nine core tables representing a simulated SaaS workflow automation platform (“Flowlytics”):

**customers**
- Used to define customer cohorts, analyze geographic revenue distribution, and segment customers when evaluating subscription revenue patterns and experiment outcomes.
- One row per customer.
- Contains **signup_date**, **acquisition** channel, and geographic attributes (**state**, **region**).

**trials**
- One row per trial signup.
- Used to analyze the trial funnel, measure trial-to-paid conversion behavior, and define the population exposed to onboarding experiments.
- Contains **trial_start**, **trial_end**, and the associated **customer_id**.

**trial_engagement_summary**
- Used to analyze which product usage patterns are associated with successful trial-to-paid conversion.
- One row per trial user summarizing engagement behavior during the trial period.
- Contains engagement metrics such as **templates_used**, **workflows_created**, **days_active_during_trial**, and **integrations_connected**.

**experiment_assignments**
- Used to evaluate whether the redesigned onboarding experience increases trial-to-paid conversion and to test statistical significance between experiment groups.
- One row per customer assigned to the onboarding experiment.
- Contains the experiment variant (**control** vs **treatment**).

**subscriptions**
- Used to track the subscription lifecycle and define which customers are expected to generate recurring revenue.
- One row per subscription lifecycle record.
- Contains **subscription_start**, **plan_tier**, and the current **subscription_status** (**active**, **cancelled**, or **trial_only**).

**subscription_events**
- Used to construct Monthly Recurring Revenue (MRR) movement and analyze revenue growth through new subscriptions, upgrades, downgrades, and churn.
- One row per subscription revenue event.
- Contains **event_date**, **event_type** (**new**, **expansion**, **contraction**, **churn**), and the associated **mrr_change**.

**billing_invoices**
- Used to represent the billing system and support reconciliation between expected subscription revenue and invoiced revenue.
- One row per billing invoice generated for an active subscription.
- Contains **invoice_month**, **invoice_amount**, and the associated **subscription_id** and **customer_id**.

**payments**
- Used to measure cash collection behavior, identify unpaid or late invoices, and reconcile billed revenue against collected payments.
- One row per payment transaction applied to an invoice.
- Contains **payment_date**, **payment_amount**, **payment_status**, and **days_to_pay**.

**acquisition_costs**
- Used to analyze customer acquisition patterns and support marketing cost analysis across the subscription lifecycle.
- One row per month per acquisition channel.
- Contains marketing spend across **channels** such as **Google Ads**, **LinkedIn**, **Partner**, and **Organic**.

## The Main Report - Key Questions Answered

### 1 — REVENUE & SUBSCRIPTION ECONOMICS
Are our existing customers bringing in more revenue over time, or do we need a constant flow of new customers just to keep the numbers up?

<br>

**1-1  How does Monthly Recurring Revenue (MRR) change each month when broken into new, expansion, contraction, and churned MRR?**


**Tables used**
- subscription_events

**SQL Method**
- **Filter subscription_events to the analytical window:** Keep only rows where event_date falls within January 2024 to June 2026. Retain subscription_id, event_date, event_type, and mrr_change.
  - Truncate **event_date** to the first day of the month and name it **mrr_month**.
- **Aggregate by month and event type:** Group by mrr_month and event_type.
  - Sum **mrr_change** to produce **total_mrr** — the total MRR contributed by each event type in that month.
- **Pivot event types into columns:** Group by mr**r**_month and conditionally sum **total_mrr** for each event type into separate columns — **new_mrr**, **expansion_mrr**, **contraction_mrr**, and **churn_mrr**.
  - Sum all four columns to produce **total_mrr** — the net MRR change for that month.

**Python Method**
- No data modeling is done on python, python is just used to visualize the data.

<br>

**Charts**

<p align="center">
  <img src="Charts/01_1_Monthly_Recurring_Revenue.png" width="100%">
</p>

<br>

**Key Insights**

- **MRR grew every single month in 2025 without exception.** The business ended the year at $97,490 in cumulative net MRR, adding positive net MRR all 12 months.
- **New customer acquisition is the sole growth engine.** New MRR runs at $16,000–$21,000 every month and completely dominates the chart. Expansion from existing customers is minimal — barely visible against the green bars.
- **Q1 was the most volatile quarter.** March shows the deepest churn of the year at over -$14,000, which nearly wiped out all new MRR that month — net MRR of only $2,994. This directly explains the NRR dip to 94.55% in March.
- **Churn is the biggest threat to the business.** Running at -$7,000 to -$14,000 every month, churn consistently offsets a large portion of new revenue. The business is essentially running on a treadmill — acquiring new customers to replace the ones leaving.
- **Expansion is too small to matter.** Expansion MRR never exceeds $2,000 in any single month. This means the business has not found a way to grow revenue from customers already on the platform — upselling and cross-selling are not working.

<br>

**1-2  How does Net Revenue Retention (NRR) change over time?**

First, generate monthly MRR table across time.

**Tables used**
- subscription_events

**SQL Method**
- **Filter subscription_events to the full historical range:** Keep only rows where event_date falls between January 2023 and December 2025. Retain **subscription_id**, **event_date**, **event_type**, and **mrr_change**.
  - Truncate event_date to the first day of the month and name it mrr_month.
- **Aggregate MRR components by month:** Group by **mrr_month** and conditionally sum **mrr_change** for each event type into **new_mrr**, **expansion_mrr**, **contraction_mrr**, and **churn_mrr**.
  - Sum all four components to produce **total_mrr** — the net MRR change for that month.
- **Calculate cumulative MRR balance:** From the aggregated table, compute **mrr_balance** as the running cumulative sum of **total_mrr** ordered by **mrr_month** — representing the total MRR the business has built up through the end of each month.

That generates "**01_2a_MRR_Across_Time.csv**"

Next we generate the NRR calculations.

**SQL Method**
- **Filter MRR table ( 01_2a_MRR_Across_Time )  without a date filter:** Retain **mrr_month**, **expansion_mrr**, **contraction_mrr**, and **churn_mrr**.
  - For each month, look back one month and pull **mrr_balance** from the prior month — name it **starting_mrr**. This is the existing revenue base going into the current month.
- **Calculate NRR per month:** Keep only rows where **mrr_month** falls within 2025. Compute **nrr_pct** as (**starting_mrr** + **expansion_mrr** + **contraction_mrr** + **churn_mrr**) / **starting_mrr** × 100.

**Python Method**
- No data modeling is done on python, python is just used to visualize the data.

<br>

**Charts**

<p align="center">
  <img src="Charts/01_2_Net_Revenue_Retention.png" width="100%">
</p>

**Key Insights**

- **Flowlytics grew every month in 2025, but entirely from new customers signing up.** Existing customers were not spending more over time — upgrades and expansions were minimal all year.
- **Existing customers were leaving or downgrading every single month.** The business lost between 2.6% and 5.5% of its existing revenue each month to cancellations and downgrades. New signups covered the losses, but just barely.
- **March was the worst month.** Churn spiked, new revenue barely covered the losses, and the business nearly flatlined. After March things improved, but the underlying problem never went away.
- **The business is entirely dependent on new customer acquisition.** Every month, Flowlytics has to sign up enough new customers just to replace the ones it lost. If new signups slow down for even one or two months, revenue will drop. That is a fragile position to be in.
- **The opportunity is in existing customers.** If Flowlytics could get them to upgrade their plans or use more features, revenue would grow even without a single new signup. Right now that is not happening.

---

**1-3  How are customers and subscription revenue distributed across U.S. states?**

**Tables used**:
- subscriptions
- subscription_events
- customers

**SQL Method**
- Filter subscriptions to active records only: Reduce the subscriptions table to rows where subscription_status = 'active'. Keep subscription_id and customer_id.
- Filter subscription events up to December 31 2025: Reduce the subscription_events table to rows where event_date is on or before December 31, 2025. This captures the full event history needed to reconstruct each customer's MRR standing as of December 31 2025. Keep subscription_id and mrr_change.
- Join active subscriptions to their events: Join the filtered subscriptions to the filtered events on subscription_id. Keep customer_id and mrr_change.
- Aggregate net MRR per customer: Group by customer_id and sum mrr_change to produce net_mrr — the MRR standing for each active customer as of December 31 2025.
- Join customer MRR to customers to bring in state: Join the aggregated customer MRR result to the customers table on customer_id. Keep customer_id, state, and net_mrr.
- Aggregate metrics by state: Group by state and produce:
  - customer_count — number of active customers in that state as of December 31 2025
  - total_mrr — sum of net_mrr across all active customers in that state

**Python Method**
- No data modeling is done on python, python is just used to visualize the data.

<br>

**Charts**

<p align="center">
  <img src="Charts/01_2_Net_Revenue_Retention.png" width="100%">
</p>

**Key Insights**

- 


























