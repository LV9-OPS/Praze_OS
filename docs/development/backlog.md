# Backlog LV8-OS

Source de vérité temporaire en attendant la migration vers GitHub Issues (ticket A-05).

## Audit initial — 2026-10-22

**État réel :** dossier `F:\PRAZE-OS` vide, aucun dépôt Git, aucun fichier, aucun remote.

**Environnement de développement constaté (Windows 11) :**

| Outil | État |
|---|---|
| Git 2.55 | présent (identité configurée en local du dépôt) |
| Python 3.10 | présent |
| Rust / Cargo 1.98 | présent |
| GitHub CLI `gh` | absent |
| Qt 6 / QML | absent |
| WSL, Docker | absents |
| QEMU, archiso, pacman | absents |

**Conséquence :** aucune construction d'ISO, aucun test en VM et aucun build QML n'est
possible sur ce poste en l'état. Ils doivent tourner en CI (runner Linux, conteneur
`archlinux`) ou sur une machine Arch.

**Risques prioritaires :**
1. Pas d'environnement Arch local → Jalon B dépend entièrement de la CI ou d'une machine Arch.
2. Dépôt GitHub inexistant → pas de protection de branche, pas de canal sécurité opérationnel.
3. Développement sous Windows → risque de CRLF dans les scripts (mitigé par `.gitattributes`
   et `check_repo.py`).

## Jalons

| Jalon | Objet | État |
|---|---|---|
| A | Fondations du dépôt | en cours |
| B | Construction ISO reproductible | non commencé |
| C | Installation et récupération | non commencé |
| D | Bureau LV8 initial | non commencé |
| E | Expériences Gaming et Pro | non commencé |
| F | Validation matérielle | non commencé |
| G | Alpha interne | non commencé |
| H | Bêta fermée | non commencé |
| I | Bêta publique | non commencé |

## Tickets

### A-01 — Squelette du dépôt et contrôles de conventions — P1 — **fait**
- **Objectif :** dépôt Git initialisé avec documents de base et un contrôle automatique.
- **Fichiers :** `README.md`, `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`,
  `.gitignore`, `.gitattributes`, `.editorconfig`, `docs/`, `scripts/check_repo.py`, `tests/unit/`.
- **Critères :** `python scripts/check_repo.py` sort 0 ; tests unitaires verts ; LICENSE = texte GPL-3.0 officiel.
- **Clôture :** commit initial sur `main`.

### A-02 — Workflow CI de base — P1 — **fait** (runs verts sur `ddbf15b` et `3698756`)
- **Objectif :** `.github/workflows/ci.yml` lance `check_repo.py` et les tests unitaires sur chaque PR.
- **Dépendances :** A-01, A-05.
- **Critères :** permissions `contents: read` ; actions épinglées par SHA ; job vert sur une PR réelle.
- **Risques :** SHA d'action à vérifier lors du premier run.
- **Clôture :** premier run vert visible sur GitHub.

### A-03 — Configurer l'identité Git et faire le commit initial — P1 — **fait**
- **Dépendances :** A-01. Action du mainteneur (identité et autorisation de commit).
- **Critères :** `git log` montre le commit initial avec l'identité réelle du mainteneur.

### A-04 — CODE_OF_CONDUCT.md et SUPPORT.md — P2
- **Objectif :** adopter un code de conduite (ex. Contributor Covenant 2.1, CC-BY-4.0) et décrire
  les canaux de support.
- **Critères :** texte officiel copié depuis sa source, licence vérifiée ; contact de modération réel.

### A-05 — Créer le dépôt GitHub et le protéger — P0 pour la publication — **en cours**
- **Fait :** dépôt privé `LV9-OPS/Praze_OS` créé, `main` poussé le 2026-10-22.
- **Reste :** protection de `main`, signalement privé, Dependabot (action du mainteneur).
- **Objectif :** dépôt GitHub `lv8-os`, branche `main` protégée (PR + CI obligatoires),
  signalement privé de vulnérabilités activé, Dependabot pour les actions.
- **Dépendances :** A-03. Action du mainteneur (compte GitHub).
- **Critères :** push direct sur `main` refusé ; onglet *Report a vulnerability* visible ;
  SECURITY.md mis à jour comme opérationnel.

### A-06 — Modèles d'issues et de PR — P2
- **Objectif :** `.github/ISSUE_TEMPLATE/` (bug avec priorité P0–P3 et matériel, compatibilité jeu)
  et `PULL_REQUEST_TEMPLATE.md`.
- **Critères :** champs obligatoires : matériel, VM/réel, version, étapes de reproduction.

### B-01 — Profil archiso minimal LV8 — P0 — **en cours**
- **Objectif :** `build/iso/` dérivé du profil `releng` d'archiso, sans personnalisation de bureau.
- **Implémentation :** `build/iso/build.sh` copie `releng` et ne change que l'identité
  (`profiledef.sh`) ; workflow `.github/workflows/iso.yml`.
- **Dépendances :** A-02. Nécessite un runner Linux (conteneur `archlinux:latest`).
- **Critères :** `mkarchiso` produit une ISO en CI ; SHA-256 publié comme artefact ; journaux conservés en cas d'échec.
- **Tests :** construction CI ; démarrage vérifié séparément (B-02).
- **Risques :** taille et durée du job ; filtrer sur `build/iso/**`.

### B-02 — Test de démarrage de l'ISO en QEMU — P0 — **en cours**
- **Dépendances :** B-01.
- **Implémentation :** `tests/vm/boot_iso.py` (QEMU, BIOS et OVMF) ; job `boot-iso` de `iso.yml` ;
  `build.sh` ajoute `console=ttyS0,115200 console=tty0` aux entrées de démarrage.
- **Limite :** démarrage en VM seulement ; ne valide ni le matériel de référence ni Secure Boot.
- **Critères :** l'ISO démarre en QEMU (UEFI via OVMF et BIOS) et atteint un shell ; détection
  automatique par la console série ; journaux archivés.

### B-04 — Construction reproductible — P1
- **Objectif :** épingler l'image `archlinux` par digest et une date du dépôt Arch Archive.
- **Dépendances :** B-01.
- **Critères :** deux constructions du même commit donnent la même SHA-256, ou les écarts sont documentés.

### B-03 — Documentation de construction — P1
- **Dépendances :** B-01.
- **Critères :** `docs/development/build.md` permet de reconstruire l'ISO sur une machine Arch.
