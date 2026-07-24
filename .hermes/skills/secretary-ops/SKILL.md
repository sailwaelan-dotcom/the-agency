---
name: secretary-ops
description: "Utilisez quand le solopreneur belge croule sous l'administratif quotidien : tri des emails, gestion d'agenda, préparation de rendez-vous clients, relances administratives, rappels d'échéances, classement documentaire. Produit des rituels et templates pour récupérer 3-5h/semaine."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [ops, admin, productivity, be]
  related_skills: [be-bookkeeping-ops, be-rgpd-compliance, content-engine-be]
  domain: ops
  language: fr
  as_of: "2026-07"
---

# Secrétariat opérationnel — solopreneur belge

## Overview

Un solopreneur est son propre secrétaire : inbox débordante, rendez-vous mal préparés,
échéances administratives ratées, documents introuvables. Ce skill installe les
**rituels et templates** qui rendent le secrétariat quasi invisible : tri email en
15 min/jour, agenda bloqué, fiches de préparation de RDV, relances standardisées,
rappels d'échéances belges. Objectif mesurable : **récupérer 3-5 heures par semaine**
sur l'administratif courant. Pour la compta mensuelle → `be-bookkeeping-ops` ; pour
les données personnelles dans les emails → `be-rgpd-compliance`.

## When to Use

- « Je passe mes matinées dans ma boîte mail »
- « J'ai raté une échéance / oublié de relancer un client »
- « Je cherche un document pendant 20 minutes à chaque fois »
- « Mes rendez-vous clients ne sont pas préparés »
- « Je veux des templates d'emails types (relance, confirmation RDV, suivi devis) »

**Ne pas utiliser pour :**
- Rituel comptable mensuel, archivage factures, impayés avec intérêts → `be-bookkeeping-ops`
- Échéances fiscales et sociales (théorie) → `be-accounting-basics`
- Production de contenu → `content-engine-be`

## Rituel 1 — Inbox zéro en 15 minutes (2×/jour, jamais en continu)

Règle : l'email se traite à **heures fixes** (ex. 9h et 16h30), notifications coupées
le reste du temps. Chaque email reçoit UNE des 4 actions :

| Action | Quand | Durée max |
|---|---|---|
| **Supprimer/archiver** | Info sans action requise | 5 sec |
| **Répondre** | Réponse < 2 min | 2 min |
| **Déléguer à l'agenda** | Demande > 2 min → devient une tâche datée | 30 sec |
| **Classer dans un dossier** | Pièce à conserver (contrat, facture reçue) | 15 sec |

*Critère de complétion* : inbox vide à chaque fin de session. Un email qui reste =
une tâche non transformée en rendez-vous agenda.

**Outils gratuits** : filtres/labels automatiques (Gmail/Outlook), modèles de réponses
enregistrés, désinscription agressive des newsletters non lues.

## Rituel 2 — Agenda défensif (le temps est ton seul actif)

- **Blocs de production** : 2-3 blocs de 2h/semaine marqués « occupé » — incompressible,
  c'est ton revenu.
- **Jours de rendez-vous regroupés** : ex. RDV clients uniquement mardi/jeudi — un RDV
  isolé détruit une demi-journée.
- **Buffer 15 min** entre chaque RDV (compte-rendu à chaud, déplacement).
- **Liens de prise de RDV** (Calendly ou équivalent) pour éliminer les allers-retours
  « vous êtes libre quand ? » — configurer avec créneaux limités et buffer intégré.

*Critère de complétion* : semaine type visible dans l'agenda avec blocs production +
jours RDV ; tout nouveau RDV rentre dans les cases prévues.

## Rituel 3 — Préparation de rendez-vous (fiche 5 min)

Avant chaque RDV client/prospect, remplir une fiche minimaliste :

```
Client : [NOM_CLIENT]
Objectif du RDV : (le mien / le sien)
Contexte : (historique, dernier échange, dossier en cours)
Question clé à poser :
Décision/next step attendu :
Pièces à avoir sous la main :
```

*Critère de complétion* : fiche remplie la veille ; compte-rendu de 3 lignes ajouté
après le RDV avec le next step daté.

