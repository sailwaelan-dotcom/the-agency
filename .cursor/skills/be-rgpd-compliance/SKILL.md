---
name: be-rgpd-compliance
description: "Utilisez quand le solopreneur belge collecte des données personnelles (formulaire de contact, newsletter, clients), doit rédiger une politique de confidentialité, gérer des cookies, répondre à une demande d'accès RGPD, ou évaluer sa conformité de base avec l'APD."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [admin, rgpd, compliance, privacy, be]
  related_skills: [be-company-setup, secretary-ops, social-listening-be]
  domain: admin
  language: fr
  as_of: "2026-07"
---

# RGPD de base pour solopreneur belge

## Overview

Le RGPD s'applique dès que tu collectes une donnée personnelle — un email de contact,
une liste de newsletter, un fichier clients. En Belgique, l'autorité de contrôle est
l'**APD** (Autorité de protection des données). Ce skill couvre les obligations
**pratiques** d'un solopreneur : registre des traitements, politique de confidentialité,
bases légales, droits des personnes, cookies, et notification de violation. Il ne
remplace pas un avocat spécialisé ni un DPO — il te rend conforme sur les fondamentaux
et t'indique quand consulter.

## When to Use

- « Je lance mon site avec un formulaire de contact, je dois faire quoi côté RGPD ? »
- « Je veux envoyer une newsletter, c'est légal ? »
- « Un client me demande de supprimer ses données, je fais comment ? »
- « Cookies sur mon site — bandeau obligatoire ? »
- « J'ai perdu un fichier clients / mon site a été piraté, que dois-je faire ? »

**Ne pas utiliser pour :**
- Questions fiscales ou comptables → `be-accounting-basics`
- Veille réseaux sociaux (collecte de données publiques) → `social-listening-be`
- Contrats commerciaux détaillés → conseil juridique spécialisé

## Concepts clés (as_of 2026-07)

### Bases légales (au moins une par traitement)

| Base | Quand l'utiliser | Exemple solopreneur |
|---|---|---|
| **Consentement** | Libre, spécifique, éclairé, univoque, révocable | Case à cocher newsletter (non pré-cochée) |
| **Contrat** | Nécessaire à l'exécution du contrat | Adresse client pour facturer |
| **Obligation légale** | Imposée par la loi | Conservation factures 7 ans (TVA) |
| **Intérêt légitime** | Équilibre avec les droits de la personne | Prospection B2B ciblée (avec opt-out) |

### Obligations principales du solopreneur

1. **Registre des traitements** (art. 30) : document listant chaque traitement —
   finalité, catégories de données, destinataires, durée de conservation, mesures de
   sécurité. Obligatoire même pour les petites structures (sauf exception étroite).
2. **Politique de confidentialité** : page publique expliquant ce que tu collectes,
   pourquoi, combien de temps, et comment exercer ses droits.
3. **Réponse aux demandes de droits** : accès, rectification, effacement, portabilité,
   opposition — délai légal d'**1 mois** (extensible de 2 mois si complexe).
4. **Sécurité** : mesures proportionnées (mots de passe forts, chiffrement disque,
   accès restreint, sauvegardes).
5. **Notification de violation** : à l'APD sous **72 heures** si risque pour les
   droits et libertés ; aux personnes concernées si risque élevé.
6. **Cookies** : consentement préalable pour tout cookie non essentiel (analytics,
   marketing) — bandeau avec acceptation/refus granulaire.

### Sous-traitants (DPA)

Tout prestataire qui traite des données pour toi (hébergeur, outil email, CRM) doit
avoir un **accord de traitement de données** (DPA). Vérifier que l'outil propose un
DPA conforme RGPD avant de l'adopter — la plupart des grands outils le proposent
dans leurs conditions.

## Workflow

### 1. Cartographier tes traitements

