import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QStackedWidget, QGridLayout, 
    QScrollArea, QFrame, QMessageBox, QTabWidget, QHeaderView, 
    QTableWidget, QTableWidgetItem, QInputDialog, QDialog, QCheckBox,
    QSizePolicy, QGraphicsDropShadowEffect, QGraphicsOpacityEffect,
    QFileDialog, QComboBox, QAbstractItemView, QDateEdit, QSpinBox,
    QAbstractSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QDate, QRect, QTimer
from PyQt6.QtGui import QPixmap, QFont, QAction, QIntValidator, QDoubleValidator, QIcon, QColor, QPainter, QPen

import backend

# ==========================================
# THEME HAUTE VISIBILITÉ (DARK)
# ==========================================

DARK_THEME = """
/* --- GLOBAL --- */
* { font-family: 'Segoe UI', 'Roboto', sans-serif; }

QMainWindow, QWidget { 
    background-color: #121212; 
    color: #E0E0E0; 
}

/* --- TEXTE --- */
QLabel { color: #E0E0E0; font-size: 14px; }
QLabel#Title { font-size: 22px; font-weight: bold; color: #ffffff; margin-bottom: 10px; }
QLabel#BigTotal { font-size: 36px; font-weight: bold; color: #10b981; } /* Vert gros */
QLabel#LabelTotal { font-size: 16px; font-weight: bold; color: #aaaaaa; }
QLabel#BestSeller { font-size: 18px; font-weight: bold; color: #fbbf24; margin-bottom: 10px; } /* Or */

/* --- INPUTS & COMBOS --- */
QLineEdit, QComboBox, QDateEdit, QSpinBox {
    background-color: #333333; 
    border: 1px solid #555555;
    border-radius: 6px; 
    padding: 6px; 
    color: #ffffff;
    font-size: 14px;
}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus {
    border: 2px solid #3b82f6; 
    background-color: #404040;
}

/* --- BOUTONS GENERIQUES --- */
QPushButton {
    background-color: #333333;
    border: 1px solid #555555;
    color: #ffffff;
    border-radius: 6px; 
    padding: 8px 16px; 
    font-weight: 600;
}
QPushButton:hover { 
    background-color: #444444; 
    border-color: #777777; 
}
QPushButton:pressed { background-color: #222222; }

/* --- BOUTONS QUANTITE PANIER (+ et -) --- */
QPushButton#QtyBtn {
    background-color: #4a4a4a;
    border: 1px solid #666;
    color: #ffffff;
    font-size: 18px; 
    font-weight: bold;
    border-radius: 4px;
    padding: 0px;
}
QPushButton#QtyBtn:hover {
    background-color: #3b82f6;
    border: 1px solid #3b82f6;
}

/* --- BOUTON POUBELLE LIGNE --- */
QPushButton#TrashBtn {
    background-color: #3f1a1a;
    border: 1px solid #ef4444;
    color: #ef4444;
    border-radius: 4px;
    font-size: 14px;
}
QPushButton#TrashBtn:hover {
    background-color: #ef4444;
    color: white;
}

/* --- BOUTONS ACTIONS --- */
QPushButton#PrimaryButton { background-color: #3b82f6; border: none; color: white; }
QPushButton#PrimaryButton:hover { background-color: #2563eb; }

QPushButton#SuccessButton { background-color: #10b981; border: none; color: white; font-weight: bold; font-size: 16px; }
QPushButton#SuccessButton:hover { background-color: #059669; }

QPushButton#DangerButton { background-color: #ef4444; border: none; color: white; font-weight: bold; }
QPushButton#DangerButton:hover { background-color: #dc2626; }

QPushButton#SellerBtn { 
    text-align: left; 
    background-color: #1e1e1e;
    border: 1px solid #3b82f6; 
    padding-left: 15px;
}

/* --- CARTE PRODUIT --- */
QFrame#ProductCard { 
    background-color: #2D2D2D; 
    border: 2px solid #444444; 
    border-radius: 12px; 
}
QFrame#ProductCard:hover {
    border: 2px solid #3b82f6; 
    background-color: #353535;
}
QLabel#ProdName { color: #ffffff; font-weight: bold; font-size: 14px; border: none; background: transparent; }
QLabel#ProdPrice { color: #3b82f6; font-weight: 800; font-size: 15px; border: none; background: transparent; }
QLabel#ProdStock { color: #aaaaaa; font-size: 12px; border: none; background: transparent; }

/* --- PANNEAUX LATERAUX --- */
QFrame#Panel { background-color: #1e1e1e; border: 1px solid #333333; border-radius: 8px; }
QFrame#CartContainer { background-color: #1a1a1a; border-left: 2px solid #333333; }
QFrame#CartItem { 
    background-color: #252525; 
    border: 1px solid #333333; 
    border-radius: 6px; 
    margin-bottom: 4px;
}

/* --- TABLEAUX --- */
QTableWidget {
    background-color: #1e1e1e; 
    gridline-color: #444444; 
    color: #ffffff; 
    border: 1px solid #444444;
}
QHeaderView::section {
    background-color: #333333; 
    color: #ffffff; 
    border: none; 
    padding: 8px; 
    font-weight: bold;
}
QTableWidget::item { border-bottom: 1px solid #333333; }

/* --- ONGLETS --- */
QTabWidget::pane { border: none; }
QTabBar::tab {
    background: #333333; 
    color: #aaaaaa; 
    padding: 10px 25px; 
    margin-right: 5px; 
    border-top-left-radius: 8px; 
    border-top-right-radius: 8px;
    font-weight: bold;
}
QTabBar::tab:selected { background: #3b82f6; color: white; }

/* SCROLLBAR */
QScrollBar:vertical { border: none; background: #121212; width: 10px; margin: 0; }
QScrollBar::handle:vertical { background: #555; min-height: 20px; border-radius: 5px; }
QScrollBar::handle:vertical:hover { background: #777; }
"""

# ==========================================
# WIDGETS PERSONNALISÉS
# ==========================================

# --- OVERLAY FILIGRANE "SOFIANE" ---
class WatermarkOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.hide() 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        color = QColor(255, 0, 0, 80)
        painter.setPen(color)
        
        font = QFont("Arial", 50, QFont.Weight.Bold)
        font.setItalic(True)
        painter.setFont(font)
        
        painter.rotate(-30)
        
        gap_x = 300
        gap_y = 150
        
        for x in range(-1000, self.width() + 1000, gap_x):
            for y in range(-1000, self.height() + 1000, gap_y):
                painter.drawText(x, y, "Sofiane")

