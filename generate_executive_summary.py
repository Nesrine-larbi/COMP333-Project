"""
Generate Executive Summary PDF for COMP 333 Project.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


OUTPUT_PATH = "Executive_Summary_TeamD.pdf"

# ── Colour palette ────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#1A3A5C")
MID_BLUE    = colors.HexColor("#2E6DA4")
LIGHT_BLUE  = colors.HexColor("#D6E8F7")
ACCENT      = colors.HexColor("#E8A020")
LIGHT_GREY  = colors.HexColor("#F5F5F5")
RULE_GREY   = colors.HexColor("#CCCCCC")

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "title",
    parent=styles["Normal"],
    fontSize=18,
    leading=23,
    textColor=DARK_BLUE,
    alignment=TA_CENTER,
    fontName="Helvetica-Bold",
    spaceAfter=3,
)
subtitle_style = ParagraphStyle(
    "subtitle",
    parent=styles["Normal"],
    fontSize=10,
    leading=13,
    textColor=MID_BLUE,
    alignment=TA_CENTER,
    fontName="Helvetica",
    spaceAfter=2,
)
meta_style = ParagraphStyle(
    "meta",
    parent=styles["Normal"],
    fontSize=8,
    leading=11,
    textColor=colors.grey,
    alignment=TA_CENTER,
    fontName="Helvetica",
)
section_style = ParagraphStyle(
    "section",
    parent=styles["Normal"],
    fontSize=10,
    leading=13,
    textColor=colors.white,
    fontName="Helvetica-Bold",
    spaceAfter=3,
    spaceBefore=6,
    leftIndent=6,
)
body_style = ParagraphStyle(
    "body",
    parent=styles["Normal"],
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#222222"),
    fontName="Helvetica",
    alignment=TA_JUSTIFY,
    spaceAfter=3,
)
bullet_style = ParagraphStyle(
    "bullet",
    parent=body_style,
    leftIndent=14,
    firstLineIndent=-8,
    spaceAfter=2,
)
bold_body = ParagraphStyle(
    "bold_body",
    parent=body_style,
    fontName="Helvetica-Bold",
)
caption_style = ParagraphStyle(
    "caption",
    parent=styles["Normal"],
    fontSize=8,
    leading=10,
    textColor=colors.grey,
    fontName="Helvetica-Oblique",
    alignment=TA_CENTER,
)


# ── Helper: coloured section header ──────────────────────────────────────────
def section_header(text, bg=MID_BLUE):
    tbl = Table(
        [[Paragraph(text, section_style)]],
        colWidths=[7.0 * inch],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [3]),
    ]))
    return tbl


def bullet(text):
    return Paragraph(f"&#x2022;&#160; {text}", bullet_style)


# ── Build content ─────────────────────────────────────────────────────────────
story = []

# ── Header / Title block ──────────────────────────────────────────────────────
story.append(Spacer(1, 0.10 * inch))
story.append(Paragraph("COMP 333 — End-to-End Data Analytics Pipeline", title_style))
story.append(Paragraph("Executive Summary", subtitle_style))
story.append(Spacer(1, 0.04 * inch))
story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=3))
story.append(
    Paragraph(
        "Team D&#160; &#160;|&#160; &#160;"
        "Ronnie Chan (27206003)&#160; &#160;·&#160; &#160;"
        "Patrice Gallant (40301020)&#160; &#160;·&#160; &#160;"
        "Nesrine Larbi (40079009)&#160; &#160;|&#160; &#160;"
        "Concordia University&#160; &#160;|&#160; &#160;April 2026",
        meta_style,
    )
)
story.append(HRFlowable(width="100%", thickness=1, color=RULE_GREY, spaceBefore=3, spaceAfter=7))


# ── 1. Project Overview ───────────────────────────────────────────────────────
story.append(section_header("1.  Project Overview"))
story.append(Spacer(1, 0.04 * inch))
story.append(Paragraph(
    "This project implements a complete, end-to-end data analytics and machine learning pipeline "
    "applied to <b>New York City (NYC) Yellow Taxi Trip Records</b> for June–July 2025. "
    "<b>Phase 1</b> covers data acquisition, wrangling, EDA, and baseline modelling; "
    "<b>Phase 2</b> advances into feature engineering, supervised classification, "
    "unsupervised clustering, and result interpretation.",
    body_style,
))
story.append(Spacer(1, 0.03 * inch))

# Dataset summary table
ds_data = [
    [Paragraph("<b>Attribute</b>", bold_body), Paragraph("<b>Detail</b>", bold_body)],
    ["Primary Dataset", "NYC Yellow Taxi Trip Records — June & July 2025 (~7.3 M rows, 1.4+ GB on disk)"],
    ["Supplementary", "NYC Hourly Weather (Open-Meteo API) — temperature (°C) and precipitation (mm)"],
    ["Environment", "Google Colab (12.7 GB RAM); Python 3 · pandas · scikit-learn · XGBoost"],
]
ds_table = Table(ds_data, colWidths=[1.5 * inch, 5.5 * inch])
ds_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), DARK_BLUE),
    ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0), (-1, -1), 8),
    ("LEADING",       (0, 0), (-1, -1), 10),
    ("ROWBACKGROUNDS",(0, 1), (-1, -1), [LIGHT_GREY, colors.white]),
    ("GRID",          (0, 0), (-1, -1), 0.4, RULE_GREY),
    ("TOPPADDING",    (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING",   (0, 0), (-1, -1), 5),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(ds_table)
story.append(Spacer(1, 0.06 * inch))


# ── 2. Phase 1 — Data Acquisition, Cleaning & Baseline ───────────────────────
story.append(section_header("2.  Phase 1 — Data Acquisition, Cleaning & Baseline Modelling"))
story.append(Spacer(1, 0.04 * inch))

story.append(Paragraph("<b>Data Wrangling & EDA Highlights</b>", bold_body))
for b in [
    "Removed 4 exact duplicates and <b>150,444 mirrored records</b>; dropped <b>238,440 zero-distance rows</b>; imputed missing values and applied Winsorization (99th-percentile) to five financial features.",
    "Final clean dataset: <b>14 features</b> across ~7 M records (Parquet). Trip distance is the strongest fare predictor (r = 0.87); credit card accounts for ~75 % of rides; demand peaks post-17:00 on weekdays.",
    "<b>Baseline (Phase 1):</b> Linear Regression Model B (<i>trip_distance</i> + <i>tip_amount</i>) selected for low MSE, high R², and stable generalisation.",
]:
    story.append(bullet(b))
story.append(Spacer(1, 0.06 * inch))


# ── 3. Research Questions ─────────────────────────────────────────────────────
story.append(section_header("3.  Research Questions"))
story.append(Spacer(1, 0.04 * inch))

rq_data = [
    [
        Paragraph("<b>RQ1 — Supervised Learning</b>", bold_body),
        Paragraph("<b>RQ2 — Unsupervised Learning</b>", bold_body),
    ],
    [
        Paragraph(
            "<i>\"Can we classify a high-tipper passenger based on trip features "
            "(distance, time of day, day of week, rate code, passenger count) "
            "and weather conditions?\"</i><br/><br/>"
            "Target: <b>is_high_tip</b> (tip ≥ 20 % of fare_amount) — Models: <b>Random Forest, XGBoost</b>",
            body_style,
        ),
        Paragraph(
            "<i>\"Can we identify distinct natural clusters of NYC taxi trips based "
            "on temporal and financial features to study customer behaviour?\"</i><br/><br/>"
            "Method: <b>PCA</b> + <b>MiniBatch K-Means</b> (k = 7)",
            body_style,
        ),
    ],
]
rq_table = Table(rq_data, colWidths=[3.5 * inch, 3.5 * inch])
rq_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), LIGHT_BLUE),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("GRID",          (0, 0), (-1, -1), 0.4, RULE_GREY),
    ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
    ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
]))
story.append(rq_table)
story.append(Spacer(1, 0.06 * inch))


# ── 4. Phase 2 — Feature Engineering ─────────────────────────────────────────
story.append(section_header("4.  Phase 2 — Feature Engineering"))
story.append(Spacer(1, 0.04 * inch))
story.append(Paragraph(
    "Thirty features were engineered across three groups: <b>(1)</b> log-transforms and cyclical "
    "hour/day encodings; <b>(2)</b> domain flags (is_rush_hour, is_airport, is_credit_card, fare_per_mile); "
    "<b>(3)</b> polynomial/interaction terms (distance², distance × passengers, temp × precipitation). "
    "Filter, embedded (RF importance), and wrapper (RFE) methods produced a "
    "<b>top-12 composite feature set (FINAL_FEATURES)</b>, excluding leakage variables "
    "(<i>tip_amount</i>, <i>total_amount</i>, <i>tip_ratio</i>).",
    body_style,
))
story.append(Spacer(1, 0.06 * inch))


# ── 5. Supervised Learning Results ───────────────────────────────────────────
story.append(section_header("5.  Supervised Learning Results  (RQ1)"))
story.append(Spacer(1, 0.04 * inch))
story.append(Paragraph(
    "Both models trained on <b>1 M stratified credit-card records</b> (70/15/15 split, "
    "RandomSearchCV 3-fold, F1 metric). <b>XGBoost selected</b> for marginally higher AUC "
    "and 40 % faster training.",
    body_style,
))
story.append(Spacer(1, 0.03 * inch))

# Performance table
perf_data = [
    [
        Paragraph("<b>Metric</b>", bold_body),
        Paragraph("<b>Random Forest</b>", bold_body),
        Paragraph("<b>XGBoost</b>", bold_body),
    ],
    ["CV / Val F1-Score",              "0.8637 / 0.8636", "0.8637 / 0.8636"],
    ["Test Accuracy",                  "0.77",            "0.77"],
    ["Recall — High Tip",              "1.00",            "1.00"],
    ["AUC-ROC",                        "0.6293",          "0.6302"],
    ["Training Time",                  "~250 s",          "~150 s"],
]
perf_table = Table(perf_data, colWidths=[2.6 * inch, 2.2 * inch, 2.2 * inch])
perf_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), DARK_BLUE),
    ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
    ("LEADING",       (0, 0), (-1, -1), 11),
    ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.white, LIGHT_GREY]),
    ("GRID",          (0, 0), (-1, -1), 0.4, RULE_GREY),
    ("TOPPADDING",    (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
    ("ALIGN",         (1, 0), (-1, -1), "CENTER"),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ("BACKGROUND",    (2, 1), (2, -1), colors.HexColor("#EBF5FF")),
]))
story.append(perf_table)
story.append(Spacer(1, 0.04 * inch))

for b in [
    "Top features: <b>improvement_surcharge</b>, <b>fare_amount</b>, <b>congestion_surcharge</b> — tipping is driven by payment method and fare structure, <i>not</i> time of day or weather.",
    "Limitation: persistent 75/25 class imbalance causes low recall (0.08) for 'Low Tip'; cash rides introduce structural label noise. Future: SMOTE or undersampling.",
]:
    story.append(bullet(b))
story.append(Spacer(1, 0.06 * inch))


# ── 6. Unsupervised Learning Results ──────────────────────────────────────────
story.append(section_header("6.  Unsupervised Learning Results  (RQ2)"))
story.append(Spacer(1, 0.04 * inch))
story.append(Paragraph(
    "PCA reduced the 8-feature space to <b>6 PCs (≈ 90 % variance)</b>; elbow method on a "
    "100 K subsample identified <b>k = 7</b>. Full dataset (~7 M rows) clustered with "
    "<b>MiniBatch K-Means</b> (Silhouette = 0.18; Davies-Bouldin = 1.35 — "
    "overlapping clusters consistent with real-world behavioural data).",
    body_style,
))
story.append(Spacer(1, 0.03 * inch))

# Cluster table
cluster_data = [
    [
        Paragraph("<b>Cluster</b>", bold_body),
        Paragraph("<b>Label</b>", bold_body),
        Paragraph("<b>Key Characteristic</b>", bold_body),
    ],
    ["0",    "Long Trip",         "Highest mean trip distance — airport or inter-borough transfers"],
    ["1, 2", "Short Trip",        "Low distance; likely artificial split of one natural group"],
    ["3",    "Medium Trip",       "Mid-range distances; no strongly differentiating secondary feature"],
    ["4",    "Weather-Impacted",  "Very high mean precipitation — rainy-day demand spike"],
    ["5",    "Peak Morning",      "Lowest mean pickup hour — morning commute segment"],
    ["6",    "High-Occupancy",    "Highest mean passenger count — group trips"],
]
cluster_table = Table(cluster_data, colWidths=[0.65 * inch, 1.55 * inch, 4.8 * inch])
cluster_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), DARK_BLUE),
    ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
    ("LEADING",       (0, 0), (-1, -1), 11),
    ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.white, LIGHT_GREY]),
    ("GRID",          (0, 0), (-1, -1), 0.4, RULE_GREY),
    ("TOPPADDING",    (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING",   (0, 0), (-1, -1), 5),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN",         (0, 0), (0, -1), "CENTER"),
]))
story.append(cluster_table)
story.append(Spacer(1, 0.06 * inch))


# ── 7. Conclusions ────────────────────────────────────────────────────────────
story.append(section_header("7.  Conclusions & Actionable Insights"))
story.append(Spacer(1, 0.04 * inch))

for b in [
    "<b>RQ1 — Tipping Behaviour:</b> XGBoost classifies high-tippers with 77 % accuracy (AUC 0.63). "
    "Tipping is driven by <b>payment method and fare economics</b> — not weather or time of day. "
    "Drivers can expect higher tips on credit-card, high-fare, or airport-rate trips.",
    "<b>RQ2 — Trip Archetypes:</b> Seven clusters reveal a service dominated by <b>short and medium city trips</b>, "
    "a strong <b>morning-commute segment</b>, minority long-distance/airport transfers, and a distinct rainy-day cluster — "
    "actionable for targeted pricing and dispatching strategies.",
    "<b>Pipeline scalability:</b> Processing 1.4+ GB within Colab's 12.7 GB RAM required aggressive memory management "
    "(GC, dtype downcasting, stratified sampling); the pipeline is transferable to cloud-scale environments.",
]:
    story.append(bullet(b))

story.append(Spacer(1, 0.06 * inch))
story.append(HRFlowable(width="100%", thickness=1, color=RULE_GREY, spaceAfter=4))
story.append(Paragraph(
    "Concordia University · COMP 333 · Team D · April 2026",
    meta_style,
))


# ── Build PDF ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_PATH,
    pagesize=letter,
    leftMargin=0.75 * inch,
    rightMargin=0.75 * inch,
    topMargin=0.65 * inch,
    bottomMargin=0.65 * inch,
    title="Executive Summary — COMP 333 Team D",
    author="Team D: Ronnie Chan, Patrice Gallant, Nesrine Larbi",
)
doc.build(story)
print(f"PDF generated: {OUTPUT_PATH}")
