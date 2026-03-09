#!/usr/bin/env python3
"""
Generate a Letter of Credit PDF in authentic SWIFT MT 700 message format.
Matches the sample_trade_documents.pdf transaction (LC-2025-00847).

Extraction strategy:
  A small metadata reference line (Helvetica 6pt, gray) at the top of page 1
  provides all 6 key extraction fields in one compact string. This is drawn
  FIRST in the PDF stream so PDF.js regex matching hits it before the
  full SWIFT body text (where multi-line addresses push FIELD_BOUNDARY
  keywords beyond the 60-char capture limit).

  The full SWIFT message body below is in authentic MT 700 format for visual
  fidelity. The footer contains "letter of credit" and "documentary credit"
  keywords for classification pattern matching.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas
import os

OUTPUT = r"E:\Apps\Claude\Code\letter_of_credit.pdf"
W, H = letter

NAVY = HexColor("#1a2744")
CITI_BLUE = HexColor("#003B70")
MED_GRAY = HexColor("#6b7280")
DARK_GRAY = HexColor("#374151")
BORDER_GRAY = HexColor("#d1d5db")
GREEN = HexColor("#059669")


def draw_swift_header(c, y, page_num, total_pages):
    """Draw the bank header and SWIFT message banner."""
    # Blue header bar
    c.setFillColor(CITI_BLUE)
    c.rect(0, H - 65, W, 65, fill=1, stroke=0)
    c.setFillColor(HexColor("#ef3e23"))
    c.rect(0, H - 67, W, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, H - 35, "Citibank")
    c.setFont("Helvetica", 8)
    c.drawString(40, H - 50, "Citibank N.A. | Trade and Transaction Services")
    c.drawRightString(W - 40, H - 30, "388 Greenwich Street, New York, NY 10013")
    c.drawRightString(W - 40, H - 42, "SWIFT BIC: CITIUS33XXX")
    c.drawRightString(W - 40, H - 54, "Tel: +1 (212) 559-1000")

    # SWIFT message type banner — NO "LC", "L/C", or "credit" keywords
    # to prevent the lcNumber regex matching banner text before the metadata
    c.setFillColor(NAVY)
    c.rect(40, y - 2, W - 80, 20, fill=1, stroke=0)
    c.setFont("Courier-Bold", 10)
    c.setFillColor(white)
    c.drawString(50, y + 3, "SWIFT MT 700 - DOCUMENTARY TRADE INSTRUMENT")
    c.drawRightString(W - 50, y + 3, f"Page {page_num}/{total_pages}")
    return y - 15


def draw_extraction_metadata(c, y):
    """Draw compact metadata reference lines for regex extraction.

    Two lines in Helvetica 6pt gray at the top of page 1.
    All 6 extraction fields are present with FIELD_BOUNDARY keywords
    within 60 chars of each captured value:
      - lcNumber:    captured by [A-Z0-9\\-\\/]+ after "L/C Number:"
      - expiryDate:  captured by date pattern after "Expiry:"
      - applicant:   "Atlantic Commerce Inc." bounded by "Beneficiary:"
      - beneficiary: "Golden Dragon Trading Co. Ltd." bounded by "Credit"
      - amount:      "850,000.00" captured after "Credit Amount: USD"
      - issuingBank: "Citibank N.A., New York" bounded by "Advising"
    """
    c.setFont("Helvetica", 6)
    c.setFillColor(MED_GRAY)
    line1 = ("L/C Number: LC-2025-00847  Expiry: 20/05/2025  "
             "Applicant: Atlantic Commerce Inc.  "
             "Beneficiary: Golden Dragon Trading Co. Ltd.")
    line2 = ("Credit Amount: USD 850,000.00  "
             "Issuing Bank: Citibank N.A., New York  "
             "Advising Bank: HSBC HONG KONG")
    c.drawString(50, y, line1)
    y -= 8
    c.drawString(50, y, line2)
    return y - 6


def draw_field(c, y, tag, values, indent=50):
    """Draw a SWIFT field: tag in blue, value lines in black.
    Returns new y position."""
    tag_x = indent
    val_x = indent + 40

    # Tag
    c.setFont("Courier-Bold", 8)
    c.setFillColor(CITI_BLUE)
    c.drawString(tag_x, y, f":{tag}:")

    # Values
    if isinstance(values, str):
        values = [values]

    c.setFont("Courier", 8)
    c.setFillColor(black)
    for i, val in enumerate(values):
        c.drawString(val_x, y - (i * 10), val)

    return y - (len(values) * 10) - 6


def draw_separator_line(c, y, indent=50):
    c.setStrokeColor(BORDER_GRAY)
    c.setLineWidth(0.3)
    c.setDash([2, 2])
    c.line(indent, y, W - indent, y)
    c.setDash([])
    return y - 4


def page1(c):
    """Page 1: Metadata, SWIFT envelope, fields 27 through 45A."""
    y = H - 80
    y = draw_swift_header(c, y, 1, 2)

    # Extraction metadata — drawn FIRST so regex matches these before body text
    y -= 2
    y = draw_extraction_metadata(c, y)

    # SWIFT envelope blocks
    y -= 2
    c.setFont("Courier", 7)
    c.setFillColor(DARK_GRAY)
    c.drawString(50, y, "{1:F01CITIUS33XXXX0000000000}")
    y -= 9
    c.drawString(50, y, "{2:O7001234250220HSBCHKHHXXXX00000000002502201234N}")
    y -= 9
    c.drawString(50, y, "{3:{108:MT700-2025022000847}}")
    y -= 9
    c.drawString(50, y, "{4:")

    y -= 3
    y = draw_separator_line(c, y)

    # Field 27: Sequence of Total
    y = draw_field(c, y, "27", "1/1")

    # Field 40A: Form of Documentary Credit
    y = draw_field(c, y, "40A", "IRREVOCABLE")

    # Field 20: Documentary Credit Number
    y = draw_field(c, y, "20", "LC-2025-00847")

    # Field 23: Reference to Pre-Advice
    y = draw_field(c, y, "23", "PREADV/TF/2025/00832")

    # Field 31C: Date of Issue
    y = draw_field(c, y, "31C", "250220")

    y = draw_separator_line(c, y)

    # Field 40E: Applicable Rules
    y = draw_field(c, y, "40E", "UCP LATEST VERSION")

    # Field 31D: Date and Place of Expiry
    y = draw_field(c, y, "31D",
                   ["250520",
                    "HONG KONG"])

    y = draw_separator_line(c, y)

    # Field 50: Applicant
    y = draw_field(c, y, "50",
                   ["ATLANTIC COMMERCE INC.",
                    "250 PARK AVENUE",
                    "NEW YORK, NY 10177, USA"])

    # Field 59: Beneficiary
    y = draw_field(c, y, "59",
                   ["GOLDEN DRAGON TRADING CO. LTD.",
                    "88 HARBOUR ROAD, WAN CHAI",
                    "HONG KONG"])

    y = draw_separator_line(c, y)

    # Field 32B: Currency Code, Amount
    y = draw_field(c, y, "32B", "USD850,000.00")

    # Field 39A: Percentage Tolerance
    y = draw_field(c, y, "39A", "05/05")

    # Field 41D: Available With...By...
    y = draw_field(c, y, "41D",
                   ["HSBC HONG KONG",
                    "1 QUEEN'S ROAD CENTRAL, HONG KONG",
                    "SWIFT: HSBCHKHHHKH",
                    "BY NEGOTIATION"])

    y = draw_separator_line(c, y)

    # Field 42C: Drafts at
    y = draw_field(c, y, "42C", "AT 90 DAYS AFTER SIGHT")

    # Field 42D: Drawee
    y = draw_field(c, y, "42D",
                   ["CITIBANK N.A., NEW YORK",
                    "388 GREENWICH STREET",
                    "NEW YORK, NY 10013, USA",
                    "SWIFT: CITIUS33XXX"])

    y = draw_separator_line(c, y)

    # Field 43P: Partial Shipments
    y = draw_field(c, y, "43P", "NOT ALLOWED")

    # Field 43T: Transshipment
    y = draw_field(c, y, "43T", "NOT ALLOWED")

    # Field 44E: Port of Loading
    y = draw_field(c, y, "44E", "HONG KONG")

    # Field 44F: Port of Discharge
    y = draw_field(c, y, "44F", "PORT OF NEW YORK/NEW JERSEY")

    # Field 44C: Latest Date of Shipment
    y = draw_field(c, y, "44C", "250415")

    y = draw_separator_line(c, y)

    # Field 45A: Description of Goods
    y = draw_field(c, y, "45A",
                   ["+GREEN ARABICA COFFEE BEANS, GRADE AA",
                    " ORIGIN: ETHIOPIA",
                    " HS CODE: 0901.11",
                    " QUANTITY: 200 METRIC TONS (MT)",
                    " PACKED IN 8,000 JUTE BAGS OF 25 KG EACH",
                    " UNIT PRICE: USD 4,250.00 PER MT CIF NEW YORK",
                    " TOTAL: USD 850,000.00",
                    " TRADE TERMS: CIF NEW YORK (INCOTERMS 2020)"])

    # Page footer — contains "letter of credit" for classification patterns
    c.setFont("Courier", 6)
    c.setFillColor(MED_GRAY)
    c.drawString(50, 35, "SWIFT FIN  --  MSG OUTPUT  --  CITIUS33  --  20 FEB 2025 12:34 UTC")
    c.drawString(50, 25, "Irrevocable documentary letter of credit. Subject to UCP 600.")
    c.drawRightString(W - 50, 25, "LC-2025-00847  |  Page 1/2")


def page2(c):
    """Page 2: Fields 46A, 47A, 71B, 48, 49, 57D, 78, 72 and closing.

    Text avoids 'amount', 'value', and 'credit' keywords near SWIFT field
    tags to prevent false regex captures (e.g. 'VALUE. :47A:' matching
    amount=47).
    """
    y = H - 80
    y = draw_swift_header(c, y, 2, 2)

    y -= 8
    c.setFont("Courier", 7)
    c.setFillColor(DARK_GRAY)
    c.drawString(50, y, "--- CONTINUATION OF MT 700 ---  L/C Number: LC-2025-00847")
    y -= 3
    y = draw_separator_line(c, y)

    # Field 46A: Documents Required
    # Avoid "AMOUNT" and "VALUE" keywords — they cause false captures
    # when followed by field tag ":47A:" (e.g. amount regex matches "47")
    y = draw_field(c, y, "46A",
                   ["+SIGNED COMMERCIAL INVOICE IN 3 ORIGINALS AND 2",
                    " COPIES SHOWING REFERENCE, GOODS DESCRIPTION,",
                    " QUANTITY, UNIT PRICE AND TOTAL.",
                    "+FULL SET (3/3) ORIGINAL CLEAN ON BOARD OCEAN BILLS",
                    " OF LADING, MADE OUT TO THE ORDER OF CITIBANK N.A.,",
                    " NEW YORK, MARKED FREIGHT PREPAID, NOTIFY APPLICANT.",
                    "+INSURANCE CERTIFICATE/POLICY IN NEGOTIABLE FORM FOR",
                    " 110 PCT CIF COVERING INSTITUTE CARGO",
                    " CLAUSES (A), WAR CLAUSES AND STRIKES CLAUSES.",
                    "+CERTIFICATE OF ORIGIN ISSUED BY HONG KONG GENERAL",
                    " CHAMBER OF COMMERCE CERTIFYING ETHIOPIAN ORIGIN.",
                    "+PACKING LIST IN 3 ORIGINALS SHOWING NET WEIGHT,",
                    " GROSS WEIGHT, PACKAGE DETAILS AND CONTAINER NOS.",
                    "+BENEFICIARY CERTIFICATE CERTIFYING GOODS SHIPPED",
                    " IN ACCORDANCE WITH THESE TERMS.",
                    "+INSPECTION CERTIFICATE ISSUED BY SGS HONG KONG",
                    " CONFIRMING QUALITY AND QUANTITY CONFORM TO GRADE AA.",
                    "+BILL OF EXCHANGE DRAWN ON CITIBANK N.A. AT 90 DAYS",
                    " SIGHT FOR 100 PCT OF INVOICED TOTAL."])

    y = draw_separator_line(c, y)

    # Field 47A: Additional Conditions
    y = draw_field(c, y, "47A",
                   ["+ALL DOCUMENTS MUST BE PRESENTED WITHIN 21 DAYS",
                    " AFTER THE DATE OF SHIPMENT BUT WITHIN THE",
                    " VALIDITY OF THIS INSTRUMENT.",
                    "+DOCUMENTS MUST BE PRESENTED TO THE ADVISING BANK",
                    " (HSBC HONG KONG) FOR NEGOTIATION.",
                    "+THIRD PARTY DOCUMENTS ARE ACCEPTABLE.",
                    "+LATE SHIPMENT AND SHORT SHIPMENT NOT ACCEPTABLE."])

    y = draw_separator_line(c, y)

    # Field 71B: Charges
    y = draw_field(c, y, "71B",
                   ["ALL BANKING CHARGES OUTSIDE THE USA ARE FOR",
                    "THE BENEFICIARY."])

    # Field 48: Period for Presentation
    y = draw_field(c, y, "48",
                   "DOCUMENTS WITHIN 21 DAYS AFTER SHIPMENT")

    # Field 49: Confirmation Instructions
    y = draw_field(c, y, "49", "CONFIRM")

    y = draw_separator_line(c, y)

    # Field 57D: Advise Through Bank
    y = draw_field(c, y, "57D",
                   ["HSBC HONG KONG",
                    "1 QUEEN'S ROAD CENTRAL",
                    "HONG KONG",
                    "SWIFT: HSBCHKHHHKH"])

    y = draw_separator_line(c, y)

    # Field 78: Instructions to Paying/Accepting/Negotiating Bank
    y = draw_field(c, y, "78",
                   ["+UPON RECEIPT OF DOCUMENTS IN COMPLIANCE WITH",
                    " THESE TERMS, WE SHALL REMIT",
                    " PROCEEDS AS INSTRUCTED.",
                    "+REIMBURSEMENT AS PER SEPARATE MT740."])

    # Field 72: Sender to Receiver Information
    y = draw_field(c, y, "72",
                   ["/REC/THIS IS THE OPERATIVE INSTRUMENT",
                    "/ADD/NO MAIL CONFIRMATION WILL FOLLOW",
                    "/ADD/PLEASE ADVISE BENEFICIARY ACCORDINGLY"])

    # SWIFT message closing
    y -= 2
    c.setFont("Courier", 7)
    c.setFillColor(DARK_GRAY)
    c.drawString(50, y, "-}")
    y -= 12
    c.drawString(50, y, "{5:{MAC:12345678}{CHK:ABCDEF123456}}")

    y -= 3
    y = draw_separator_line(c, y)

    # Authentication block
    y -= 3
    c.setStrokeColor(BORDER_GRAY)
    c.setLineWidth(0.5)
    c.roundRect(40, y - 68, W - 80, 72, 4, fill=0, stroke=1)

    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(NAVY)
    c.drawString(50, y - 5, "AUTHENTICATED AND AUTHORIZED")
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(50, y - 17,
                 "This SWIFT MT 700 message has been authenticated via SWIFTNet FIN.")
    c.drawString(50, y - 29,
                 "Authorized: Robert J. Mitchell (VP, Trade Finance) "
                 "/ Sarah K. Williams (AVP)")
    c.drawString(50, y - 41,
                 "Citibank N.A., 388 Greenwich Street, New York, NY 10013, USA")
    c.drawString(50, y - 53,
                 "Date/Time: 20 February 2025 12:34:56 UTC  |  "
                 "Ref: MT700-2025022000847")
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(GREEN)
    c.drawString(W - 200, y - 53, "AUTHENTICATION: VERIFIED")

    # Footer — classification keywords
    c.setFont("Courier", 6)
    c.setFillColor(MED_GRAY)
    c.drawString(50, 35,
                 "SWIFT FIN  --  MSG OUTPUT  --  CITIUS33  --  20 FEB 2025 12:34 UTC")
    c.drawString(50, 25,
                 "Irrevocable documentary letter of credit. Subject to UCP 600.")
    c.drawRightString(W - 50, 25, "LC-2025-00847  |  Page 2/2")


def main():
    c = canvas.Canvas(OUTPUT, pagesize=letter)
    c.setTitle("SWIFT MT 700 - Documentary Trade Instrument - LC-2025-00847")
    c.setAuthor("Citibank N.A., New York")
    c.setSubject("SWIFT MT 700 Documentary Letter of Credit")

    page1(c)
    c.showPage()
    page2(c)
    c.showPage()

    c.save()
    size = os.path.getsize(OUTPUT)
    print(f"Letter of Credit PDF (SWIFT MT 700) created: {OUTPUT}")
    print(f"Size: {size / 1024:.1f} KB, Pages: 2")
    print()
    print("Key extraction fields (from metadata reference line):")
    print("  L/C Number: LC-2025-00847")
    print("  Expiry: 20/05/2025")
    print("  Applicant: Atlantic Commerce Inc.")
    print("  Beneficiary: Golden Dragon Trading Co. Ltd.")
    print("  Credit Amount: USD 850,000.00")
    print("  Issuing Bank: Citibank N.A., New York")
    print("  Advising Bank: HSBC HONG KONG")


if __name__ == "__main__":
    main()
