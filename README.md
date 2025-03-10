# 📝 NoteMaster - Assistant d'Apprentissage Actif

NoteMaster est une application web qui combine la prise de notes et l'apprentissage actif grâce à l'intégration de Python et de l'API DeepSeek de OpenRouter. L'application permet aux étudiants de prendre des notes, de générer des questions basées sur leurs notes, de répondre à ces questions et de suivre leur progression. 🚀

---

## 🛠️ Fonctionnalités

### 📝 Gestion des Notes

- **Création et édition** : Ajoutez, modifiez et supprimez des notes facilement
- **Interface intuitive** : Éditeur de texte intégré pour une prise de notes confortable
- **Organisation simple** : Toutes vos notes accessibles en un coup d'œil

### 📚 Mode Quiz

- **Génération intelligente** : Questions générées automatiquement à partir de vos notes
- **Évaluation bienveillante** : Système de notation qui valorise la compréhension des concepts clés
- **Réponses libres** : Questions ouvertes pour un apprentissage plus actif
- **Notation sur 5** : Évaluation claire et motivante de vos réponses

### 📊 Suivi des Performances

- **Statistiques détaillées** : Visualisez vos progrès par note
- **Graphiques intuitifs** :
  - Score moyen global
  - Évolution des scores dans le temps
  - Comparaison entre différentes notes
- **Historique complet** : Accès à toutes vos tentatives précédentes

### 🔒 Stockage Local des Données

- **Confidentialité** : Vos notes et données sont stockées uniquement dans votre navigateur
- **Import/Export** : Sauvegardez et restaurez vos données facilement
- **Multi-utilisateurs** : Chaque utilisateur a ses propres données, même sur une instance partagée

---

## 🚀 Installation

PS: Il est considéré comme bonne pratique de mettre un environnement virtuel. C'est très simple, demandes à ChatGPT comment faire :)

1. **Clonez le dépôt :**

```bash
git clone https://github.com/mamour-dx/NoteMaster.git
cd NoteMaster
```

2. **Installez les dépendances :**

```bash
pip install -r requirements.txt
```

3. **Lancez l'application :**

```bash
streamlit run app.py
```

---

## 📁 Structure du Projet

```
NoteMaster/
├── app.py                 # Application principale Streamlit
├── config.py             # Configuration (chemins, constantes)
├── requirements.txt      # Dépendances Python
├── utils/
│   ├── note_manager.py   # Gestion des notes (fichiers)
│   ├── question_generator.py  # Génération des questions
│   ├── stats_manager.py  # Gestion des statistiques (fichiers)
│   └── session_storage.py  # Stockage des données en session
├── notes/               # Stockage des notes (serveur)
├── questions/          # Stockage des questions générées (serveur)
└── stats/             # Stockage des statistiques (serveur)
```

---

## 💡 Utilisation

1. **Dashboard**

   - Vue d'ensemble de l'application
   - Accès rapide aux fonctionnalités principales

2. **Prise de Notes**

   - Créez une nouvelle note
   - Modifiez vos notes existantes
   - Supprimez les notes inutiles

3. **Mode Quiz**

   - Sélectionnez une note
   - Générez des questions
   - Répondez aux questions
   - Obtenez une évaluation immédiate

4. **Statistiques**

   - Consultez vos performances
   - Analysez votre progression
   - Gérez votre historique

5. **Import/Export**

   - Sauvegardez vos données localement
   - Restaurez vos données depuis un fichier JSON
   - Gardez vos notes et statistiques privées

---

## 🔧 Configuration de l'API (Optionnel)

Si vous souhaitez utiliser vos propres clés API pour la génération de questions, suivez ces étapes :

### 1️⃣ Obtenir une clé API OpenRouter

- Rendez-vous sur [OpenRouter](https://openrouter.ai) et créez un compte.
- Générez une clé API gratuite pour le modèle DeepSeek V3.

### 2️⃣ Ajouter votre clé API à l'application

**Via un fichier `.env` (manuel)**

- Créez un fichier `.env` à la racine du projet.
- Ajoutez-y la ligne suivante en remplaçant `VOTRE_CLE_API` par votre clé API :
  ```
  DEEPSEEK_KEY=VOTRE_CLE_API
  ```
- Redémarrez l'application pour que les modifications soient prises en compte.

---

## ❓ Résolution des problèmes

### Problèmes d'API

Si vous rencontrez des problèmes avec l'API :

- Vérifiez que votre clé API est correcte et valide.
- Assurez-vous que vous avez bien installé les dépendances nécessaires (`pip install openai python-dotenv`).
- Consultez la documentation d'OpenRouter ici : [Documentation OpenRouter](https://openrouter.ai/docs).

### Problèmes de démarrage

- Assurez-vous que toutes les dépendances sont installées : `pip install -r requirements.txt`
- Vérifiez que vous utilisez Python 3.8 ou supérieur
- Pour de meilleures performances, installez Watchdog : `pip install watchdog`

### Problèmes de stockage

- Si vos données ne sont pas sauvegardées entre les sessions, utilisez la fonction Import/Export pour sauvegarder manuellement vos données
- Assurez-vous que votre navigateur n'est pas en mode navigation privée

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

Si vous avez un problème ou souhaitez suggérer une amélioration, ouvrez un **issue** sur GitHub :
👉 [Ouvrir un issue](https://github.com/mamour-dx/NoteMaster/issues)

---

## 📫 Contact

- Email: [me@mxr.codes](mailto:me@mxr.codes)
- YouTube : [@mxr_codes](https://youtube.com/@mxr_codes)

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