Lister chaque endroit où tu collectes des données :
- Formulaire de contact (nom, email, message)
- Newsletter (email, consentement)
- Clients (coordonnées, historique, factures)
- Analytics site (IP, navigation)
- Réseaux sociaux (si tu exportes des données)

*Critère de complétion* : tableau rempli — pour chaque traitement : finalité, base
légale, données, durée, destinataires.

### 2. Rédiger la politique de confidentialité

Structure minimale :
- Qui est responsable (ton nom/dénomination, contact)
- Quelles données et pourquoi (par traitement)
- Base légale de chaque traitement
- Durées de conservation
- Destinataires / sous-traitants
- Droits des personnes et comment les exercer
- Coordonnées de l'APD pour plainte

*Critère de complétion* : page publiée et liée depuis le footer du site + chaque
formulaire.

### 3. Mettre en place le registre

Document interne (pas public) : même contenu que la politique mais détaillé, avec
mesures de sécurité. Format libre — l'APD propose des modèles sur son site.

*Critère de complétion* : registre rempli, daté, et mis à jour à chaque nouveau
traitement.

### 4. Gérer les cookies

- Inventaire des cookies du site (dev tools → Application → Cookies)
- Bloquer tout cookie non essentiel avant consentement
- Bandeau avec « Accepter » / « Refuser » / « Personnaliser » — pas de mur de cookies

*Critère de complétion* : aucun cookie analytics/marketing ne se dépose sans clic
positif de l'utilisateur.

### 5. Préparer les processus

- **Demande de droit** : procédure écrite pour répondre sous 1 mois (vérifier
  l'identité, localiser les données, répondre par écrit)
- **Violation** : procédure écrite pour évaluer le risque et notifier l'APD sous 72h
- **Consentement** : preuve conservée (date, contenu du formulaire, case cochée)

*Critère de complétion* : les trois procédures sont écrites et tu sais où les trouver.

## Références belges

- **APD** (autoriteprotectiondonnees.be) : modèles de registre, guides PME,
  notification de violation en ligne, formulaires de plainte
- **RGPD** (règlement UE 2016/679) : texte intégral
- **CNIL** (cnil.fr) : guides pratiques détaillés (France, mais principes identiques)
- **EDPB** : lignes directrices européennes
- Données datées : **as_of 2026-07** — vérifier les exigences en vigueur.

## Common Pitfalls

1. **Case pré-cochée.** Le consentement doit être un acte positif — une case déjà
   cochée ne vaut pas consentement.
2. **« Intérêt légitime » fourre-tout.** Cette base exige un test d'équilibre documenté
   — pas une excuse pour tout collecter.
3. **Conserver indéfiniment.** Chaque donnée a une durée de vie ; la dépasser est une
   violation. Définir des durées et purger.
4. **Ignorer les sous-traitants.** Utiliser un outil sans DPA te rend responsable de
   ses manquements.
5. **Paniquer en cas de violation.** La notification à l'APD n'est pas un aveu de
   faute — c'est une obligation légale ; ne pas notifier aggrave la sanction.
6. **Copier la politique d'un concurrent.** Ta politique doit refléter TES traitements
   réels, pas ceux d'un autre.

## Verification Checklist

- [ ] Registre des traitements rempli et daté
- [ ] Politique de confidentialité publiée et liée
- [ ] Base légale identifiée pour chaque traitement
- [ ] Bandeau cookies avec refus granulaire
- [ ] DPA signé avec chaque sous-traitant
- [ ] Procédure de réponse aux droits écrite (1 mois)
- [ ] Procédure de notification de violation écrite (72h)
- [ ] Preuves de consentement conservées

> ⚠️ **Disclaimer** : information générale (as_of 2026-07), pas un conseil juridique
> personnalisé. Le RGPD est complexe et factuel : pour toute situation spécifique
> (données sensibles, transferts hors UE, profilage), consultez un avocat spécialisé
> en protection des données ou un délégué à la protection des données (DPO) agréé
> en Belgique.
