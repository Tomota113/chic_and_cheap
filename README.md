<div align="center">

# 👗 Chic & Cheap — Gestion de Prêt-à-Porter & Commerce

[![Release](https://img.shields.io/github/v/release/Tomota113/chic_and_cheap?style=for-the-badge&logo=github&color=38BDF8)](https://github.com/Tomota113/chic_and_cheap/releases)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/UI-Modern_Tkinter-emerald?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)
[![Database](https://img.shields.io/badge/Database-SQLite3-003B57?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?style=for-the-badge)](https://github.com/Tomota113/chic_and_cheap/releases)

**Application de bureau autonome et moderne pour la gestion intégrale de boutique de prêt-à-porter, commerce et distribution.**

[📦 Télécharger l'Exécutable](#-téléchargement--exécutables) • [✨ Fonctionnalités](#-fonctionnalités-clés) • [🚀 Démarrage Rapide](#-démarrage-rapide) • [📊 Architecture](#-architecture-technique)

</div>

---

## 🌟 Présentation

**Chic & Cheap** est une solution logicielle tout-en-un développée pour les commerçants, gérants de boutiques de mode et gestionnaires de stock. Conçue avec une interface ergonomique et intuitive, elle fonctionne **entièrement hors-ligne** grâce à son moteur de base de données SQLite embarqué, sans nécessiter de configuration serveur complexe.

---

## ✨ Fonctionnalités Clés

- 🔐 **Authentification & Rôles sécurisés** : Hachage de mot de passe industriel avec `bcrypt` (accès Administrateur vs Vendeur).
- 🏷️ **Gestion de Catalogue & Produits** : Catégorisation, tailles, couleurs, prix d'achat/vente et alertes automatiques de stock bas.
- 💳 **Caisse & Encaissement Rapide** : Interface de vente fluide, panier d'achats, impression et export de reçus de vente en PDF (`reportlab`).
- 📦 **Contrôle & Réapprovisionnement des Stocks** : Historique des entrées/sorties, ajustements et valorisation en temps réel.
- 📈 **Tableau de Bord & Rapports d'Activité** : Statistiques des ventes quotidiennes/mensuelles, top articles, marge brute et export comptable.
- 🔄 **Initialisation Automatique** : Schéma de base de données créé au premier lancement avec jeu de données de démonstration.

---

## 📦 Téléchargement & Exécutables

Aucun prérequis technique ni installation de Python ne sont nécessaires pour utiliser Chic & Cheap :

| Système d'exploitation | Format | Téléchargement direct |
|---|---|---|
| **Windows 10 / 11 (64-bit)** | `.exe` autonome | [⬇️ Télécharger ChicAndCheap.exe](https://github.com/Tomota113/chic_and_cheap/releases/latest) |
| **Linux (Ubuntu, Debian, Fedora)** | Binaire exécutable x86_64 | [⬇️ Télécharger ChicAndCheap-linux](https://github.com/Tomota113/chic_and_cheap/releases/latest) |

### Lancer sous Linux :
```bash
chmod +x ChicAndCheap
./ChicAndCheap
```

---

## 🚀 Démarrage pour Développeurs

Pour cloner et exécuter le projet depuis les sources :

```bash
# 1. Cloner le dépôt
git clone https://github.com/Tomota113/chic_and_cheap.git
cd chic_and_cheap

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python app.py
```

### Compiler soi-même les exécutables :
* **Sur Linux** : `./build_linux.sh`
* **Sur Windows** : `build_exe.bat`

---

## 📊 Architecture Technique

```
chic_and_cheap/
├── app.py                 # Point d'entrée principal
├── chiccheap/
│   ├── db/                # Initialisation & requêtes SQLite
│   ├── models/            # Modèles métier (Produits, Ventes, Utilisateurs)
│   ├── services/          # Logique applicative & calculs financiers
│   └── ui/                # Vues Tkinter modulaires (Ventes, Stocks, Rapports)
├── tests/                 # Tests unitaires Pytest
├── requirements.txt       # Dépendances Python
└── .github/workflows/     # CI/CD & Compilation automatique des binaires
```

---

## 📄 Licence

Ce projet est sous licence [MIT](LICENSE). Développé par **[Ibrahim Tomota](https://github.com/Tomota113)**.
