**Market Intelligence Platform*

**Contents**
[Overview](#overview)
[Handoff to a team member](#_Toc229936769)
[Data Sources](#data-sources)
[Why these sources were selected](#why-these-sources-were-selected)
[Repository Structure](#repository-structure)

[Setup Instructions](#setup-instructions)
[Prerequisites](#prerequisites)
[Python Dependencies](#python-dependencies)
[Running the Pipeline](#running-the-pipeline)

[Step 1 – Run ingestion](#step-1--run-ingestion)
[Step 2 – Run transformation](#step-2--run-transformation)
[Step 3 – Open Power BI](#step-3--open-power-bi)

[Pipeline Design Decisions](#pipeline-design-decisions)
[Separation of Layers](#separation-of-layers)
[Data Lineage](#data-lineage)
[Source-to-Consumption Flow](#source-to-consumption-flow)
[Data Curation](#data-curation)
[1. Common Time Axis](#common-time-axis)
[2. Trading Day Handling](#trading-day-handling)
[Failure Handling](#failure-handling)
[Missing Data After Alignment](#missing-data-after-alignment)
[Telemetry and Observability](#telemetry-and-observability)
[Dashboard Design](#dashboard-design)
[Calculated Metrics](#calculated-metrics)

# Overview

This product was developed as part of the Data Analytics Engineering Lead assessment: the objective was to build a lightweight but production-minded market intelligence platform that answers the business question:

*“How has market activity trended over the past 90 days, and is there anything we should be watching?”*

I believe this project fundamentally explores the tension between speed and risk when leveraging AI. **Leveraging AI without guardrails is a liability; but governance without speed is obsolete.**

**The challenge is: the practical implementation.** The goal is to build a trusted, well-governed semantic foundation so analytics and AI agents all draw from the same governed source of truth.

I would design according to these principles which I have developed based on my own experience in BI:

1\. **One integrated platform**: A single, fit-for-purpose platform connects ingestion, curation, semantic modelling, lineage, governance and reporting. This reduces waste through duplication and fragmentation and therefore makes AI-assisted analytics easier to govern and scale.

2\. **Human accountability where we matter**: Humans remain accountable for business meaning, semantic correctness, controls, exceptions and interpretation. An integrated platform supports this.

3\. **Business meaning reflected in the semantic layer**: Data teams exist to help the business make better decisions, reduce risk and create value. That business meaning must be translated into trusted definitions, relationships and rules: for AI-ready modelling and agentic reporting and insights.

4\. **Transparency and governance by design**: Lineage, security, telemetry and controls should be visible through the single platform. This reduces effort through duplication of oversight in disparate systems.

5\. **Data quality**: Reusable data products depend on trusted, well-governed data. High-quality sources enable BI teams and AI agents to deliver reliable insights on demand and future success.

# Handoff to a team member

For handoff with team leader:

1.  Read this document
2.  Do a walk-through of the end-to-end process as a recorded session for reference
3.  Team leader will only sign off on access to tooling (Python library, VS Code,etc) after you complete the above and demonstrate an understanding of the business context and risks

🟠 **BEFORE YOU START**: for handoff you need to ensure that you can answer these contextual questions:

-   What does the business need from our product (which questions do they need answered)?
-   How does our product help the business reach their financial goals; does the product impact external customers?
-   Which teams exist upstream and downstream in our ecosystem; can you name the key stakeholders? Introduce yourself to them.
-   What is our biggest risk we face as a team, and how do we address that in practice?

If you don’t yet know these answers, reach out to the lead reporting engineer, Tina Taylor.

🟠 **You own your product outcomes** **and are responsible** for checking and verifying any changes, including code or updates created via use of AI. If you’re unsure, ask someone before committing code.

Solution Architecture: High level flow

```
Yahoo Finance (S&P 500)
        ↓
FRED (VIX)
        ↓
Python ingestion layer
        ↓
Raw storage layer
        ↓
Python transformation layer
        ↓
Curated dataset (market_base.csv)
        ↓
Power BI semantic model
        ↓
Executive dashboard (visible in App in future state)
```

`
`

# Data Sources

| Source        |                                                 | Type         | Purpose                          |
|---------------|-------------------------------------------------|--------------|----------------------------------|
| Yahoo Finance | ![](media/81e2a918200469bc1ce6560cd5745971.png) | Market Index | S&P 500 daily market performance |
| FRED          | ![](media/09535882b1d023fd81543bce50f1f5b1.png) | Macro Series | VIX volatility index             |

## Why these sources were selected

The solution allows the dashboard to compare actual market movement from the S&P 500 against investor sentiment and expected volatility (VIX volatility index). Together, these measures help distinguish between stable market growth and periods where investor uncertainty may be increasing. Management can monitor market direction, and investor uncertainty.

| Feature              | S&P 500                                                       | VIX                                                                   |
|----------------------|---------------------------------------------------------------|-----------------------------------------------------------------------|
| **What it measures** | Market performance of 500 leading US companies; values in USD | Expected market volatility over the next 30 days                      |
| **Directionality**   | Generally rises with economic growth                          | Typically moves inversely to the market                               |
| **Business Value**   | Shows how markets are performing                              | Shows how nervous investors are; informally known as the ‘Fear index’ |
| **Data Nature**      | Price-driven market data                                      | Derived volatility index                                              |

## Repository Structure

```
Market-Intelligence-Platform/
│
├── data/
│   ├── raw/
│   │   ├── sp500_data.csv
│   │   └── vix_data.csv
│   │
│   └── curated/
│       └── market_base.csv
│
├── logs/
│   └── data_quality_log.csv
│
├── src/
│   ├── ingest.py
│   └── transform.py
│
├── README.md
└── Market_Intelligence.pbix
```

# Setup Instructions

## Prerequisites

Install:

-   Python 3.13+
-   Visual Studio Code
-   Power BI Desktop

## Python Dependencies

Install required libraries:

```
pandas (data transformation) yfinance (finance data)
```

🟢# Running the Pipeline

**3 x steps required in running the pipeline:**

## Step 1 – Run ingestion

```
(Run in VS Code Terminal) python src/ingest.py
```

This:

-   retrieves S&P 500 data from Yahoo Finance
-   retrieves VIX data from FRED
-   stores raw files locally

Outputs:

```
/data/raw/sp500_data.csv
/data/raw/vix_data.csv
```

## Step 2 – Run transformation

```
(Run in VS Code Terminal) python src/transform.py 
```

-   This standardises dates
-   aligns both sources onto a common time axis based on UTC time
-   handles missing data by preserving and logging those instances to the data quality log
-   applies data quality checks (null detection)
-   creates a trading-day flag to explicitly distinguish trading vs non-trading days for time-intelligence reporting in semantic layer
-   produces curated output that can be re-used in other analytics projects and semantic modelling

Outputs:

```
/data/curated/market_base.csv   (check for confirmation message "Transformation complete.")
/logs/data_quality_log.csv
```

## Step 3 – Open Power BI

Open:

```
Market Project.pbix
```

Refresh the model:

```
Home → Refresh
Future steps:  Not included in this project
Determine appropriate access and create appropriate access groups to apply to Power BI app.
Publish the report to our team’s Workspace and then include in relevant audience App in Power BI. 
```

# Pipeline Design Decisions

## Separation of Layers

The solution intentionally separates:

| Layer          | Responsibility                     |
|----------------|------------------------------------|
| Ingestion      | Retrieve external data             |
| Raw storage    | Preserve source outputs            |
| Transformation | Standardise, align and curate data |
| Semantic model | Business calculations and DAX      |
| Presentation   | Executive dashboard                |

This separation allows the platform to evolve independently over time without too tightly coupling operational pipelines to reporting outputs.

# Data Lineage

## Source-to-Consumption Flow

```
Yahoo Finance (S&P 500)
    → data/raw/sp500_data.csv
    → data/curated/market_base.csv
    → Power BI semantic model
    	→ S&P 500 visuals and rolling averages

FRED (VIX)
    → data/raw/vix_data.csv
    → data/curated/market_base.csv
    → Power BI semantic model
    	→ Volatility monitoring and market signals
A dynamic Calendar table is created in the Power BI semantic model to act as a dimensional date table in Power BI
```

# Data Curation

Curation logic is implemented within: src/transform.py

## Common Time Axis

The S&P 500 and VIX datasets were aligned onto a shared date axis based on UTC time.

Date handling included:

-   explicit timezone normalization using UTC conversion
-   handling non-trading days through ‘Is trading day’ column (see item 2)
-   preservation of missing observations through outer join

Both datasets were aligned to a shared reporting period beginning 1 April 2024 for demonstration purposes. This filter should be removed in a final production environment.

## Trading Day Handling

A trading-day flag was generated upstream in the curated layer:

```
Is_SP500_Trading_Day
```

This identifies whether the S&P 500 had a valid market close value for a given reporting date. The flag is derived directly from the availability of an actual market close value, rather than inferred from calendar logic. i.e. markets don’t trade every calendar day, given public holidays.

The flag was then surfaced into the Power BI Calendar table which acts as a dimension table. This column is used to support semantic modelling and date filtering logic.

# Failure Handling

## Missing Data After Alignment

The S&P 500 and VIX series may not both contain values for every reporting date due to:

-   weekends
-   market holidays
-   source update timing differences or missing source observations

The transformation layer intentionally uses an **outer join** when aligning the datasets.

This ensures missing observations and null values are retained rather than being hidden or dropped.

After alignment:

-   missing values are logged in

    `├── logs/`  
    `    └── data_quality_log.csv`

-   quality outcomes are recorded
-   rows remain visible in the curated dataset

This allows gaps to remain transparent in Power BI to show data quality in the report

# Telemetry and Observability

| Telemetry /<br> observability item | How it is addressed in the code                                                                                            |
|------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| Execution timestamp                | datetime.now().isoformat() records when a data quality event occurred                                                      |
| Source / stage                     | source records whether the issue came from Yahoo Finance S&P 500, FRED VIX, or the merged dataset                          |
| Issue type                         | issue_type captures the category of issue, such as null values or missing values after alignment                           |
| Affected record count              | record_count captures how many values were affected                                                                        |
| Corrective action                  | action_taken records how the pipeline handled the issue                                                                    |
| Missing observation monitoring     | market_base.isnull().sum().sum() checks for missing values after source alignment                                          |
| Transformation success visibility  | print("Transformation complete.") confirms the process completed successfully                                              |
| Output traceability                | print(f"Saved curated dataset: {output_path}") and print(f"Saved quality log: {log_path}") show where outputs were written |

# Dashboard Design

The target audience is financially literate business users. The dashboard answers the question: *“How has market activity trended over the past 90 days, and is there anything we should be watching?”*

It focuses on:

-   market trend visibility
-   simplified executive signals
-   readability over technical complexity

| Concepts used in dashboard   | Purpose                                                                                                |
|------------------------------|--------------------------------------------------------------------------------------------------------|
| S&P 500 trend of close price | Market direction over 90 days                                                                          |
| Rolling average overlay      | Trend smoothing on top of S&P 500 trend                                                                |
| Macro overlay                | Compare market movement of S&P 500 against volatility, fear index                                      |
| Market signal                | Executive monitoring indicator via RAG, to be easily recognised                                        |
| Data quality indicators      | Transparency and observability to show number of poor quality records included in selected report view |

# Calculated Metrics

The solution includes the following calculated measures in the semantic layer: Power BI (DAX).

|   | Metric                   | Purpose                             |
|---|--------------------------|-------------------------------------|
| 1 | SP500 7D Rolling Average | Smooths the short-term market noise |
| 2 | SP500 90D Change %       | Show directional market momentum    |
| 3 | Market Signal (RAG)      | Executive monitoring indicator      |
|   |                          |                                     |

1.  **S&P 500 7-Day Rolling Average**

Business Requirement: Management should be able to see the short-term direction of the market without overreacting to daily volatility. It helps them distinguish between normal day-to-day price fluctuation and meaningful market direction changes.

**Requirement:** Calculate a rolling average using the most recent 7 valid S&P 500 trading days

-   Exclude weekends and non-trading days from the calculation.
-   Smooth short-term market noise to make directional trends easier to interpret.
-   This will need to be displayed with the daily S&P 500 market trend
2.  **S&P 500 90-Day Change %**

Business Requirement: Management should be able to quickly understand whether market momentum has strengthened or weakened over the reporting period.

**Requirement:** Compare the latest valid S&P 500 close against the valid trading close approximately 90 days earlier

-   Rather than just simple calendar subtraction of -90, take into account weekends and non-trading days
-   Return the directional percentage movement over the reporting window as a %
3.  **Market Signal (RAG)**

Business Requirement: Management should have a simplified indicator that highlights whether market conditions appear stable, cautionary, or elevated risk. They need to know whether to act.

**Requirement:** Combine market performance and market volatility into a single signal

-   Use the VIX as a proxy for investor uncertainty
-   Compare current market performance against the recent 7-day market trend
-   Trigger escalating signals when volatility increases or market performance weakens materially
-   Threshold Logic

| **Signal** | **Logic**                                                                                          |
|------------|----------------------------------------------------------------------------------------------------|
|🔴Red       | VIX ≥ 30 OR S&P 500 more than 3% below its recent 7-day trading average                            |
|🟠 Amber    | VIX ≥ 20 OR S&P 500 below its recent 7-day trading average, where Red conditions are not triggered |
|🟢Green     | Market conditions broadly stable relative to recent trading conditions                             |

Note: for presentation layer: The signal was summarized to business viewers in the dashboard as:

**Red**  VIX ≥ 30 OR S&P500 \< 97% of rolling average, *else if*

**Amber** VIX ≥ 20 OR S&P500 below rolling average,

**Green** everything else

