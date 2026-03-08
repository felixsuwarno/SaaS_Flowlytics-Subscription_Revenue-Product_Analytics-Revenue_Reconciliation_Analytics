WIP - Work in Progress - March 08 2026

# SaaS_Flowlytics-Subscription_Revenue-Product_Analytics-Revenue_Reconciliation_Analytics
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

1. REVENUE & SUBSCRIPTION ECONOMICS
  1. How does Monthly Recurring Revenue (MRR) change each month when broken into new, expansion, contraction, and churned MRR?
  2. How does Net Revenue Retention (NRR) change over time?
  3. How are customers and subscription revenue distributed across U.S. states?
   
2. PRODUCT EXPERIMENTATION
  1. Does the new onboarding experience increase trial-to-paid conversion?
  2. Is the difference in trial-to-paid conversion between the control and treatment groups statistically significant?
  3. What user characteristics are associated with trial-to-paid conversion?

3. FINANCIAL DATA VALIDATION
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











































