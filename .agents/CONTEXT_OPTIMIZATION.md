# Optimisation du Contexte & Progressive Disclosure (Two-Tier Architecture)

Ce document décrit la stratégie d'ingénierie de contexte mise en œuvre dans **The Agency** pour maximiser l'efficacité des agents, minimiser les coûts d'API et exploiter le **Prompt Caching** (Anthropic Claude Prompt Caching et OpenAI Prefix Caching).

---

## 1. Le Problème du "Full Context Saturation"

Charger 22 compétences complètes (`SKILL.md`) dans le prompt système d'un agent représente :
- **~80 000 tokens de contexte** consommés dès le premier message.
- **Phénomène de dégradation d'attention ("Lost in the Middle")** : l'agent a tendance à oublier ou halluciner des consignes situées au milieu d'un prompt colossal.
- **Coûts prohibitifs** en facturation par jeton d'entrée sur les sessions longues.

---

## 2. Architecture à Deux Niveaux (Two-Tier Progressive Disclosure)

```
                                  REQUÊTE UTILISATEUR
                                           │
                                           ▼
┌───────────────────────────────────────────────────────────────────────────────────────┐
│ TIER 1 : MANIFEST CONDENSÉ (catalog_lite.json, ~2 300 tokens)                         │
│ - Injecté systématiquement dans le prompt système                                     │
│ - Contient uniquement : nom du skill, déclencheur précis (trigger), et rôle en 1 ligne│
└──────────────────────────────────────────┬────────────────────────────────────────────┘
                                           │
                        L'agent identifie le besoin métier
                                           │
                                           ▼
┌───────────────────────────────────────────────────────────────────────────────────────┐
│ TIER 2 : CHARGEMENT ON-DEMAND (Micro-outil MCP load_skill_context)                   │
│ - Appel ciblé : load_skill_context("be-invoicing-peppol")                             │
│ - Injection dynamique du corps complet du SKILL.md (workflow, pièges, checklist)      │
│ - Isolation : un seul skill complet chargé à la fois                                  │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Optimisation du Prompt Caching (KV-Cache Prefix Stability)

Pour permettre aux fournisseurs d'IA (Anthropic Claude 3.5 / 3.7, OpenAI GPT-4o) de réutiliser le cache de prompt (facturé à -90 % par rapport aux tokens réguliers) :

1. **Préfixe immuable** : Les règles système globales et le catalogue léger `catalog_lite.json` sont placés en tout début de contexte.
2. **Ordre stable** : Les listes d'outils et de ressources sont triées alphabétiquement de manière déterministe.
3. **Variables volatiles en fin de prompt** : Les données dynamiques (date courante, historique de conversation, fiches clients) sont injectées après le point de rupture de cache.