class SellerSelectionDialog(QDialog):
    def __init__(self, vendeurs, selected_ids, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sélection Vendeurs")
        self.setFixedSize(300, 400)
        self.setStyleSheet(DARK_THEME)
        
        layout = QVBoxLayout(self)
        
        lbl = QLabel("Qui participe à la vente ?")
        lbl.setStyleSheet("font-weight: bold; font-size: 16px; color: white; margin-bottom: 10px;")
        layout.addWidget(lbl)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self.checklist_layout = QVBoxLayout(container)
        self.checklist_layout.setSpacing(5)
        
        self.checkboxes = {}
        for v in vendeurs:
            cb = QCheckBox(v['nom'])
            cb.setStyleSheet("QCheckBox { font-size: 14px; padding: 5px; } QCheckBox::indicator { width: 20px; height: 20px; }")
            cb.setCursor(Qt.CursorShape.PointingHandCursor)
            if v['id'] in selected_ids:
                cb.setChecked(True)
            self.checkboxes[v['id']] = cb
            self.checklist_layout.addWidget(cb)
            
        self.checklist_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)

        btn_box = QHBoxLayout()
        btn_none = QPushButton("Tout décocher")
        btn_none.clicked.connect(self.deselect_all)
        
        btn_ok = QPushButton("Valider")
        btn_ok.setObjectName("PrimaryButton")
        btn_ok.clicked.connect(self.accept)
        
        btn_box.addWidget(btn_none)
        btn_box.addWidget(btn_ok)
        layout.addLayout(btn_box)

    def deselect_all(self):
        for cb in self.checkboxes.values():
            cb.setChecked(False)

    def get_selected_ids(self):
        return [vid for vid, cb in self.checkboxes.items() if cb.isChecked()]

# --- HISTORIQUE (PANIER) ---
class HistoryDialog(QDialog):
    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Historique des Transactions (Paniers)")
        self.resize(1000, 600) # Plus large pour voir les produits
        self.setStyleSheet(DARK_THEME)
        
        layout = QVBoxLayout(self)
        
        lbl = QLabel("Derniers Paniers Vendus")
        lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
        layout.addWidget(lbl)

        self.table = QTableWidget()
        cols = ["Date", "Heure", "Vendeurs", "Contenu du Panier", "Total (€)", "Action"]
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents) 
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) # Colonne contenu élastique
        
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setStyleSheet("alternate-background-color: #252525;")
        layout.addWidget(self.table)
        
        btn_close = QPushButton("Fermer")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        # On utilise la nouvelle fonction backend par transaction
        transactions = backend.get_historique_transactions(limit=50) 
        
        self.table.setRowCount(len(transactions))
        for i, t in enumerate(transactions):
            self.table.setItem(i, 0, QTableWidgetItem(t['date']))
            self.table.setItem(i, 1, QTableWidgetItem(t['heure']))
            self.table.setItem(i, 2, QTableWidgetItem(t['vendeurs']))
            
            # Contenu (Liste des produits concaténés)
            item_contenu = QTableWidgetItem(t['produits'])
            item_contenu.setToolTip(t['produits']) # Tooltip si trop long
            self.table.setItem(i, 3, item_contenu)
            
            # Total
            item_total = QTableWidgetItem(f"{t['total']:.2f} €")
            item_total.setForeground(QColor("#10b981")) # Vert
            item_total.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            self.table.setItem(i, 4, item_total)
            
            # Bouton Suppression Panier
            btn_del = QPushButton("Tout Annuler")
            btn_del.setObjectName("DangerButton")
            btn_del.setFixedSize(100, 30)
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.clicked.connect(lambda _, tid=t['tid']: self.delete_full_cart(tid))
            
            w = QWidget()
            wl = QHBoxLayout(w); wl.setContentsMargins(0,0,0,0); wl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            wl.addWidget(btn_del)
            self.table.setCellWidget(i, 5, w)

    def delete_full_cart(self, transaction_id):
        if QMessageBox.question(self, "Annuler Panier", 
                              "⚠️ Voulez-vous supprimer ce PANIER COMPLET ?\n\nLe stock de tous les articles sera remis.", 
                              QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            if backend.supprimer_transaction_complete(transaction_id):
                self.load_data()
                self.data_changed.emit()
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de supprimer le panier.")

class CartItemWidget(QFrame):
    qty_changed = pyqtSignal(int)
    item_removed = pyqtSignal()

    def __init__(self, product_data, current_qty):
        super().__init__()
        self.setObjectName("CartItem") 
        self.product = product_data
        self.pid = product_data['id']
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)
        
        lbl_name = QLabel(product_data['nom'])
        lbl_name.setStyleSheet("font-weight: bold; color: white; border: none; font-size: 13px;")
        lbl_name.setWordWrap(True)
        layout.addWidget(lbl_name, stretch=1)

        qty_layout = QHBoxLayout()
        qty_layout.setSpacing(2)

        self.btn_minus = QPushButton("-")
        self.btn_minus.setObjectName("QtyBtn")
        self.btn_minus.setFixedSize(28, 28)
        self.btn_minus.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_minus.clicked.connect(self.decrease_qty)

        self.spin_qty = QSpinBox()
        self.spin_qty.setFixedSize(45, 28)
        self.spin_qty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_qty.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spin_qty.setRange(0, 999)
        self.spin_qty.setValue(current_qty)
        self.spin_qty.setReadOnly(True) 
        self.spin_qty.setStyleSheet("font-weight: bold; font-size: 14px; border: 1px solid #555;")

        self.btn_plus = QPushButton("+")
        self.btn_plus.setObjectName("QtyBtn")
        self.btn_plus.setFixedSize(28, 28)
        self.btn_plus.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_plus.clicked.connect(self.increase_qty)

        qty_layout.addWidget(self.btn_minus)
        qty_layout.addWidget(self.spin_qty)
        qty_layout.addWidget(self.btn_plus)
        layout.addLayout(qty_layout)

        self.lbl_price = QLabel(f"{(product_data['prix'] * current_qty):.2f} €")
        self.lbl_price.setStyleSheet("color: #3b82f6; font-weight: bold; border: none; font-size: 13px;")
        self.lbl_price.setFixedWidth(60)
        self.lbl_price.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.lbl_price)

        self.btn_trash = QPushButton("🗑️")
        self.btn_trash.setObjectName("TrashBtn")
        self.btn_trash.setFixedSize(30, 28)
        self.btn_trash.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_trash.clicked.connect(self.delete_item)
        layout.addWidget(self.btn_trash)

    def update_display(self):
        qty = self.spin_qty.value()
        total = self.product['prix'] * qty
        self.lbl_price.setText(f"{total:.2f} €")

    def increase_qty(self):
        if backend.ajuster_stock_immediat(self.pid, -1):
            new_val = self.spin_qty.value() + 1
            self.spin_qty.setValue(new_val)
            self.update_display()
            self.qty_changed.emit(-1) 
        else:
            self.btn_plus.setStyleSheet("background-color: #ef4444; border: 1px solid #ef4444;")
            QTimer.singleShot(300, lambda: self.btn_plus.setStyleSheet(""))

    def decrease_qty(self):
        current = self.spin_qty.value()
        if current > 1:
            backend.ajuster_stock_immediat(self.pid, 1)
            new_val = current - 1
            self.spin_qty.setValue(new_val)
            self.update_display()
            self.qty_changed.emit(1)
        elif current == 1:
            self.delete_item()

    def delete_item(self):
        qty = self.spin_qty.value()
        if qty > 0:
            backend.ajuster_stock_immediat(self.pid, qty)
            self.qty_changed.emit(qty)
        self.item_removed.emit()

