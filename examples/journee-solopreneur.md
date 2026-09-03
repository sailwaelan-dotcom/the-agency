# Une journée de solopreneur belge, assisté par The Agency

Walkthrough flagship : comment un agent IA équipé des skills de ce repo enchaîne
quatre demandes typiques d'une journée de travail — sans changer d'outil, sans
quitter la conversation.

Persona de démo : **Alex**, consultant indépendant en personne physique, régime
TVA normal, installé en Belgique. Toutes les données sont fictives (placeholders).

---

## 08:30 — Le tri matinal

**Demande :**

> « Ma boîte mail déborde, je passe mes matinées dedans. Installe-moi un système
> de tri rapide. »

**Skill déclenché :** `secretary-ops`

**Extrait de sortie :**

> ### Rituel inbox — 15 minutes, 2×/jour (jamais en continu)
>
> | Créneau | Durée | Règle |
> |---|---|---|
> | 08:30 | 15 min | Trier, pas traiter : chaque mail → une action |
> | 16:30 | 15 min | Idem, puis fermeture de la boîte |
>
> Règle des 4D pour chaque message :
> 1. **Delete** — info sans suite → archivage immédiat
> 2. **Delegate** — pas ton rôle → transfert avec deadline explicite
> 3. **Defer** — >2 min → tâche datée dans l'agenda, mail classé
> 4. **Do** — <2 min → traité sur le champ
>
> Notifications coupées en dehors des deux créneaux. Objectif mesurable :
> récupérer 3-5 h/semaine sur l'administratif courant.

---

## 09:00 — Les échéances du mois

**Demande :**

> « C'est quoi mes échéances fiscales et sociales ce mois-ci ? Mets-moi des
> rappels. »

**Skill déclenché :** `be-admin-deadlines`

**Extrait de sortie :**

> ### Calendrier du mois — Alex (PP, TVA trimestrielle)
>
> | Échéance | Date | Rappels | Action |
> |---|---|---|---|
> | Déclaration TVA trimestrielle | le 20 | J-10, J-3 | Encoder via Intervat, transmettre les chiffres au comptable |
> | Cotisations sociales INASTI | fin de trimestre | J-14, J-3 | Vérifier le montant provisionnel auprès de la caisse d'assurances sociales |
> | Versement anticipé IPP | le 10 du trimestre | J-14 | Évaluer avec le comptable si un VA est opportun |
>
> Chaque échéance est créée dans l'agenda en récurrent, avec ses deux rappels.
>
> ⚠️ **Disclaimer** : information générale (as_of 2026-07), pas un conseil fiscal
> ou comptable personnalisé. Les dates et montants exacts dépendent de votre
> situation — faites valider par un comptable ou expert-comptable agréé en
> Belgique et vérifiez sur finances.belgium.be.

---

## 11:15 — Émettre une facture

**Demande :**

> « Je dois envoyer une facture de 1 500 € à [NOM_CLIENT], une SRL belge.
> Peppol obligatoire, paraît-il — je fais comment ? »

**Skill déclenché :** `be-invoicing-peppol`

**Extrait de sortie :**

> ### Facture 2026-0042 — checklist avant envoi
>
> **1. Peppol s'applique** : B2B entre assujettis belges → facture électronique
> structurée (UBL via Peppol) obligatoire depuis janvier 2026. Le PDF seul ne
> suffit plus.
>
> **2. Client vérifié** : [NOM_CLIENT] trouvé dans l'annuaire Peppol
> (directory.peppol.eu) sous son numéro d'entreprise `BE0123.456.789`.
>
> **3. Structure de la facture (mentions légales contrôlées) :**
>
> | Champ | Valeur |
> |---|---|
> | Numéro séquentiel | 2026-0042 |
> | Date d'émission | [DATE_EMISSION] |
> | Vendeur | Alex [NOM], [ADRESSE] — BCE/TVA : BE0123.456.789 |
> | Client | [NOM_CLIENT] SRL, [ADRESSE_CLIENT] — BCE/TVA : BE0123.456.789 |
> | Prestation | [DESCRIPTION_PRESTATION] |
> | Montant HTVA | 1 500,00 € |
> | TVA 21 % | 315,00 € |
> | Total TVAC | 1 815,00 € |
> | Paiement | 30 jours — compte [IBAN], communication structurée [COMMUNICATION] |
>
> **4. Envoi** : via votre Access Point (logiciel de facturation connecté Peppol),
> archivage du XML UBL + accusé de réception.
>
> ⚠️ **Disclaimer** : information générale (as_of 2026-07). Vérifiez les mentions
> obligatoires et le taux de TVA applicables à votre prestation sur
> finances.belgium.be, et faites valider votre première facture par un
> professionnel agréé.

---

## 17:00 — Le post LinkedIn

**Demande :**

> « Il faut que je poste sur LinkedIn cette semaine mais je n'ai aucune idée.
> Base-toi sur ma journée. »

**Skill déclenché :** `content-engine-be`

**Extrait de sortie :**

> ### Plan de contenu — pilier « Peppol vu du terrain »
>
> **Post pilier (mardi 08:15) — structure hook / preuve / leçon / CTA :**
>
> 1. **Hook** : « Ce matin, j'ai failli envoyer une facture non conforme. Comme
>    beaucoup d'indépendants, j'ai découvert Peppol à la dernière minute. »
> 2. **Preuve** : les 3 étapes réellement suivies (annuaire, Access Point,
>    mentions légales) — factuel, sans jargon.
> 3. **Leçon actionnable** : « Vérifiez votre client dans l'annuaire Peppol
>    AVANT d'émettre — 2 minutes qui évitent un refus. »
> 4. **CTA léger** : « Vous êtes passé à Peppol comment ? Racontez en
>    commentaire. »
>
> **Déclinaisons du même pilier (repurposing) :**
> - Jeudi : carrousel « 5 mentions légales oubliées sur une facture belge »
> - Vendredi : commentaire expert sous un post du sujet + relance newsletter
>
> Rappel de posture : partager l'expérience, renvoyer vers un professionnel
> pour le conseil — jamais l'inverse.

---

## Ce que démontre cette journée

- **Activation naturelle** : chaque demande en langage courant a chargé le bon
  skill via sa `description` (voir `tests/ACTIVATION.md`).
- **Enchaînement** : les skills se référencent (`related_skills`) — la sortie de
  l'un alimente la demande suivante.
- **Conformité intégrée** : disclaimers réglementaires, placeholders, sources
  officielles belges — pas de données réelles, pas de conseil personnalisé déguisé.
