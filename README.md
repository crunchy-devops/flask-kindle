# Application Flask pour la gestion de fichiers .mobi

Cette application Flask permet d'afficher, télécharger et supprimer des fichiers .mobi présents dans le répertoire `uploads`.

## Fonctionnalités

- Affichage des fichiers .mobi triés par date de modification (plus récents en haut)
- Téléchargement des fichiers
- Suppression des fichiers avec confirmation
- Interface responsive et moderne
- Gestion des erreurs
- Serveur accessible depuis l'extérieur (0.0.0.0:5000)

## Installation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

2. Lancez l'application :
```bash
python app.py
```

3. Accédez à l'application depuis votre navigateur :
   - Local : http://localhost:5000
   - Réseau : http://VOTRE_IP:5000

## Utilisation

1. Placez vos fichiers .mobi dans le répertoire `uploads`
2. Actualisez la page pour voir les fichiers apparaître
3. Utilisez les boutons "Télécharger" et "Supprimer" pour gérer vos fichiers

## Structure du projet

```
flask-kindle/
├── app.py              # Application Flask principale
├── requirements.txt    # Dépendances Python
├── uploads/           # Répertoire pour les fichiers .mobi
└── templates/
    ├── index.html     # Template principal
    └── error.html     # Template d'erreur
```

## Sécurité

- Validation des noms de fichiers avec `secure_filename()`
- Restriction aux fichiers .mobi uniquement
- Gestion des erreurs appropriée
- Protection contre les attaques de type path traversal

## Développement

Le code respecte les conventions PEP8 et inclut une documentation complète.
