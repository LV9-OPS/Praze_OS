# ADR 0002 — Politique de compatibilité matérielle

- **Statut :** acceptée
- **Date :** 2026-10-25
- **Complète :** ADR 0001

## Contexte

Le projet exige la compatibilité la plus large techniquement possible en CPU et en GPU,
sans supposer un fabricant, avec détection à l'exécution et repli logiciel, et sans jamais
déclarer compatible une configuration non testée. LV8-OS repose sur Arch Linux (ADR 0001),
ce qui fixe une partie des limites.

## Décisions

### CPU
| Cible | Statut | Raison |
|---|---|---|
| x86-64 AMD et Intel | **pris en charge** | seule architecture officielle d'Arch Linux |
| Niveau minimal | **x86-64 de base (v1)** | aucun paquet LV8 ne doit exiger SSE4, AVX, AVX2 ou AVX-512 |
| ARM64 | **hors périmètre** | Arch Linux ARM est un projet distinct (autres paquets, autre cycle) ; Proton cible x86-64. Réévaluation après la bêta. |
| x86 32 bits | **non pris en charge** | abandonné par Arch Linux |

Règles :
- Les composants Rust sont compilés pour `x86_64-unknown-linux-gnu` sans `target-cpu=native`
  ni `target-feature` imposé ; une accélération optionnelle passe par
  `is_x86_feature_detected!` avec un chemin de repli.
- Aucun dépôt optimisé (`x86-64-v3`…) n'est activé par défaut.
- La CI démarre l'ISO avec un modèle de CPU QEMU `qemu64` (sans SSE4/AVX) pour détecter
  les instructions illégales.

### GPU
| Fabricant | Pilote | Statut |
|---|---|---|
| AMD Radeon (GCN et plus récents) | `amdgpu` + Mesa (RADV, radeonsi) | cible prioritaire, référence RX 9070 XT |
| Intel intégré et Arc | `i915` / `xe` + Mesa (ANV, iris) | prévu (Jalon F) |
| NVIDIA Turing et plus récents | `nvidia-open` | prévu (Jalon F) |
| NVIDIA plus anciens | `nouveau` / NVK | au mieux, sans garantie pour le jeu |
| Aucun GPU accéléré | Mesa `llvmpipe` / `lavapipe` | repli logiciel : bureau utilisable, jeu non pris en charge |
| GPU Apple | — | hors périmètre (lié à ARM64 / Asahi Linux) |

Règles :
- Seules des API multi-fabricants sont utilisées par LV8 : Vulkan, OpenGL, Wayland.
  CUDA et ROCm restent des options facultatives (IA locale), jamais une dépendance.
- L'installateur choisit les pilotes selon les identifiants PCI détectés ; une détection
  ratée retombe sur Mesa, jamais sur un écran noir.
- Le bureau doit démarrer en rendu logiciel si l'accélération échoue.

### Déclaration de compatibilité
Une configuration n'est « prise en charge » que si elle figure comme testée dans
[docs/compatibility/matrix.md](../compatibility/matrix.md), avec date, version et résultat.
Tout le reste est « non testé », même si cela fonctionne en théorie.

## Conséquences
- La compatibilité CPU ancien est testée en CI dès le Jalon B.
- Les tests GPU réels exigent du matériel : NVIDIA, Intel et portables restent non testés
  tant qu'aucune machine de test n'est disponible.
