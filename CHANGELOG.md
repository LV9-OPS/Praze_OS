# Changelog

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).

## [Non publié]

### Ajouté
- Squelette du dépôt : README, licence GPL-3.0, CONTRIBUTING, SECURITY, conventions d'édition.
- ADR 0001 : décisions fondatrices.
- Backlog initial (jalons A à I, tickets du Jalon A/B).
- Script `scripts/check_repo.py` (fichiers requis, licence, fins de ligne, clés privées) et ses tests.
- Workflow CI `ci.yml` exécutant ces contrôles.
- `build/iso/build.sh` et workflow `iso.yml` : ISO live minimale dérivée de `releng`, avec SHA256SUMS.
