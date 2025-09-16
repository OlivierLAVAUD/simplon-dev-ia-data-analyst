# 📊 Analyse des Ventes - Dashboard Interactif

Dashboard interactif pour l'analyse des performances commerciales avec visualisations Plotly et traitement de données pandas.

## 🚀 Fonctionnalités

- **Analyse complète** du chiffre d'affaires
- **Ventes par produit** et **par région**
- **Visualisations interactives** avec Plotly
- **Export HTML** 
- **Requêtes SQL intégrées** 
- **Serveur HTTP intégré** pour visualisation locale

## 📋 Prérequis

- Python 3.8
- UV (gestionnaire de packages moderne)
- Git

## 🛠️ Installation & Configuration


### 1. Cloner le repository, creer et activer l'environnement
```bash
git clone https://github.com/OlivierLAVAUD/simplon-dev-ia-data-analyst.git
cd simplon-dev-ia-data-analyst
```
### 2. Installer UV 

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Créer et activer l'environnement virtuel

```bash
# Créer l'environnement virtuel
uv venv

# Activer l'environnement (Linux/Mac)
source .venv/bin/activate

# Activer l'environnement (Windows)
.venv\Scripts\activate
```

### 4.Installer les dépendances
```bash
uv pip install -r requirements.txt
```

## 🎯 Utilisation

1. Exécuter l'analyse
```bash
uv run app.py
```

2. Monter le serveur HTTP pour visualiser les résultats
```bash
cd html
uv run python -m http.server 8000
```

3. Accéder au dashboard
Cliquez sur le lien ou Ouvrez votre navigateur et allez sur :
```bash
http://localhost:8000
```
5. Navigation dans les visualisations

   - Dashboard complet : http://localhost:8000/dashboard-ventes-complet.html
   - CA par région : http://localhost:8000/ca-region.html
   - CA par produit : http://localhost:8000/ca-produit.html
   - Quantité par région : http://localhost:8000/ventes-quantite-region.html

![Dashboard](/img/image.png "Dashboard")
