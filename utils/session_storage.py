import streamlit as st
import json
from datetime import datetime

# Initialize session state for user data if not already present
def init_session_storage():
    if 'notes' not in st.session_state:
        st.session_state.notes = {}  # {title: content}
    
    if 'questions' not in st.session_state:
        st.session_state.questions = {}  # {note_title: [questions]}
    
    if 'stats' not in st.session_state:
        st.session_state.stats = {}  # {note_title: {attempts: []}}

# Notes management
def load_session_notes():
    init_session_storage()
    notes = []
    for title, content in st.session_state.notes.items():
        notes.append({"title": title, "content": content})
    return notes

def save_session_note(title, content):
    init_session_storage()
    st.session_state.notes[title] = content

def delete_session_note(title):
    init_session_storage()
    if title in st.session_state.notes:
        del st.session_state.notes[title]
    
    # Also delete associated questions and stats
    if title in st.session_state.questions:
        del st.session_state.questions[title]
    
    if title in st.session_state.stats:
        del st.session_state.stats[title]

def update_session_note(title, new_content):
    init_session_storage()
    if title in st.session_state.notes:
        st.session_state.notes[title] = new_content
        return True
    return False

# Questions management
def save_session_questions(note_title, questions):
    init_session_storage()
    st.session_state.questions[note_title] = questions

def get_session_questions(note_title):
    init_session_storage()
    return st.session_state.questions.get(note_title, [])

# Stats management
def save_session_quiz_result(note_title, question_text, user_answer, correct_answer, score):
    init_session_storage()
    
    if note_title not in st.session_state.stats:
        st.session_state.stats[note_title] = {"attempts": []}
    
    attempt = {
        "timestamp": datetime.now().isoformat(),
        "question": question_text,
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "score": score
    }
    
    st.session_state.stats[note_title]["attempts"].append(attempt)

def get_session_note_stats(note_title):
    init_session_storage()
    return st.session_state.stats.get(note_title, {"attempts": []})

def get_all_session_stats():
    init_session_storage()
    return st.session_state.stats

def delete_session_note_stats(note_title):
    init_session_storage()
    if note_title in st.session_state.stats:
        del st.session_state.stats[note_title]

def delete_all_session_stats():
    init_session_storage()
    st.session_state.stats = {}

# Browser local storage persistence
def save_to_local_storage():
    """
    Save session state to browser's local storage using st.download_button
    """
    data = {
        "notes": st.session_state.notes,
        "questions": st.session_state.questions,
        "stats": st.session_state.stats
    }
    return json.dumps(data)

def load_from_local_storage(json_data):
    """
    Load data from uploaded JSON file into session state
    """
    try:
        data = json.loads(json_data)
        st.session_state.notes = data.get("notes", {})
        st.session_state.questions = data.get("questions", {})
        st.session_state.stats = data.get("stats", {})
        return True
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return False 