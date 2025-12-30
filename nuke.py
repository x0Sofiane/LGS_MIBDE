import backend

def run_clear():
    print("⚠️  ATTENTION : SUPPRESSION TOTALE EN COURS...")
    
    # Appel de la fonction de reset dans backend
    backend.reset_database()
    
    print("✅  Terminé ! La base de données a été remise à zéro.")
    print("    Il n'y a plus aucun vendeur, produit ou vente.")

if __name__ == "__main__":
    run_clear()