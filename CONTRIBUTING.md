# Contribuer à LV8-OS

## Flux de travail

1. Une branche courte par ticket : `<type>/<id-ticket>-<sujet>` (ex. `feat/A-03-ci-base`).
2. Pull request obligatoire vers `main` (branche protégée). Pas de push direct.
3. La CI doit passer. Les changements sensibles (services privilégiés, construction ISO,
   signature, installateur, récupération) exigent une revue humaine.
4. Messages de commit descriptifs, format [Conventional Commits](https://www.conventionalcommits.org/) :
   `feat:`, `fix:`, `docs:`, `ci:`, `build:`, `test:`, `refactor:`, `chore:`.

## Tickets

Chaque ticket indique : identifiant, objectif, contexte, dépendances, fichiers concernés,
critères d'acceptation vérifiables, tests requis, risques, priorité et conditions de clôture.

| Priorité | Signification |
|---|---|
| P0 | Blocage du démarrage, de l'installation, de la sécurité ou de la récupération |
| P1 | Régression importante ou fonctionnalité essentielle inutilisable |
| P2 | Fonction secondaire ou problème avec contournement acceptable |
| P3 | Amélioration facultative, finition visuelle |

Ne pas abaisser une priorité pour faciliter une publication.

## Règles techniques

- Aucune commande privilégiée exécutée depuis QML ; passer par un service Rust via IPC documenté.
- Aucune entrée utilisateur transmise à un shell sans validation.
- Aucun secret dans le dépôt ni dans les tests de base de la CI.
- Fins de ligne LF (imposées par `.gitattributes`).
- Un test non exécuté n'est jamais déclaré réussi. Indiquer où il a tourné :
  VM, matériel de référence AMD, ou autre configuration.
- Compatibilité des jeux : consigner version du jeu, version de Proton, matériel, résultat,
  limitations et date. Aucune tentative de contournement anti-cheat.

## Contrôles avant PR

```sh
python scripts/check_repo.py
python -m unittest discover -s tests/unit -v
```

## Licence des contributions

Toute contribution est publiée sous GPL-3.0-or-later. Vérifier la licence de tout
composant, dépendance ou élément graphique ajouté.