class ModernProductCard(QFrame):
    clicked = pyqtSignal(dict)
    def __init__(self, produit):
        super().__init__()
        self.setObjectName("ProductCard") 
        self.produit = produit
        self.current_stock = produit.get('stock', 0)
        self.setFixedSize(170, 230) 

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        self.lbl_img = QLabel()
        self.lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_img.setStyleSheet("background-color: transparent; border: none;")
        self.load_image(produit.get('image_path'))
        layout.addWidget(self.lbl_img, stretch=1)

        lbl_nom = QLabel(produit.get('nom', 'Inconnu'))
        lbl_nom.setObjectName("ProdName")
        lbl_nom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_nom.setWordWrap(True)
        layout.addWidget(lbl_nom)

        bottom_layout = QHBoxLayout()
        lbl_prix = QLabel(f"{produit.get('prix', 0):.2f} €")
        lbl_prix.setObjectName("ProdPrice")
        
        self.lbl_stock = QLabel()
        self.lbl_stock.setObjectName("ProdStock")
        self.update_stock_label() 

        bottom_layout.addWidget(lbl_prix)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.lbl_stock)
        layout.addLayout(bottom_layout)

    def load_image(self, path):
        final_path = path if path and os.path.exists(path) else "assets/No_Image.jpg"
        pixmap = QPixmap(final_path)
        if not pixmap.isNull():
            self.lbl_img.setPixmap(pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.lbl_img.setText("📷")
            self.lbl_img.setStyleSheet("color: #555; font-size: 40px; border: none; background: transparent;")

    def update_stock_label(self):
        if self.current_stock <= 0:
            self.lbl_stock.setText("RUPTURE")
            self.lbl_stock.setStyleSheet("color: #ef4444; font-size: 11px; font-weight: bold; border: none; background: transparent;")
            self.setCursor(Qt.CursorShape.ForbiddenCursor)
            self.setStyleSheet("QFrame#ProductCard { border: 2px solid #ef4444; background-color: rgba(239, 68, 68, 0.1); }")
        else:
            self.lbl_stock.setText(f"Stock: {self.current_stock}")
            self.lbl_stock.setStyleSheet("color: #aaaaaa; font-size: 12px; border: none; background: transparent;")
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.setStyleSheet("QFrame#ProductCard { background-color: #2D2D2D; border: 2px solid #444444; } QFrame#ProductCard:hover { border: 2px solid #3b82f6; background-color: #353535; }")

    def adjust_visual_stock(self, delta):
        self.current_stock += delta
        self.update_stock_label()

    def mousePressEvent(self, event):
        if self.current_stock > 0 and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.produit)

# ==========================================
# FENETRE PRINCIPALE
# ==========================================

