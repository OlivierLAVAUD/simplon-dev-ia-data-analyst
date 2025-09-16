import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from pathlib import Path
import numpy as np

# Créer le répertoire html s'il n'existe pas
html_dir = Path('html')
html_dir.mkdir(exist_ok=True)

# Chargement des données
donnees = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv')

# Définition des requêtes SQL
requetes_sql = {
    'ca_total': """
        SELECT SUM(prix * qte) AS chiffre_affaires_total
        FROM donnees
    """,
    
    'ventes_par_produit': """
        SELECT 
            produit,
            SUM(qte) AS quantite_vendue,
            SUM(prix * qte) AS chiffre_affaires
        FROM donnees
        GROUP BY produit
        ORDER BY chiffre_affaires DESC
    """,
    
    'ventes_par_region': """
        SELECT 
            region,
            SUM(qte) AS quantite_vendue,
            SUM(prix * qte) AS chiffre_affaires
        FROM donnees
        GROUP BY region
        ORDER BY chiffre_affaires DESC
    """,
    
    'quantite_par_produit': """
        SELECT 
            produit,
            SUM(qte) AS quantite_vendue
        FROM donnees
        GROUP BY produit
        ORDER BY quantite_vendue DESC
    """
}

# Fonction pour exécuter les requêtes SQL avec pandas
def executer_requete_sql(requete_sql, df):
    """Exécute une requête SQL sur un DataFrame pandas"""
    # Nettoyage de la requête
    requete_sql = requete_sql.strip().replace(';', '')
    
    # Exécution selon le type de requête
    if 'SUM(prix * qte) AS chiffre_affaires_total' in requete_sql:
        result = pd.DataFrame({
            'chiffre_affaires_total': [df['prix'].mul(df['qte']).sum()]
        })
    
    elif 'GROUP BY produit' in requete_sql and 'quantite_vendue' in requete_sql and 'chiffre_affaires' in requete_sql:
        result = df.groupby('produit').agg(
            quantite_vendue=('qte', 'sum'),
            chiffre_affaires=('prix', lambda x: (x * df.loc[x.index, 'qte']).sum())
        ).reset_index()
    
    elif 'GROUP BY region' in requete_sql:
        result = df.groupby('region').agg(
            quantite_vendue=('qte', 'sum'),
            chiffre_affaires=('prix', lambda x: (x * df.loc[x.index, 'qte']).sum())
        ).reset_index()
    
    elif 'GROUP BY produit' in requete_sql and 'quantite_vendue' in requete_sql:
        result = df.groupby('produit').agg(
            quantite_vendue=('qte', 'sum')
        ).reset_index().sort_values('quantite_vendue', ascending=False)
    
    else:
        result = df
    
    return result

# Exécution des requêtes avec affichage 
print("=" * 60)
print("🔍 EXÉCUTION DES REQUÊTES SQL")
print("=" * 60)

# a. Chiffre d'affaires total
print("\n📈 REQUÊTE a - Chiffre d'affaires total:")
print(requetes_sql['ca_total'])
ca_result = executer_requete_sql(requetes_sql['ca_total'], donnees)
ca_total = ca_result['chiffre_affaires_total'].iloc[0]
print(f"✅ Résultat: {ca_total:,.2f} €")

# b. Ventes par produit (quantité + CA)
print("\n📦 REQUÊTE b - Ventes par produit (quantité + CA):")
print(requetes_sql['ventes_par_produit'])
ventes_produit = executer_requete_sql(requetes_sql['ventes_par_produit'], donnees)
print(f"✅ Résultat: {len(ventes_produit)} produits analysés")

# c. Ventes par région
print("\n🌍 REQUÊTE c - Ventes par région:")
print(requetes_sql['ventes_par_region'])
ventes_region = executer_requete_sql(requetes_sql['ventes_par_region'], donnees)
print(f"✅ Résultat: {len(ventes_region)} régions analysées")

# d. Quantité par produit
print("\n📊 REQUÊTE d - Quantité vendue par produit:")
print(requetes_sql['quantite_par_produit'])
quantite_produit = executer_requete_sql(requetes_sql['quantite_par_produit'], donnees)
print(f"✅ Résultat: {len(quantite_produit)} produits analysés")

print("\n" + "=" * 60)
print("🎨 CRÉATION DES VISUALISATIONS")
print("=" * 60)

# Création du dashboard principal avec plus de graphiques
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        '📊 CA par région', 
        '📦 Quantité vendue par région', 
        '💰 CA par produit', 
        '📈 Quantité vendue par produit',
        '🏆 Top 5 produits par CA',
        '🥇 Top 5 produits par quantité'
    ),
    specs=[
        [{"type": "pie"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}]
    ],
    vertical_spacing=0.10,
    horizontal_spacing=0.08
)

