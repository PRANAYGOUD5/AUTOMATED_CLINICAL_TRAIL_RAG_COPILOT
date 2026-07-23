"""
Generates a realistic synthetic clinical trial protocol PDF for
learning/testing the document processing pipeline. Not a real trial -
structured like one, so extraction/chunking code behaves realistically.
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

styles = getSampleStyleSheet()
heading_style = styles["Heading1"]
subheading_style = styles["Heading2"]
body_style = styles["Normal"]

doc = SimpleDocTemplate("data/raw/protocols/sample_protocol.pdf", pagesize=letter)
story = []

# --- Title page ---
story.append(Paragraph("Clinical Trial Protocol", styles["Title"]))
story.append(Spacer(1, 12))
story.append(Paragraph("Protocol Number: SYNTH-2026-001", body_style))
story.append(Paragraph("A Phase II Study Evaluating Drug X in Patients with Condition Y", body_style))
story.append(PageBreak())

# --- Section 1: Study Overview ---
story.append(Paragraph("1. Study Overview", heading_style))
story.append(Paragraph(
    "This is a randomized, double-blind, placebo-controlled Phase II study "
    "designed to evaluate the safety and efficacy of Drug X in adult patients "
    "diagnosed with Condition Y. The study will enroll approximately 200 "
    "participants across 15 sites.", body_style))
story.append(Spacer(1, 12))
story.append(Paragraph("1.1 Primary Objective", subheading_style))
story.append(Paragraph(
    "To assess the change in symptom severity score from baseline to Week 12 "
    "in participants receiving Drug X compared to placebo.", body_style))
story.append(PageBreak())

# --- Section 2: Inclusion Criteria ---
story.append(Paragraph("2. Inclusion Criteria", heading_style))
story.append(Paragraph(
    "Participants must meet ALL of the following criteria to be eligible "
    "for enrollment:", body_style))
inclusion_items = [
    "Age 18 to 75 years, inclusive, at the time of screening.",
    "Confirmed diagnosis of Condition Y per standard diagnostic criteria "
    "within 6 months prior to screening.",
    "Symptom severity score of at least 15 on the standardized rating scale "
    "at baseline.",
    "Willing and able to provide written informed consent.",
    "Able to comply with all study visits and procedures for the duration "
    "of the 12-week treatment period.",
]
for item in inclusion_items:
    story.append(Paragraph(f"&bull; {item}", body_style))
story.append(PageBreak())

# --- Section 3: Exclusion Criteria ---
story.append(Paragraph("3. Exclusion Criteria", heading_style))
story.append(Paragraph(
    "Participants meeting ANY of the following criteria will be excluded:", body_style))
exclusion_items = [
    "Pregnant or breastfeeding at the time of screening.",
    "History of hypersensitivity to Drug X or any of its excipients.",
    "Participation in another investigational drug trial within 30 days "
    "prior to screening.",
    "Severe hepatic impairment (Child-Pugh Class C).",
    "Estimated glomerular filtration rate (eGFR) below 30 mL/min/1.73m^2.",
    "Current diagnosis of active malignancy requiring treatment.",
]
for item in exclusion_items:
    story.append(Paragraph(f"&bull; {item}", body_style))
story.append(PageBreak())

# --- Section 4: Adverse Event Reporting ---
story.append(Paragraph("4. Adverse Event Reporting", heading_style))
story.append(Paragraph(
    "An adverse event (AE) is defined as any untoward medical occurrence "
    "in a participant administered a study drug, which does not necessarily "
    "have a causal relationship with the treatment.", body_style))
story.append(Spacer(1, 12))
story.append(Paragraph("4.1 Serious Adverse Events", subheading_style))
story.append(Paragraph(
    "A serious adverse event (SAE) is any AE that results in death, is "
    "life-threatening, requires inpatient hospitalization or prolongation "
    "of existing hospitalization, results in persistent or significant "
    "disability, or is a congenital anomaly. All SAEs must be reported to "
    "the sponsor within 24 hours of investigator awareness.", body_style))
story.append(PageBreak())

# --- Section 5: Dosing Schedule ---
story.append(Paragraph("5. Dosing Schedule", heading_style))
story.append(Paragraph(
    "Participants randomized to the active treatment arm will receive "
    "Drug X 200mg orally once daily for 12 weeks. Participants randomized "
    "to placebo will receive matching placebo tablets on the same schedule. "
    "Dose reductions to 100mg daily are permitted in the event of "
    "moderate adverse events, per Section 4 guidelines.", body_style))

doc.build(story)
print("Generated: data/raw/protocols/sample_protocol.pdf")