class MainWindow(QMainWindow):
    data_changed_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LGS - MIBDE")
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet(DARK_THEME)

        self.secret_input = ""
        self.overlay = WatermarkOverlay(self)
        self.overlay.resize(self.size()) 

        self.panier_widgets = {} 
        self.product_cards = {} 
        self.saved_seller_ids = [] 
        self.is_loading_data = False 
        self.current_image_path = None 
        self.stats_rows_data = [] 

        self.reset_timer = QTimer()
        self.reset_timer.setSingleShot(True)
        self.reset_timer.timeout.connect(self.reset_total_display)

        self.data_changed_signal.connect(self.on_data_changed_by_admin)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.init_pos_screen()
        self.init_admin_screen()

        self.stack.setCurrentWidget(self.page_pos)
        self.refresh_sellers_button_label()

    def keyPressEvent(self, event):
        txt = event.text().lower()
        if txt:
            self.secret_input += txt
        
        if len(self.secret_input) > 15:
            self.secret_input = self.secret_input[-15:]

        if self.secret_input.endswith("sofiane"):
            if self.overlay.isVisible():
                self.overlay.hide()
            else:
                self.overlay.show()
                self.overlay.raise_() 
            self.secret_input = ""

        super().keyPressEvent(event)

    def resizeEvent(self, event):
        self.overlay.resize(self.size())
        super().resizeEvent(event)

    def on_data_changed_by_admin(self):
        self.refresh_pos_grid()
        if self.stack.currentWidget() == self.page_admin and self.adm_tabs.currentWidget() == self.tab_stats:
            self.load_stats_data()

    # ==========================
    # 1. ÉCRAN POS (VENTE)
    # ==========================
    def init_pos_screen(self):
        self.page_pos = QWidget()
        main_layout = QHBoxLayout(self.page_pos)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- GAUCHE : CATALOGUE ---
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(20, 20, 20, 10)
        left_layout.setSpacing(15)

        header = QHBoxLayout()
        header.setSpacing(15)
        
        self.btn_vendeurs = QPushButton("Sélectionner Vendeurs ▾")
        self.btn_vendeurs.setObjectName("SellerBtn")
        self.btn_vendeurs.setFixedWidth(280)
        self.btn_vendeurs.setMinimumHeight(45)
        self.btn_vendeurs.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_vendeurs.clicked.connect(self.open_seller_dialog)
        header.addWidget(self.btn_vendeurs)
        
        header.addStretch()

        btn_history = QPushButton("📜 Historique")
        btn_history.setMinimumHeight(45)
        btn_history.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_history.clicked.connect(self.open_history)
        header.addWidget(btn_history)
        
        btn_admin = QPushButton("🔧 Admin")
        btn_admin.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_admin.setMinimumHeight(45)
        btn_admin.clicked.connect(self.request_admin_access)
        header.addWidget(btn_admin)
        
        left_layout.addLayout(header)

        self.pos_tabs = QTabWidget()
        self.category_grids = {} 
        self.pos_categories = ["TOUT", "NOUILLE", "SUCRE", "SALE", "BOISSONS", "AUTRES"]
        self.admin_categories_list = ["NOUILLE", "SUCRE", "SALE", "BOISSONS", "AUTRES"]
        
        for cat in self.pos_categories:
            tab = QWidget()
            t_layout = QVBoxLayout(tab)
            t_layout.setContentsMargins(5, 15, 5, 0)
            
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("border: none; background: transparent;")
            
            grid_cont = QWidget()
            grid = QGridLayout(grid_cont)
            grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            grid.setSpacing(15)
            
            self.category_grids[cat] = grid
            scroll.setWidget(grid_cont)
            t_layout.addWidget(scroll)
            self.pos_tabs.addTab(tab, cat)
            
        left_layout.addWidget(self.pos_tabs)

        # --- DROITE : PANIER ---
        right_container = QFrame()
        right_container.setObjectName("CartContainer")
        right_container.setFixedWidth(460) 
        
        shadow_panel = QGraphicsDropShadowEffect()
        shadow_panel.setBlurRadius(20)
        shadow_panel.setColor(QColor(0,0,0,100))
        right_container.setGraphicsEffect(shadow_panel)
        
        r_layout = QVBoxLayout(right_container)
        r_layout.setContentsMargins(15, 40, 15, 20)
        r_layout.setSpacing(15)
        
        lbl_panier = QLabel("🛒 Panier")
        lbl_panier.setObjectName("Title")
        r_layout.addWidget(lbl_panier)

        scroll_c = QScrollArea()
        scroll_c.setWidgetResizable(True)
        scroll_c.setStyleSheet("border: none; background: transparent;")
        
        self.cart_container_widget = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_container_widget)
        self.cart_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cart_layout.setSpacing(8)
        
        scroll_c.setWidget(self.cart_container_widget)
        r_layout.addWidget(scroll_c)

        total_frame = QFrame()
        total_frame.setStyleSheet("background-color: #252525; border-radius: 8px; padding: 15px; border: 1px solid #444;")
        t_layout = QHBoxLayout(total_frame)
        
        lbl_tot_txt = QLabel("TOTAL :")
        lbl_tot_txt.setStyleSheet("font-weight: bold; color: #aaa; border:none; background:transparent; font-size: 16px;")
        self.lbl_total = QLabel("0.00 €")
        self.lbl_total.setStyleSheet("font-size: 32px; font-weight: bold; color: #3b82f6; border:none; background:transparent;")
        self.lbl_total.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        t_layout.addWidget(lbl_tot_txt)
        t_layout.addStretch()
        t_layout.addWidget(self.lbl_total)
        r_layout.addWidget(total_frame)

        btns_layout = QHBoxLayout()
        btns_layout.setSpacing(10)
        
        btn_cancel = QPushButton("🗑️ Vider")
        btn_cancel.setObjectName("DangerButton")
        btn_cancel.setMinimumHeight(55)
        btn_cancel.clicked.connect(self.annuler_panier)
        
        self.btn_pay = QPushButton("✅ ENCAISSER")
        self.btn_pay.setObjectName("SuccessButton")
        self.btn_pay.setMinimumHeight(55)
        self.btn_pay.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_pay.clicked.connect(self.valider_vente)

        btns_layout.addWidget(btn_cancel, 1)
        btns_layout.addWidget(self.btn_pay, 3)
        r_layout.addLayout(btns_layout)

        main_layout.addWidget(left_container)
        main_layout.addWidget(right_container)
        self.stack.addWidget(self.page_pos)
        
        self.refresh_pos_grid()

    # --- LOGIQUE VENDEURS ---
    def open_seller_dialog(self):
        vendeurs = backend.get_tous_vendeurs()
        dlg = SellerSelectionDialog(vendeurs, self.saved_seller_ids, self)
        if dlg.exec():
            self.saved_seller_ids = dlg.get_selected_ids()
            self.refresh_sellers_button_label()

    def refresh_sellers_button_label(self):
        vendeurs = backend.get_tous_vendeurs()
        selected_names = [v['nom'] for v in vendeurs if v['id'] in self.saved_seller_ids]
        
        if not selected_names:
            self.btn_vendeurs.setText("⚠️ Sélectionner Vendeurs ▾")
            self.btn_vendeurs.setStyleSheet("text-align: left; padding-left: 15px; border: 1px solid #eab308; color: #eab308;")
        elif len(selected_names) == 1:
            self.btn_vendeurs.setText(f"👤 {selected_names[0]} ▾")
            self.btn_vendeurs.setStyleSheet("text-align: left; padding-left: 15px; border: 1px solid #3b82f6; color: white;")
        else:
            self.btn_vendeurs.setText(f"👥 {len(selected_names)} Vendeurs actifs ▾")
            self.btn_vendeurs.setStyleSheet("text-align: left; padding-left: 15px; border: 1px solid #3b82f6; color: white;")

    # --- LOGIQUE HISTORIQUE ---
    def open_history(self):
        dlg = HistoryDialog(self)
        dlg.data_changed.connect(self.on_data_changed_by_admin)
        dlg.exec()

    # --- LOGIQUE PRODUITS & PANIER ---
    def refresh_pos_grid(self):
        self.product_cards.clear()
        for grid in self.category_grids.values():
            while grid.count():
                w = grid.takeAt(0).widget()
                if w: w.deleteLater()
        
        produits = backend.get_produits()
        counters = {k: {'r':0, 'c':0} for k in self.category_grids}
        
        for p in produits:
            cat_db = p.get('categorie', 'AUTRES')
            if cat_db not in self.admin_categories_list: cat_db = "AUTRES"
            
            card_all = ModernProductCard(p)
            card_all.clicked.connect(self.add_to_cart)
            self._add_card_to_specific_grid("TOUT", card_all, counters)
            self._register_card_ref(p['id'], card_all)

            if cat_db != "TOUT" and cat_db in self.category_grids:
                card_cat = ModernProductCard(p)
                card_cat.clicked.connect(self.add_to_cart)
                self._add_card_to_specific_grid(cat_db, card_cat, counters)
                self._register_card_ref(p['id'], card_cat)

    def _register_card_ref(self, pid, card):
        if pid not in self.product_cards:
            self.product_cards[pid] = []
        self.product_cards[pid].append(card)

    def update_local_stock_display(self, pid, delta):
        if pid in self.product_cards:
            for card in self.product_cards[pid]:
                card.adjust_visual_stock(delta)

    def _add_card_to_specific_grid(self, category_name, card_widget, counters_dict):
        if category_name not in self.category_grids: return
        grid = self.category_grids[category_name]
        r = counters_dict[category_name]['r']
        c = counters_dict[category_name]['c']
        grid.addWidget(card_widget, r, c)
        
        counters_dict[category_name]['c'] += 1
        if counters_dict[category_name]['c'] >= 5:
            counters_dict[category_name]['c'] = 0
            counters_dict[category_name]['r'] += 1

    def add_to_cart(self, p):
        if self.reset_timer.isActive():
            self.reset_timer.stop()
            self.reset_total_display()

        if not self.saved_seller_ids:
            QMessageBox.warning(self, "Oups", "Veuillez sélectionner au moins un vendeur !")
            self.open_seller_dialog()
            return

        pid = p['id']
        
        if pid in self.panier_widgets:
            self.panier_widgets[pid].increase_qty()
        else:
            if backend.ajuster_stock_immediat(pid, -1):
                item_widget = CartItemWidget(p, 1)
                item_widget.qty_changed.connect(lambda delta: self.update_local_stock_display(pid, delta))
                item_widget.qty_changed.connect(self.calculate_total)
                item_widget.item_removed.connect(lambda: self.remove_cart_item(pid))
                
                self.cart_layout.insertWidget(0, item_widget)
                self.panier_widgets[pid] = item_widget
                self.calculate_total()
                self.update_local_stock_display(pid, -1)
            else:
                if pid in self.product_cards:
                    for c in self.product_cards[pid]:
                        c.setStyleSheet("QFrame#ProductCard { border: 2px solid #ef4444; }")
                        QTimer.singleShot(300, lambda card=c: card.update_stock_label())

    def remove_cart_item(self, pid):
        if self.reset_timer.isActive():
            self.reset_timer.stop()
            self.reset_total_display()

        if pid in self.panier_widgets:
            w = self.panier_widgets.pop(pid)
            w.deleteLater()
            self.calculate_total()

    def calculate_total(self):
        total = 0.0
        has_items = False
        for w in self.panier_widgets.values():
            qty = w.spin_qty.value()
            price = w.product['prix']
            total += (qty * price)
            has_items = True
        
        self.lbl_total.setText(f"{total:.2f} €")
        if not self.reset_timer.isActive():
            self.lbl_total.setStyleSheet("font-size: 32px; font-weight: bold; color: #3b82f6; border:none; background:transparent;")
        
        self.btn_pay.setEnabled(has_items)

    def annuler_panier(self):
        if self.reset_timer.isActive():
            self.reset_timer.stop()
            self.reset_total_display()

        if not self.panier_widgets: return
        for pid, w in self.panier_widgets.items():
            qty = w.spin_qty.value()
            if qty > 0:
                backend.ajuster_stock_immediat(pid, qty)
                self.update_local_stock_display(pid, qty)
        
        self.panier_widgets.clear()
        while self.cart_layout.count():
            item = self.cart_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        self.calculate_total()

    def valider_vente(self):
        if not self.panier_widgets: return
        
        data = []
        for pid, w in self.panier_widgets.items():
            qty = w.spin_qty.value()
            if qty > 0:
                data.append({'id': pid, 'qty': qty})
        
        if not data: return

        current_total_text = self.lbl_total.text()

        if backend.enregistrer_commande(data, self.saved_seller_ids):
            self.panier_widgets.clear()
            while self.cart_layout.count():
                item = self.cart_layout.takeAt(0)
                if item.widget(): item.widget().deleteLater()
            
            self.lbl_total.setText(f"OK {current_total_text}")
            self.lbl_total.setStyleSheet("font-size: 32px; font-weight: bold; color: #10b981; border:none; background:transparent;")
            self.btn_pay.setEnabled(False) 
            
            self.reset_timer.start(2500)

        else:
            QMessageBox.critical(self, "Erreur", "Echec lors de l'enregistrement.")

    def reset_total_display(self):
        self.lbl_total.setText("0.00 €")
        self.lbl_total.setStyleSheet("font-size: 32px; font-weight: bold; color: #3b82f6; border:none; background:transparent;")
        self.btn_pay.setEnabled(False)

    # ==========================
    # 2. ADMIN
    # ==========================
    def request_admin_access(self):
        code, ok = QInputDialog.getText(self, "Admin", "Code d'accès :", QLineEdit.EchoMode.Password)
        if ok and code == "1234":
            self.refresh_admin_ui()
            self.stack.setCurrentWidget(self.page_admin)
        elif ok:
            QMessageBox.warning(self, "Erreur", "Code incorrect")

    def init_admin_screen(self):
        self.page_admin = QWidget()
        layout = QVBoxLayout(self.page_admin)
        layout.setContentsMargins(30, 30, 30, 30)
        
        h = QHBoxLayout()
        btn_back = QPushButton("← Retour Vente")
        btn_back.setFixedWidth(150)
        btn_back.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_pos))
        
        lbl_adm = QLabel("Panneau Administration")
        lbl_adm.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        
        h.addWidget(btn_back)
        h.addStretch()
        h.addWidget(lbl_adm)
        layout.addLayout(h)

        self.adm_tabs = QTabWidget()
        self.adm_tabs.setIconSize(QSize(20, 20))
        
        self.tab_team = QWidget()
        self.setup_team_tab()
        self.adm_tabs.addTab(self.tab_team, "👥 Équipe")
        
        self.tab_stock = QWidget()
        self.setup_stock_tab()
        self.adm_tabs.addTab(self.tab_stock, "📦 Stocks")
        
        self.tab_stats = QWidget()
        self.setup_stats_tab()
        self.adm_tabs.addTab(self.tab_stats, "📊 Performance")

        layout.addWidget(self.adm_tabs)
        self.stack.addWidget(self.page_admin)
        self.adm_tabs.currentChanged.connect(self.refresh_admin_ui)

    def refresh_admin_ui(self):
        idx = self.adm_tabs.currentIndex()
        if idx == 0: self.load_team_data()
        elif idx == 1: self.load_stock_data()
        elif idx == 2: self.load_stats_data()
        self.refresh_sellers_button_label()

    # --- TAB EQUIPE ---
    def setup_team_tab(self):
        l = QVBoxLayout(self.tab_team)
        l.setContentsMargins(0, 20, 0, 0)
        
        add_frame = QFrame()
        add_frame.setObjectName("Panel")
        hl = QHBoxLayout(add_frame)
        hl.setContentsMargins(15, 15, 15, 15)
        
        self.inp_new_seller = QLineEdit()
        self.inp_new_seller.setPlaceholderText("Nom du nouveau vendeur...")
        self.inp_new_seller.setMinimumWidth(300)
        
        btn_add = QPushButton("Ajouter")
        btn_add.setObjectName("PrimaryButton")
        btn_add.setFixedWidth(100)
        btn_add.clicked.connect(self.add_seller)
        
        hl.addWidget(self.inp_new_seller)
        hl.addWidget(btn_add)
        hl.addStretch()
        l.addWidget(add_frame)

        self.tbl_team = QTableWidget()
        self.tbl_team.setColumnCount(3)
        self.tbl_team.setHorizontalHeaderLabels(["ID", "Nom", "Action"])
        self.tbl_team.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tbl_team.verticalHeader().setVisible(False)
        self.tbl_team.setShowGrid(False)
        self.tbl_team.setAlternatingRowColors(True)
        self.tbl_team.setStyleSheet("alternate-background-color: #252525;")
        l.addWidget(self.tbl_team)

    def load_team_data(self):
        vendeurs = backend.get_tous_vendeurs()
        self.tbl_team.setRowCount(len(vendeurs))
        for i, v in enumerate(vendeurs):
            self.tbl_team.setItem(i, 0, QTableWidgetItem(str(v['id'])))
            self.tbl_team.setItem(i, 1, QTableWidgetItem(v['nom']))
            
            btn_del = QPushButton("Supprimer")
            btn_del.setObjectName("DangerButton")
            btn_del.setFixedSize(100, 30)
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.clicked.connect(lambda _, vid=v['id']: self.delete_seller(vid))
            
            w = QWidget()
            wl = QHBoxLayout(w); wl.setContentsMargins(0,0,0,0); wl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            wl.addWidget(btn_del)
            self.tbl_team.setCellWidget(i, 2, w)

    def add_seller(self):
        if self.inp_new_seller.text():
            backend.ajouter_vendeur(self.inp_new_seller.text())
            self.inp_new_seller.clear()
            self.load_team_data()

    def delete_seller(self, vid):
        if QMessageBox.question(self, "Confirmer", "Supprimer ce vendeur ?", 
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            backend.supprimer_vendeur(vid)
            self.load_team_data()

    # --- TAB STOCKS (Avec Recherche) ---
    def setup_stock_tab(self):
        l = QVBoxLayout(self.tab_stock)
        l.setContentsMargins(0, 20, 0, 0)
        
        add_group = QFrame()
        add_group.setObjectName("Panel")
        hl = QHBoxLayout(add_group)
        hl.setSpacing(15)
        hl.setContentsMargins(15, 15, 15, 15)
        
        self.btn_img_select = QPushButton("📷 Image")
        self.btn_img_select.setFixedWidth(100)
        self.btn_img_select.clicked.connect(self.select_image_file)
        self.current_image_path = None

        self.inp_prod_nom = QLineEdit()
        self.inp_prod_nom.setPlaceholderText("Nom du produit")
        
        self.cmb_prod_cat = QComboBox()
        self.cmb_prod_cat.addItems(self.admin_categories_list)
        self.cmb_prod_cat.setCurrentText("AUTRES")
        self.cmb_prod_cat.setFixedWidth(130)

        self.inp_prod_prix = QLineEdit()
        self.inp_prod_prix.setPlaceholderText("Prix (€)")
        self.inp_prod_prix.setFixedWidth(80)
        self.inp_prod_prix.setValidator(QDoubleValidator(0.0, 999.0, 2))
        
        self.inp_prod_stock = QLineEdit()
        self.inp_prod_stock.setPlaceholderText("Stock")
        self.inp_prod_stock.setFixedWidth(80)
        self.inp_prod_stock.setValidator(QIntValidator(0, 9999))

        btn_add = QPushButton("Ajouter")
        btn_add.setObjectName("PrimaryButton")
        btn_add.setFixedWidth(100)
        btn_add.clicked.connect(self.adm_add_prod)
        
        hl.addWidget(self.btn_img_select)
        hl.addWidget(self.inp_prod_nom)
        hl.addWidget(self.cmb_prod_cat)
        hl.addWidget(self.inp_prod_prix)
        hl.addWidget(self.inp_prod_stock)
        hl.addWidget(btn_add)
        l.addWidget(add_group)
        
        lbl_info = QLabel("💡 Tout est automatique : changez une valeur dans le tableau et appuyez sur ENTRÉE pour sauvegarder.")
        lbl_info.setStyleSheet("color: #eab308; font-style: italic; margin: 5px 0; font-weight: bold;")
        l.addWidget(lbl_info)

        # BARRE DE RECHERCHE STOCK
        search_stock_frame = QHBoxLayout()
        
        self.txt_search_stock = QLineEdit()
        self.txt_search_stock.setPlaceholderText("🔍 Rechercher produit dans le stock...")
        self.txt_search_stock.textChanged.connect(self.filter_stock_table)
        
        self.cmb_filter_stock = QComboBox()
        self.cmb_filter_stock.addItem("Toutes Catégories")
        self.cmb_filter_stock.addItems(self.admin_categories_list)
        self.cmb_filter_stock.currentIndexChanged.connect(self.filter_stock_table)
        self.cmb_filter_stock.setFixedWidth(180)
        
        search_stock_frame.addWidget(self.txt_search_stock)
        search_stock_frame.addWidget(self.cmb_filter_stock)
        l.addLayout(search_stock_frame)

        self.tbl_stock = QTableWidget()
        cols = ["ID", "Img", "Nom", "Catégorie", "Prix", "Stock", "Suppr."]
        self.tbl_stock.setColumnCount(len(cols))
        self.tbl_stock.setHorizontalHeaderLabels(cols)
        
        header = self.tbl_stock.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) 
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed) 
        self.tbl_stock.setColumnWidth(1, 60)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed) 
        self.tbl_stock.setColumnWidth(6, 80)

        self.tbl_stock.verticalHeader().setVisible(False)
        self.tbl_stock.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.tbl_stock.setAlternatingRowColors(True)
        self.tbl_stock.setStyleSheet("alternate-background-color: #252525;")
        self.tbl_stock.itemChanged.connect(self.on_stock_item_changed)
        
        l.addWidget(self.tbl_stock)

    def filter_stock_table(self):
        search_txt = self.txt_search_stock.text().lower()
        cat_filter = self.cmb_filter_stock.currentText()
        
        for i in range(self.tbl_stock.rowCount()):
            # Nom (Item)
            item_nom = self.tbl_stock.item(i, 2)
            nom_txt = item_nom.text().lower() if item_nom else ""
            
            # Categorie (Widget QComboBox)
            widget_cat = self.tbl_stock.cellWidget(i, 3)
            cat_txt = widget_cat.currentText() if widget_cat else ""
            
            match_search = search_txt in nom_txt
            match_cat = (cat_filter == "Toutes Catégories") or (cat_txt == cat_filter)
            
            if match_search and match_cat:
                self.tbl_stock.setRowHidden(i, False)
            else:
                self.tbl_stock.setRowHidden(i, True)

    def select_image_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.jpg *.jpeg)")
        if fname:
            self.current_image_path = fname
            self.btn_img_select.setText("✅ OK")
            self.btn_img_select.setStyleSheet("border: 1px solid #10b981; color: white;")

    def load_stock_data(self):
        self.is_loading_data = True
        self.tbl_stock.clearContents()
        prods = backend.get_produits()
        self.tbl_stock.setRowCount(len(prods))
        
        for i, p in enumerate(prods):
            item_id = QTableWidgetItem(str(p['id']))
            item_id.setFlags(Qt.ItemFlag.NoItemFlags) 
            self.tbl_stock.setItem(i, 0, item_id)
            
            btn_img = QPushButton()
            path = p.get('image_path', 'assets/No_Image.jpg')
            if not os.path.exists(path): path = 'assets/No_Image.jpg'
            pix = QPixmap(path)
            if not pix.isNull():
                icon = QIcon(pix)
                btn_img.setIcon(icon)
                btn_img.setIconSize(QSize(30, 30))
            else:
                btn_img.setText("📷")
            btn_img.setFlat(True)
            btn_img.setStyleSheet("border: none;")
            btn_img.clicked.connect(lambda _, pid=p['id']: self.change_product_image(pid))
            self.tbl_stock.setCellWidget(i, 1, btn_img)

            self.tbl_stock.setItem(i, 2, QTableWidgetItem(p['nom']))
            
            cmb = QComboBox()
            cmb.blockSignals(True)
            cmb.addItems(self.admin_categories_list)
            current_cat = p.get('categorie', 'AUTRES')
            if current_cat in self.admin_categories_list:
                cmb.setCurrentText(current_cat)
            else:
                cmb.setCurrentText("AUTRES")
            cmb.blockSignals(False)
            cmb.currentIndexChanged.connect(lambda idx, pid=p['id'], c=cmb: self.update_product_category_combo(pid, c))
            self.tbl_stock.setCellWidget(i, 3, cmb)
            
            self.tbl_stock.setItem(i, 4, QTableWidgetItem(str(p['prix'])))
            self.tbl_stock.setItem(i, 5, QTableWidgetItem(str(p['stock'])))
            
            btn_del = QPushButton("Supprimer")
            btn_del.setObjectName("DangerButton")
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.clicked.connect(lambda _, pid=p['id']: self.delete_product(pid))
            
            w = QWidget()
            wl = QHBoxLayout(w); wl.setContentsMargins(0,0,0,0); wl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            wl.addWidget(btn_del)
            self.tbl_stock.setCellWidget(i, 6, w)

        self.is_loading_data = False 
        self.filter_stock_table() 

    def update_product_category_combo(self, pid, combo_widget):
        if self.is_loading_data: return
        new_cat = combo_widget.currentText()
        if backend.update_produit_attribut(pid, "categorie", new_cat):
            self.data_changed_signal.emit() 
            self.filter_stock_table() 
        else:
            QMessageBox.warning(self, "Erreur", "Sauvegarde échouée.")

    def change_product_image(self, pid):
        fname, _ = QFileDialog.getOpenFileName(self, "Changer l'image", "", "Images (*.png *.jpg *.jpeg)")
        if fname:
            if backend.update_produit_attribut(pid, "image_path", fname):
                self.load_stock_data()
                self.data_changed_signal.emit() 

    def delete_product(self, pid):
        if QMessageBox.question(self, "Supprimer", "Voulez-vous supprimer ce produit ?", 
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            if backend.supprimer_produit(pid):
                self.load_stock_data()
                self.data_changed_signal.emit() 

    def adm_add_prod(self):
        nom = self.inp_prod_nom.text().strip()
        cat = self.cmb_prod_cat.currentText()
        img = self.current_image_path 
        try:
            px_txt = self.inp_prod_prix.text().replace(',', '.')
            if not px_txt: px_txt = "0"
            px = float(px_txt)
            stk_txt = self.inp_prod_stock.text()
            if not stk_txt: stk_txt = "0"
            stk = int(stk_txt)
            
            if not nom: return

            if backend.ajouter_produit(nom, px, stk, cat, img):
                self.inp_prod_nom.clear()
                self.inp_prod_prix.clear()
                self.inp_prod_stock.clear()
                self.current_image_path = None
                self.btn_img_select.setText("📷 Image")
                self.btn_img_select.setStyleSheet("")
                self.load_stock_data()
                self.data_changed_signal.emit() 
            else:
                QMessageBox.warning(self, "Erreur", "Nom déjà pris ?")
        except ValueError:
            pass

    def on_stock_item_changed(self, item):
        if self.is_loading_data: return
        row = item.row()
        col = item.column()
        try:
            id_item = self.tbl_stock.item(row, 0)
            if not id_item: return
            prod_id = int(id_item.text())
            new_val = item.text()
            
            success = False
            if col == 2: 
                success = backend.update_produit_attribut(prod_id, "nom", new_val)
            elif col == 4: 
                val = float(new_val.replace(',', '.'))
                success = backend.update_produit_attribut(prod_id, "prix", val)
            elif col == 5: 
                val = int(new_val)
                success = backend.update_produit_attribut(prod_id, "stock", val)
            
            if success:
                self.data_changed_signal.emit() 
        except ValueError:
            self.load_stock_data()

    # --- TAB STATS (TABLEAUX ONGLET) ---
    def setup_stats_tab(self):
        l = QVBoxLayout(self.tab_stats)
        l.setContentsMargins(0, 10, 0, 0)
        
        # --- Total CA Frame (Haut) ---
        total_frame = QFrame()
        total_frame.setStyleSheet("background-color: #1a1a1a; border-radius: 10px; border: 1px solid #333;")
        l_total = QVBoxLayout(total_frame)
        l_total.setContentsMargins(20, 15, 20, 15)
        
        lbl_titre_tot = QLabel("CHIFFRE D'AFFAIRES TOTAL (PÉRIODE)")
        lbl_titre_tot.setObjectName("LabelTotal")
        lbl_titre_tot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_grand_total = QLabel("0.00 €")
        self.lbl_grand_total.setObjectName("BigTotal")
        self.lbl_grand_total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        l_total.addWidget(lbl_titre_tot)
        l_total.addWidget(self.lbl_grand_total)
        l.addWidget(total_frame)
        
        # --- Filtres ---
        filter_frame = QFrame()
        filter_frame.setObjectName("Panel")
        h_filt = QHBoxLayout(filter_frame)
        h_filt.setContentsMargins(15, 10, 15, 10)
        
        lbl_from = QLabel("Du :")
        self.date_start = QDateEdit()
        self.date_start.setCalendarPopup(True)
        self.date_start.setDate(QDate(QDate.currentDate().year(), QDate.currentDate().month(), 1))
        
        lbl_to = QLabel("Au :")
        self.date_end = QDateEdit()
        self.date_end.setCalendarPopup(True)
        self.date_end.setDate(QDate.currentDate())
        
        btn_refresh = QPushButton("Actualiser")
        btn_refresh.setObjectName("PrimaryButton")
        btn_refresh.setFixedWidth(120)
        btn_refresh.clicked.connect(self.load_stats_data)
        
        h_filt.addWidget(lbl_from)
        h_filt.addWidget(self.date_start)
        h_filt.addSpacing(20)
        h_filt.addWidget(lbl_to)
        h_filt.addWidget(self.date_end)
        h_filt.addSpacing(20)
        h_filt.addWidget(btn_refresh)
        l.addWidget(filter_frame)

        # --- SOUS-ONGLETS ---
        self.stats_sub_tabs = QTabWidget()
        
        # > ONGLET 1: PRODUITS
        tab_prod = QWidget()
        l_prod = QVBoxLayout(tab_prod)
        l_prod.setContentsMargins(5, 10, 5, 5)
        
        # Recherche Produits
        search_frame = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Rechercher produit...")
        self.txt_search.textChanged.connect(self.filter_stats_table)
        
        self.cmb_filter_cat = QComboBox()
        self.cmb_filter_cat.addItem("Toutes Catégories")
        self.cmb_filter_cat.addItems(self.admin_categories_list)
        self.cmb_filter_cat.currentIndexChanged.connect(self.filter_stats_table)
        self.cmb_filter_cat.setFixedWidth(180)
        
        search_frame.addWidget(self.txt_search)
        search_frame.addWidget(self.cmb_filter_cat)
        l_prod.addLayout(search_frame)

        self.tbl_stats = QTableWidget()
        cols = ["Produit", "Catégorie", "Qté Vendue", "CA Généré (€)"]
        self.tbl_stats.setColumnCount(len(cols))
        self.tbl_stats.setHorizontalHeaderLabels(cols)
        self.tbl_stats.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tbl_stats.setSortingEnabled(True)
        self.tbl_stats.verticalHeader().setVisible(False)
        self.tbl_stats.setAlternatingRowColors(True)
        self.tbl_stats.setStyleSheet("alternate-background-color: #252525;")
        self.tbl_stats.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tbl_stats.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        l_prod.addWidget(self.tbl_stats)
        
        self.stats_sub_tabs.addTab(tab_prod, "📦 Produits")

        # > ONGLET 2: VENDEURS
        tab_vend = QWidget()
        l_vend = QVBoxLayout(tab_vend)
        l_vend.setContentsMargins(5, 10, 5, 5)
        
        self.lbl_best_seller = QLabel("")
        self.lbl_best_seller.setObjectName("BestSeller")
        self.lbl_best_seller.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l_vend.addWidget(self.lbl_best_seller)

        self.tbl_vendeurs = QTableWidget()
        cols_v = ["Vendeur", "Ventes (Qté)", "CA Cumulé (€)"]
        self.tbl_vendeurs.setColumnCount(len(cols_v))
        self.tbl_vendeurs.setHorizontalHeaderLabels(cols_v)
        self.tbl_vendeurs.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tbl_vendeurs.setSortingEnabled(True)
        self.tbl_vendeurs.verticalHeader().setVisible(False)
        self.tbl_vendeurs.setAlternatingRowColors(True)
        self.tbl_vendeurs.setStyleSheet("alternate-background-color: #252525;")
        self.tbl_vendeurs.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tbl_vendeurs.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        l_vend.addWidget(self.tbl_vendeurs)
        
        self.stats_sub_tabs.addTab(tab_vend, "👥 Vendeurs")

        l.addWidget(self.stats_sub_tabs)

    def load_stats_data(self):
        d_start = self.date_start.date().toString("yyyy-MM-dd") + " 00:00:00"
        d_end = self.date_end.date().toString("yyyy-MM-dd") + " 23:59:59"
        
        # 1. Données Produits (Utilisé pour le CA Réel)
        data_prods = backend.get_stats_tableau(d_start, d_end)
        self.stats_rows_data = data_prods
        
        # Calcul Grand Total sur la base des PRODUITS (Chiffre d'affaire réel)
        total_ca = sum(d['ca_total'] for d in data_prods)
        self.lbl_grand_total.setText(f"{total_ca:.2f} €")
        
        self.populate_stats_table(data_prods)

        # 2. Données Vendeurs (CUMULATIF : A et B gagnent tous les deux le montant)
        data_vends = backend.get_stats_vendeurs_tableau(d_start, d_end)
        self.populate_vendeurs_table(data_vends)

    def populate_stats_table(self, data):
        self.tbl_stats.setSortingEnabled(False)
        self.tbl_stats.setRowCount(len(data))
        
        for i, row in enumerate(data):
            self.tbl_stats.setItem(i, 0, QTableWidgetItem(row['nom']))
            self.tbl_stats.setItem(i, 1, QTableWidgetItem(row['categorie']))
            
            qty_item = QTableWidgetItem()
            qty_item.setData(Qt.ItemDataRole.DisplayRole, row['qty_totale'])
            self.tbl_stats.setItem(i, 2, qty_item)
            
            ca_item = QTableWidgetItem()
            ca_item.setData(Qt.ItemDataRole.DisplayRole, row['ca_total'])
            self.tbl_stats.setItem(i, 3, ca_item)

        self.tbl_stats.setSortingEnabled(True)
        self.filter_stats_table()

    def filter_stats_table(self):
        search_txt = self.txt_search.text().lower()
        cat_filter = self.cmb_filter_cat.currentText()
        
        for i in range(self.tbl_stats.rowCount()):
            item_nom = self.tbl_stats.item(i, 0).text().lower()
            item_cat = self.tbl_stats.item(i, 1).text()
            
            match_search = search_txt in item_nom
            match_cat = (cat_filter == "Toutes Catégories") or (item_cat == cat_filter)
            
            self.tbl_stats.setRowHidden(i, not (match_search and match_cat))

    def populate_vendeurs_table(self, data):
        self.tbl_vendeurs.setSortingEnabled(False)
        self.tbl_vendeurs.setRowCount(len(data))
        
        best_vendeur_nom = ""
        best_vendeur_ca = -1

        for i, row in enumerate(data):
            if row['ca_total'] > best_vendeur_ca:
                best_vendeur_ca = row['ca_total']
                best_vendeur_nom = row['nom']

            self.tbl_vendeurs.setItem(i, 0, QTableWidgetItem(row['nom']))
            
            qty_item = QTableWidgetItem()
            qty_item.setData(Qt.ItemDataRole.DisplayRole, row['qty_totale'])
            self.tbl_vendeurs.setItem(i, 1, qty_item)
            
            ca_item = QTableWidgetItem()
            ca_item.setData(Qt.ItemDataRole.DisplayRole, row['ca_total'])
            self.tbl_vendeurs.setItem(i, 2, ca_item)

        self.tbl_vendeurs.setSortingEnabled(True)

        if best_vendeur_nom:
            self.lbl_best_seller.setText(f"🏆 Meilleur Vendeur : {best_vendeur_nom} ({best_vendeur_ca:.2f} €)")
        else:
            self.lbl_best_seller.setText("")