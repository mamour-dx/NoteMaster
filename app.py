import streamlit as st
import os, json
from utils.note_manager import load_notes, save_note, delete_note, update_note
from utils.question_generator import generate_questions, evaluate_answer
from config import QUESTIONS_DIR
from utils.stats_manager import get_all_stats, save_quiz_result, delete_note_stats, delete_all_stats

# Application principale

# Sidebar 
st.sidebar.title("📝 **NoteMaster**")
st.sidebar.markdown("<h3>Navigation rapide</h3>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "📂 <span style='color: #0066CC;'>Choisissez une option :</span>", 
    ["Dashboard", "Prise de Notes", "Mode Quiz", "Statistiques", "API", "Docs"], 
    format_func=lambda x: f"🔹 {x}", 
    index=0,
    label_visibility="hidden", 
    key="menu_radio"
)

# Main content
if menu == "Dashboard":
    # Header with custom styles
    st.markdown("<h1>Bienvenue sur NoteMaster ⚡️</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Apprendre ses cours grâce au _Active Learning_!")

    # Feature list with emojis and custom formatting
    st.markdown(
        """
        <div style='padding: 10px;'>
            <p><strong>NoteMaster</strong> vous permet de :</p>
            <ul>
                <li>🗒️ <strong>Prendre des notes</strong> et les organiser.</li>
                <li>❓ <strong>Générer des questions</strong> pour vos cours.</li>
                <li>✅ <strong>Pratiquer l'apprentissage actif</strong> et suivre vos progrès.</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )


elif menu == "Prise de Notes":
    st.header("Prise de Notes")
    
    if "notes" not in st.session_state:
        st.session_state.notes = load_notes()
    
    if "editing_note" not in st.session_state:
        st.session_state.editing_note = None

    # Affichage des notes existantes
    st.write("### Vos notes :")
    if st.session_state.notes:
        for note in st.session_state.notes:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"📝 {note['title']}")
            with col2:
                if st.button("Voir/Modifier", key=f"edit_{note['title']}"):
                    st.session_state.editing_note = note
            with col3:
                if st.button("Supprimer", key=f"delete_{note['title']}"):
                    delete_note(note['title'])
                    st.session_state.notes = load_notes()
                    if st.session_state.editing_note and st.session_state.editing_note['title'] == note['title']:
                        st.session_state.editing_note = None
                    st.rerun()
    else:
        st.info("Aucune note disponible pour le moment.")

    # Section d'édition/visualisation
    if st.session_state.editing_note:
        st.markdown("---")
        st.subheader(f"Modifier la note : {st.session_state.editing_note['title']}")
        edited_content = st.text_area(
            "Contenu de la note",
            value=st.session_state.editing_note['content'],
            height=300,
            key="edit_content"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sauvegarder les modifications"):
                if update_note(st.session_state.editing_note['title'], edited_content):
                    st.success("Note mise à jour avec succès!")
                    st.session_state.notes = load_notes()
                    st.session_state.editing_note = None
                    st.rerun()
                else:
                    st.error("Erreur lors de la mise à jour de la note")
        with col2:
            if st.button("Annuler"):
                st.session_state.editing_note = None
                st.rerun()

    # Section pour créer une nouvelle note
    st.markdown("---")
    st.subheader("Créer une nouvelle note")
    note_title = st.text_input("Titre de la note")
    note_content = st.text_area("Contenu de la note", height=200)
    if st.button("Sauvegarder"):
        if note_title and note_content:
            save_note(note_title, note_content)
            st.session_state.notes = load_notes()
            st.success(f"Note '{note_title}' sauvegardée avec succès !")
            st.rerun()
        else:
            st.warning("Veuillez fournir un titre et un contenu pour votre note.")



elif menu == "Mode Quiz":
    st.header("Mode Quiz")
    
    # Charger les notes disponibles
    notes = load_notes()
    note_titles = [note["title"] for note in notes]
    selected_note = st.selectbox("Choisissez une note", note_titles)

    if selected_note:
        note_content = next(note["content"] for note in notes if note["title"] == selected_note)
        json_file_path = os.path.join(QUESTIONS_DIR, f"{selected_note}.json")
        
        # Initialisation des questions
        if "questions" not in st.session_state or st.session_state.get("current_note") != selected_note:
            if os.path.exists(json_file_path):
                with open(json_file_path, "r") as file:
                    st.session_state.questions = json.load(file)
            else:
                st.session_state.questions = []
            st.session_state.current_note = selected_note
            # Initialiser un dictionnaire pour stocker les réponses
            st.session_state.user_answers = {}

        # Générer de nouvelles questions
        if st.button("Générer des questions"):
            try:
                with st.spinner("Génération des questions en cours..."):
                    new_questions = generate_questions(selected_note, note_content)
                
                if new_questions:
                    with open(json_file_path, "w") as file:
                        json.dump(new_questions, file, indent=4, ensure_ascii=False)
                    
                    st.session_state.questions = new_questions
                    st.session_state.user_answers = {}  # Réinitialiser les réponses
                    st.success("Questions générées et sauvegardées avec succès !")
                else:
                    st.error("L'API n'a retourné aucune question.")
            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")

        # Afficher les questions
        if st.session_state.questions:
            st.write("### Questions :")
            
            # Afficher toutes les questions avec des champs de réponse
            for i, question in enumerate(st.session_state.questions, 1):
                st.write(f"**Question {i}:** {question['text']}")
                # Stocker la réponse dans session_state
                answer_key = f"answer_{i}"
                user_answer = st.text_area(
                    "Votre réponse",
                    key=answer_key,
                    height=100
                )
                st.session_state.user_answers[answer_key] = user_answer
                st.markdown("---")

            # Bouton unique pour vérifier toutes les réponses
            if st.button("📝 Vérifier toutes les réponses"):
                total_score = 0
                with st.spinner("Évaluation des réponses en cours..."):
                    for i, question in enumerate(st.session_state.questions, 1):
                        answer_key = f"answer_{i}"
                        user_answer = st.session_state.user_answers.get(answer_key, "")
                        
                        # Évaluer la réponse
                        evaluation = evaluate_answer(
                            question['text'],
                            user_answer,
                            question['reponse']
                        )
                        
                        # Sauvegarder le résultat
                        save_quiz_result(
                            selected_note,
                            question['text'],
                            user_answer,
                            question['reponse'],
                            evaluation['score']
                        )
                        
                        total_score += evaluation['score']
                        
                        # Afficher le résultat pour cette question
                        with st.expander(f"Résultat Question {i}"):
                            st.write(f"**Votre réponse:** {user_answer}")
                            st.write(f"**Réponse correcte:** {question['reponse']}")
                            st.write(f"**Score:** {evaluation['score']}/5")
                
                # Afficher le score total
                avg_score = total_score / len(st.session_state.questions)
                st.success(f"Score total : {avg_score:.1f}/5")
                
                # Option pour recommencer
                if st.button("🔄 Recommencer le quiz"):
                    st.session_state.user_answers = {}
                    st.rerun()

            # Bouton pour supprimer les questions
            if st.button("🗑️ Supprimer toutes les questions"):
                try:
                    os.remove(json_file_path)
                    st.session_state.questions = []
                    st.session_state.user_answers = {}
                    st.success("Les questions ont été supprimées avec succès !")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur lors de la suppression : {e}")
        
        else:
            st.info("Aucune question disponible. Cliquez sur 'Générer des questions' pour commencer.")


elif menu == "Statistiques":
    st.header("📊 Statistiques d'apprentissage")
    
    stats = get_all_stats()
    if not stats:
        st.info("Aucune statistique disponible pour le moment. Commencez à répondre à des quiz pour voir vos performances !")
    else:
        # Vue d'ensemble globale
        st.subheader("Vue d'ensemble")
        
        # Calculer les statistiques globales
        all_scores = []
        notes_avg_scores = {}
        for note_title, note_stats in stats.items():
            if note_stats["attempts"]:
                scores = [attempt["score"] for attempt in note_stats["attempts"]]
                notes_avg_scores[note_title] = sum(scores) / len(scores)
                all_scores.extend(scores)
        
        # Afficher le score moyen global
        if all_scores:
            global_avg = sum(all_scores) / len(all_scores)
            st.metric("Score moyen global", f"{global_avg:.1f}/5")
            
            # Graphique des scores moyens par note
            st.bar_chart(notes_avg_scores)
        
        # Détails par note
        st.subheader("Détails par note")
        for note_title, note_stats in stats.items():
            with st.expander(f"📝 {note_title}"):
                if note_stats["attempts"]:
                    col1, col2, col3 = st.columns(3)
                    
                    # Statistiques de base
                    scores = [attempt["score"] for attempt in note_stats["attempts"]]
                    avg_score = sum(scores) / len(scores)
                    with col1:
                        st.metric("Score moyen", f"{avg_score:.1f}/5")
                    with col2:
                        st.metric("Meilleur score", f"{max(scores)}/5")
                    with col3:
                        st.metric("Nombre de questions", len(scores))
                    
                    # Graphique d'évolution des scores
                    scores_df = {
                        "Question": range(1, len(scores) + 1),
                        "Score": scores
                    }
                    st.line_chart(scores_df, x="Question", y="Score")
                    
                    # Historique détaillé
                    st.write("### Historique détaillé")
                    for attempt in reversed(note_stats["attempts"]):
                        st.markdown(f"""
                        **📅 {attempt['timestamp'][:16].replace('T', ' à ')}**
                        - **Question:** {attempt['question']}
                        - **Votre réponse:** {attempt['user_answer']}
                        - **Réponse correcte:** {attempt['correct_answer']}
                        - **Score:** {attempt['score']}/5
                        ---
                        """)
                    
                    # Bouton pour supprimer l'historique de cette note
                    if st.button("🗑️ Supprimer l'historique", key=f"delete_{note_title}"):
                        if delete_note_stats(note_title):
                            st.success(f"Historique supprimé pour {note_title}")
                            st.rerun()
                        else:
                            st.error("Erreur lors de la suppression de l'historique")

        # Bouton pour supprimer tout l'historique
        st.markdown("---")
        if st.button("🗑️ Supprimer tout l'historique", type="secondary"):
            if delete_all_stats():
                st.success("Tout l'historique a été supprimé")
                st.rerun()
            else:
                st.error("Erreur lors de la suppression de l'historique")


elif menu == "API":
    st.header("Configuration de l'API")

    # Charger la clé API existante (si elle existe)
    if "api_key" not in st.session_state:
        from dotenv import load_dotenv
        load_dotenv()
        st.session_state.api_key = os.getenv("DEEPSEEK_KEY", "")

    # Formulaire pour entrer ou mettre à jour la clé API
    st.write("Entrez votre clé API de OpenRouter pour activer les fonctionnalités de génération.")
    api_key_input = st.text_input(
        "Clé API",
        value=st.session_state.api_key,
        placeholder="Entrez votre clé API",
        type="password",
        key="api_input"
    )

    # Boutons pour enregistrer ou réinitialiser
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Enregistrer la clé API"):
            if len(api_key_input) == 73:
                with open(".env", "w") as file:
                    file.write(f'DEEPSEEK_KEY="{api_key_input}"')
                st.session_state.api_key = api_key_input
                st.success("Clé API enregistrée avec succès !")
            else:
                st.error("Clé API invalide. Elle doit comporter exactement 73 caractères.")

    with col2:
        if st.button("Réinitialiser la clé API"):
            if os.path.exists(".env"):
                os.remove(".env")
            st.session_state.api_key = ""
            st.warning("Clé API réinitialisée. Veuillez en entrer une nouvelle.")


elif menu == "Docs":
    st.header("📖 Docs")

    # Bouton vers le dépôt GitHub
    st.subheader("Accéder au Répo GitHub")
    st.write("Vous pouvez accéder au code source et aux détails du projet sur le répo GitHub.")
    st.link_button("👉 Aller au dépôt GitHub", url="https://github.com/mamour-dx/NoteMaster")

    # Documentation sur la gestion de l'API DeepSeek via OpenRouter
    st.subheader("Configurer l'API DeepSeek V3 via OpenRouter")
    st.markdown(
        """
        Pour utiliser l'API DeepSeek dans cette application, vous devez générer une clé API OpenRouter et la configurer. Deux options sont disponibles :

        ### 1️⃣ Obtenir une clé API OpenRouter
        - Rendez-vous sur [OpenRouter](https://openrouter.ai) et créez un compte.
        - Générez une clé API gratuite pour le model DeepSeek V3.

        ### 2️⃣ Ajouter votre clé API à l'application

        **Option 1 : via un fichier `.env` (manuel)**
        - Créez un fichier `.env` à la racine du projet.
        - Ajoutez-y la ligne suivante en remplaçant `VOTRE_CLE_API` par votre clé API :
          ```
          DEEPSEEK_KEY=VOTRE_CLE_API
          ```
        - Redémarrez l'application pour que les modifications soient prises en compte :
          ```bash
          streamlit run app.py
          ```

        **Option 2 : directement via l'application (automatique)**
        - Accédez à l'onglet **API** dans le menu latéral de l'application.
        - Entrez votre clé API dans le champ prévu et cliquez sur **Enregistrer**.
        - L'application enregistrera automatiquement la clé pour une utilisation immédiate.

        ### 💡 Résolution des problèmes
        Si vous rencontrez des problèmes avec l'API :
        - Vérifiez que votre clé API est correcte et valide.
        - Assurez-vous que vous avez bien installé les dépendances nécessaires (`pip install openai`).
        - Consultez la documentation d'OpenRouter ici : [Documentation OpenRouter](https://openrouter.ai/docs).

        ### 🚀 Besoin d'aide ou d'une nouvelle fonctionnalité ?
        Si vous avez un problème ou souhaitez suggérer une amélioration, ouvrez un **issue** sur GitHub :
        👉 [Ouvrir un issue](https://github.com/mamour-dx/NoteMaster/issues)
        """
    )
    
    # Ajout d'un espace pour d'autres paramètres futurs
    st.subheader("Autres paramètres")
    st.write("Des options supplémentaires seront ajoutées ici à l'avenir.")




# Divider
st.markdown("---")


st.markdown("### 🌟 Ressources utiles :")
# Align the buttons horizontally
col1, col2 = st.columns(2)
with col1:
    st.link_button("📄 Répo Github", url="https://github.com/mamour-dx/NoteMaster")
with col2:
    st.link_button("📚 Vidéo YouTube", url="https://youtube.com/@mxr_codes")