"""
Generate Project Documentation PDF using ReportLab.
Format: A4, Arial (Helvetica), Justified, Page numbers bottom-right
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
import os

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

# ── Page number callback ──────────────────────────────────────────────────────
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawRightString(PAGE_W - MARGIN, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()

# ── Styles ────────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    s = {}

    s["title"] = ParagraphStyle("DocTitle",
        fontName="Helvetica-Bold", fontSize=20,
        alignment=TA_CENTER, spaceAfter=6, textColor=colors.HexColor("#1a73e8"))

    s["subtitle"] = ParagraphStyle("DocSubtitle",
        fontName="Helvetica", fontSize=13,
        alignment=TA_CENTER, spaceAfter=3, textColor=colors.HexColor("#444444"))

    s["meta"] = ParagraphStyle("Meta",
        fontName="Helvetica", fontSize=11,
        alignment=TA_CENTER, spaceAfter=2, textColor=colors.HexColor("#666666"))

    s["h1"] = ParagraphStyle("H1",
        fontName="Helvetica-Bold", fontSize=15,
        spaceBefore=14, spaceAfter=5, textColor=colors.HexColor("#1a73e8"),
        borderPad=2)

    s["h2"] = ParagraphStyle("H2",
        fontName="Helvetica-Bold", fontSize=14,
        spaceBefore=10, spaceAfter=4, textColor=colors.HexColor("#333333"))

    s["body"] = ParagraphStyle("Body",
        fontName="Helvetica", fontSize=12,
        leading=18, alignment=TA_JUSTIFY, spaceAfter=6)

    s["bullet"] = ParagraphStyle("Bullet",
        fontName="Helvetica", fontSize=12,
        leading=18, leftIndent=14, spaceAfter=3,
        bulletIndent=4)

    s["caption"] = ParagraphStyle("Caption",
        fontName="Helvetica-Oblique", fontSize=10,
        alignment=TA_CENTER, spaceAfter=8, textColor=colors.HexColor("#555555"))

    s["code"] = ParagraphStyle("Code",
        fontName="Courier", fontSize=10,
        leading=14, leftIndent=10, spaceAfter=6,
        backColor=colors.HexColor("#f5f5f5"))

    return s

# ── Helpers ───────────────────────────────────────────────────────────────────
def chart_img(path, width=160*mm, caption=None, s=None):
    items = []
    if os.path.exists(path):
        img = Image(path, width=width, height=width * 0.38)
        items.append(img)
        if caption and s:
            items.append(Paragraph(caption, s["caption"]))
    return items

def section_line():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#dddddd"), spaceAfter=6)

# ── Build ─────────────────────────────────────────────────────────────────────
def build_pdf(output_path="outputs/Project_Documentation.pdf"):
    os.makedirs("outputs", exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=20 * mm,
    )
    s = build_styles()
    story = []

    # ── PAGE 1: TITLE PAGE ────────────────────────────────────────────────────
    story.append(Spacer(1, 30 * mm))
    story.append(Paragraph("Google Stock Market", s["title"]))
    story.append(Paragraph("Data Engineering Pipeline", s["title"]))
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="60%", thickness=2,
                             color=colors.HexColor("#1a73e8"),
                             hAlign="CENTER", spaceAfter=8))
    story.append(Paragraph("Capstone Project — Data Analytics — Data Engineering Capstone", s["subtitle"]))
    story.append(Spacer(1, 20 * mm))

    meta_data = [
        ["Name", "Srijita Mandal"],
        ["Roll Number", "23053373"],
        ["Batch / Program", "Data Engineering (B.Tech CSE, 3rd Year)"],
        ["Submission Date", "April 21, 2026"],
    ]
    meta_table = Table(meta_data, colWidths=[55*mm, 100*mm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME",    (0,0), (-1,-1), "Helvetica"),
        ("FONTNAME",    (0,0), (0,-1),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 12),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("TOPPADDING",  (0,0), (-1,-1), 7),
        ("TEXTCOLOR",   (0,0), (0,-1),  colors.HexColor("#444444")),
        ("LINEBELOW",   (0,0), (-1,-2), 0.4, colors.HexColor("#dddddd")),
    ]))
    story.append(meta_table)
    story.append(PageBreak())

    # ── PAGE 2: PROBLEM STATEMENT + SOLUTION ─────────────────────────────────
    story.append(Paragraph("1. Problem Statement", s["h1"]))
    story.append(section_line())
    story.append(Paragraph(
        "In modern financial markets, vast amounts of stock data are generated every trading day. "
        "Without a structured data pipeline, this raw data remains difficult to analyze, compare, "
        "or use for decision-making. Manual analysis is time-consuming, error-prone, and not "
        "scalable. There is a clear need for an automated, end-to-end pipeline that can ingest, "
        "clean, transform, store, and visualize stock market data efficiently.",
        s["body"]))
    story.append(Paragraph(
        "This project focuses on Google (GOOGL) stock data — one of the most actively traded "
        "technology stocks — and aims to build a robust data engineering solution that transforms "
        "raw OHLCV (Open, High, Low, Close, Volume) data into actionable financial insights.",
        s["body"]))

    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("2. Solution & Features", s["h1"]))
    story.append(section_line())
    story.append(Paragraph(
        "The project implements a four-stage data pipeline entirely in Python, covering all core "
        "data engineering disciplines — ingestion, transformation, storage, and analysis.",
        s["body"]))

    features = [
        ("Data Ingestion", "Fetches 2 years of GOOGL OHLCV data (503 trading days) and saves it as a structured CSV file."),
        ("Data Transformation", "Cleans raw data and engineers 5 analytical features: 7-day MA, 30-day MA, Daily Return %, 7-day Volatility, and Price Range."),
        ("Data Storage", "Persists the processed dataset into a SQLite relational database and exports summary statistics."),
        ("Analysis & Visualization", "Generates 5 publication-quality charts covering price trends, volume, returns, distribution, and volatility."),
        ("Automation", "A single main.py script orchestrates all pipeline stages end-to-end."),
    ]
    for feat, desc in features:
        story.append(Paragraph(f"<b>• {feat}:</b> {desc}", s["bullet"]))
    story.append(PageBreak())

    # ── PAGE 3: SCREENSHOTS ───────────────────────────────────────────────────
    story.append(Paragraph("3. Screenshots & Output Charts", s["h1"]))
    story.append(section_line())

    charts = [
        ("outputs/chart1_price_ma.png",
         "Figure 1: GOOGL Close Price with 7-Day and 30-Day Moving Averages"),
        ("outputs/chart2_volume.png",
         "Figure 2: Daily Trading Volume (in Millions)"),
        ("outputs/chart3_daily_returns.png",
         "Figure 3: Daily Return % — Green = Gain, Red = Loss"),
    ]
    for path, cap in charts:
        story.extend(chart_img(path, caption=cap, s=s))
        story.append(Spacer(1, 3 * mm))

    story.append(PageBreak())

    # ── PAGE 4: MORE CHARTS + TECH STACK ─────────────────────────────────────
    story.append(Paragraph("3. Screenshots (continued)", s["h1"]))
    story.append(section_line())
    story.extend(chart_img("outputs/chart4_return_distribution.png",
                            caption="Figure 4: Distribution of Daily Returns with KDE Curve", s=s))
    story.append(Spacer(1, 3 * mm))
    story.extend(chart_img("outputs/chart5_volatility.png",
                            caption="Figure 5: 7-Day Rolling Volatility Over Time", s=s))

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("4. Tech Stack", s["h1"]))
    story.append(section_line())

    tech_data = [
        ["Technology", "Purpose", "Version"],
        ["Python 3.x",   "Core programming language",            "3.12"],
        ["pandas",       "Data manipulation & transformation",   "2.x"],
        ["NumPy",        "Numerical simulation & computation",   "1.x"],
        ["yfinance",     "Stock data ingestion (API wrapper)",   "1.3.0"],
        ["SQLite3",      "Relational database storage",          "Built-in"],
        ["matplotlib",   "Chart generation & visualization",     "3.x"],
        ["seaborn",      "Statistical visualization styling",    "0.13.x"],
    ]
    tech_table = Table(tech_data, colWidths=[55*mm, 90*mm, 30*mm])
    tech_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#1a73e8")),
        ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME",    (0,1), (-1,-1),"Helvetica"),
        ("FONTSIZE",    (0,0), (-1,-1), 11),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f8f9fa"), colors.white]),
        ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(tech_table)
    story.append(PageBreak())

    # ── PAGE 5: UNIQUE POINTS + FUTURE ───────────────────────────────────────
    story.append(Paragraph("5. Unique Points", s["h1"]))
    story.append(section_line())
    unique = [
        "End-to-end pipeline in pure Python with zero cloud dependency — runs locally on any machine.",
        "Engineered 5 domain-specific financial features (moving averages, return %, volatility) beyond raw OHLCV data.",
        "Dual storage strategy: CSV files for portability and SQLite database for structured querying.",
        "5 distinct chart types covering trend, volume, momentum, distribution, and risk — comprehensive market view.",
        "Modular design — each pipeline stage is an independent script, making the system easy to extend or swap components.",
        "Single-command execution via main.py — entire pipeline from raw data to charts in one run.",
    ]
    for pt in unique:
        story.append(Paragraph(f"• {pt}", s["bullet"]))

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("6. Future Improvements", s["h1"]))
    story.append(section_line())
    future = [
        "Live Data Integration: Connect to Yahoo Finance or Alpha Vantage APIs for real-time GOOGL data ingestion.",
        "Multi-Stock Support: Extend the pipeline to compare GOOGL against AAPL, MSFT, AMZN — sector analysis.",
        "Automated Scheduling: Use Apache Airflow or cron jobs to run the pipeline daily at market close.",
        "Machine Learning Layer: Build a price prediction model (LSTM or XGBoost) using the engineered features.",
        "Interactive Dashboard: Deploy a Streamlit or Dash web dashboard for live chart exploration.",
        "Cloud Storage: Replace SQLite with AWS S3 + Athena or Google BigQuery for scalable data warehousing.",
        "Alerting System: Email or Slack notifications when volatility exceeds a threshold or price drops sharply.",
    ]
    for pt in future:
        story.append(Paragraph(f"• {pt}", s["bullet"]))

    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor("#dddddd"), spaceAfter=4))
    story.append(Paragraph(
        "This project demonstrates a complete, production-style data engineering pipeline — "
        "from raw financial data to cleaned, stored, and visualized insights.",
        s["body"]))

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"[SUCCESS] PDF saved to '{output_path}'")

if __name__ == "__main__":
    build_pdf()
