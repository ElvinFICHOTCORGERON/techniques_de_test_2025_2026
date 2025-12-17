Pour les tests je pense avoir eu une bonne couverture des la première étape. Quand j'ai modifié les tests j'ai plus modifié le contenu lié à l'architecture du projet surtout avec les mocks que le nombre de test en question. Lors de l'éxécution des tests j'ai eu 96% de coverage.

Au niveau des tests de performance j'ai vu trop grand le nombre de tests j'ai donc diminué le nombre de points à tester car l'algo de delaunnay possède un complexité de n^2 ce qui prend beaucoup de trop de temps avec 10000 points.

Au niveau de ruff j'ai rencontré quelques erreur sur la manière don't j'ai écris ma doc j'ai donc désactivé l'option D dans le fichier pyproject.toml