## Rituel 4 — Échéances belges : le calendrier d'alerte

Une seule source de vérité (agenda avec rappels J-14 et J-3) pour :

| Échéance type | Fréquence | Rappel |
|---|---|---|
| Déclaration TVA (si régime normal) | Mensuelle/trimestrielle — le 20 | J-10 |
| Cotisations sociales INASTI | Trimestrielle | J-14 |
| Versements anticipés IPP/ISOC | Trimestrielle | J-14 |
| Listing annuel clients TVA | Annuelle | J-30 |
| Renouvellement assurances / contrats | Annuelle | J-60 |
| Comptes annuels SRL (dépôt BNB) | Annuelle | J-60 |

*Critère de complétion* : chaque échéance applicable est dans l'agenda avec ses deux
rappels, récurrente. Les montants/dates exacts se règlent avec le comptable —
voir `be-accounting-basics`.

## Rituel 5 — Classement documentaire (retrouver en 30 secondes)

Structure miroir de `be-bookkeeping-ops` mais pour l'administratif courant :

```
admin/
  clients/[NOM_CLIENT]/     # contrats, correspondances importantes
  fournisseurs/
  banque-assurances/
  officiel/                 # BCE, statuts, attestations, permis
  modeles/                  # templates d'emails et documents
```

Nommage : `AAAA-MM-JJ_objet.pdf`. *Critère : tout document courant retrouvé en
< 30 secondes ; rien ne vit dans la boîte mail ou sur le bureau.*

## Templates d'emails (à personnaliser avec `brand-voice-solopreneur`)

**Confirmation de RDV** : « Bonjour [Prénom], suite à notre échange, je vous propose
[date/heure]. Merci de me confirmer que cela vous convient. Bien à vous, »

**Suivi de devis (J+7)** : « Bonjour [Prénom], je me permets de revenir vers vous
concernant le devis du [date]. Souhaitez-vous que nous en discutions ? Je reste
disponible cette semaine. Bien à vous, »

**Relance document manquant** : « Bonjour [Prénom], pour finaliser [dossier], il me
manque [document]. Pourriez-vous me le transmettre avant le [date] ? Merci d'avance. »

**Refus poli** : « Bonjour [Prénom], merci pour votre proposition. Après réflexion,
je ne pourrai pas y donner suite — mon planning est complet sur cette période. Je vous
souhaite une belle réussite dans votre projet. »

## Common Pitfalls

1. **L'email comme to-do list.** Un email gardé « pour ne pas oublier » = une tâche
   invisible. Toute demande devient un RDV agenda daté, l'email est archivé.
2. **Les notifications permanentes.** Chaque interruption coûte ~20 min de refocus.
   Deux sessions email par jour suffisent pour un solo — aucun client n'exige une
   réponse en 12 minutes.
3. **RDV éparpillés.** Lundi 10h, mardi 15h, jeudi 9h = trois demi-journées tuées.
   Regrouper sur 1-2 jours, refuser poliment le reste.
4. **Zéro rappel sur les échéances « rares ».** Le listing annuel TVA ou le dépôt BNB
   s'oublient facilement — et coûtent cher. Tout va dans l'agenda récurrent, même
   l'annuel.
5. **Réinventer chaque email.** 80 % des emails d'un solo sont 5 situations types.
   Template + personnalisation = 30 secondes au lieu de 5 minutes.
6. **Classer « plus tard ».** Le document classé plus tard est perdu. 15 secondes
   maintenant, ou jamais.

## Verification Checklist

- [ ] Sessions email à heures fixes (2×/jour), notifications coupées ailleurs
- [ ] Agenda avec blocs production + jours RDV regroupés
- [ ] Lien de prise de RDV configuré (buffer inclus)
- [ ] Fiche de préparation utilisée sur les 3 derniers RDV
- [ ] Toutes les échéances BE applicables dans l'agenda avec rappels J-14/J-3
- [ ] Arborescence `admin/` créée, documents courants classés
- [ ] 4 templates d'emails sauvegardés dans l'outil mail