# 1. Pie chart - CA par région
fig.add_trace(
    go.Pie(
        values=ventes_region['chiffre_affaires'], 
        labels=ventes_region['region'], 
        name="CA Région",
        textinfo='label+percent+value',
        hovertemplate='<b>%{label}</b><br>CA: %{value:,.0f} €<br>Part: %{percent}<extra></extra>'
    ),
    row=1, col=1
)

# 2. Bar chart - Quantité par région
fig.add_trace(
    go.Bar(
        x=ventes_region['region'], 
        y=ventes_region['quantite_vendue'], 
        name="Quantité Région",
        marker_color='#1f77b4',
        hovertemplate='<b>%{x}</b><br>Quantité: %{y:,.0f} units<extra></extra>'
    ),
    row=1, col=2
)

# 3. Bar chart - CA par produit
fig.add_trace(
    go.Bar(
        x=ventes_produit['produit'], 
        y=ventes_produit['chiffre_affaires'], 
        name="CA Produit",
        marker_color='#2ca02c',
        hovertemplate='<b>%{x}</b><br>CA: %{y:,.0f} €<extra></extra>'
    ),
    row=2, col=1
)

# 4. Bar chart - Quantité par produit
fig.add_trace(
    go.Bar(
        x=quantite_produit['produit'], 
        y=quantite_produit['quantite_vendue'], 
        name="Quantité Produit",
        marker_color='#9467bd',
        hovertemplate='<b>%{x}</b><br>Quantité: %{y:,.0f} units<extra></extra>'
    ),
    row=2, col=2
)

# 5. Top 5 produits par CA
top5_ca_produits = ventes_produit.nlargest(5, 'chiffre_affaires')
fig.add_trace(
    go.Bar(
        x=top5_ca_produits['produit'], 
        y=top5_ca_produits['chiffre_affaires'], 
        name="Top 5 CA Produits",
        marker_color='#ff7f0e',
        hovertemplate='<b>%{x}</b><br>CA: %{y:,.0f} €<extra></extra>'
    ),
    row=3, col=1
)

# 6. Top 5 produits par quantité
top5_qte_produits = quantite_produit.nlargest(5, 'quantite_vendue')
fig.add_trace(
    go.Bar(
        x=top5_qte_produits['produit'], 
        y=top5_qte_produits['quantite_vendue'], 
        name="Top 5 Quantité Produits",
        marker_color='#e377c2',
        hovertemplate='<b>%{x}</b><br>Quantité: %{y:,.0f} units<extra></extra>'
    ),
    row=3, col=2
)

