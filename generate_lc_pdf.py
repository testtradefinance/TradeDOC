#!/usr/bin/env python3
"""
Generate a realistic Letter of Credit PDF matching the sample_trade_documents.pdf transaction.
2-page SWIFT MT700 style documentary credit.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas
import os

OUTPUT = r"E:\Apps\Claude\Code\letter_of_credit.pdf"
W, H = letter

NAVY = HexColor("#1a2744")
DARK_BLUE = HexColor("#1e3a5f")
MED_BLUE = HexColor("#2563eb")
LIGHT_BLUE = HexColor("#e8f0fe")
LIGHT_GRAY = HexColor("#f3f4f6")
MED_GRAY = HexColor("#6b7280")
DARK_GRAY = HexColor("#374151")
BORDER_GRAY = HexColor("#d1d5db")
GREEN = HexColor("#059669")
GOLD = HexColor("#b8860b")
CITI_BLUE = HexColor("#003B70")

def draw_box(c, x, y, w, h, fill=None):
    if fill:
        c.setFillColor(fill)
        c.roundRect(x, y, w, h, 4, fill=1, stroke=0)
    c.setStrokeColor(BORDER_GRAY)
    c.setLineWidth(0.5)
    c.roundRect(x, y, w, h, 4, fill=0, stroke=1)

def draw_separator(c, y):
    c.setStrokeColor(BORDER_GRAY)
    c.setLineWidth(0.5)
    c.line(50, y, W - 50, y)

def draw_field_row(c, y, label, value, label_x=55, value_x=200, bold_val=False):
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(label_x, y, label)
    c.setFont("Helvetica-Bold" if bold_val else "Helvetica", 8)
    c.setFillColor(black)
    c.drawString(value_x, y, str(value))

def draw_signature_line(c, x, y, name, title_text):
    c.setStrokeColor(DARK_GRAY)
    c.setLineWidth(0.8)
    c.line(x, y, x + 180, y)
    c.setFont("Courier-Oblique", 11)
    c.setFillColor(DARK_BLUE)
    c.drawString(x + 30, y + 8, name.split()[0][0] + ". " + name.split()[-1])
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(black)
    c.drawString(x, y - 12, name)
    c.setFont("Helvetica", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(x, y - 22, title_text)

def draw_stamp(c, x, y, lines, color=DARK_BLUE):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(2)
    c.circle(x, y, 35, fill=0, stroke=1)
    c.circle(x, y, 30, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 6)
    c.setFillColor(color)
    for i, line in enumerate(lines):
        c.drawCentredString(x, y + 10 - (i * 9), line)
    c.restoreState()


def page1(c):
    """Page 1: LC Header, Parties, Terms, Commodity Details"""
    # Citibank header
    c.setFillColor(CITI_BLUE)
    c.rect(0, H - 90, W, 90, fill=1, stroke=0)
    # White arc accent
    c.setFillColor(HexColor("#ef3e23"))
    c.rect(0, H - 92, W, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, H - 45, "Citibank")
    c.setFont("Helvetica", 9)
    c.drawString(50, H - 62, "Citibank N.A. | Trade Finance Division")
    c.drawRightString(W - 50, H - 40, "388 Greenwich Street")
    c.drawRightString(W - 50, H - 53, "New York, NY 10013, USA")
    c.drawRightString(W - 50, H - 66, "SWIFT: CITIUS33XXX")
    c.drawRightString(W - 50, H - 79, "Tel: +1 (212) 559-1000")

    y = H - 115
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(NAVY)
    c.drawCentredString(W / 2, y, "IRREVOCABLE DOCUMENTARY LETTER OF CREDIT")
    y -= 18
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawCentredString(W / 2, y, "Issued pursuant to ICC Uniform Customs and Practice for Documentary Credits (UCP 600)")

    # LC Number bar
    y -= 25
    c.setFillColor(HexColor("#fef3c7"))
    c.rect(45, y - 15, W - 90, 22, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y - 8, "L/C Number: LC-2025-00847")
    c.drawCentredString(W / 2, y - 8, "Form: IRREVOCABLE")
    c.drawRightString(W - 55, y - 8, "SWIFT MT700")

    # Key dates row
    y -= 30
    draw_box(c, 45, y - 25, (W - 100) / 3, 28, fill=LIGHT_BLUE)
    draw_box(c, 45 + (W - 100) / 3 + 5, y - 25, (W - 100) / 3, 28, fill=LIGHT_BLUE)
    draw_box(c, 45 + 2 * ((W - 100) / 3 + 5), y - 25, (W - 100) / 3, 28, fill=LIGHT_BLUE)

    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(55, y - 5, "DATE OF ISSUE")
    c.drawString(55 + (W - 100) / 3 + 5 + 10, y - 5, "EXPIRY DATE")
    c.drawString(55 + 2 * ((W - 100) / 3 + 5) + 10, y - 5, "PLACE OF EXPIRY")
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(black)
    c.drawString(55, y - 18, "20 February 2025")
    c.drawString(55 + (W - 100) / 3 + 5 + 10, y - 18, "Expiry Date: 20/05/2025")
    c.drawString(55 + 2 * ((W - 100) / 3 + 5) + 10, y - 18, "Hong Kong")

    # Parties section
    y -= 45
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawString(50, y, "PARTIES TO THIS DOCUMENTARY CREDIT")
    y -= 5
    draw_separator(c, y)

    # Issuing Bank / Advising Bank
    y -= 20
    col_w = (W - 110) / 2
    draw_box(c, 45, y - 55, col_w, 58)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(55, y - 5, "ISSUING BANK (Field 52a)")
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(black)
    c.drawString(55, y - 18, "Issuing Bank: Citibank N.A., New York")
    c.setFont("Helvetica", 7)
    c.drawString(55, y - 30, "388 Greenwich Street, New York, NY 10013")
    c.drawString(55, y - 42, "SWIFT: CITIUS33XXX")

    draw_box(c, W / 2 + 10, y - 55, col_w, 58)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(W / 2 + 20, y - 5, "ADVISING BANK (Field 57a)")
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(black)
    c.drawString(W / 2 + 20, y - 18, "Advising Bank: HSBC Hong Kong")
    c.setFont("Helvetica", 7)
    c.drawString(W / 2 + 20, y - 30, "1 Queen's Road Central, Hong Kong")
    c.drawString(W / 2 + 20, y - 42, "SWIFT: HSBCHKHHHKH")

    # Applicant / Beneficiary
    y -= 70
    draw_box(c, 45, y - 55, col_w, 58)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(55, y - 5, "APPLICANT (Field 50)")
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(black)
    c.drawString(55, y - 18, "Applicant: Atlantic Commerce Inc.")
    c.setFont("Helvetica", 7)
    c.drawString(55, y - 30, "250 Park Avenue, New York, NY 10177, USA")
    c.drawString(55, y - 42, "Tax ID: US-EIN 13-9876543")

    draw_box(c, W / 2 + 10, y - 55, col_w, 58)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(W / 2 + 20, y - 5, "BENEFICIARY (Field 59)")
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(black)
    c.drawString(W / 2 + 20, y - 18, "Beneficiary: Golden Dragon Trading Co. Ltd.")
    c.setFont("Helvetica", 7)
    c.drawString(W / 2 + 20, y - 30, "88 Harbour Road, Wan Chai, Hong Kong")
    c.drawString(W / 2 + 20, y - 42, "EORI: HK8801234567")

    # Amount section
    y -= 75
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawString(50, y, "CREDIT DETAILS")
    y -= 5
    draw_separator(c, y)

    y -= 15
    draw_box(c, 45, y - 45, W - 90, 48, fill=LIGHT_GRAY)
    draw_field_row(c, y - 8, "Credit Amount (Field 32B):", "Credit Amount: USD 850,000.00", bold_val=True)
    draw_field_row(c, y - 22, "Amount in Words:", "United States Dollars Eight Hundred and Fifty Thousand Only")
    draw_field_row(c, y - 36, "Currency Code:", "USD (United States Dollar)")

    # Terms
    y -= 60
    draw_field_row(c, y, "Available With (Field 41a):", "Any bank by negotiation")
    y -= 14
    draw_field_row(c, y, "Drafts At (Field 42C):", "At 90 days after sight")
    y -= 14
    draw_field_row(c, y, "Drawee (Field 42a):", "Citibank N.A., New York (CITIUS33XXX)")
    y -= 14
    draw_field_row(c, y, "Partial Shipments (Field 43P):", "Not Allowed")
    y -= 14
    draw_field_row(c, y, "Transshipment (Field 43T):", "Not Allowed")

    # Commodity details
    y -= 25
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawString(50, y, "GOODS DESCRIPTION (Field 45A)")
    y -= 5
    draw_separator(c, y)

    y -= 15
    draw_box(c, 45, y - 80, W - 90, 83)
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    goods = [
        "Green Arabica Coffee Beans, Grade AA, Origin: Ethiopia",
        "HS Code: 0901.11",
        "Quantity: 200 Metric Tons (MT) packed in 8,000 jute bags of 25 KG each",
        "Unit Price: USD 4,250.00 per MT",
        "Total Value: USD 850,000.00",
        "Trade Terms: CIF New York (Incoterms 2020)",
    ]
    dy = y - 10
    for line in goods:
        c.drawString(55, dy, line)
        dy -= 12

    # Page number
    c.setFont("Helvetica", 7)
    c.setFillColor(MED_GRAY)
    c.drawCentredString(W / 2, 25, "Page 1 of 2")
    c.drawRightString(W - 50, 25, "L/C Number: LC-2025-00847")
    c.drawString(50, 25, "CONFIDENTIAL")


def page2(c):
    """Page 2: Shipment Details, Documents Required, Conditions, Signatures"""
    # Continuation header
    c.setFillColor(CITI_BLUE)
    c.rect(0, H - 50, W, 50, fill=1, stroke=0)
    c.setFillColor(HexColor("#ef3e23"))
    c.rect(0, H - 52, W, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, H - 35, "IRREVOCABLE DOCUMENTARY LETTER OF CREDIT (Continued)")
    c.setFont("Helvetica", 8)
    c.drawRightString(W - 50, H - 30, "L/C Number: LC-2025-00847")
    c.drawRightString(W - 50, H - 42, "Citibank N.A., New York")

    y = H - 75
    # Shipment details
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawString(50, y, "SHIPMENT DETAILS")
    y -= 5
    draw_separator(c, y)

    y -= 15
    draw_field_row(c, y, "Port of Loading (Field 44E):", "Hong Kong")
    y -= 14
    draw_field_row(c, y, "Port of Discharge (Field 44F):", "Port of New York/New Jersey")
    y -= 14
    draw_field_row(c, y, "Latest Shipment (Field 44C):", "15 April 2025")
    y -= 14
    draw_field_row(c, y, "Vessel:", "MV Pacific Star, Voyage PS-2025-031")
    y -= 14
    draw_field_row(c, y, "Shipment Period:", "Within 45 days from date of issue of this credit")

    # Documents required
    y -= 25
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawString(50, y, "DOCUMENTS REQUIRED (Field 46A)")
    y -= 5
    draw_separator(c, y)

    y -= 12
    docs_required = [
        "1. Signed Commercial Invoice in 3 originals and 2 copies, showing LC number,",
        "   goods description, quantity, unit price, and total amount.",
        "2. Full set (3/3) original clean on board ocean Bills of Lading, made out to",
        "   the order of Citibank N.A., New York, marked \"Freight Prepaid\", notify",
        "   applicant, showing port of loading and port of discharge as stipulated.",
        "3. Insurance Certificate/Policy in negotiable form for 110% of CIF value,",
        "   covering Institute Cargo Clauses (A), Institute War Clauses, and Institute",
        "   Strikes Clauses, claims payable in USD at destination.",
        "4. Certificate of Origin issued by Hong Kong General Chamber of Commerce,",
        "   certifying goods are of Ethiopian origin.",
        "5. Packing List in 3 originals showing net weight, gross weight, package",
        "   details, and container numbers.",
        "6. Beneficiary Certificate certifying that goods have been shipped in",
        "   accordance with the terms of this letter of credit.",
        "7. Inspection Certificate issued by SGS Hong Kong confirming quality and",
        "   quantity of goods conform to Grade AA specifications.",
        "8. Bill of Exchange drawn on Citibank N.A., at 90 days sight for 100%",
        "   of invoice value.",
    ]
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    for line in docs_required:
        c.drawString(55, y, line)
        y -= 10

    # Additional conditions
    y -= 10
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawString(50, y, "ADDITIONAL CONDITIONS (Field 47A)")
    y -= 5
    draw_separator(c, y)

    y -= 12
    conditions = [
        "1. All documents must be presented within 21 days after the date of shipment.",
        "2. All banking charges outside the USA are for account of the beneficiary.",
        "3. Documents to be presented to the advising bank for negotiation.",
        "4. This credit is subject to the Uniform Customs and Practice for Documentary",
        "   Credits, 2007 Revision, ICC Publication No. 600 (UCP 600).",
        "5. The issuing bank undertakes to honor drafts drawn and presented in conformity",
        "   with the terms and conditions of this documentary credit.",
        "6. Reimbursement instructions as per SWIFT MT740.",
    ]
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    for line in conditions:
        c.drawString(55, y, line)
        y -= 10

    # Confirmation block
    y -= 15
    draw_box(c, 45, y - 40, W - 90, 43, fill=HexColor("#ecfdf5"))
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(GREEN)
    c.drawString(55, y - 8, "CONFIRMATION STATUS")
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(55, y - 22, "This credit has been confirmed by the Advising Bank (HSBC Hong Kong) as per Field 49.")
    c.drawString(55, y - 33, "The confirming bank adds its confirmation and undertakes to honor or negotiate compliant presentations.")

    # Signatures
    y -= 65
    draw_signature_line(c, 50, y, "Robert J. Mitchell", "VP, Trade Finance Operations")
    draw_signature_line(c, 350, y, "Sarah K. Williams", "Authorized Signatory")
    draw_stamp(c, W / 2, y + 20, ["CITIBANK N.A.", "NEW YORK", "TRADE FINANCE", "AUTHORIZED"])

    # Footer
    y -= 45
    c.setFont("Helvetica", 6)
    c.setFillColor(MED_GRAY)
    c.drawString(50, y, "This letter of credit is issued subject to the Uniform Customs and Practice for Documentary Credits (UCP 600),")
    c.drawString(50, y - 9, "International Chamber of Commerce Publication No. 600. Citibank N.A. is a member of the Citigroup family of companies.")
    c.drawString(50, y - 18, "SWIFT Reference: MT700-2025022000847  |  Internal Ref: TF/LC/NY/2025/00847  |  Issuing Date: 20 February 2025")

    # Page number
    c.setFont("Helvetica", 7)
    c.setFillColor(MED_GRAY)
    c.drawCentredString(W / 2, 25, "Page 2 of 2")
    c.drawRightString(W - 50, 25, "L/C Number: LC-2025-00847")
    c.drawString(50, 25, "CONFIDENTIAL")


def main():
    c = canvas.Canvas(OUTPUT, pagesize=letter)
    c.setTitle("Irrevocable Documentary Letter of Credit - LC-2025-00847")
    c.setAuthor("Citibank N.A., New York")
    c.setSubject("Documentary Letter of Credit")

    page1(c)
    c.showPage()
    page2(c)
    c.showPage()

    c.save()
    size = os.path.getsize(OUTPUT)
    print(f"Letter of Credit PDF created: {OUTPUT}")
    print(f"Size: {size / 1024:.1f} KB, Pages: 2")

if __name__ == "__main__":
    main()
