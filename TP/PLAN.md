# Plan d'action TP techniques de test

## Objectif

L'objectif du TP est de réaliser un composant **Triangulator** et d'assurer une couverture de test complète

## Tests à réaliser

| Type de test    | Objectif                                                   | Exemple de vérification                                                                      |
| --------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Unitaires**   | Vérifier les fonctions internes (calculs, parsing binaire) | Tester les méthodes du composant `triangulation`                                             |
| **Intégration** | Vérifier la communication entre plusieurs modules          | Vérifier que le module triangulation stocke correctement le résultat dans la base de données |
| **API**         | Vérifier le bon fonctionnement des endpoints HTTP          | Appel HTTP vers `/triangulation/{pointSetId}` et vérification de la réponse JSON             |
| **Performance** | Évaluer la rapidité et l’efficacité des algorithmes        | Mesurer le temps de calcul pour 10, 1000, 10000 points                                       |

## Structure du projet

```

root/
│ README.md
│ requirements.txt
│ dev_requirements.txt
│ pyproject.toml
└───TP/
    │ Makefile
    │ point_set_manager.yml
    │ triangulator.yml
    │ PLAN.md
    │ RETEX.md
    └───src/
    │   └───triangulator/
    │       fichier lié au triangulator
    └───tests/
    │   ├───unit/
    │   │   Test unitaire du projet
    │   ├───integration/
    │   │   Tests d’intégration du projet
    │   └───performance/
    │       Test de performance du projet
    └───docs/
        Documentation générée automatiquement via pdoc3 en html
```

## Exemple de test envisagé

- Test unitaires : Tester les différentes fonctions internes du composant tel que la sortie d'un seul triangle quand il y a 3 point en entrée.

- Test d'API : tester les différents endpoint ainsi que toutes les erreurs qui peuvent être renvoyer (200,400,...) et les différents type d'entrée.

- Test d'intégration : Utilisation des mocks pour simuler les intéractions avec les différents composants (client et pointSetManager)

- Test de performance : Tester le temps d'éxécution du programme pour différent nombres de points.

## Méthodologie de travail

Utilisation du TDD pour développer le composant. Refactorer le code sans casser l'existant et utilisant ruff pour voir la qualité du code.
