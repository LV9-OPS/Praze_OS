#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Construit l'ISO live/secours LV8 minimale à partir du profil releng d'archiso.
# À exécuter en root sur Arch Linux avec le paquet archiso installé.
# Usage : build/iso/build.sh [répertoire de sortie]
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
out=$(realpath -m "${1:-$here/../../out}")
releng=/usr/share/archiso/configs/releng

[[ $EUID -eq 0 ]] || { echo "build.sh : root requis (mkarchiso)" >&2; exit 1; }
[[ -d $releng ]] || { echo "build.sh : $releng absent, installer archiso" >&2; exit 1; }

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
profile=$work/profile
cp -r "$releng" "$profile"

# shortcut: profil releng non versionné ici, il suit la version d'archiso installée ;
# vendoriser le profil quand LV8 le personnalisera au-delà de l'identité.
sed -i \
    -e 's/^iso_name=.*/iso_name="lv8-os"/' \
    -e 's/^iso_label="ARCH_/iso_label="LV8_/' \
    -e 's|^iso_publisher=.*|iso_publisher="LV8-OS <https://github.com/LV9-OPS/Praze_OS>"|' \
    -e 's/^iso_application=.*/iso_application="LV8-OS Live\/Rescue"/' \
    "$profile/profiledef.sh"

for expected in '^iso_name="lv8-os"' '^iso_label="LV8_' '^iso_publisher="LV8-OS' '^iso_application="LV8-OS'; do
    grep -q "$expected" "$profile/profiledef.sh" \
        || { echo "build.sh : profiledef.sh non personnalisé ($expected)" >&2; exit 1; }
done

# Console série pour le test de démarrage automatisé (tests/vm/boot_iso.py).
# tty0 en dernier : l'écran reste la console principale (/dev/console).
mapfile -t boot_entries < <(grep -rl 'archisobasedir=%INSTALL_DIR%' \
    "$profile/syslinux" "$profile/efiboot" "$profile/grub" 2>/dev/null || true)
[[ ${#boot_entries[@]} -gt 0 ]] || { echo "build.sh : aucune entrée de démarrage trouvée" >&2; exit 1; }
sed -i 's/archisobasedir=%INSTALL_DIR%/& console=ttyS0,115200 console=tty0/' "${boot_entries[@]}"

mkdir -p "$out"
mkarchiso -v -w "$work/work" -o "$out" "$profile"

cd "$out"
pacman -Q archiso > build-info.txt
echo "SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-non défini}" >> build-info.txt
grep '^Server' /etc/pacman.d/mirrorlist >> build-info.txt || true
sha256sum -- *.iso > SHA256SUMS
cat SHA256SUMS
