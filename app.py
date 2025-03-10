import streamlit as st

st.set_page_config(
    page_title="NoteMaster",
    page_icon="📝",
    layout="wide"
)

import os, json
from utils.note_manager import load_notes, save_note, delete_note, update_note
from utils.question_generator import generate_questions, evaluate_answer
from config import QUESTIONS_DIR
from utils.stats_manager import get_all_stats, save_quiz_result, delete_note_stats, delete_all_stats
# Import session storage functions
from utils.session_storage import (
    init_session_storage, load_session_notes, save_session_note, delete_session_note, update_session_note,
    save_session_questions, get_session_questions, save_session_quiz_result, get_session_note_stats,
    get_all_session_stats, delete_session_note_stats, delete_all_session_stats,
    save_to_local_storage, load_from_local_storage
)

# Initialize session storage
init_session_storage()

# Application principale

# Sidebar 
st.sidebar.title("📝 **NoteMaster**")
st.sidebar.markdown("<h3>Menu</h3>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "📂 <span style='color: #0066CC;'>Choisissez une option :</span>", 
    ["Dashboard", "Prise de Notes", "Mode Quiz", "Performances", "Import/Export"], 
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
    st.title("📝 Prise de Notes")
    st.markdown("---")

    # Afficher les notes existantes
    notes = load_session_notes()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Notes existantes")
        if not notes:
            st.info("Aucune note pour le moment. Créez votre première note !")
        else:
            selected_note = st.selectbox(
                "Sélectionnez une note à afficher",
                options=[note["title"] for note in notes],
                index=0 if notes else None,
                key="note_select"
            )
            
            if selected_note:
                selected_content = next((note["content"] for note in notes if note["title"] == selected_note), "")
                
                # Boutons d'action
                col1a, col1b = st.columns(2)
                with col1a:
                    if st.button("🗑️ Supprimer", key="delete_note_btn"):
                        delete_session_note(selected_note)
                        st.success(f"Note '{selected_note}' supprimée !")
                        st.rerun()
                
                with col1b:
                    if st.button("📋 Modifier", key="edit_note_btn"):
                        st.session_state.editing_note = selected_note
                        st.session_state.editing_content = selected_content
                        st.rerun()
    
    with col2:
        st.subheader("Créer/Modifier une note")
        
        # Mode édition
        if st.session_state.get("editing_note"):
            note_title = st.text_input("Titre de la note", value=st.session_state.editing_note, key="edit_title_input")
            note_content = st.text_area("Contenu de la note", value=st.session_state.editing_content, height=300, key="edit_content_input")
            
            col2a, col2b = st.columns(2)
            with col2a:
                if st.button("💾 Enregistrer les modifications", key="save_edit_btn"):
                    if note_title != st.session_state.editing_note:
                        # Le titre a changé, supprimer l'ancienne note et créer une nouvelle
                        delete_session_note(st.session_state.editing_note)
                        save_session_note(note_title, note_content)
                        st.success(f"Note renommée et mise à jour : '{note_title}'")
                    else:
                        # Mettre à jour la note existante
                        update_session_note(note_title, note_content)
                        st.success(f"Note mise à jour : '{note_title}'")
                    
                    # Réinitialiser le mode édition
                    st.session_state.editing_note = None
                    st.session_state.editing_content = None
                    st.rerun()
            
            with col2b:
                if st.button("❌ Annuler", key="cancel_edit_btn"):
                    st.session_state.editing_note = None
                    st.session_state.editing_content = None
                    st.rerun()
        
        # Mode création
        else:
            note_title = st.text_input("Titre de la note", key="new_title_input")
            note_content = st.text_area("Contenu de la note", height=300, key="new_content_input")
            
            if st.button("➕ Créer la note", key="create_note_btn"):
                if note_title and note_content:
                    save_session_note(note_title, note_content)
                    st.success(f"Note créée : '{note_title}'")
                    # Réinitialiser les champs
                    st.session_state.new_title_input = ""
                    st.session_state.new_content_input = ""
                    st.rerun()
                else:
                    st.error("Veuillez remplir le titre et le contenu de la note.")



elif menu == "Mode Quiz":
    st.title("❓ Mode Quiz")
    st.markdown("---")
    
    # Charger les notes disponibles
    notes = load_session_notes()
    
    if not notes:
        st.warning("Vous n'avez pas encore de notes. Veuillez d'abord créer des notes.")
    else:
        # Sélection de la note
        selected_note = st.selectbox(
            "Sélectionnez une note pour générer des questions",
            options=[note["title"] for note in notes],
            key="quiz_note_select"
        )
        
        # Récupérer le contenu de la note sélectionnée
        selected_content = next((note["content"] for note in notes if note["title"] == selected_note), "")
        
        # Afficher un aperçu du contenu
        with st.expander("Aperçu de la note"):
            st.write(selected_content)
        
        # Bouton pour générer des questions
        if st.button("🔄 Générer des questions", key="generate_questions_btn"):
            with st.spinner("Génération des questions en cours..."):
                questions = generate_questions(selected_note, selected_content)
                if questions:
                    # Sauvegarder les questions dans la session
                    save_session_questions(selected_note, questions)
                    st.success(f"{len(questions)} questions générées avec succès !")
                    st.session_state.show_quiz = True
                    st.rerun()
                else:
                    st.error("Erreur lors de la génération des questions. Veuillez réessayer.")
        
        # Afficher le quiz si des questions ont été générées
        if st.session_state.get("show_quiz", False):
            questions = get_session_questions(selected_note)
            
            if not questions:
                st.warning("Aucune question disponible. Veuillez générer des questions.")
            else:
                st.subheader("Quiz")
                
                # Initialiser l'index de question si nécessaire
                if "question_index" not in st.session_state:
                    st.session_state.question_index = 0
                    st.session_state.quiz_completed = False
                    st.session_state.quiz_results = []
                
                # Afficher la question actuelle
                if not st.session_state.quiz_completed and st.session_state.question_index < len(questions):
                    current_q = questions[st.session_state.question_index]
                    
                    st.markdown(f"**Question {st.session_state.question_index + 1}/{len(questions)}**")
                    st.markdown(f"### {current_q['text']}")
                    
                    # Zone de réponse
                    user_answer = st.text_area("Votre réponse:", key=f"answer_{st.session_state.question_index}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Soumettre", key="submit_answer_btn"):
                            if user_answer.strip():
                                # Évaluer la réponse
                                score, feedback = evaluate_answer(user_answer, current_q['reponse'])
                                
                                # Sauvegarder le résultat
                                save_session_quiz_result(
                                    selected_note, 
                                    current_q['text'], 
                                    user_answer, 
                                    current_q['reponse'], 
                                    score
                                )
                                
                                # Stocker le résultat pour l'affichage final
                                st.session_state.quiz_results.append({
                                    "question": current_q['text'],
                                    "user_answer": user_answer,
                                    "correct_answer": current_q['reponse'],
                                    "score": score,
                                    "feedback": feedback
                                })
                                
                                # Passer à la question suivante
                                st.session_state.question_index += 1
                                
                                # Vérifier si le quiz est terminé
                                if st.session_state.question_index >= len(questions):
                                    st.session_state.quiz_completed = True
                                
                                st.rerun()
                            else:
                                st.error("Veuillez entrer une réponse avant de soumettre.")
                    
                    with col2:
                        if st.button("⏭️ Passer", key="skip_question_btn"):
                            st.session_state.question_index += 1
                            if st.session_state.question_index >= len(questions):
                                st.session_state.quiz_completed = True
                            st.rerun()
                
                # Afficher les résultats à la fin du quiz
                if st.session_state.quiz_completed:
                    st.subheader("Résultats du quiz")
                    
                    # Calculer le score total
                    total_score = sum(result["score"] for result in st.session_state.quiz_results)
                    max_score = len(st.session_state.quiz_results) * 5  # 5 points par question
                    percentage = (total_score / max_score) * 100 if max_score > 0 else 0
                    
                    st.markdown(f"**Score total: {total_score}/{max_score} ({percentage:.1f}%)**")
                    
                    # Afficher les résultats détaillés
                    for i, result in enumerate(st.session_state.quiz_results):
                        with st.expander(f"Question {i+1} - Score: {result['score']}/5"):
                            st.markdown(f"**Q: {result['question']}**")
                            st.markdown(f"**Votre réponse:** {result['user_answer']}")
                            st.markdown(f"**Réponse correcte:** {result['correct_answer']}")
                            st.markdown(f"**Feedback:** {result['feedback']}")
                    
                    # Bouton pour recommencer
                    if st.button("🔄 Recommencer le quiz", key="restart_quiz_btn"):
                        st.session_state.question_index = 0
                        st.session_state.quiz_completed = False
                        st.session_state.quiz_results = []
                        st.rerun()
                    
                    # Bouton pour revenir à la sélection de note
                    if st.button("📝 Choisir une autre note", key="choose_other_note_btn"):
                        st.session_state.show_quiz = False
                        st.session_state.question_index = 0
                        st.session_state.quiz_completed = False
                        st.session_state.quiz_results = []
                        st.rerun()


elif menu == "Performances":
    st.title("📊 Performances")
    st.markdown("---")
    
    # Récupérer toutes les statistiques
    all_stats = get_all_session_stats()
    
    if not all_stats:
        st.info("Aucune statistique disponible. Complétez d'abord quelques quiz !")
    else:
        # Sélection de la note pour afficher les statistiques
        note_titles = list(all_stats.keys())
        selected_note = st.selectbox(
            "Sélectionnez une note pour voir les statistiques",
            options=note_titles,
            key="stats_note_select"
        )
        
        if selected_note:
            note_stats = all_stats[selected_note]
            attempts = note_stats.get("attempts", [])
            
            if not attempts:
                st.warning(f"Aucune tentative pour la note '{selected_note}'.")
            else:
                # Afficher les statistiques générales
                st.subheader(f"Statistiques pour '{selected_note}'")
                
                # Calculer les statistiques
                total_attempts = len(attempts)
                total_score = sum(attempt["score"] for attempt in attempts)
                max_possible = total_attempts * 5  # 5 points par question
                avg_score = total_score / total_attempts if total_attempts > 0 else 0
                
                # Afficher les métriques
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Nombre de questions", total_attempts)
                with col2:
                    st.metric("Score moyen", f"{avg_score:.1f}/5")
                with col3:
                    st.metric("Score total", f"{total_score}/{max_possible}")
                
                # Afficher l'historique des tentatives
                st.subheader("Historique des tentatives")
                
                # Trier les tentatives par date (plus récentes en premier)
                sorted_attempts = sorted(attempts, key=lambda x: x["timestamp"], reverse=True)
                
                for i, attempt in enumerate(sorted_attempts):
                    with st.expander(f"Tentative {i+1} - {attempt['timestamp'][:10]} - Score: {attempt['score']}/5"):
                        st.markdown(f"**Question:** {attempt['question']}")
                        st.markdown(f"**Votre réponse:** {attempt['user_answer']}")
                        st.markdown(f"**Réponse correcte:** {attempt['correct_answer']}")
                
                # Option pour supprimer les statistiques
                if st.button("🗑️ Supprimer les statistiques pour cette note", key="delete_note_stats_btn"):
                    delete_session_note_stats(selected_note)
                    st.success(f"Statistiques supprimées pour '{selected_note}'")
                    st.rerun()
        
        # Option pour supprimer toutes les statistiques
        if st.button("🗑️ Supprimer toutes les statistiques", key="delete_all_stats_btn"):
            delete_all_session_stats()
            st.success("Toutes les statistiques ont été supprimées")
            st.rerun()


elif menu == "Import/Export":
    st.title("📤 Import/Export des données")
    st.markdown("---")
    
    st.info("Cette fonctionnalité vous permet de sauvegarder vos données localement et de les restaurer ultérieurement.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Exporter vos données")
        st.write("Téléchargez toutes vos notes, questions et statistiques dans un fichier JSON.")
        
        # Générer le contenu JSON pour le téléchargement
        json_data = save_to_local_storage()
        
        st.download_button(
            label="📥 Télécharger mes données",
            data=json_data,
            file_name="notemaster_data.json",
            mime="application/json",
            key="download_data_btn"
        )
    
    with col2:
        st.subheader("Importer vos données")
        st.write("Restaurez vos données à partir d'un fichier JSON précédemment exporté.")
        
        uploaded_file = st.file_uploader("Choisissez un fichier JSON", type=["json"], key="upload_data_file")
        
        if uploaded_file is not None:
            if st.button("📤 Importer les données", key="import_data_btn"):
                # Lire le contenu du fichier
                json_data = uploaded_file.read().decode("utf-8")
                
                # Charger les données dans la session
                if load_from_local_storage(json_data):
                    st.success("Données importées avec succès !")
                    st.rerun()
                else:
                    st.error("Erreur lors de l'importation des données. Vérifiez le format du fichier.")


# Divider
st.markdown("---")


st.markdown("### 🌟 Ressources utiles :")
# Align the buttons horizontally
col1, col2 = st.columns(2)
with col1:
    st.link_button("📄 Répo Github", url="https://github.com/mamour-dx/NoteMaster")
with col2:
    st.link_button("📚 Vidéo YouTube", url="https://www.youtube.com/watch?v=1hFGjvgwC_8&t=60s")
