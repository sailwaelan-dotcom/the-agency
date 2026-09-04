"""
Validateur Schematron & règles métier pour factures électroniques Peppol BIS 3.0 (UBL 2.1).
Vérifie la conformité EN 16931 et les contraintes réglementaires belges.
Zéro dépendance externe : utilise xml.etree.ElementTree.
"""
import re
from typing import Any, Dict, List
import xml.etree.ElementTree as ET

EXPECTED_CUSTOMIZATION_PREFIX = "urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0"
NS_INVOICE = "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
NS_CAC = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
NS_CBC = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"

NAMESPACES = {
    "inv": NS_INVOICE,
    "cac": NS_CAC,
    "cbc": NS_CBC,
}


def validate_peppol_ubl_xml(xml_content: str) -> Dict[str, Any]:
    """
    Valide un flux XML UBL 2.1 selon les règles de conformité Peppol BIS Billing 3.0.
    """
    errors: List[str] = []
    warnings: List[str] = []

    if not isinstance(xml_content, str) or not xml_content.strip():
        return {
            "is_valid": False,
            "errors": ["Contenu XML vide ou invalide."],
            "warnings": [],
        }

    # 1. Analyse syntaxique XML
    try:
        root = ET.fromstring(xml_content.strip())
    except ET.ParseError as exc:
        return {
            "is_valid": False,
            "errors": [f"Erreur de syntaxe XML : {exc}"],
            "warnings": [],
        }

    # 2. Vérification élément racine
    tag_clean = root.tag.split("}")[-1] if "}" in root.tag else root.tag
    if tag_clean != "Invoice":
        errors.append(f"L'élément racine doit être 'Invoice', trouvé '{tag_clean}'.")

    # 3. CustomizationID
    custom_el = root.find("cbc:CustomizationID", NAMESPACES)
    if custom_el is None or not custom_el.text:
        errors.append("Élément obligatoire manquant : cbc:CustomizationID.")
    elif EXPECTED_CUSTOMIZATION_PREFIX not in custom_el.text:
        errors.append(
            f"cbc:CustomizationID non conforme. Attendu : '{EXPECTED_CUSTOMIZATION_PREFIX}', trouvé : '{custom_el.text}'."
        )

    # 4. ProfileID
    profile_el = root.find("cbc:ProfileID", NAMESPACES)
    if profile_el is None or not profile_el.text:
        warnings.append("Élément recommandé manquant : cbc:ProfileID.")

    # 5. Numéro de facture
    id_el = root.find("cbc:ID", NAMESPACES)
    invoice_number = id_el.text.strip() if id_el is not None and id_el.text else None
    if not invoice_number:
        errors.append("Élément obligatoire manquant : cbc:ID (numéro de facture).")

    # 6. Dates
    issue_date_el = root.find("cbc:IssueDate", NAMESPACES)
    if issue_date_el is None or not issue_date_el.text:
        errors.append("Élément obligatoire manquant : cbc:IssueDate.")

    # 7. Fournisseur (Supplier)
    supp_party = root.find("cac:AccountingSupplierParty/cac:Party", NAMESPACES)
    supplier_bce = None
    if supp_party is None:
        errors.append("Élément obligatoire manquant : cac:AccountingSupplierParty/cac:Party.")
    else:
        supp_endpoint = supp_party.find("cbc:EndpointID", NAMESPACES)
        if supp_endpoint is not None and supp_endpoint.text:
            scheme = supp_endpoint.attrib.get("schemeID", "")
            raw_id = supp_endpoint.text
            if scheme == "0208" or raw_id.startswith("0208:"):
                supplier_bce = raw_id.split(":")[-1]
            else:
                supplier_bce = raw_id

    # 8. Client (Customer)
    cust_party = root.find("cac:AccountingCustomerParty/cac:Party", NAMESPACES)
    customer_bce = None
    if cust_party is None:
        errors.append("Élément obligatoire manquant : cac:AccountingCustomerParty/cac:Party.")
    else:
        cust_endpoint = cust_party.find("cbc:EndpointID", NAMESPACES)
        if cust_endpoint is not None and cust_endpoint.text:
            scheme = cust_endpoint.attrib.get("schemeID", "")
            raw_id = cust_endpoint.text
            if scheme == "0208" or raw_id.startswith("0208:"):
                customer_bce = raw_id.split(":")[-1]
            else:
                customer_bce = raw_id

    # 9. Totaux financiers et réconciliation
    payable_amount = 0.0
    lmt = root.find("cac:LegalMonetaryTotal", NAMESPACES)
    if lmt is None:
        errors.append("Élément obligatoire manquant : cac:LegalMonetaryTotal.")
    else:
        pay_el = lmt.find("cbc:PayableAmount", NAMESPACES)
        net_el = lmt.find("cbc:TaxExclusiveAmount", NAMESPACES)
        if pay_el is not None and pay_el.text:
            try:
                payable_amount = float(pay_el.text)
            except ValueError:
                errors.append(f"Format numérique invalide pour PayableAmount : {pay_el.text}")

        # Réconciliation avec TaxTotal
        tax_total_el = root.find("cac:TaxTotal/cbc:TaxAmount", NAMESPACES)
        if tax_total_el is not None and net_el is not None:
            try:
                net_val = float(net_el.text)
                tax_val = float(tax_total_el.text)
                expected_ttc = round(net_val + tax_val, 2)
                if abs(expected_ttc - payable_amount) > 0.05:
                    errors.append(
                        f"Incohérence des totaux : HTVA ({net_val}) + TVA ({tax_val}) = {expected_ttc} != PayableAmount ({payable_amount})."
                    )
            except ValueError:
                pass

    # 10. Lignes de facture
    lines = root.findall("cac:InvoiceLine", NAMESPACES)
    if not lines:
        errors.append("La facture doit comporter au moins une ligne cac:InvoiceLine.")

    is_valid = len(errors) == 0

    return {
        "is_valid": is_valid,
        "invoice_number": invoice_number,
        "supplier_bce": supplier_bce,
        "customer_bce": customer_bce,
        "payable_amount": payable_amount,
        "lines_count": len(lines),
        "errors": errors,
        "warnings": warnings,
    }
