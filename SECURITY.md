# Politique de sécurité

## Signaler une vulnérabilité

**Ne publiez pas de détails exploitables dans un ticket public.**

Canal prévu : signalement privé GitHub (onglet *Security* → *Report a vulnerability*).

> **État : NON OPÉRATIONNEL.** Le dépôt n'est pas encore publié sur GitHub ; le
> signalement privé doit y être activé (ticket A-05). Tant que ce n'est pas fait,
> ce canal n'existe pas.

## Versions prises en charge

Aucune version publiée. LV8-OS est en pré-alpha.

## Chaîne de confiance (cible)

- Artefacts accompagnés de sommes SHA-256 **et** d'une signature. Une somme seule
  vérifie l'intégrité, pas l'identité de l'auteur.
- Clé de signature gérée hors des runners CI ordinaires ; procédure de rotation
  et de récupération documentée avant toute bêta.
- Paquets du dépôt LV8 signés selon les mécanismes Pacman.
