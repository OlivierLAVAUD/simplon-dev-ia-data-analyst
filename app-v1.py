import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Chargement des données
donnees = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv')

# Calcul du chiffre d'affaires
donnees['chiffre_affaires'] = donnees['prix'] * donnees['qte']

# a. Chiffre d'affaires total
ca_total = donnees['chiffre_affaires'].sum()
print(f"Chiffre d'affaires total: {ca_total:,.2f} €")

# b. Ventes par produit
ventes_produit = donnees.groupby('produit').agg({
    'qte': 'sum',
    'chiffre_affaires': 'sum'
}).reset_index()

# c. Ventes par région
ventes_region = donnees.groupby('region').agg({
    'qte': 'sum',
    'chiffre_affaires': 'sum'
}).reset_index()

# Création des visualisations
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Chiffre d\'affaires par région', 'Quantité vendue par région', 
                   'Chiffre d\'affaires par produit', 'Top 5 produits par CA'),
    specs=[[{"type": "pie"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "bar"}]]
)

# 1. Pie chart - CA par région
fig.add_trace(
    go.Pie(values=ventes_region['chiffre_affaires'], labels=ventes_region['region'], name="CA Région"),
    row=1, col=1
)

# 2. Bar chart - Quantité par région
fig.add_trace(
    go.Bar(x=ventes_region['region'], y=ventes_region['qte'], name="Quantité Région"),
    row=1, col=2
)

# 3. Bar chart - CA par produit
fig.add_trace(
    go.Bar(x=ventes_produit['produit'], y=ventes_produit['chiffre_affaires'], name="CA Produit"),
    row=2, col=1
)

# 4. Top 5 produits par CA
top5_produits = ventes_produit.nlargest(5, 'chiffre_affaires')
fig.add_trace(
    go.Bar(x=top5_produits['produit'], y=top5_produits['chiffre_affaires'], name="Top 5 Produits"),
    row=2, col=2
)

# Mise en page
fig.update_layout(
    height=800,
    width=1000,
    title_text="Analyse des ventes de l'entreprise",
    showlegend=False
)

# Sauvegarde
fig.write_html('analyse-ventes-complete.html')

# Graphiques individuels
# 1. Ventes par région (quantité)
fig_region_qte = px.pie(donnees, values='qte', names='region', 
                       title='Quantité vendue par région')
fig_region_qte.write_html('ventes-quantite-region.html')

# 2. Ventes par région (CA)
fig_region_ca = px.pie(ventes_region, values='chiffre_affaires', names='region',
                      title='Chiffre d\'affaires par région')
fig_region_ca.write_html('ca-region.html')

# 3. Ventes par produit (CA)
fig_produit_ca = px.bar(ventes_produit, x='produit', y='chiffre_affaires',
                       title='Chiffre d\'affaires par produit')
fig_produit_ca.write_html('ca-produit.html')

print('Tous les fichiers HTML ont été générés avec succès !')
print(f'Chiffre d\'affaires total: {ca_total:,.2f} €')
