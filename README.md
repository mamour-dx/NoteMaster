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

### ⚙️ Configuration Facile

- **Interface API** : Gérez votre clé API DeepSeek directement depuis l'application
- **Documentation intégrée** : Guide complet d'utilisation accessible dans l'app

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

3. **Configurez l'API :**

- Créez un compte sur [OpenRouter](https://openrouter.ai)
- Obtenez une clé API pour DeepSeek (détaillé sur ce [blog](https://apidog.com/blog/how-to-use-deepseek-api-for-free/))
- Configurez la clé dans l'application via l'interface ou le fichier `.env`

4. **Lancez l'application :**

```bash
streamlit run app.py
```

**Autre alternative avec Docker**

**Executez ces commandes**
```bash
docker build . -t notemaster
docker run --env-file .env -dp 5000:5000 notemaster
```

---

## 📁 Structure du Projet

```
NoteMaster/
├── app.py                 # Application principale Streamlit
├── config.py             # Configuration (chemins, constantes)
├── requirements.txt      # Dépendances Python
├── utils/
│   ├── note_manager.py   # Gestion des notes
│   ├── question_generator.py  # Génération des questions
│   └── stats_manager.py  # Gestion des statistiques
├── notes/               # Stockage des notes
├── questions/          # Stockage des questions générées
└── stats/             # Stockage des statistiques
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

5. **Configuration API**
   - Configurez votre clé API
   - Vérifiez le statut de la connexion

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

---

## 📫 Contact

- Email: [me@mxr.codes](mailto:me@mxr.codes)
- YouTube : [@mxr_codes](https://youtube.com/@mxr_codes)

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
