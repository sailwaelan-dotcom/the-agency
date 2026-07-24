# Mentions légales obligatoires — facture belge (as_of 2026-07)

> Ce fichier complète `be-invoicing-peppol`. Il détaille chaque mention obligatoire
> avec le fondement légal et un exemple concret. Consulter le SKILL.md parent pour
> le workflow complet.

---

## Mentions obligatoires (toutes factures)

| # | Mention | Fondement | Exemple |
|---|---|---|---|
| 1 | **Numéro séquentiel ininterrompu** | Art. 53 CTVA | `2026-001`, `2026-002`, … (pas de trous, pas de réinitialisation mensuelle) |
| 2 | **Date d'émission** | Art. 53 CTVA | `15/01/2026` |
| 3 | **Date de livraison/prestation** si ≠ émission | Art. 53 CTVA | `Livraison le 10/01/2026` |
| 4 | **Nom/dénomination + adresse du fournisseur** | Art. 53 CTVA | `Dupont Consulting SRL — Rue de la Loi 1, 1000 Bruxelles` |
| 5 | **Numéro BCE du fournisseur** précédé de `TVA BE` | Art. 53 CTVA | `TVA BE 0123.456.789` |
| 6 | **Numéro TVA du client** (si assujetti) | Art. 53 CTVA | `TVA BE 9876.543.210` |
| 7 | **Nom + adresse du client** | Art. 53 CTVA | `SA Martin — Avenue Louise 100, 1050 Bruxelles` |
| 8 | **Nature et quantité** des biens/services | Art. 53 CTVA | `Consulting stratégique — 8 jours × 600 €` |
| 9 | **Prix unitaire HTVA** hors taxes | Art. 53 CTVA | `600,00 €` |
| 10 | **Taux TVA par ligne** (ou exonération) | Art. 53 CTVA | `21 %` / `6 %` / `Exonéré — art. 44 §1, 1° CTVA` |
| 11 | **Montant TVA par taux** | Art. 53 CTVA | `TVA 21 % : 1.008,00 €` |
| 12 | **Total HTVA** | Art. 53 CTVA | `4.800,00 €` |
| 13 | **Total TVAC** | Art. 53 CTVA | `5.808,00 €` |
| 14 | **Date et conditions de paiement** | Art. 53 CTVA + Loi retards paiement | `Paiement dans les 30 jours — [IBAN_FOURNISSEUR]` |
| 15 | **Numéro de compte bancaire** du fournisseur | Pratique | `[IBAN_FOURNISSEUR]` |

## Mentions spéciales (selon cas)

### Franchise TVA (art. 56bis CTVA)
```
Franchise de TVA — article 56bis du Code de la TVA.
Pas de TVA facturée. La TVA n'est ni déductible ni récupérable.
```
**Obligatoire** sur CHAQUE facture si vous êtes au régime de franchise.

### Autoliquidation (art. 20 §2 AR n°1 — sous-traitance construction)
```
TVA due par le cocontractant — article 20, §2 de l'AR n°1.
```
Le fournisseur ne facture PAS la TVA ; le client la reverse lui-même.

### Exonération (art. 44 CTVA — activités exonérées)
```
Exonéré de TVA — article 44, §1, 1° du Code de la TVA.
```
Pas de TVA facturée, mais le droit à déduction est limité.

### Reverse charge intracommunautaire (art. 51 CTVA — services)
```
Autoliquidation — article 51, §3, 3° du Code de la TVA.
```
Le fournisseur belge ne facture pas la TVA ; le client dans un autre État membre la reverse.

### Livraison intracommunautaire de biens (art. 39 CTVA)
```
Exonéré — livraison intracommunautaire — article 39 du Code de la TVA.
```
Exonération sous conditions (transport hors Belgique, numéro TVA client vérifié dans VIES).

## Vérification avant envoi

- [ ] Numéro séquentiel cohérent avec le dernier émis (pas de trou)
- [ ] Numéro TVA client vérifié dans VIES (ec.europa.eu/taxation_customs/vies/) si intracommunautaire
- [ ] Taux TVA correct pour la catégorie de prestation (pas de 21 % par défaut)
- [ ] Conditions de paiement claires (délai + compte bancaire)
- [ ] Mention spéciale présente si franchise/autoliquidation/exonération
- [ ] Copie UBL conservée (pour Peppol) ou PDF archivée 7 ans

> ⚠️ **Disclaimer** : information générale (as_of 2026-07), pas un conseil fiscal
> personnalisé. Les taux et règles évoluent — vérifier sur finances.belgium.be et
> faire valider par un comptable ou expert-comptable agréé en Belgique.
