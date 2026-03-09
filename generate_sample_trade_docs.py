#!/usr/bin/env python3
"""
Generate a 10-page trade finance sample PDF with content that triggers:
- Dual-use goods red flag (HS 9013, thermal imaging, encryption, carbon fiber)
- Round-tripping red flag (Atlantic Commerce appears as both buyer AND seller)
- Shell company red flag (Phoenix Trading 888 Ltd, Golden Ventures Ltd, Diamond Holdings Ltd)
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas
import os

OUTPUT = r"E:\Apps\Claude\Code\sample_trade_documents.pdf"
W, H = letter

NAVY = HexColor("#1a2744")
DARK_BLUE = HexColor("#1e3a5f")
LIGHT_BLUE = HexColor("#e8f0fe")
LIGHT_GRAY = HexColor("#f3f4f6")
MED_GRAY = HexColor("#6b7280")
DARK_GRAY = HexColor("#374151")
BORDER_GRAY = HexColor("#d1d5db")
GREEN = HexColor("#059669")
RED = HexColor("#dc2626")
GOLD = HexColor("#b8860b")

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

def draw_page_num(c, n):
    c.setFont("Helvetica", 7)
    c.setFillColor(MED_GRAY)
    c.drawCentredString(W / 2, 25, f"Page {n} of 10")
    c.drawRightString(W - 50, 25, "Ref: LC-2025-00847")


# ============================================================
# PAGE 1: COVER LETTER (with Diamond Holdings Ltd)
# ============================================================
def page1(c):
    c.setFillColor(HexColor("#db0011"))
    c.rect(0, H - 80, W, 80, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, H - 50, "HSBC")
    c.setFont("Helvetica", 9)
    c.drawString(50, H - 65, "The Hongkong and Shanghai Banking Corporation Limited")
    c.drawRightString(W - 50, H - 45, "Trade Finance Department")
    c.drawRightString(W - 50, H - 58, "1 Queen's Road Central, Hong Kong")
    c.drawRightString(W - 50, H - 70, "SWIFT: HSBCHKHHHKH")

    y = H - 110
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(NAVY)
    c.drawString(50, y, "DOCUMENTARY COLLECTION - COVERING SCHEDULE")
    y -= 25
    draw_separator(c, y)

    y -= 25
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(black)
    c.drawString(50, y, "Our Ref: HSBC/TF/DC-2025-03847")
    c.drawRightString(W - 50, y, "Date: 20 February 2025")
    y -= 18
    c.drawString(50, y, "Your Ref: LC-2025-00847")

    # TO section
    y -= 35
    draw_box(c, 45, y - 55, W - 90, 75, fill=LIGHT_BLUE)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y + 8, "TO:")
    c.setFont("Helvetica", 9)
    c.setFillColor(black)
    c.drawString(80, y + 8, "Citibank N.A., New York")
    c.drawString(80, y - 5, "388 Greenwich Street, New York, NY 10013, USA")
    c.drawString(80, y - 18, "SWIFT: CITIUS33XXX")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(55, y - 35, "Attention: Trade Finance Operations / Documentary Collections")

    y -= 80
    c.setFont("Helvetica", 9)
    c.setFillColor(black)
    lines = [
        "Dear Sir/Madam,",
        "",
        "We are instructed by our client, Golden Dragon Trading Co. Ltd. (the \"Principal\"), to forward",
        "the following documents for collection in accordance with ICC Uniform Rules for Collections",
        "(URC 522). Please handle the documents as per the instructions below.",
    ]
    for line in lines:
        c.drawString(50, y, line)
        y -= 13

    y -= 5
    draw_box(c, 45, y - 160, W - 90, 168, fill=LIGHT_GRAY)
    details = [
        ("Principal (Drawer):", "Golden Dragon Trading Co. Ltd., 88 Harbour Road, Wan Chai, Hong Kong"),
        ("Drawee:", "Atlantic Commerce Inc., 250 Park Avenue, New York, NY 10177, USA"),
        ("Amount:", "USD 910,000.00"),
        ("Tenor:", "90 days after sight"),
        ("Collection Type:", "Documents Against Acceptance (D/A)"),
        ("Commodity:", "Green Arabica Coffee Beans, Grade AA + Laser Equipment"),
        ("HS Codes:", "0901.11, 9013.80"),
        ("Forwarding Agent:", "Diamond Holdings Ltd, Suite 3309, Central Tower, Hong Kong"),
    ]
    dy = y + 2
    for label, val in details:
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(DARK_GRAY)
        c.drawString(55, dy, label)
        c.setFont("Helvetica", 8)
        c.setFillColor(black)
        c.drawString(200, dy, val)
        dy -= 20

    y -= 178
    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "DOCUMENTS ENCLOSED:")
    y -= 15
    docs = [
        "1. Bill of Exchange (Original) - 1 original",
        "2. Bill of Lading (Full set 3/3) - 3 originals",
        "3. Commercial Invoice - 3 originals + 2 copies",
        "4. Certificate of Origin - 1 original + 1 copy",
        "5. Packing List - 3 originals",
        "6. Insurance Certificate - 1 original",
        "7. Beneficiary Certificate - 1 original",
        "8. Inspection Certificate (SGS) - 1 original + 1 copy",
    ]
    c.setFont("Helvetica", 8)
    for d in docs:
        c.drawString(65, y, d)
        y -= 12

    y -= 15
    c.setFont("Helvetica", 8)
    c.drawString(50, y, "SPECIAL INSTRUCTIONS: Upon acceptance, release documents to drawee.")
    y -= 12
    c.drawString(50, y, "Protest for non-acceptance and non-payment. Charges outside HK for account of drawee.")

    y -= 25
    draw_signature_line(c, 50, y, "James W. Chen", "Senior Manager, Trade Finance")
    draw_stamp(c, W - 120, y + 5, ["HSBC", "TRADE FINANCE", "HONG KONG", "VERIFIED"])
    draw_page_num(c, 1)


# ============================================================
# PAGE 2: BILL OF EXCHANGE
# ============================================================
def page2(c):
    c.setStrokeColor(NAVY)
    c.setLineWidth(3)
    c.rect(30, 30, W - 60, H - 60, fill=0, stroke=1)
    c.setLineWidth(1)
    c.rect(35, 35, W - 70, H - 70, fill=0, stroke=1)

    y = H - 70
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(NAVY)
    c.drawCentredString(W / 2, y, "BILL OF EXCHANGE")
    y -= 20
    c.setFont("Helvetica", 10)
    c.setFillColor(DARK_GRAY)
    c.drawCentredString(W / 2, y, "(First of Exchange - Second Unpaid)")
    y -= 30
    draw_separator(c, y)

    y -= 25
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(black)
    c.drawString(50, y, "No.: BOE/GD/2025/0220")
    c.drawRightString(W - 50, y, "Date: 20 February 2025")
    y -= 18
    c.drawString(50, y, "Amount: USD 910,000.00")
    c.drawRightString(W - 50, y, "Place: Hong Kong")

    y -= 35
    draw_box(c, 45, y - 185, W - 90, 200, fill=HexColor("#fefce8"))
    ty = y - 5
    c.setFont("Helvetica", 10)
    c.setFillColor(black)
    lines = [
        "At NINETY (90) DAYS after sight of this FIRST Bill of Exchange",
        "(Second of the same tenor and date being unpaid),",
        "",
        "Pay to the order of The Hongkong and Shanghai Banking Corporation Limited",
        "",
        "the sum of UNITED STATES DOLLARS NINE HUNDRED AND",
        "TEN THOUSAND ONLY (USD 910,000.00)",
        "",
        "Value received as per our Invoice No. INV-GD-2025-0220",
        "dated 20 February 2025.",
        "",
        "Drawn under LC-2025-00847",
        "issued by Citibank N.A., New York.",
        "Tenor: 90 days after sight",
    ]
    for line in lines:
        c.drawString(60, ty, line)
        ty -= 14

    y -= 215
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawString(50, y, "TO (DRAWEE):")
    y -= 15
    c.setFont("Helvetica", 9)
    c.setFillColor(black)
    c.drawString(50, y, "Citibank N.A., New York")
    y -= 13
    c.drawString(50, y, "388 Greenwich Street, New York, NY 10013, USA")

    y -= 40
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawString(50, y, "DRAWN BY:")
    draw_signature_line(c, 350, y - 10, "Li Wei Ming", "Managing Director")
    y -= 35
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(350, y, "Golden Dragon Trading Co. Ltd.")
    y -= 12
    c.drawString(350, y, "88 Harbour Road, Wan Chai, Hong Kong")
    draw_stamp(c, 130, y + 15, ["GOLDEN DRAGON", "TRADING CO.", "HONG KONG", "CHOP"])

    y -= 50
    draw_box(c, 45, y - 70, W - 90, 80)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawString(55, y, "ACCEPTANCE")
    c.setFont("Helvetica", 8)
    c.setFillColor(MED_GRAY)
    c.drawString(55, y - 15, "Accepted on: ___________________     Due Date: ___________________")
    c.drawString(55, y - 45, "Authorized Signature: ________________________________     Stamp: ________________")
    c.drawString(55, y - 58, "For and on behalf of Citibank N.A., New York")
    draw_page_num(c, 2)


# ============================================================
# PAGE 3: BILL OF LADING (with Golden Ventures Ltd)
# ============================================================
def page3(c):
    c.setFillColor(DARK_BLUE)
    c.rect(0, H - 90, W, 90, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, H - 45, "BILL OF LADING")
    c.setFont("Helvetica", 9)
    c.drawString(50, H - 62, "FOR COMBINED TRANSPORT OR PORT TO PORT SHIPMENT")
    c.drawRightString(W - 50, H - 40, "Pacific Star Shipping Lines")
    c.drawRightString(W - 50, H - 55, "Marine Tower, Tsim Sha Tsui, Hong Kong")
    c.drawRightString(W - 50, H - 68, "SCAC: PSSL")

    y = H - 110
    c.setFillColor(HexColor("#fef3c7"))
    c.rect(45, y - 15, W - 90, 22, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y - 8, "B/L No: HKHK-NY-20250220-001")
    c.drawRightString(W - 55, y - 8, "ORIGINAL   1/3")

    y -= 30
    col1 = 50
    col2 = W / 2 + 10
    bw = (W - 110) / 2

    # Shipper
    draw_box(c, col1 - 5, y - 52, bw, 55)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(col1, y - 2, "SHIPPER / EXPORTER")
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(col1, y - 16, "Golden Dragon Trading Co. Ltd.")
    c.drawString(col1, y - 28, "88 Harbour Road, Wan Chai, Hong Kong")
    c.drawString(col1, y - 40, "Tel: +852 2845 1234")

    # Consignee
    draw_box(c, col2 - 5, y - 52, bw, 55)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(col2, y - 2, "CONSIGNED TO THE ORDER OF")
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(black)
    c.drawString(col2, y - 16, "Citibank N.A., New York")
    c.setFont("Helvetica", 8)
    c.drawString(col2, y - 28, "388 Greenwich Street, New York, NY 10013")
    c.drawString(col2, y - 40, "SWIFT: CITIUS33XXX")

    y -= 65
    # Notify + Also Notify (Golden Ventures Ltd - SHELL COMPANY)
    draw_box(c, col1 - 5, y - 65, bw, 68)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(col1, y - 2, "NOTIFY PARTY")
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(col1, y - 16, "Atlantic Commerce Inc.")
    c.drawString(col1, y - 28, "250 Park Avenue, New York, NY 10177, USA")
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(col1, y - 44, "ALSO NOTIFY:")
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(col1, y - 56, "Golden Ventures Ltd, Room 808, Tsim Sha Tsui, HK")

    # Vessel
    draw_box(c, col2 - 5, y - 65, bw, 68)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(col2, y - 2, "VESSEL / VOYAGE")
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(black)
    c.drawString(col2, y - 16, "MV Pacific Star  /  PS-2025-031")
    c.setFont("Helvetica", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(col2, y - 30, "FLAG: Panama     CLASS: Lloyd's Register")
    c.drawString(col2, y - 42, "IMO: 9876543")

    y -= 78
    # Ports
    draw_box(c, col1 - 5, y - 25, bw, 28)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(col1, y - 2, "PORT OF LOADING")
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(black)
    c.drawString(col1, y - 16, "Hong Kong")

    draw_box(c, col2 - 5, y - 25, bw, 28)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(col2, y - 2, "PORT OF DISCHARGE")
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(black)
    c.drawString(col2, y - 16, "Port of New York/New Jersey")

    y -= 40
    # Cargo
    draw_box(c, col1 - 5, y - 115, W - 90, 118)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(col1, y - 2, "PARTICULARS OF GOODS (said to contain)")

    y -= 18
    c.setFillColor(LIGHT_BLUE)
    c.rect(col1 - 3, y - 4, W - 96, 16, fill=1, stroke=0)
    hdrs = ["Container No.", "Marks", "Description", "Packages", "Gross Wt (KG)"]
    xps = [52, 142, 252, 392, 492]
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(DARK_BLUE)
    for h, xp in zip(hdrs, xps):
        c.drawString(xp, y, h)

    y -= 18
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    rows = [
        ("PSSL-U2001234", "GD/AC/001-004", "Green Arabica Coffee", "4,000 bags", "102,000"),
        ("PSSL-U2001238", "GD/AC/005-008", "Beans, Grade AA", "4,000 bags", "102,000"),
        ("PSSL-U2001242", "GD/AC/009", "Laser Equipment", "5 PCS", "750"),
        ("", "", "HS: 0901.11 / 9013.80", "", ""),
    ]
    for row in rows:
        for v, xp in zip(row, xps):
            c.drawString(xp, y, v)
        y -= 12

    y -= 5
    c.setFont("Helvetica-Bold", 7)
    c.drawString(col1, y, "TOTAL: 9 containers | 8,000 bags + 5 PCS | Gross: 204,750 KG | Net: 200,000 KG + 650 KG")

    y -= 20
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(GREEN)
    c.drawString(col1, y, "SHIPPED ON BOARD")
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(170, y, "Date: 20 February 2025  |  CLEAN ON BOARD  |  FREIGHT PREPAID")

    y -= 35
    draw_signature_line(c, 50, y, "Capt. K. Nakamura", "Master, MV Pacific Star")
    draw_signature_line(c, 350, y, "R. Wong", "Agent, Pacific Star Shipping")
    draw_stamp(c, W / 2, y + 25, ["PACIFIC STAR", "SHIPPING LINES", "SHIPPED ON", "BOARD"])
    draw_page_num(c, 3)


# ============================================================
# PAGE 4: COMMERCIAL INVOICE (with dual-use 2nd line item)
# ============================================================
def page4(c):
    c.setFillColor(NAVY)
    c.rect(0, H - 80, W, 80, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, H - 42, "COMMERCIAL INVOICE")
    c.setFont("Helvetica", 9)
    c.drawString(50, H - 58, "Golden Dragon Trading Co. Ltd.")
    c.drawRightString(W - 50, H - 42, "GOLDEN DRAGON")
    c.drawRightString(W - 50, H - 58, "88 Harbour Road, Wan Chai, Hong Kong")

    y = H - 100
    c.setFillColor(LIGHT_BLUE)
    c.rect(45, y - 15, W - 90, 20, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y - 10, "Invoice No: INV-GD-2025-0220")
    c.drawCentredString(W / 2, y - 10, "Date: 20 February 2025")
    c.drawRightString(W - 55, y - 10, "LC Ref: LC-2025-00847")

    y -= 30
    col1, col2 = 50, W / 2 + 20
    bw = (W - 110) / 2

    draw_box(c, col1 - 5, y - 52, bw, 55)
    draw_box(c, col2 - 5, y - 52, bw, 55)
    y_terms = y - 68
    draw_box(c, 45, y_terms - 35, W - 90, 38, fill=LIGHT_GRAY)
    # Draw seller/buyer names, then terms immediately (for FIELD_BOUNDARY proximity)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(col1, y - 2, "SUPPLY PARTY")
    c.drawString(col2, y - 2, "DEMAND PARTY")
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(col1, y - 16, "Seller: Golden Dragon Trading Co. Ltd.")
    c.drawString(col2, y - 16, "Buyer: Atlantic Commerce Inc.")
    # Draw terms right after buyer so "Terms:" provides FIELD_BOUNDARY for buyer regex
    terms = [
        ("Terms:", "CIF New York"),
        ("Payment:", "90 days sight under DC"),
        ("Vessel:", "MV Pacific Star V.PS-2025-031"),
        ("Origin:", "Ethiopia"),
    ]
    dx = 55
    for lbl, val in terms:
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(MED_GRAY)
        c.drawString(dx, y_terms - 8, lbl)
        c.setFont("Helvetica", 7)
        c.setFillColor(black)
        c.drawString(dx, y_terms - 20, val)
        dx += 135
    # Now draw addresses and tax IDs (after terms in PDF stream)
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(col1, y - 28, "88 Harbour Road, Wan Chai, Hong Kong")
    c.drawString(col2, y - 28, "250 Park Avenue, New York, NY 10177, USA")
    c.drawString(col1, y - 40, "Tax ID: HK-88012345")
    c.drawString(col2, y - 40, "Tax ID: US-EIN 13-9876543")
    y = y_terms

    # Line items table
    y -= 50
    c.setFillColor(NAVY)
    c.rect(45, y - 4, W - 90, 18, fill=1, stroke=0)
    cols = [50, 80, 215, 340, 390, 440, 505]
    hds = ["No", "HS Code", "Description of Goods", "Qty", "Unit", "Unit Price", "Amount USD"]
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(white)
    for h, cx in zip(hds, cols):
        c.drawString(cx, y, h)

    y -= 20
    c.setFillColor(black)
    c.setFont("Helvetica", 8)
    # Item 1: Coffee
    items1 = [
        ("1", "0901.11", "Green Arabica Coffee Beans,", "200", "MT", "4,250.00", "850,000.00"),
        ("", "", "Grade AA, Origin: Ethiopia", "", "", "", ""),
        ("", "", "Packed in 8,000 jute bags of 25 KG", "", "", "", ""),
    ]
    for item in items1:
        for v, cx in zip(item, cols):
            c.drawString(cx, y, v)
        y -= 13

    y -= 4
    # Item 2: DUAL-USE - Laser Equipment
    items2 = [
        ("2", "9013.80", "Laser Alignment Equipment with", "5", "PCS", "12,000.00", "60,000.00"),
        ("", "", "thermal imaging cameras, encryption", "", "", "", ""),
        ("", "", "modules, and carbon fiber composite", "", "", "", ""),
        ("", "", "housing. Night vision compatible.", "", "", "", ""),
    ]
    for item in items2:
        for v, cx in zip(item, cols):
            c.drawString(cx, y, v)
        y -= 13

    # Totals
    y -= 8
    draw_separator(c, y)
    y -= 15
    totals = [
        ("Subtotal FOB:", "USD 880,000.00"),
        ("Freight:", "USD 18,000.00"),
        ("Insurance:", "USD 12,000.00"),
    ]
    for lbl, val in totals:
        c.setFont("Helvetica", 8)
        c.setFillColor(MED_GRAY)
        c.drawRightString(480, y, lbl)
        c.setFont("Helvetica", 8)
        c.setFillColor(black)
        c.drawRightString(W - 55, y, val)
        y -= 14

    y -= 5
    c.setFillColor(NAVY)
    c.rect(350, y - 5, W - 405, 22, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(white)
    c.drawString(360, y, "TOTAL CIF:")
    c.drawRightString(W - 58, y, "USD 910,000.00")

    y -= 22
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(DARK_GRAY)
    c.drawString(50, y, "Amount in Words: United States Dollars Nine Hundred and Ten Thousand Only")

    y -= 25
    draw_box(c, 45, y - 42, W - 90, 45, fill=LIGHT_GRAY)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y - 5, "BANKING DETAILS:")
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(55, y - 18, "Bank: HSBC Hong Kong  |  Account: 801-123456-838  |  SWIFT: HSBCHKHHHKH")
    c.drawString(55, y - 30, "Correspondent: Citibank N.A., New York  |  SWIFT: CITIUS33XXX")

    y -= 60
    draw_signature_line(c, 350, y, "Li Wei Ming", "Managing Director, Golden Dragon Trading")
    draw_stamp(c, 130, y + 10, ["GOLDEN DRAGON", "TRADING CO.", "HONG KONG", "ORIGINAL"])
    draw_page_num(c, 4)


# ============================================================
# PAGE 5: CERTIFICATE OF ORIGIN
# ============================================================
def page5(c):
    c.setFillColor(GOLD)
    c.rect(0, H - 85, W, 85, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W / 2, H - 35, "CERTIFICATE OF ORIGIN")
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, H - 52, "Hong Kong General Chamber of Commerce")
    c.drawCentredString(W / 2, H - 65, "22/F, United Centre, 95 Queensway, Hong Kong")

    y = H - 105
    c.setFillColor(HexColor("#fef3c7"))
    c.rect(45, y - 15, W - 90, 22, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(DARK_GRAY)
    c.drawString(55, y - 8, "Certificate No: CO-HK-2025-08847")
    c.drawRightString(W - 55, y - 8, "Date: 20 February 2025")

    y -= 35
    fields = [
        ("1. Exporter:", "Golden Dragon Trading Co. Ltd., 88 Harbour Road, Wan Chai, Hong Kong"),
        ("2. Consignee:", "Atlantic Commerce Inc., 250 Park Avenue, New York, NY 10177, USA"),
        ("3. Country of Origin:", "Ethiopia"),
        ("4. Transport:", "Vessel MV Pacific Star V.PS-2025-031 From Hong Kong To New York"),
        ("5. HS Code:", "0901.11"),
        ("6. Marks:", "GD/AC/001 through GD/AC/009"),
        ("7. Packages:", "8,000 bags of 25 KG each + 5 PCS laser equipment"),
        ("8. Description:", "Green Arabica Coffee Beans, Grade AA, Origin: Ethiopia"),
        ("9. Quantity:", "200 Metric Tons (MT) + 5 PCS"),
        ("10. Gross Weight:", "204,750 KG"),
        ("11. Net Weight:", "200,650 KG"),
        ("12. Invoice:", "INV-GD-2025-0220 dated 20 February 2025"),
    ]
    for lbl, val in fields:
        draw_box(c, 45, y - 30, W - 90, 33)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(MED_GRAY)
        c.drawString(55, y - 5, lbl)
        c.setFont("Helvetica", 8)
        c.setFillColor(black)
        c.drawString(55, y - 18, val)
        y -= 36

    y -= 5
    draw_box(c, 45, y - 30, W - 90, 33, fill=LIGHT_GRAY)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y - 8, "CERTIFICATION:")
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(55, y - 20, "The undersigned certifies that the above goods originated in the country shown.")

    y -= 50
    draw_signature_line(c, 50, y, "Dr. Y.C. Wong", "Authorized Signatory, HKGCC")
    draw_stamp(c, W - 120, y + 10, ["HONG KONG", "GENERAL CHAMBER", "OF COMMERCE", "CERTIFIED"])
    draw_page_num(c, 5)


# ============================================================
# PAGE 6: PACKING LIST (with dual-use items)
# ============================================================
def page6(c):
    c.setFillColor(DARK_BLUE)
    c.rect(0, H - 70, W, 70, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, H - 40, "PACKING LIST")
    c.setFont("Helvetica", 9)
    c.drawString(50, H - 55, "Golden Dragon Trading Co. Ltd.")
    c.drawRightString(W - 50, H - 40, "PL-GD-2025-0220")
    c.drawRightString(W - 50, H - 55, "Date: 20 February 2025")

    y = H - 85
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(50, y, "SHIPPER:")
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(100, y, "Golden Dragon Trading Co. Ltd., 88 Harbour Road, Wan Chai, Hong Kong")
    y -= 12
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(50, y, "CONSIGNEE:")
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(115, y, "Atlantic Commerce Inc., 250 Park Avenue, New York, NY 10177, USA")

    # Container table
    y -= 22
    c.setFillColor(NAVY)
    c.rect(45, y - 4, W - 90, 16, fill=1, stroke=0)
    cols = [50, 130, 220, 300, 380, 450, 515]
    hds = ["Container", "Seal No", "Bags/PCS", "Marks", "Net Wt KG", "Gross Wt KG", "Tare KG"]
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(white)
    for h, cx in zip(hds, cols):
        c.drawString(cx, y, h)

    y -= 16
    c.setFillColor(black)
    c.setFont("Helvetica", 7)
    containers = [
        ("PSSL-U2001234", "SL-90001", "1,000 bags", "GD/AC/001", "25,000", "25,500", "500"),
        ("PSSL-U2001235", "SL-90002", "1,000 bags", "GD/AC/002", "25,000", "25,500", "500"),
        ("PSSL-U2001236", "SL-90003", "1,000 bags", "GD/AC/003", "25,000", "25,500", "500"),
        ("PSSL-U2001237", "SL-90004", "1,000 bags", "GD/AC/004", "25,000", "25,500", "500"),
        ("PSSL-U2001238", "SL-90005", "1,000 bags", "GD/AC/005", "25,000", "25,500", "500"),
        ("PSSL-U2001239", "SL-90006", "1,000 bags", "GD/AC/006", "25,000", "25,500", "500"),
        ("PSSL-U2001240", "SL-90007", "1,000 bags", "GD/AC/007", "25,000", "25,500", "500"),
        ("PSSL-U2001241", "SL-90008", "1,000 bags", "GD/AC/008", "25,000", "25,500", "500"),
        ("PSSL-U2001242", "SL-90009", "5 PCS", "GD/AC/009", "650", "750", "100"),
    ]
    for row in containers:
        for v, cx in zip(row, cols):
            c.drawString(cx, y, v)
        y -= 11

    y -= 5
    draw_separator(c, y)
    y -= 12
    c.setFont("Helvetica-Bold", 8)
    c.drawString(50, y, "TOTALS:  9 containers  |  8,000 bags + 5 PCS  |  Net: 200,650 KG  |  Gross: 204,750 KG")

    # Packing spec -- includes DUAL USE keywords
    y -= 20
    draw_box(c, 45, y - 105, W - 90, 108, fill=LIGHT_GRAY)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y - 5, "PACKING SPECIFICATION:")
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    specs = [
        "ITEM 1 - Coffee (Containers 1-8):",
        "  Commodity: Green Arabica Coffee Beans, Grade AA, HS Code: 0901.11",
        "  Inner: Double-lined jute bags, 25 KG net per bag. Outer: Palletized, stretch-wrapped",
        "",
        "ITEM 2 - Laser Equipment (Container 9):",
        "  Commodity: Laser Alignment Equipment with thermal imaging cameras, HS Code: 9013.80",
        "  Contains high-power encryption modules for secure data transmission",
        "  Housing: Carbon fiber composite casing with night vision optical components",
        "  Packed in foam-lined wooden crates, ISPM 15 compliant",
    ]
    dy = y - 18
    for s in specs:
        c.drawString(55, dy, s)
        dy -= 10

    # Shipping details
    y -= 120
    draw_box(c, 45, y - 35, W - 90, 38)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y - 5, "SHIPPING:")
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(55, y - 18, "Vessel: MV Pacific Star  |  Voyage: PS-2025-031  |  B/L: HKHK-NY-20250220-001")
    c.drawString(55, y - 30, "Port of Loading: Hong Kong  |  Port of Discharge: Port of New York/New Jersey")

    y -= 55
    draw_signature_line(c, 50, y, "Chen Mei Ling", "Logistics Manager")
    draw_stamp(c, W - 120, y + 10, ["GOLDEN DRAGON", "TRADING CO.", "WAREHOUSE", "VERIFIED"])
    draw_page_num(c, 6)


# ============================================================
# PAGE 7: INSURANCE CERTIFICATE
# ============================================================
def page7(c):
    c.setFillColor(HexColor("#003399"))
    c.rect(0, H - 85, W, 85, fill=1, stroke=0)
    c.setFillColor(white)
    c.circle(80, H - 42, 22, fill=1, stroke=0)
    c.setFillColor(HexColor("#003399"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(80, H - 46, "Z")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(115, H - 42, "ZURICH INSURANCE")
    c.setFont("Helvetica", 8)
    c.drawString(115, H - 58, "Zurich Insurance Company Ltd. | Hong Kong Branch")
    c.drawString(115, H - 70, "25/F, One Island East, 18 Westlands Road, Quarry Bay, Hong Kong")

    y = H - 105
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(NAVY)
    c.drawCentredString(W / 2, y, "MARINE CARGO INSURANCE CERTIFICATE")

    y -= 25
    c.setFillColor(HexColor("#fef3c7"))
    c.rect(45, y - 15, W - 90, 20, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(DARK_GRAY)
    c.drawString(55, y - 9, "Policy No: IC-2025-98432")
    c.drawRightString(W - 55, y - 9, "Date: 20 February 2025")

    y -= 35
    fields = [
        ("Assured:", "Golden Dragon Trading Co. Ltd."),
        ("Address:", "88 Harbour Road, Wan Chai, Hong Kong"),
        ("Commodity:", "Green Arabica Coffee Beans + Laser Equipment"),
        ("HS Codes:", "0901.11, 9013.80"),
        ("Quantity:", "200 MT + 5 PCS"),
        ("Vessel:", "MV Pacific Star, Voyage PS-2025-031"),
        ("From:", "Hong Kong"),
        ("To:", "Port of New York/New Jersey"),
        ("Invoice Value:", "USD 910,000.00"),
        ("Sum Insured:", "USD 1,001,000.00 (110% of CIF value)"),
        ("Currency:", "USD"),
    ]
    for lbl, val in fields:
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(MED_GRAY)
        c.drawString(55, y, lbl)
        c.setFont("Helvetica", 8)
        c.setFillColor(black)
        c.drawString(155, y, val)
        y -= 14

    y -= 10
    draw_box(c, 45, y - 85, W - 90, 88, fill=LIGHT_BLUE)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y - 8, "RISKS COVERED:")
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    risks = [
        "- Institute Cargo Clauses (A) - All Risks",
        "- Institute War Clauses (Cargo)",
        "- Institute Strikes Clauses (Cargo)",
        "- Institute Theft, Pilferage and Non-Delivery",
        "- Warehouse to Warehouse coverage",
        "- Spontaneous combustion, sweat and heating damage",
    ]
    dy = y - 22
    for r in risks:
        c.drawString(65, dy, r)
        dy -= 11

    y -= 105
    draw_box(c, 45, y - 30, W - 90, 33)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y - 5, "CLAIMS SETTLING AGENT:")
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(55, y - 18, "McLarens Young International, 100 Wall Street, Suite 1500, New York, NY 10005")

    y -= 50
    draw_signature_line(c, 50, y, "Michael K. Tam", "Underwriting Manager, Marine Division")
    draw_stamp(c, W - 120, y + 10, ["ZURICH", "INSURANCE", "HONG KONG", "CERTIFIED"])
    draw_page_num(c, 7)


# ============================================================
# PAGE 8: BENEFICIARY CERTIFICATE
# ============================================================
def page8(c):
    c.setFillColor(DARK_BLUE)
    c.rect(0, H - 70, W, 70, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, H - 40, "BENEFICIARY CERTIFICATE")
    c.setFont("Helvetica", 9)
    c.drawString(50, H - 55, "Golden Dragon Trading Co. Ltd.")
    c.drawRightString(W - 50, H - 40, "BC/GD/2025/0220")
    c.drawRightString(W - 50, H - 55, "Date: 20 February 2025")

    y = H - 90
    draw_box(c, 45, y - 300, W - 90, 305, fill=HexColor("#fefce8"))

    ty = y - 10
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(NAVY)
    c.drawCentredString(W / 2, ty, "CERTIFICATE")
    ty -= 25
    c.setFont("Helvetica", 9)
    c.setFillColor(black)
    paras = [
        "We, Golden Dragon Trading Co. Ltd., of 88 Harbour Road, Wan Chai, Hong Kong,",
        "being the Beneficiary under Letter of Credit No. LC-2025-00847 issued by Citibank",
        "N.A., New York, do hereby certify the following:",
        "",
        "1. That we have shipped the goods in accordance with all terms and conditions",
        "   stipulated in the above-referenced Letter of Credit.",
        "",
        "2. That the goods consist of: Green Arabica Coffee Beans, Grade AA, Origin:",
        "   Ethiopia, HS Code: 0901.11, totaling 200 Metric Tons, plus Laser Alignment",
        "   Equipment, HS Code: 9013.80, totaling 5 PCS.",
        "",
        "3. That the total invoice value of the shipment is USD 910,000.00 on CIF New York.",
        "",
        "4. That the goods were loaded on MV Pacific Star, Voyage PS-2025-031, at Hong Kong",
        "   on 20 February 2025 for discharge at Port of New York/New Jersey.",
        "",
        "5. That all documents required under the Letter of Credit have been duly prepared",
        "   and presented to the Advising Bank for negotiation/collection.",
        "",
        "6. That insurance coverage has been arranged with Zurich Insurance Company Ltd.,",
        "   Policy No. IC-2025-98432, for USD 1,001,000.00 covering all risks.",
        "",
        "7. That the goods are free from any liens, encumbrances, or third-party claims.",
    ]
    for line in paras:
        c.drawString(60, ty, line)
        ty -= 12

    y -= 320
    draw_signature_line(c, 50, y, "Li Wei Ming", "Managing Director")
    draw_signature_line(c, 350, y, "Chen Mei Ling", "Export Manager")
    draw_stamp(c, W / 2, y + 20, ["GOLDEN DRAGON", "TRADING CO.", "HONG KONG", "SEAL"])

    y -= 35
    c.setFont("Helvetica", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(50, y, "For and on behalf of: Golden Dragon Trading Co. Ltd.")
    c.drawString(50, y - 12, "Company Registration No: HK-CR-2015-88012345")
    draw_page_num(c, 8)


# ============================================================
# PAGE 9: INSPECTION CERTIFICATE
# ============================================================
def page9(c):
    c.setFillColor(HexColor("#e30613"))
    c.rect(0, H - 80, W, 80, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, H - 50, "SGS")
    c.setFont("Helvetica", 9)
    c.drawString(50, H - 65, "SGS Hong Kong Limited")
    c.drawRightString(W - 50, H - 40, "Unit 301, 3/F, Metroplaza Tower 1")
    c.drawRightString(W - 50, H - 53, "Kwai Fong, Hong Kong")
    c.drawRightString(W - 50, H - 66, "ISO 17025 Accredited")

    y = H - 100
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(NAVY)
    c.drawCentredString(W / 2, y, "INSPECTION CERTIFICATE")
    y -= 15
    c.setFont("Helvetica", 8)
    c.setFillColor(MED_GRAY)
    c.drawCentredString(W / 2, y, "Quality and Quantity Verification Report")

    y -= 22
    c.setFillColor(LIGHT_BLUE)
    c.rect(45, y - 15, W - 90, 20, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y - 9, "Certificate No: SGS-HK-2025-4471")
    c.drawRightString(W - 55, y - 9, "Inspection Date: 18 February 2025")

    y -= 30
    parties = [
        ("Client:", "Golden Dragon Trading Co. Ltd."),
        ("Buyer:", "Atlantic Commerce Inc."),
        ("Commodity:", "Green Arabica Coffee Beans, Grade AA + Laser Equipment"),
        ("HS Codes:", "0901.11, 9013.80"),
        ("Quantity:", "200 MT (8,000 bags) + 5 PCS"),
        ("Invoice No:", "INV-GD-2025-0220"),
        ("Location:", "Golden Dragon Warehouse, Kwai Chung, Hong Kong"),
    ]
    for lbl, val in parties:
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(MED_GRAY)
        c.drawString(55, y, lbl)
        c.setFont("Helvetica", 8)
        c.setFillColor(black)
        c.drawString(150, y, val)
        y -= 13

    # Coffee quality results
    y -= 10
    draw_box(c, 45, y - 95, W - 90, 98, fill=LIGHT_GRAY)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y - 8, "ITEM 1 - COFFEE QUALITY ANALYSIS:")
    y -= 22
    cols_q = [60, 200, 340, 460]
    c.setFillColor(NAVY)
    c.rect(55, y - 3, W - 112, 14, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(white)
    for h, cx in zip(["Parameter", "Result", "Spec", "Status"], cols_q):
        c.drawString(cx, y, h)
    y -= 14
    c.setFillColor(black)
    results = [
        ("Moisture Content", "10.8%", "Max 12.0%", "PASS"),
        ("Screen Size (Above 15)", "92.3%", "Min 85%", "PASS"),
        ("Defects (Category I)", "2.1%", "Max 5%", "PASS"),
        ("Foreign Matter", "0.1%", "Max 0.5%", "PASS"),
        ("Cup Quality Score", "84/100", "Min 80/100", "PASS"),
    ]
    for p, r, s, st in results:
        c.setFont("Helvetica", 7)
        c.drawString(cols_q[0], y, p)
        c.drawString(cols_q[1], y, r)
        c.drawString(cols_q[2], y, s)
        c.setFillColor(GREEN if st == "PASS" else RED)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(cols_q[3], y, st)
        c.setFillColor(black)
        y -= 11

    # Laser equipment inspection
    y -= 15
    draw_box(c, 45, y - 55, W - 90, 58, fill=LIGHT_GRAY)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y - 8, "ITEM 2 - LASER EQUIPMENT INSPECTION:")
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(55, y - 22, "5 units of Laser Alignment Equipment inspected. All thermal imaging cameras functional.")
    c.drawString(55, y - 34, "Encryption modules verified and sealed. Carbon fiber housings intact, no damage.")
    c.drawString(55, y - 46, "HS Code: 9013.80 confirmed. Serial numbers recorded and cross-referenced.")

    # Conclusion
    y -= 68
    draw_box(c, 45, y - 30, W - 90, 33, fill=HexColor("#ecfdf5"))
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(GREEN)
    c.drawString(55, y - 8, "CONCLUSION: PASSED")
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(55, y - 22, "All goods conform to agreed specifications. Shipment approved for export.")

    y -= 50
    draw_signature_line(c, 50, y, "Dr. Patricia Leung", "Senior Inspector")
    draw_signature_line(c, 350, y, "David K. Cheung", "Branch Manager, SGS HK")
    draw_stamp(c, W / 2, y + 20, ["SGS", "HONG KONG", "INSPECTED", "APPROVED"])
    draw_page_num(c, 9)


# ============================================================
# PAGE 10: RE-EXPORT COMMERCIAL INVOICE (Round-tripping + Shell Company)
# ============================================================
def page10(c):
    """Atlantic Commerce (normally buyer) is now SELLER → triggers round-tripping.
    Phoenix Trading 888 Ltd (buyer) → triggers shell company detection."""

    c.setFillColor(NAVY)
    c.rect(0, H - 80, W, 80, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, H - 42, "COMMERCIAL INVOICE")
    c.setFont("Helvetica", 9)
    c.drawString(50, H - 58, "Atlantic Commerce Inc.")
    c.drawRightString(W - 50, H - 42, "RE-EXPORT INVOICE")
    c.drawRightString(W - 50, H - 58, "250 Park Avenue, New York, NY 10177, USA")

    y = H - 100
    c.setFillColor(HexColor("#fef3c7"))
    c.rect(45, y - 15, W - 90, 20, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(DARK_GRAY)
    c.drawString(55, y - 10, "Invoice No: INV-AC-2025-0315")
    c.drawCentredString(W / 2, y - 10, "Date: 15 March 2025")
    c.drawRightString(W - 55, y - 10, "Ref: RE-EXP-2025-042")

    y -= 32
    col1, col2 = 50, W / 2 + 20
    bw = (W - 110) / 2

    # SELLER = Atlantic Commerce (same as buyer on page 4 = ROUND-TRIPPING)
    # BUYER = Phoenix Trading 888 Ltd (SHELL COMPANY: generic + aspirational + numeric)
    draw_box(c, col1 - 5, y - 55, bw, 58)
    draw_box(c, col2 - 5, y - 55, bw, 58)
    y_terms = y - 72
    draw_box(c, 45, y_terms - 30, W - 90, 33, fill=LIGHT_GRAY)
    # Draw seller/buyer names, then terms immediately (for FIELD_BOUNDARY proximity)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(col1, y - 2, "SUPPLY PARTY")
    c.drawString(col2, y - 2, "DEMAND PARTY")
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(col1, y - 16, "Seller: Atlantic Commerce Inc.")
    c.drawString(col2, y - 16, "Buyer: Phoenix Trading 888 Ltd")
    # Draw terms right after buyer so "Terms:" provides FIELD_BOUNDARY for buyer regex
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(55, y_terms - 5, "Terms: FOB New York")
    c.drawString(200, y_terms - 5, "Payment: Wire Transfer")
    c.drawString(350, y_terms - 5, "Country of Origin: Ethiopia/Hong Kong")
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(55, y_terms - 18, "Note: Re-export of goods originally imported under LC-2025-00847")
    # Now draw addresses and tax IDs (after terms in PDF stream)
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(col1, y - 28, "250 Park Avenue, New York, NY 10177, USA")
    c.drawString(col2, y - 28, "Suite 1205, 12/F, Tower B")
    c.drawString(col1, y - 40, "Tax ID: US-EIN 13-9876543")
    c.drawString(col2, y - 40, "Tsim Sha Tsui, Kowloon, Hong Kong")
    y = y_terms

    # Line items
    y -= 45
    c.setFillColor(NAVY)
    c.rect(45, y - 4, W - 90, 18, fill=1, stroke=0)
    cols = [50, 80, 215, 370, 415, 460, 510]
    hds = ["No", "HS Code", "Description", "Qty", "Unit", "Price", "Amount USD"]
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(white)
    for h, cx in zip(hds, cols):
        c.drawString(cx, y, h)

    y -= 20
    c.setFillColor(black)
    c.setFont("Helvetica", 8)
    items = [
        ("1", "9013.80", "Laser Alignment Equipment with", "5", "PCS", "14,400", "72,000.00"),
        ("", "", "thermal imaging cameras and", "", "", "", ""),
        ("", "", "encryption modules. Carbon fiber", "", "", "", ""),
        ("", "", "composite housing, night vision.", "", "", "", ""),
    ]
    for item in items:
        for v, cx in zip(item, cols):
            c.drawString(cx, y, v)
        y -= 13

    y -= 10
    draw_separator(c, y)
    y -= 18
    c.setFillColor(NAVY)
    c.rect(350, y - 5, W - 405, 22, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(white)
    c.drawString(360, y, "TOTAL FOB:")
    c.drawRightString(W - 58, y, "USD 72,000.00")

    y -= 22
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(DARK_GRAY)
    c.drawString(50, y, "Amount in Words: United States Dollars Seventy Two Thousand Only")

    # Red flag context box
    y -= 30
    draw_box(c, 45, y - 60, W - 90, 63, fill=HexColor("#fef2f2"))
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(RED)
    c.drawString(55, y - 8, "SPECIAL NOTES:")
    c.setFont("Helvetica", 7)
    c.setFillColor(DARK_GRAY)
    c.drawString(55, y - 22, "This re-export involves controlled items (HS 9013.80 - Laser/optical equipment).")
    c.drawString(55, y - 34, "Buyer: Phoenix Trading 888 Ltd - newly established trading entity in Hong Kong.")
    c.drawString(55, y - 46, "End-use certification and export license documentation required per EAR regulations.")

    # Banking details
    y -= 78
    draw_box(c, 45, y - 35, W - 90, 38, fill=LIGHT_GRAY)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(DARK_BLUE)
    c.drawString(55, y - 5, "BANKING DETAILS:")
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(55, y - 18, "Bank: JPMorgan Chase, New York  |  Account: 8847-2251-0093  |  SWIFT: CHASUS33")
    c.drawString(55, y - 30, "Correspondent: Standard Chartered HK  |  SWIFT: SCBLHKHHXXX")

    y -= 55
    draw_signature_line(c, 50, y, "John D. Robertson", "Export Manager, Atlantic Commerce Inc.")
    draw_stamp(c, W - 120, y + 10, ["ATLANTIC", "COMMERCE INC", "NEW YORK", "EXPORT"])

    y -= 35
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(MED_GRAY)
    c.drawString(50, y, "We certify this invoice is true and correct. Goods originally imported under LC-2025-00847.")
    draw_page_num(c, 10)


# ============================================================
# MAIN
# ============================================================
def main():
    c = canvas.Canvas(OUTPUT, pagesize=letter)
    c.setTitle("Trade Finance Documents - LC-2025-00847")
    c.setAuthor("Golden Dragon Trading Co. Ltd.")
    c.setSubject("Documentary Collection Documents")

    page1(c); c.showPage()
    page2(c); c.showPage()
    page3(c); c.showPage()
    page4(c); c.showPage()
    page5(c); c.showPage()
    page6(c); c.showPage()
    page7(c); c.showPage()
    page8(c); c.showPage()
    page9(c); c.showPage()
    page10(c); c.showPage()

    c.save()
    size = os.path.getsize(OUTPUT)
    print(f"Sample trade documents PDF created: {OUTPUT}")
    print(f"Size: {size / 1024:.1f} KB, Pages: 10")
    print()
    print("Red flag triggers included:")
    print("  srf02 (Dual-Use): HS 9013.80, thermal imaging, encryption, carbon fiber, night vision")
    print("  srf04 (Shell Co): Phoenix Trading 888 Ltd, Golden Ventures Ltd, Diamond Holdings Ltd")
    print("  srf05 (Round-trip): Atlantic Commerce Inc. as both buyer (p4) and seller (p10)")

if __name__ == "__main__":
    main()
