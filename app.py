import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Chargement des données
donnees = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv')

# Définition des requêtes SQL élégantes
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
    
    elif 'GROUP BY produit' in requete_sql:
        result = df.groupby('produit').agg(
            quantite_vendue=('qte', 'sum'),
            chiffre_affaires=('prix', lambda x: (x * df.loc[x.index, 'qte']).sum())
        ).reset_index()
    
    elif 'GROUP BY region' in requete_sql:
        result = df.groupby('region').agg(
            quantite_vendue=('qte', 'sum'),
            chiffre_affaires=('prix', lambda x: (x * df.loc[x.index, 'qte']).sum())
        ).reset_index()
    
    else:
        result = df
    
    return result

# Exécution des requêtes avec affichage élégant
print("🔍 EXÉCUTION DES REQUÊTES SQL")
print("=" * 50)

# a. Chiffre d'affaires total
print("\n📈 REQUÊTE a - Chiffre d'affaires total:")
print(requetes_sql['ca_total'])
ca_result = executer_requete_sql(requetes_sql['ca_total'], donnees)
ca_total = ca_result['chiffre_affaires_total'].iloc[0]
print(f"✅ Résultat: {ca_total:,.2f} €")

# b. Ventes par produit
print("\n📦 REQUÊTE b - Ventes par produit:")
print(requetes_sql['ventes_par_produit'])
ventes_produit = executer_requete_sql(requetes_sql['ventes_par_produit'], donnees)
print(f"✅ Résultat: {len(ventes_produit)} produits analysés")

# c. Ventes par région
print("\n🌍 REQUÊTE c - Ventes par région:")
print(requetes_sql['ventes_par_region'])
ventes_region = executer_requete_sql(requetes_sql['ventes_par_region'], donnees)
print(f"✅ Résultat: {len(ventes_region)} régions analysées")

print("\n" + "=" * 50)
print("🎨 CRÉATION DES VISUALISATIONS")
print("=" * 50)

# Création du dashboard principal
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        '📊 CA par région', 
        '📦 Quantité vendue par région', 
        '💰 CA par produit', 
        '🏆 Top 5 produits'
    ),
    specs=[[{"type": "pie"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "bar"}]],
    vertical_spacing=0.12,
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

# 4. Top 5 produits par CA
top5_produits = ventes_produit.nlargest(5, 'chiffre_affaires')
fig.add_trace(
    go.Bar(
        x=top5_produits['produit'], 
        y=top5_produits['chiffre_affaires'], 
        name="Top 5 Produits",
        marker_color='#ff7f0e',
        hovertemplate='<b>%{x}</b><br>CA: %{y:,.0f} €<extra></extra>'
    ),
    row=2, col=2
)

# Mise en page élégante
fig.update_layout(
    height=900,
    width=1200,
    title_text="📈 ANALYSE DES VENTES - DASHBOARD COMPLET",
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
    }
}

# Sauvegarde des visualisations individuelles
for filename, config in visualisations.items():
    fig_ind = config['figure']
    fig_ind.update_layout(
        font=dict(family="Arial", size=12),
        hoverlabel=dict(bgcolor="white", font_size=12)
    )
    fig_ind.write_html('html/'+filename)
    print(f"✅ {config['description']} sauvegardé dans {filename}")

# Résumé final
print("\n" + "=" * 60)
print("🎯 RÉSUMÉ DE L'ANALYSE")
print("=" * 60)
print(f"💰 Chiffre d'affaires total: {ca_total:,.2f} €")
print(f"📦 Nombre de produits: {len(ventes_produit)}")
print(f"🌍 Nombre de régions: {len(ventes_region)}")
print(f"📊 Fichier principal: dashboard-ventes-complet.html")
print("=" * 60)

# Affichage des top performers
print("\n🏆 TOP PERFORMERS")
print("-" * 30)
print(f"📍 Meilleure région: {ventes_region.nlargest(1, 'chiffre_affaires')['region'].iloc[0]}")
print(f"⭐ Meilleur produit: {ventes_produit.nlargest(1, 'chiffre_affaires')['produit'].iloc[0]}")
print("=" * 60)