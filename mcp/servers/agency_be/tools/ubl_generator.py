"""
Générateur de facture électronique Peppol BIS Billing 3.0 (UBL 2.1).
Conforme à la norme européenne EN 16931 et à l'obligation belge B2B.
Zéro dépendance externe : utilise xml.etree.ElementTree de la bibliothèque standard.
"""
import re
from typing import Any, Dict, List
import xml.etree.ElementTree as ET

PEPPOL_CUSTOMIZATION_ID = "urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0"
PEPPOL_PROFILE_ID = "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"
NS_INVOICE = "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
NS_CAC = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
NS_CBC = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"


def _clean_bce(num: str) -> str:
    clean = re.sub(r"^(?i:BE)", "", str(num).strip())
    raw = re.sub(r"[^0-9]", "", clean)
    if len(raw) == 9:
        raw = "0" + raw
    return raw


def _sub_el(parent: ET.Element, tag: str, text: str = "", attrs: Dict[str, str] = None) -> ET.Element:
    el = ET.SubElement(parent, tag, attrs or {})
    if text:
        el.text = str(text)
    return el


def generate_peppol_ubl_xml(invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Génère le code XML UBL 2.1 canonique conforme à la spécification Peppol BIS Billing 3.0.
    """
    if not isinstance(invoice_data, dict):
        return {"success": False, "error": "invoice_data doit être un dictionnaire."}

    invoice_number = invoice_data.get("invoice_number")
    supplier = invoice_data.get("supplier", {})
    customer = invoice_data.get("customer", {})
    lines = invoice_data.get("lines", [])

    if not invoice_number or not supplier or not customer or not lines:
        return {
            "success": False,
            "error": "Champs obligatoires manquants : invoice_number, supplier, customer, lines.",
        }

    issue_date = invoice_data.get("issue_date", "2026-01-01")
    due_date = invoice_data.get("due_date", issue_date)
    currency = invoice_data.get("currency", "EUR")
    payment_ref = invoice_data.get("payment_reference", f"INV-{invoice_number}")

    # Calculs mathématiques
    total_htva = 0.0
    taxes_by_rate: Dict[float, float] = {}

    for idx, line in enumerate(lines, start=1):
        qty = float(line.get("quantity", 1.0))
        price = float(line.get("unit_price", 0.0))
        line_total = round(qty * price, 2)
        total_htva += line_total

        vat_rate = float(line.get("vat_rate", 0.21))
        taxes_by_rate[vat_rate] = taxes_by_rate.get(vat_rate, 0.0) + line_total

    total_htva = round(total_htva, 2)
    total_tva = 0.0
    for rate, base in taxes_by_rate.items():
        total_tva += round(base * rate, 2)
    total_tva = round(total_tva, 2)
    total_ttc = round(total_htva + total_tva, 2)

    # Construction de l'arbre XML
    ET.register_namespace("", NS_INVOICE)
    ET.register_namespace("cac", NS_CAC)
    ET.register_namespace("cbc", NS_CBC)

    root = ET.Element(f"{{{NS_INVOICE}}}Invoice")

    _sub_el(root, f"{{{NS_CBC}}}CustomizationID", PEPPOL_CUSTOMIZATION_ID)
    _sub_el(root, f"{{{NS_CBC}}}ProfileID", PEPPOL_PROFILE_ID)
    _sub_el(root, f"{{{NS_CBC}}}ID", invoice_number)
    _sub_el(root, f"{{{NS_CBC}}}IssueDate", issue_date)
    _sub_el(root, f"{{{NS_CBC}}}DueDate", due_date)
    _sub_el(root, f"{{{NS_CBC}}}InvoiceTypeCode", "380")
    _sub_el(root, f"{{{NS_CBC}}}DocumentCurrencyCode", currency)

    # 1. Supplier
    supp_party = _sub_el(root, f"{{{NS_CAC}}}AccountingSupplierParty")
    s_party = _sub_el(supp_party, f"{{{NS_CAC}}}Party")
    supp_bce = _clean_bce(supplier.get("bce_number", "0000000000"))
    _sub_el(s_party, f"{{{NS_CBC}}}EndpointID", f"0208:{supp_bce}", {"schemeID": "0208"})

    s_party_id = _sub_el(s_party, f"{{{NS_CAC}}}PartyIdentification")
    _sub_el(s_party_id, f"{{{NS_CBC}}}ID", supp_bce)

    s_party_name = _sub_el(s_party, f"{{{NS_CAC}}}PartyName")
    _sub_el(s_party_name, f"{{{NS_CBC}}}Name", supplier.get("name", "Fournisseur"))

    s_addr = _sub_el(s_party, f"{{{NS_CAC}}}PostalAddress")
    _sub_el(s_addr, f"{{{NS_CBC}}}StreetName", supplier.get("street", ""))
    _sub_el(s_addr, f"{{{NS_CBC}}}PostalZone", supplier.get("postal_code", ""))
    _sub_el(s_addr, f"{{{NS_CBC}}}CityName", supplier.get("city", ""))
    s_country = _sub_el(s_addr, f"{{{NS_CAC}}}Country")
    _sub_el(s_country, f"{{{NS_CBC}}}IdentificationCode", supplier.get("country_code", "BE"))

    s_tax = _sub_el(s_party, f"{{{NS_CAC}}}PartyTaxScheme")
    _sub_el(s_tax, f"{{{NS_CBC}}}CompanyID", supplier.get("vat_number", f"BE{supp_bce}"))
    s_tax_scheme = _sub_el(s_tax, f"{{{NS_CAC}}}TaxScheme")
    _sub_el(s_tax_scheme, f"{{{NS_CBC}}}ID", "VAT")

    s_legal = _sub_el(s_party, f"{{{NS_CAC}}}PartyLegalEntity")
    _sub_el(s_legal, f"{{{NS_CBC}}}RegistrationName", supplier.get("name", "Fournisseur"))
    _sub_el(s_legal, f"{{{NS_CBC}}}CompanyID", supp_bce)

    # 2. Customer
    cust_party = _sub_el(root, f"{{{NS_CAC}}}AccountingCustomerParty")
    c_party = _sub_el(cust_party, f"{{{NS_CAC}}}Party")
    cust_bce = _clean_bce(customer.get("bce_number", "0000000000"))
    cust_country = customer.get("country_code", "BE")
    scheme = "0208" if cust_country == "BE" else "9925"
    _sub_el(c_party, f"{{{NS_CBC}}}EndpointID", f"{scheme}:{cust_bce}", {"schemeID": scheme})

    c_party_id = _sub_el(c_party, f"{{{NS_CAC}}}PartyIdentification")
    _sub_el(c_party_id, f"{{{NS_CBC}}}ID", cust_bce)

    c_party_name = _sub_el(c_party, f"{{{NS_CAC}}}PartyName")
    _sub_el(c_party_name, f"{{{NS_CBC}}}Name", customer.get("name", "Client"))

    c_addr = _sub_el(c_party, f"{{{NS_CAC}}}PostalAddress")
    _sub_el(c_addr, f"{{{NS_CBC}}}StreetName", customer.get("street", ""))
    _sub_el(c_addr, f"{{{NS_CBC}}}PostalZone", customer.get("postal_code", ""))
    _sub_el(c_addr, f"{{{NS_CBC}}}CityName", customer.get("city", ""))
    c_country_el = _sub_el(c_addr, f"{{{NS_CAC}}}Country")
    _sub_el(c_country_el, f"{{{NS_CBC}}}IdentificationCode", cust_country)

    c_tax = _sub_el(c_party, f"{{{NS_CAC}}}PartyTaxScheme")
    _sub_el(c_tax, f"{{{NS_CBC}}}CompanyID", customer.get("vat_number", f"BE{cust_bce}"))
    c_tax_scheme = _sub_el(c_tax, f"{{{NS_CAC}}}TaxScheme")
    _sub_el(c_tax_scheme, f"{{{NS_CBC}}}ID", "VAT")

    c_legal = _sub_el(c_party, f"{{{NS_CAC}}}PartyLegalEntity")
    _sub_el(c_legal, f"{{{NS_CBC}}}RegistrationName", customer.get("name", "Client"))
    _sub_el(c_legal, f"{{{NS_CBC}}}CompanyID", cust_bce)

    # 3. Payment Means
    pm = _sub_el(root, f"{{{NS_CAC}}}PaymentMeans")
    _sub_el(pm, f"{{{NS_CBC}}}PaymentMeansCode", "30")
    _sub_el(pm, f"{{{NS_CBC}}}PaymentID", payment_ref)
    if supplier.get("iban"):
        p_account = _sub_el(pm, f"{{{NS_CAC}}}PayeeFinancialAccount")
        _sub_el(p_account, f"{{{NS_CBC}}}ID", supplier.get("iban"))

    # 4. Tax Total
    tax_total_el = _sub_el(root, f"{{{NS_CAC}}}TaxTotal")
    _sub_el(tax_total_el, f"{{{NS_CBC}}}TaxAmount", f"{total_tva:.2f}", {"currencyID": currency})

    for rate, taxable_amt in taxes_by_rate.items():
        sub_tax = round(taxable_amt * rate, 2)
        sub_el = _sub_el(tax_total_el, f"{{{NS_CAC}}}TaxSubtotal")
        _sub_el(sub_el, f"{{{NS_CBC}}}TaxableAmount", f"{taxable_amt:.2f}", {"currencyID": currency})
        _sub_el(sub_el, f"{{{NS_CBC}}}TaxAmount", f"{sub_tax:.2f}", {"currencyID": currency})

        cat_el = _sub_el(sub_el, f"{{{NS_CAC}}}TaxCategory")
        cat_id = "S" if rate > 0 else "E"
        _sub_el(cat_el, f"{{{NS_CBC}}}ID", cat_id)
        _sub_el(cat_el, f"{{{NS_CBC}}}Percent", f"{rate * 100:.1f}")
        sch_el = _sub_el(cat_el, f"{{{NS_CAC}}}TaxScheme")
        _sub_el(sch_el, f"{{{NS_CBC}}}ID", "VAT")

    # 5. Legal Monetary Total
    lmt = _sub_el(root, f"{{{NS_CAC}}}LegalMonetaryTotal")
    _sub_el(lmt, f"{{{NS_CBC}}}LineExtensionAmount", f"{total_htva:.2f}", {"currencyID": currency})
    _sub_el(lmt, f"{{{NS_CBC}}}TaxExclusiveAmount", f"{total_htva:.2f}", {"currencyID": currency})
    _sub_el(lmt, f"{{{NS_CBC}}}TaxInclusiveAmount", f"{total_ttc:.2f}", {"currencyID": currency})
    _sub_el(lmt, f"{{{NS_CBC}}}PayableAmount", f"{total_ttc:.2f}", {"currencyID": currency})

    # 6. Invoice Lines
    for idx, line in enumerate(lines, start=1):
        line_id = str(line.get("id", idx))
        qty = float(line.get("quantity", 1.0))
        price = float(line.get("unit_price", 0.0))
        line_amt = round(qty * price, 2)
        vat_rate = float(line.get("vat_rate", 0.21))

        inv_line = _sub_el(root, f"{{{NS_CAC}}}InvoiceLine")
        _sub_el(inv_line, f"{{{NS_CBC}}}ID", line_id)
        _sub_el(inv_line, f"{{{NS_CBC}}}InvoicedQuantity", f"{qty:.2f}", {"unitCode": "C62"})
        _sub_el(inv_line, f"{{{NS_CBC}}}LineExtensionAmount", f"{line_amt:.2f}", {"currencyID": currency})

        item_el = _sub_el(inv_line, f"{{{NS_CAC}}}Item")
        _sub_el(item_el, f"{{{NS_CBC}}}Description", line.get("description", ""))
        _sub_el(item_el, f"{{{NS_CBC}}}Name", line.get("name", f"Prestation {line_id}"))

        cls_tax = _sub_el(item_el, f"{{{NS_CAC}}}ClassifiedTaxCategory")
        _sub_el(cls_tax, f"{{{NS_CBC}}}ID", "S" if vat_rate > 0 else "E")
        _sub_el(cls_tax, f"{{{NS_CBC}}}Percent", f"{vat_rate * 100:.1f}")
        cls_sch = _sub_el(cls_tax, f"{{{NS_CAC}}}TaxScheme")
        _sub_el(cls_sch, f"{{{NS_CBC}}}ID", "VAT")

        price_el = _sub_el(inv_line, f"{{{NS_CAC}}}Price")
        _sub_el(price_el, f"{{{NS_CBC}}}PriceAmount", f"{price:.2f}", {"currencyID": currency})

    xml_bytes = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    xml_str = xml_bytes.decode("utf-8")

    return {
        "success": True,
        "xml": xml_str,
        "invoice_number": invoice_number,
        "total_htva": total_htva,
        "total_tva": total_tva,
        "total_ttc": total_ttc,
        "currency": currency,
        "customization_id": PEPPOL_CUSTOMIZATION_ID,
    }
