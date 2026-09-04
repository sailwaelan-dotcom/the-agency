# Couche MCP & APIs — The Agency (`agency-be-mcp`)

Serveur [Model Context Protocol](https://modelcontextprotocol.io/) officiel pour **The Agency**, apportant aux agents IA autonomes (Claude Code, Cursor, Hermes, Kilocode) l'accès direct aux données réglementaires, administratives et fiscales belges.

---

## 🎯 Pourquoi une couche MCP pour The Agency ?

Les prompts génériques et les LLMs "nus" hallucinent fréquemment sur la réglementation belge :
- Ils inventent des échéances fiscales erronées ou oublient les versements anticipés (VA).
- Ils ne savent pas calculer un checksum Modulo 97 pour valider un numéro d'entreprise BCE.
- Ils ne peuvent pas vérifier si un client est assujetti à la TVA intracommunautaire avant facturation.
- Ils ne peuvent pas sonder l'annuaire Peppol pour savoir si un destinataire peut recevoir des factures électroniques UBL.

Le serveur `agency-be-mcp` résout ces problèmes en injectant des **outils déterministes et auditables** directement dans le context window des agents.

---

## 🛠️ Outils disponibles

| Outil | Type | Source officielle | Description |
|---|---|---|---|
| `validate_bce_number` | Local (offline) | SPF Economie | Validation Modulo 97 d'un numéro d'entreprise BCE/KBO, formatage canonique et génération du lien vers le registre public. |
| `get_be_tax_calendar` | Local (offline) | SPF Finances / INASTI | Calendrier fiscal et social belge dynamique (TVA trimestrielle Intervat, VA1-VA4, cotisations INASTI) avec alertes J-14 et J-3. |
| `calc_inasti_provision` | Local (offline) | INASTI | Simulation des cotisations sociales provisionnelles trimestrielles selon les tranches légales et plafonds en vigueur. |
| `check_vat_vies` | API REST | Commission Européenne (VIES) | Validation en temps réel d'un numéro de TVA intracommunautaire (nom officiel et adresse enregistrée). |
| `lookup_peppol_participant` | API REST | OpenPeppol Directory | Vérification de l'enregistrement d'un numéro d'entreprise pour la réception de factures électroniques Peppol. |

---

## 🔒 Principes de sécurité et robustesse

1. **Zéro dépendance externe** : Implémenté à 100 % en Python standard (`urllib.request`, `json`, `math`, `datetime`). Aucun package tiers risqué, aucune surface d'attaque superflue.
2. **APIs officielles et passives uniquement** : Aucun scraping agressif, aucun contournement de CAPTCHA, aucun stockage d'identifiants.
3. **Zéro fuite de données privées** : Les outils n'écrivent jamais sur le disque sans instruction explicite et ne journalisent aucune donnée confidentielle. Les numéros de test utilisent des placeholders factices comme `0202.239.951` (modulo valide) ou `BE0123.456.789`.

---

## 🚀 Installation & Configuration par Harness

### 1. Claude Code
Ajoutez la configuration dans votre fichier de configuration Claude Code ou importez `mcp/configs/claude_code.json` :

```json
{
  "mcpServers": {
    "agency-be": {
      "command": "python",
      "args": ["-m", "agency_be.server"],
      "env": {
        "PYTHONPATH": "mcp/servers"
      }
    }
  }
}
```

Ou en ligne de commande :
```bash
claude mcp add agency-be -- python -m agency_be.server
```

### 2. Cursor
Placez ou fusionnez `mcp/configs/cursor_mcp.json` dans votre configuration MCP Cursor (`Settings > Features > MCP`) :

```json
{
  "mcpServers": {
    "agency-be": {
      "command": "python",
      "args": ["-m", "agency_be.server"],
      "env": {
        "PYTHONPATH": "mcp/servers"
      }
    }
  }
}
```

### 3. Hermes Agent
Ajoutez la section suivante dans votre `~/.hermes/config.yaml` (ou utilisez `mcp/configs/hermes_config.yaml`) :

```yaml
mcp_servers:
  agency_be:
    command: "python"
    args:
      - "-m"
      - "agency_be.server"
    env:
      PYTHONPATH: "mcp/servers"
```

### 4. Kilocode
Importez `mcp/configs/kilocode_mcp.json` dans vos paramètres MCP Kilocode.

---

## 🧪 Tests & Validation TDD

La suite de tests automatisée valide la conformité mathématique, la gestion réseau (avec mocks hors-ligne) et la compatibilité JSON-RPC 2.0 :

```bash
python -m pytest tests/test_mcp_integration.py -v
```

Tous les tests doivent être au vert (`18 passed`) avant toute mise en production.