# Mise en page élégante
fig.update_layout(
    height=1200,
    width=1400,
    title_text="📈 ANALYSE COMPLÈTE DES VENTES - DASHBOARD",
    title_font_size=20,
    title_x=0.5,
    showlegend=False,
    font=dict(family="Arial", size=10),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# Amélioration des axes
fig.update_xaxes(tickangle=45)
fig.update_yaxes(tickformat=",.0f")

# Sauvegarde du dashboard principal
fig.write_html('html/dashboard-ventes-complet.html')

# Création des visualisations individuelles
visualisations = {
    'ventes-quantite-region.html': {
        'figure': px.pie(
            ventes_region, 
            values='quantite_vendue', 
            names='region', 
            title='📦 Quantité vendue par région',
            hover_data=['chiffre_affaires'],
            labels={'quantite_vendue': 'Quantité', 'chiffre_affaires': 'CA'}
        ),
        'description': 'Quantité par région'
    },
    
    'ca-region.html': {
        'figure': px.pie(
            ventes_region, 
            values='chiffre_affaires', 
            names='region',
            title='💰 Chiffre d\'affaires par région',
            hover_data=['quantite_vendue'],
            labels={'quantite_vendue': 'Quantité', 'chiffre_affaires': 'CA'}
        ),
        'description': 'CA par région'
    },
    
    'ca-produit.html': {
        'figure': px.bar(
            ventes_produit, 
            x='produit', 
            y='chiffre_affaires',
            title='📊 Chiffre d\'affaires par produit',
            hover_data=['quantite_vendue'],
            labels={'quantite_vendue': 'Quantité', 'chiffre_affaires': 'CA'},
            color='chiffre_affaires',
            color_continuous_scale='Viridis'
        ),
        'description': 'CA par produit'
    },
    
    'quantite-produit.html': {
        'figure': px.bar(
            quantite_produit, 
            x='produit', 
            y='quantite_vendue',
            title='📈 Quantité vendue par produit',
            labels={'quantite_vendue': 'Quantité vendue'},
            color='quantite_vendue',
            color_continuous_scale='Blues'
        ),
        'description': 'Quantité par produit'
    },
    
    'top5-ca-produits.html': {
        'figure': px.bar(
            top5_ca_produits, 
            x='produit', 
            y='chiffre_affaires',
            title='🏆 Top 5 produits par chiffre d\'affaires',
            labels={'chiffre_affaires': 'Chiffre d\'affaires (€)'},
            color='chiffre_affaires',
            color_continuous_scale='Oranges'
        ),
        'description': 'Top 5 produits par CA'
    },
    
    'top5-quantite-produits.html': {
        'figure': px.bar(
            top5_qte_produits, 
            x='produit', 
            y='quantite_vendue',
            title='🥇 Top 5 produits par quantité vendue',
            labels={'quantite_vendue': 'Quantité vendue'},
            color='quantite_vendue',
            color_continuous_scale='Purples'
        ),
        'description': 'Top 5 produits par quantité'
    }
}

# Sauvegarde des visualisations individuelles
for filename, config in visualisations.items():
    fig_ind = config['figure']
    fig_ind.update_layout(
        font=dict(family="Arial", size=12),
        hoverlabel=dict(bgcolor="white", font_size=12),
        xaxis_tickangle=45
    )
    fig_ind.write_html('html/' + filename)
    print(f"✅ {config['description']} sauvegardé dans {filename}")

# CORRECTION : Calcul du prix moyen correct
ventes_produit['prix_moyen'] = ventes_produit['chiffre_affaires'] / ventes_produit['quantite_vendue']
ventes_produit['prix_moyen'] = ventes_produit['prix_moyen'].replace([np.inf, -np.inf], np.nan).fillna(0)

# Trouver le produit avec le meilleur prix moyen
if not ventes_produit.empty and 'prix_moyen' in ventes_produit.columns:
    produit_meilleur_prix = ventes_produit.loc[ventes_produit['prix_moyen'].idxmax(), 'produit']
    meilleur_prix = ventes_produit['prix_moyen'].max()
else:
    produit_meilleur_prix = "N/A"
    meilleur_prix = 0

# Résumé final détaillé
print("\n" + "=" * 70)
print("🎯 RÉSUMÉ DÉTAILLÉ DE L'ANALYSE")
print("=" * 70)
print(f"💰 Chiffre d'affaires total: {ca_total:,.2f} €")
print(f"📦 Nombre total de produits: {len(ventes_produit)}")
print(f"🌍 Nombre total de régions: {len(ventes_region)}")
print(f"📊 Fichier principal: dashboard-ventes-complet.html")
print("=" * 70)

# Affichage des top performers détaillés
print("\n🏆 TOP PERFORMERS - DÉTAIL")
print("-" * 40)
print(f"📍 Meilleure région (CA): {ventes_region.nlargest(1, 'chiffre_affaires')['region'].iloc[0]} "
      f"({ventes_region.nlargest(1, 'chiffre_affaires')['chiffre_affaires'].iloc[0]:,.0f} €)")

print(f"📦 Meilleure région (Quantité): {ventes_region.nlargest(1, 'quantite_vendue')['region'].iloc[0]} "
      f"({ventes_region.nlargest(1, 'quantite_vendue')['quantite_vendue'].iloc[0]:,.0f} units)")

print(f"⭐ Meilleur produit (CA): {ventes_produit.nlargest(1, 'chiffre_affaires')['produit'].iloc[0]} "
      f"({ventes_produit.nlargest(1, 'chiffre_affaires')['chiffre_affaires'].iloc[0]:,.0f} €)")

print(f"🚀 Meilleur produit (Quantité): {quantite_produit.nlargest(1, 'quantite_vendue')['produit'].iloc[0]} "
      f"({quantite_produit.nlargest(1, 'quantite_vendue')['quantite_vendue'].iloc[0]:,.0f} units)")

# Statistiques supplémentaires CORRIGÉES
print("\n📊 STATISTIQUES SUPPLÉMENTAIRES")
print("-" * 30)
print(f"📈 Produit avec le meilleur prix moyen: {produit_meilleur_prix} ({meilleur_prix:,.2f} €/unit)")

if not ventes_produit.empty:
    print(f"📊 CA moyen par produit: {ventes_produit['chiffre_affaires'].mean():,.0f} €")
    print(f"📦 Quantité moyenne par produit: {ventes_produit['quantite_vendue'].mean():,.0f} units")
    print(f"💰 Prix moyen pondéré: {ventes_produit['chiffre_affaires'].sum() / ventes_produit['quantite_vendue'].sum():.2f} €/unit")
else:
    print("📊 Aucune donnée produit disponible")

print("=" * 70)

print(f"\n🌐 Pour visualiser les résultats: cd html && python -m http.server 8000")
print("=" * 70)