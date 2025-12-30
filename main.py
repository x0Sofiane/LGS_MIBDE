import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from interface import MainWindow
import database  # <-- 1. On importe le module database

if __name__ == "__main__":
    # 2. On initialise/met à jour la BDD avant de lancer l'interface
    # Cela va exécuter le script de migration et créer la colonne 'categorie' si elle manque.
    print("Vérification de la base de données...")
    database.init_db()

    # 3. Création de l'instance de l'application (Obligatoire pour PyQt)
    app = QApplication(sys.argv)

    # 4. Chargement de notre fenêtre principale
    window = MainWindow()
    window.show()

    # 5. Lancement de la boucle d'événements (Garde la fenêtre ouverte)
    sys.exit(app.exec())