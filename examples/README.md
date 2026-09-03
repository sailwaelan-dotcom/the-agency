# Exemples — The Agency

Des walkthroughs commentés qui montrent comment un agent IA équipé des skills
de ce repo accompagne concrètement un solopreneur belge.

## Contenu

| Fichier | Scénario | Skills enchaînés |
|---|---|---|
| [`journee-solopreneur.md`](journee-solopreneur.md) | Une journée type de solopreneur belge, du tri matinal au post LinkedIn | `secretary-ops` → `be-admin-deadlines` → `be-invoicing-peppol` → `content-engine-be` |

## Comment lire ces exemples

Chaque étape suit le même format :

1. **La demande** — ce que l'utilisateur tape, tel quel, en langage naturel.
2. **Le skill déclenché** — celui dont la `description` matche la demande
   (voir `tests/ACTIVATION.md` pour la logique d'activation).
3. **Un extrait de sortie** — représentatif de ce que l'agent produit une fois
   le skill chargé. Les extraits sont raccourcis pour la lisibilité ; le skill
   complet produit des artefacts plus détaillés.

## Données fictives

Tous les exemples utilisent des placeholders (`[NOM_CLIENT]`, `BE0123.456.789`,
montants ronds fictifs). Aucune donnée réelle. Les contenus fiscaux, comptables
et juridiques sont de l'information générale — voir le disclaimer de chaque
skill concerné.
