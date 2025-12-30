import sqlite3
import os

DB_NAME = "lgs_mibde.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # --- TABLE VENDEURS ---
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendeurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL UNIQUE,
        actif INTEGER DEFAULT 1
    )
    ''')

    # --- TABLE PRODUITS ---
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL UNIQUE,
        prix REAL NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0,
        image_path TEXT,
        categorie TEXT DEFAULT 'AUTRES'
    )
    ''')

    # --- TABLE VENTES ---
    # Ajout de transaction_id pour grouper par panier
    # Ajout de vendeurs_str pour stocker "Sofiane, Paul" sans diviser le prix
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produit_id INTEGER,
        vendeur_id INTEGER,
        quantite INTEGER NOT NULL,
        prix_total REAL NOT NULL,
        date_vente TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        transaction_id TEXT,
        vendeurs_str TEXT,
        FOREIGN KEY(produit_id) REFERENCES produits(id),
        FOREIGN KEY(vendeur_id) REFERENCES vendeurs(id)
    )
    ''')

    # --- MIGRATIONS AUTOMATIQUES (Mise à jour sans perte de données) ---
    
    # 1. Ajout colonne 'categorie' si elle manque
    try:
        cursor.execute("SELECT categorie FROM produits LIMIT 1")
    except sqlite3.OperationalError:
        print("Mise à jour BDD : Ajout colonne 'categorie'...")
        cursor.execute("ALTER TABLE produits ADD COLUMN categorie TEXT DEFAULT 'AUTRES'")
    
    # 2. Ajout colonnes pour le mode Transaction/Panier si elles manquent
    try:
        cursor.execute("SELECT transaction_id FROM ventes LIMIT 1")
    except sqlite3.OperationalError:
        print("Mise à jour BDD : Ajout colonnes 'transaction_id' et 'vendeurs_str'...")
        cursor.execute("ALTER TABLE ventes ADD COLUMN transaction_id TEXT")
        cursor.execute("ALTER TABLE ventes ADD COLUMN vendeurs_str TEXT")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()