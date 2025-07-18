# Utilisation d'une vraie base de données avec SQLAlchemy (SQLite ou MySQL)

Ce guide explique comment configurer l'application Flask pour utiliser une base de données persistante (SQLite ou MySQL) au lieu de la base en mémoire par défaut.

## 1. SQLite (fichier local)

Par défaut, si aucune variable d'environnement n'est définie, l'application utilise SQLite en mode fichier local :

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../bloomzy.db'
```

Cela créera un fichier `bloomzy.db` à la racine du projet (adapter le chemin si besoin). Le fichier sera persistant entre les redémarrages de l'application.

## 2. MySQL

Pour utiliser MySQL, installez le connecteur dans le venv :

```zsh
pip install mysqlclient
```

Définissez la variable d'environnement `SQLALCHEMY_DATABASE_URI` dans votre configuration Docker ou votre shell :

```env
SQLALCHEMY_DATABASE_URI=mysql://<user>:<password>@<host>/<database>
```

Exemple :

```env
SQLALCHEMY_DATABASE_URI=mysql://bloomzy:motdepasse@mysql/bloomzy_db
```

Remplacez `<user>`, `<password>`, `<host>`, `<database>` par vos informations. Assurez-vous que la base existe et que l'utilisateur a les droits nécessaires.


## 3. Utilisation avec Docker et variables d'environnement

Pour configurer dynamiquement la base de données (SQLite ou MySQL), utilisez la variable d'environnement `SQLALCHEMY_DATABASE_URI` dans vos fichiers `docker-compose` :

### Exemple (docker-compose.dev.yml ou prod.yml)

```yaml
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
      # Exemple SQLite local (décommenter pour activer)
      # - SQLALCHEMY_DATABASE_URI=sqlite:///../bloomzy.db
      # Exemple MySQL (décommenter et adapter pour activer)
      # - SQLALCHEMY_DATABASE_URI=mysql://user:password@mysql/bloomzy_db
```

Adaptez la chaîne selon votre environnement. Par défaut, si la variable n'est pas définie, l'application utilisera SQLite local.

**Conseils**
- Ne jamais versionner le fichier `.db` (ajoutez-le à `.gitignore`).
- Utilisez les variables d'environnement pour stocker les credentials sensibles.
- Pour la production, privilégiez MySQL ou PostgreSQL.

## 4. Documentation officielle
- [SQLAlchemy - SQLite](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html)
- [SQLAlchemy - MySQL](https://docs.sqlalchemy.org/en/20/dialects/mysql.html)
