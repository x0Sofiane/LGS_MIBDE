
\# 🛒 LGS Caisse Manager



> \*\*Un système de point de vente (POS) moderne, intuitif et performant développé en Python \& PyQt6.\*\*



!\[Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)

!\[PyQt6](https://img.shields.io/badge/GUI-PyQt6-green?style=for-the-badge\&logo=qt)

!\[SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?style=for-the-badge\&logo=sqlite)

!\[Platform](https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge\&logo=windows)



---



\## 📋 Présentation



\*\*LGS Caisse Manager\*\* est une application de gestion de caisse conçue pour faciliter les événements de vente rapides. Elle se distingue par une interface sombre "Haute Visibilité", une gestion multi-vendeurs avancée et un suivi des stocks en temps réel.



L'objectif est de fluidifier l'encaissement tout en attribuant équitablement la performance aux vendeurs impliqués.



---



\## ✨ Fonctionnalités Clés



\### 🛍️ Interface de Vente (POS)

\* \*\*Design Ergonomique :\*\* Thème sombre (Dark Mode) optimisé pour réduire la fatigue visuelle.

\* \*\*Catalogue Visuel :\*\* Grille de produits avec images et indicateurs de rupture de stock.

\* \*\*Panier Dynamique :\*\* Calcul automatique, modification des quantités et suppression rapide.



\### 👥 Gestion Multi-Vendeurs (Fonctionnalité Unique)

\* \*\*Attribution Multiple :\*\* Une vente peut être réalisée par plusieurs vendeurs simultanément (ex: "Sofiane et Paul").

\* \*\*Stats Cumulatives :\*\* Chaque vendeur participant à une transaction reçoit le crédit complet du montant pour ses statistiques personnelles, encourageant le travail d'équipe.



\### 📦 Administration \& Stocks

\* \*\*Back-office complet :\*\* Ajout, modification et suppression de produits et vendeurs.

\* \*\*Images :\*\* Gestion simple des visuels produits.

\* \*\*Sécurité :\*\* Accès aux réglages protégé par code PIN (Défaut : `1234`).



\### 📊 Historique \& Annulations

\* \*\*Historique Transactionnel :\*\* Vue par "Tickets" (Paniers complets) et non par ligne.

\* \*\*Annulation Totale :\*\* Possibilité de supprimer une transaction entière. Le stock est automatiquement remis à jour.



\### 🥚 Easter Egg

\* Un mode filigrane caché est activable via une combinaison de touches secrète (`sofiane`).



---



\## 🛠️ Installation (Environnement de Développement)



Si vous souhaitez modifier le code source :



1\.  \*\*Cloner le dépôt :\*\*

&nbsp;   ```bash

&nbsp;   git clone \[https://github.com/VOTRE-PSEUDO/LGS\_Caisse.git](https://github.com/VOTRE-PSEUDO/LGS\_Caisse.git)

&nbsp;   cd LGS\_Caisse

&nbsp;   ```



2\.  \*\*Installer les dépendances :\*\*

&nbsp;   ```bash

&nbsp;   pip install PyQt6

&nbsp;   ```



3\.  \*\*Lancer l'application :\*\*

&nbsp;   ```bash

&nbsp;   python main.py

&nbsp;   ```



---



\## 📦 Création de l'exécutable (.exe)



Pour transformer ce projet en logiciel Windows autonome (sans avoir besoin d'installer Python sur l'ordinateur cible).



\### 1. Prérequis

Assurez-vous d'avoir le logo `logo.ico` à la racine du projet.



Installez \*\*PyInstaller\*\* :

```bash

pip install pyinstaller

```


\### 2. Compilation



Lancez cette commande dans votre terminal à la racine du projet :



```powershell

python -m PyInstaller --noconsole --onefile --icon=logo.ico --name="LGS\_Caisse" main.py

```



\### 3. Distribution (Important)



Le fichier `LGS\_Caisse.exe` sera généré dans le dossier `dist/`.

Pour que le logiciel fonctionne sur un autre PC, vous devez fournir un dossier contenant :



\* 📁 `LGS\_Caisse.exe`

\* 📁 Le dossier `assets/` (pour les images)

\* 📄 Le fichier `lgs\_mibde.db` (votre base de données)



---



\## 📂 Structure des Fichiers



\* \*\*`main.py`\*\* : Point d'entrée. Initialise la BDD et lance l'interface.

\* \*\*`interface.py`\*\* : Contient toute l'interface graphique (Fenêtres, Tableaux, CSS).

\* \*\*`backend.py`\*\* : Logique métier (Calculs, communication BDD, Transactions).

\* \*\*`database.py`\*\* : Gestion de la structure SQLite (Création tables, migrations).

\* \*\*`assets/`\*\* : Dossier contenant les images des produits et le logo.



---



\## 👤 Auteur



Projet développé par Sofiane Aibibaouen pour le MIBDE de Paris Cité.



---



```



```

