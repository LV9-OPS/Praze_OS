# LV8-OS

LV8-OS est un système d'exploitation basé sur Arch Linux qui réunit, dans une seule
installation, une expérience **Gaming** et une expérience **Pro** sur KDE Plasma (Wayland).

> **État : pré-alpha — fondations du dépôt (Jalon A).**
> Aucune ISO, aucun paquet et aucun composant d'interface n'existe encore.
> Rien dans ce dépôt n'est utilisable pour installer un système.

## Décisions fondatrices

Résumé ; le détail est dans [docs/decisions/0001-decisions-fondatrices.md](docs/decisions/0001-decisions-fondatrices.md).

- Base Arch Linux, Pacman, dépôt LV8 signé, Flatpak facultatif.
- KDE Plasma personnalisé sous Wayland, interface Qt 6/QML.
- Services système en Rust, tests et automatisation en Python.
- Btrfs avec snapshots, noyau standard + noyau LTS de secours, mode récupération.
- Installateur Calamares personnalisé, chiffrement facultatif.
- Aucune télémétrie automatique.
- Matériel de référence : AMD Ryzen 7 9800X3D + Radeon RX 9070 XT.

## Feuille de route

Les jalons A à I et le backlog courant sont dans [docs/development/backlog.md](docs/development/backlog.md).
Un jalon est validé par ses critères d'acceptation, pas par une compilation réussie.

## Contrôles locaux

```sh
python scripts/check_repo.py
python -m unittest discover -s tests/unit -v
```

## Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md). Vulnérabilités : voir [SECURITY.md](SECURITY.md).

## Licence

GPL-3.0-or-later. Voir [LICENSE](LICENSE).
