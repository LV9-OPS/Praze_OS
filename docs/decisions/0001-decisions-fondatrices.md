# ADR 0001 — Décisions fondatrices

- **Statut :** acceptée
- **Date :** 2026-10-22

## Contexte

LV8-OS démarre d'un dépôt vide. Les décisions ci-dessous sont actées par le porteur du
projet. Elles ne sont remises en cause que face à un blocage technique réel, via une
nouvelle ADR argumentée.

## Décisions

### Système
| Sujet | Choix |
|---|---|
| Base | Arch Linux |
| Paquets | Pacman, dépôt LV8 signé, Flatpak facultatif |
| Bureau | KDE Plasma personnalisé, Wayland |
| Interface LV8 | Qt 6 / QML |
| Services système | Rust, privilèges minimaux, IPC explicite et documenté |
| Tests / automatisation | Python ; shell seulement pour la construction système |
| Système de fichiers | Btrfs + snapshots |
| Noyaux | `linux` standard + `linux-lts` de secours |
| Installateur | Calamares personnalisé |
| Récupération | Mode récupération LV8 + restauration de snapshots |
| Sécurité | Chiffrement facultatif, documentation Secure Boot |
| Télémétrie | Aucune ; diagnostics uniquement volontaires |

### Produit
- Une installation, deux expériences (Gaming, Pro), bascule rapide, positions de fenêtres
  mémorisées par expérience.
- Gaming : jeux natifs et Proton (DX11/DX12), lanceurs tiers dans la limite de leur
  compatibilité réelle, incompatibilités anti-cheat signalées honnêtement, émulation séparée.
- Pro : espaces de travail dev, choix des outils à l'installation, conteneurs et IA locale facultatifs.
- Accessibilité complète ; animations désactivables.

### Projet
- GitHub + GitHub Actions ; licence GPL-3.0-or-later.
- Publication : alpha interne → bêta fermée → bêta publique ; aucun P0/P1 ouvert, récupération
  validée, artefacts signés, une semaine sans régression critique.
- Matériel de référence : AMD Ryzen 7 9800X3D + Radeon RX 9070 XT. AMD d'abord ; NVIDIA,
  Intel et portables ensuite. Les résultats d'une machine ne sont jamais généralisés.

## Ordre de priorité
1. Démarrage et installation  2. Récupération  3. Stabilité du bureau  4. Mises à jour
5. Gaming/Pro  6. Performances  7. Fonctions avancées  8. Finitions visuelles

## Conséquences
- La construction ISO (archiso) vit dans `build/`, séparée du code d'interface : un changement
  de documentation ne déclenche pas de construction ISO.
- Les dossiers de modules (`desktop/`, `services/`, `installer/`…) ne sont créés qu'avec un
  premier contenu réel.
