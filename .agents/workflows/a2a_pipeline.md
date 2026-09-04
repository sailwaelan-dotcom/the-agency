# Protocole Multi-Agents A2A (Agent-to-Agent Pipeline)

Ce document décrit le pipeline d'orchestration et la machine à états de transition entre les personas spécialisés de **The Agency**.

---

## 🔄 Machine à États du Pipeline Commercial & Administratif

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  DEVIS_DRAFT    │ ────> │  LEGAL_REVIEW   │ ────> │ PEPPOL_INVOICE  │ ────> │   OPS_CLOSING   │
│ (deviseur-be)   │       │  (juriste-be)   │       │ (comptable-be)  │       │ (secretaire-be) │
└─────────────────┘       └─────────────────┘       └─────────────────┘       └─────────────────┘
  Produit :                 Produit :                 Produit :                 Produit :
  quote_draft.v1            contract_terms.v1         invoice_event.v1          Rituels, rappels
  .json                     .json                     .json (XML UBL 2.1)       J-14 / J-3 & archivage
```

---

## 📋 Spécification des Transitions et Contrats d'Interface

### Étape 1 : Chiffrage & Proposition Commerciale (`deviseur-be`)
- **Rôle** : Cadrer la prestation, choisir le modèle tarifaire (TJM / forfait / phases) et fixer le montant de l'acompte (généralement 30 %).
- **Outils MCP mobilisés** : `validate_bce_number` pour vérifier l'identité du client.
- **Artefact produit** : Objet conforme à `.agents/schemas/quote_draft.v1.json`.
- **Condition de transition vers l'Étape 2** : Devis validé par le solopreneur et envoyé au client.

### Étape 2 : Sécurisation Contractuelle & Cession IP (`juriste-be`)
- **Rôle** : Définir les clauses de propriété intellectuelle (cession totale après paiement intégral du solde), le plafond de responsabilité, la juridiction compétente (tribunaux de Bruxelles ou arrondissement local) et les mentions RGPD.
- **Artefact produit** : Objet conforme à `.agents/schemas/contract_terms.v1.json`.
- **Condition de transition vers l'Étape 3** : Devis accepté et bon de commande signé par le client.

### Étape 3 : Émission Peppol & Ventilation TVA (`comptable-be`)
- **Rôle** : Générer la facture électronique légale en format structuré Peppol BIS 3.0 (UBL 2.1), ventiler la TVA (21 %, 12 %, 6 %, autoliquidation ou franchise) et calculer la communication structurée.
- **Outils MCP mobilisés** : `lookup_peppol_participant`, `check_vat_vies`, `generate_peppol_ubl`.
- **Artefact produit** : Objet conforme à `.agents/schemas/invoice_event.v1.json` et fichier XML UBL 2.1 validé.
- **Condition de transition vers l'Étape 4** : Facture transmise sur le réseau Peppol (ou PDF conforme si dérogation légale).

### Étape 4 : Gestion Opérationnelle & Échéancier (`secretaire-be`)
- **Rôle** : Planifier les dates d'échéance dans l'agenda, configurer les relances automatiques d'impayés à J+7 et J+14, et intégrer la pièce dans le dossier comptable trimestriel.
- **Outils MCP mobilisés** : `get_be_tax_calendar`.
- **Artefact produit** : Fiche de suivi client et rappels agenda.

---

## 🛡️ Résilience & Tolérance aux Pannes
- Si un numéro BCE est invalide à l'étape 1, le pipeline est interrompu par le Guardrail avant toute transition.
- Si le client est absent de l'annuaire Peppol à l'étape 3, le pipeline bifurque automatiquement vers l'émission d'une facture PDF avec mention d'invitation à l'enregistrement Peppol.
