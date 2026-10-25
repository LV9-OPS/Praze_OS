#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Manifeste d'une ISO LV8 : métadonnées et SHA-256 de chaque fichier de l'ISO et du
# système live (airootfs.sfs). Sert à localiser les écarts entre deux constructions.
# Usage : build/iso/manifest.sh ISO SORTIE   (root requis pour conserver les propriétaires)
set -euo pipefail

iso=$(realpath "$1")
out=$(realpath -m "$2")
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir "$tmp/iso"
bsdtar -xf "$iso" -C "$tmp/iso"

sfs=$(find "$tmp/iso" -name airootfs.sfs | head -n1)
[[ -n $sfs ]] || { echo "manifest.sh : airootfs.sfs absent (image non squashfs ?)" >&2; exit 1; }
unsquashfs -q -d "$tmp/root" "$sfs" >/dev/null

manifest() {
    # Une ligne par entrée : type, droits, propriétaire, mtime, taille, chemin, puis empreinte.
    # mindepth 1 : la date du répertoire d'extraction lui-même varie à chaque exécution.
    (cd "$1" && find . -mindepth 1 -printf '%y %m %U:%G %T@ %s %p\n' | LC_ALL=C sort -k6)
    (cd "$1" && find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum)
}

{
    echo "# iso"
    manifest "$tmp/iso"
    echo "# airootfs"
    manifest "$tmp/root"
} > "$out"
wc -l "$out"
