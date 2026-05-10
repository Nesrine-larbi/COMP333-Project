# COMP 333 — End-to-End Data Analytics Pipeline

Full machine learning pipeline on NYC Yellow Taxi Trip Records, built as the final project for COMP 333 at Concordia University (April 2026).

---

## Overview

We designed and implemented an end-to-end data science pipeline covering data acquisition, wrangling, exploratory analysis, feature engineering, supervised classification, and unsupervised clustering — applied to 7.3 million real-world taxi trips.

---

## Team

| Name | Student ID |
|------|-----------|
| Nesrine Larbi | 40079009 |
| Patrice Gallant | 40301020 |
| Ronnie Chan | 27206003 |

## Dataset

| Field | Value |
|-------|-------|
| Source | [NYC TLC Yellow Taxi Trip Records](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) |
| Weather | [Open-Meteo Historical Weather API](https://open-meteo.com/) |
| Period | June – July 2025 |
| Volume | ~7.3M trips · 1.4+ GB (Parquet) |
| Features | 14 clean features after wrangling |

---

## Research Questions

**RQ1 — Supervised Learning**
> Can we classify a high-tipper passenger based on trip features, rate code, and weather conditions?

- Target: `is_high_tip` (tip ≥ 20% of fare amount)
- Models: Random Forest, XGBoost

**RQ2 — Unsupervised Learning**
> Can we identify distinct natural clusters of NYC taxi trips based on temporal and financial features to study customer behavior?

- Method: PCA + MiniBatch K-Means (k = 7)

---

## Pipeline

```
Data Acquisition → Wrangling & EDA → Feature Engineering → Supervised Learning → Unsupervised Learning → Insights
```

### Data Wrangling
- Removed exact duplicates and 150K mirrored (cancelled) entries
- Dropped 238K zero-distance records and invalid date entries
- Replaced zero-passenger values with mode; flagged negative fares
- Capped outliers at the 99th percentile (Winsorization)

### Feature Engineering
- Log transforms: `log_trip_distance`, `log_fare_per_km`
- Cyclical encoding: `hour_sin/cos`, `day_sin/cos`
- Domain flags: `is_rush_hour`, `is_airport`, `is_weekend`, `is_night`, `fare_per_mile`
- Interaction features: `trip_distance²`, `distance × passengers`, `temp × precipitation`
- 3-stage feature selection: Filter (Pearson + mutual info) → Embedded (RF importance) → Wrapper (RFE) → **12 final features**

---

## Results

### RQ1 — Supervised Classification

| Metric | Random Forest | XGBoost |
|--------|--------------|---------|
| Test Accuracy | 0.77 | 0.77 |
| F1-Score (CV) | 0.8637 | 0.8637 |
| AUC-ROC | 0.6293 | 0.6302 |
| Avg Precision | 0.8176 | 0.8192 |
| Train Time | ~250s | ~150s |

**Selected model: XGBoost** — marginally higher AUC, 40% faster training.

Top features: `improvement_surcharge`, `fare_amount`, `congestion_surcharge` — tipping is driven by payment structure, not weather or time of day.

### RQ2 — Unsupervised Clustering

| Metric | Value |
|--------|-------|
| Silhouette Score | 0.18 |
| Davies-Bouldin Index | 1.35 |
| PCA components | 6 (≈90% variance) |
| Clusters | 7 |

| Cluster | Label | Actionable Strategy |
|---------|-------|-------------------|
| 0 | Long Trip | Premium pricing · pre-position near JFK/LGA |
| 1–2 | Short Trip | Investigate merging for sharper targeting |
| 3 | Medium Trip | Standard base-fare offers |
| 4 | Weather-Impacted | Dynamic surge pricing during rain |
| 5 | Peak Morning | Pre-position in business districts before 08:00 |
| 6 | High-Occupancy | Group-ride promotions |

---

## Tools & Technologies

| Category | Tools |
|----------|-------|
| Language | Python 3 |
| Data | pandas, NumPy |
| ML | scikit-learn, XGBoost |
| Visualization | matplotlib, seaborn |
| Environment | Google Colab |
| Data format | Parquet, CSV |

---

## Project Structure

```
├── teamd_phase1.ipynb              # Phase 1: Data acquisition, wrangling, EDA, baseline model
├── TeamD_Phase2.ipynb              # Phase 2: Feature engineering, supervised & unsupervised learning
├── TeamD_Phase3.ipynb              # Phase 3: Full pipeline + advanced evaluation + insights
├── generate_executive_summary.py
├── Executive_Summary_TeamD.pdf
├── TeamD_DEMO_COMP333.pptx
└── README.md
```

---



Concordia University · COMP 333 · April 2026
