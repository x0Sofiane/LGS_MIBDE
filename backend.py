import sqlite3
import uuid
from database import get_db_connection

# ==========================================
# GESTION DES VENDEURS
# ==========================================
def get_tous_vendeurs():
    conn = get_db_connection()
    vendeurs = conn.execute("SELECT * FROM vendeurs").fetchall()
    conn.close()
    return [dict(row) for row in vendeurs]

def ajouter_vendeur(nom):
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO vendeurs (nom) VALUES (?)", (nom,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def supprimer_vendeur(vendeur_id):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM vendeurs WHERE id = ?", (vendeur_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur suppression vendeur: {e}")
        return False
    finally:
        conn.close()

# ==========================================
# GESTION DES PRODUITS
# ==========================================
def ajouter_produit(nom, prix, stock, categorie, image_path=None):
    conn = get_db_connection()
    try:
        if not image_path:
            image_path = "assets/No_Image.jpg"
        if not categorie:
            categorie = "AUTRES"
            
        conn.execute(
            "INSERT INTO produits (nom, prix, stock, categorie, image_path) VALUES (?, ?, ?, ?, ?)", 
            (nom, prix, stock, categorie, image_path)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def supprimer_produit(prod_id):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM produits WHERE id = ?", (prod_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur suppression produit: {e}")
        return False
    finally:
        conn.close()

def get_produits():
    conn = get_db_connection()
    produits = conn.execute("SELECT * FROM produits ORDER BY nom ASC").fetchall()
    conn.close()
    return [dict(row) for row in produits]

def update_produit_attribut(prod_id, colonne, valeur):
    conn = get_db_connection()
    try:
        allowed = ['nom', 'prix', 'stock', 'categorie', 'image_path']
        if colonne not in allowed:
            return False

        query = f"UPDATE produits SET {colonne} = ? WHERE id = ?"
        conn.execute(query, (valeur, prod_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur update produit: {e}")
        return False
    finally:
        conn.close()

def ajuster_stock_immediat(produit_id, delta):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cur_stock = cursor.execute("SELECT stock FROM produits WHERE id = ?", (produit_id,)).fetchone()
        if not cur_stock: return False
        
        new_stock = cur_stock['stock'] + delta
        if new_stock < 0:
            return False 

        cursor.execute("UPDATE produits SET stock = ? WHERE id = ?", (new_stock, produit_id))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

# ==========================================
# VENTES & LOGIQUE PANIER
# ==========================================

def enregistrer_commande(panier, liste_vendeurs_ids):
    """
    Enregistre une commande complète sous un seul Transaction ID.
    Ne divise PAS le prix : le prix enregistré est le prix réel.
    Les vendeurs sont stockés en chaîne de caractères (ex: "Sofiane, Paul").
    """
    if not liste_vendeurs_ids:
        return False

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Générer un ID unique pour tout le panier
        transaction_id = str(uuid.uuid4())
        
        # 2. Récupérer les noms des vendeurs
        placeholders = ','.join('?' * len(liste_vendeurs_ids))
        res_vendeurs = cursor.execute(f"SELECT nom FROM vendeurs WHERE id IN ({placeholders})", liste_vendeurs_ids).fetchall()
        vendeurs_names = [r['nom'] for r in res_vendeurs]
        vendeurs_str = ", ".join(vendeurs_names)

        # 3. Enregistrer chaque ligne de produit
        for item in panier:
            p_id = item['id']
            qty = item['qty']
            
            prod = cursor.execute("SELECT prix FROM produits WHERE id = ?", (p_id,)).fetchone()
            if prod:
                # Prix total payé par le client pour cette ligne (PAS de division)
                prix_total_ligne = prod['prix'] * qty
                
                # On insère la ligne avec transaction_id et vendeurs_str
                cursor.execute('''
                    INSERT INTO ventes (produit_id, quantite, prix_total, date_vente, transaction_id, vendeurs_str)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?, ?)
                ''', (p_id, qty, prix_total_ligne, transaction_id, vendeurs_str))
        
        conn.commit()
        return True
    except Exception as e:
        print("Erreur vente:", e)
        conn.rollback()
        return False
    finally:
        conn.close()

# ==========================================
# STATISTIQUES
# ==========================================

def get_stats_tableau(date_debut, date_fin):
    """
    Stats par Produit : Somme réelle des ventes (Chiffre d'affaire réel).
    Utilisé pour le tableau "Produits" et le "Total CA".
    """
    conn = get_db_connection()
    query = '''
        SELECT p.nom, p.categorie, SUM(v.quantite) as qty_totale, SUM(v.prix_total) as ca_total
        FROM ventes v
        JOIN produits p ON v.produit_id = p.id
        WHERE v.date_vente >= ? AND v.date_vente <= ?
        GROUP BY p.id
        ORDER BY ca_total DESC
    '''
    rows = conn.execute(query, (date_debut, date_fin)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_stats_vendeurs_tableau(date_debut, date_fin):
    """
    Stats par Vendeur (CUMULATIF).
    Si une vente de 10€ a les vendeurs "A, B", A prend 10€ et B prend 10€.
    """
    conn = get_db_connection()
    
    # On récupère toutes les lignes de ventes brutes
    query = '''
        SELECT vendeurs_str, quantite, prix_total
        FROM ventes
        WHERE date_vente >= ? AND date_vente <= ?
    '''
    rows = conn.execute(query, (date_debut, date_fin)).fetchall()
    conn.close()

    # Dictionnaire d'accumulation : stats['Nom'] = { ... }
    stats = {}

    for row in rows:
        v_str = row['vendeurs_str']
        if not v_str: continue 
        
        # On sépare les vendeurs
        names = [n.strip() for n in v_str.split(',')]
        
        for name in names:
            if name not in stats:
                stats[name] = {'nom': name, 'qty_totale': 0, 'ca_total': 0.0}
            
            # On ajoute TOUT le montant à CE vendeur (duplication volontaire pour la perf individuelle)
            stats[name]['qty_totale'] += row['quantite']
            stats[name]['ca_total'] += row['prix_total']

    # Conversion en liste triée
    return sorted(list(stats.values()), key=lambda x: x['ca_total'], reverse=True)

# ==========================================
# HISTORIQUE & ANNULATION (PAR PANIER)
# ==========================================

def get_historique_transactions(limit=50):
    """
    Retourne l'historique groupé par PANIER (Transaction).
    Concatène les produits dans une seule cellule.
    """
    conn = get_db_connection()
    query = f'''
        SELECT 
            transaction_id,
            date_vente,
            vendeurs_str,
            COUNT(*) as nb_lignes,
            SUM(prix_total) as total_panier,
            GROUP_CONCAT(p.nom || ' (x' || v.quantite || ')', ', ') as details_produits
        FROM ventes v
        LEFT JOIN produits p ON v.produit_id = p.id
        WHERE transaction_id IS NOT NULL
        GROUP BY transaction_id
        ORDER BY date_vente DESC
        LIMIT {limit}
    '''
    rows = conn.execute(query).fetchall()
    conn.close()
    
    results = []
    for r in rows:
        # Formatage Date/Heure
        full_date = r['date_vente']
        parts = full_date.split(' ')
        d = parts[0]
        h = parts[1] if len(parts) > 1 else ""
        
        results.append({
            'tid': r['transaction_id'],
            'date': d,
            'heure': h,
            'vendeurs': r['vendeurs_str'],
            'produits': r['details_produits'],
            'total': r['total_panier'] if r['total_panier'] else 0.0
        })
    return results

def supprimer_transaction_complete(transaction_id):
    """
    Supprime tout un panier (via transaction_id) et remet le stock.
    """
    conn = get_db_connection()
    try:
        # 1. Récupérer les articles pour remettre le stock
        lignes = conn.execute("SELECT produit_id, quantite FROM ventes WHERE transaction_id = ?", (transaction_id,)).fetchall()
        
        for lig in lignes:
            pid = lig['produit_id']
            qty = lig['quantite']
            if pid and qty:
                conn.execute("UPDATE produits SET stock = stock + ? WHERE id = ?", (qty, pid))
        
        # 2. Supprimer les lignes de vente
        conn.execute("DELETE FROM ventes WHERE transaction_id = ?", (transaction_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur annulation transaction: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# ==========================================
# RESET ADMIN
# ==========================================
def reset_database():
    conn = get_db_connection()
    try:
        conn.execute("DROP TABLE IF EXISTS ventes")
        conn.execute("DROP TABLE IF EXISTS produits")
        conn.execute("DROP TABLE IF EXISTS vendeurs")
        conn.execute("DELETE FROM sqlite_sequence")
        conn.commit()
    except Exception as e:
        print(f"Erreur reset DB: {e}")
    finally:
        conn.close()
    
    import database
    database.init_db()
    return True