#!/usr/bin/env python3
import os
import http.server
import socketserver
import webbrowser
from pathlib import Path

def demarrer_serveur():
    # Se déplacer dans le répertoire html
    html_dir = Path('html')
    os.chdir(html_dir)
    
    PORT = 8000
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(html_dir), **kwargs)
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 Serveur HTTP démarré sur http://localhost:{PORT}")
        print("📁 Servant les fichiers depuis le répertoire: html/")
        print("📊 Fichiers disponibles:")
        for file in html_dir.glob('*.html'):
            print(f"   • http://localhost:{PORT}/{file.name}")
        print("\n🛑 Pour arrêter le serveur: Ctrl+C")
        print("=" * 50)
        
        # Ouvrir le dashboard automatiquement
        webbrowser.open(f"http://localhost:{PORT}/dashboard-ventes-complet.html")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Serveur arrêté")

if __name__ == "__main__":
    demarrer_serveur()