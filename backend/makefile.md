# Documentation Makefile backend

Le Makefile du backend permet d’automatiser les tâches courantes :

- **make venv** : Crée l’environnement virtuel Python et installe les dépendances.
- **make test** : Lance tous les tests Pytest du backend.
- **make clean** : Supprime le venv et les fichiers temporaires Python (__pycache__, .pyc).

Utilisation :
```zsh
cd backend
make venv   # Initialisation
make test   # Exécution des tests
make clean  # Nettoyage
```

Ce fichier doit être mis à jour à chaque ajout de commande ou modification du Makefile.
