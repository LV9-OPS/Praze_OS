# Matrice de compatibilité

Seules les lignes **testées** valent prise en charge (voir ADR 0002).
Chaque résultat indique le lieu du test : CI (VM QEMU), matériel de référence, ou autre machine.

## ISO live (Jalon B)

| Configuration | Firmware | Lieu | Résultat | Date | Preuve |
|---|---|---|---|---|---|
| QEMU, CPU hôte (KVM), VGA standard | BIOS | CI | démarre jusqu'à `login:` | 2026-10-22 | run 39780665394 |
| QEMU, CPU hôte (KVM), VGA standard | UEFI (OVMF) | CI | démarre jusqu'à `login:` | 2026-10-22 | run 39780665394 |
| QEMU, CPU `qemu64` (x86-64 v1, sans AVX) | BIOS | CI | en attente | — | ticket B-05 |

## Non testé

| Configuration | Statut |
|---|---|
| AMD Ryzen 7 9800X3D + Radeon RX 9070 XT (référence) | non testé |
| GPU NVIDIA | non testé |
| GPU Intel | non testé |
| Portables / GPU hybrides | non testé |
| Secure Boot | non testé (ISO non signée) |
| ARM64, GPU Apple | hors périmètre (ADR 0002) |
