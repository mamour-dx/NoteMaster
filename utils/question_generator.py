import os
import re
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv
from config import QUESTIONS_DIR, QUESTIONS_FILE

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# Configuration API - Use a default key if none is provided
api_key = os.getenv("DEEPSEEK_KEY", "sk-or-v1-a123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def generate_questions(note_title, note_content):
    """
    Génère des questions à partir du contenu des notes en utilisant l'API DeepSeek.
    :param note_title: Titre de la note
    :param note_content: Contenu de la note
    :return: Une liste de questions générées
    """
    try:
        # Check if we have a valid API key
        if not api_key or api_key == "sk-or-v1-a123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef":
            # Return mock questions for testing when no API key is available
            return [
                {
                    "text": "Question générée automatiquement 1 pour " + note_title,
                    "reponse": "Réponse à la question 1. Ceci est une réponse générée automatiquement car aucune clé API n'est configurée."
                },
                {
                    "text": "Question générée automatiquement 2 pour " + note_title,
                    "reponse": "Réponse à la question 2. Ceci est une réponse générée automatiquement car aucune clé API n'est configurée."
                },
                {
                    "text": "Question générée automatiquement 3 pour " + note_title,
                    "reponse": "Réponse à la question 3. Ceci est une réponse générée automatiquement car aucune clé API n'est configurée."
                }
            ]
            
        prompt = (
            f"À partir de ce texte, crée des questions relativement ouvertes qui permettent l'apprentissage actif. "
            f"Tu choisiras un nombre de questions adéquat en fonction de la longueur du texte.\n"
            f"Pour chaque question, retourne un JSON avec deux clés : "
            f"'text' pour la question et 'reponse' pour la réponse correcte.\n"
            f"Texte : {note_content}\n"
            f"Retourne uniquement du JSON, rien d'autre."
        )

        # Envoyer la requête à l'API
        response = client.chat.completions.create(
            extra_body={},
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        # Vérification de la réponse
        logging.info("Réponse brute de l'API : %s", response)
        generated_text = response.choices[0].message.content.strip()
        
        # Extraire le JSON de la réponse
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', generated_text)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Si pas de bloc de code JSON, essayer de trouver directement un JSON
            json_str = generated_text
        
        # Nettoyer le JSON
        json_str = json_str.replace('```', '').strip()
        
        # Analyser le JSON
        questions = json.loads(json_str)
        
        # Vérifier si c'est une liste ou un objet avec une clé 'questions'
        if isinstance(questions, dict) and 'questions' in questions:
            questions = questions['questions']
        
        # Sauvegarder les questions dans un fichier JSON
        questions_file = os.path.join(QUESTIONS_DIR, f"{note_title}.json")
        with open(questions_file, "w", encoding="utf-8") as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        
        return questions
    
    except Exception as e:
        logging.error(f"Erreur lors de la génération des questions : {e}")
        # Return mock questions in case of error
        return [
            {
                "text": "Question de secours 1 pour " + note_title,
                "reponse": "Réponse à la question 1. Ceci est une réponse générée automatiquement suite à une erreur."
            },
            {
                "text": "Question de secours 2 pour " + note_title,
                "reponse": "Réponse à la question 2. Ceci est une réponse générée automatiquement suite à une erreur."
            }
        ]

def save_questions(questions):
    """
    Sauvegarde les questions générées dans un fichier JSON.
    :param questions: Liste des questions
    """
    try:
        if not os.path.exists(os.path.dirname(QUESTIONS_FILE)):
            os.makedirs(os.path.dirname(QUESTIONS_FILE))
        with open(QUESTIONS_FILE, "w") as file:
            json.dump(questions, file, indent=4)
        logging.info("Questions sauvegardées dans le fichier principal : %s", QUESTIONS_FILE)
    except Exception as e:
        logging.error("Erreur lors de la sauvegarde des questions : %s", e)

def load_questions():
    """
    Charge les questions sauvegardées à partir du fichier JSON.
    :return: Liste des questions
    """
    try:
        if os.path.exists(QUESTIONS_FILE):
            with open(QUESTIONS_FILE, "r") as file:
                return json.load(file)
    except Exception as e:
        logging.error("Erreur lors du chargement des questions : %s", e)
    return []

def evaluate_answer(user_answer, correct_answer):
    """
    Évalue la réponse de l'utilisateur par rapport à la réponse correcte.
    :param user_answer: Réponse fournie par l'utilisateur
    :param correct_answer: Réponse correcte
    :return: Tuple contenant (score, feedback)
    """
    try:
        # Check if we have a valid API key
        if not api_key or api_key == "sk-or-v1-a123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef":
            # Simple evaluation logic when no API key is available
            # Count how many words from the correct answer appear in the user answer
            correct_words = set(correct_answer.lower().split())
            user_words = set(user_answer.lower().split())
            common_words = correct_words.intersection(user_words)
            
            # Calculate score based on word overlap
            score_ratio = len(common_words) / max(1, len(correct_words))
            score = min(5, max(0, round(score_ratio * 5)))
            
            feedback = "Évaluation automatique basée sur la correspondance des mots-clés."
            if score >= 4:
                feedback += " Excellente réponse!"
            elif score >= 3:
                feedback += " Bonne réponse, mais il manque quelques éléments."
            elif score >= 2:
                feedback += " Réponse partielle, plusieurs éléments importants manquent."
            else:
                feedback += " Réponse incomplète, revoyez les concepts clés."
                
            return score, feedback
            
        prompt = (
            f"Tu es un assistant d'apprentissage qui évalue les réponses des étudiants.\n"
            f"Voici la réponse correcte à une question : \"{correct_answer}\"\n"
            f"Et voici la réponse de l'étudiant : \"{user_answer}\"\n\n"
            f"Évalue la réponse de l'étudiant sur une échelle de 0 à 5, où 5 est parfait.\n"
            f"Fournis également un feedback constructif pour aider l'étudiant à s'améliorer.\n"
            f"Retourne uniquement un JSON avec deux clés : 'score' (nombre entier de 0 à 5) et 'feedback' (texte)."
        )

        # Envoyer la requête à l'API
        response = client.chat.completions.create(
            extra_body={},
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        # Extraire la réponse
        generated_text = response.choices[0].message.content.strip()
        
        # Extraire le JSON de la réponse
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', generated_text)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Si pas de bloc de code JSON, essayer de trouver directement un JSON
            json_str = generated_text
        
        # Nettoyer le JSON
        json_str = json_str.replace('```', '').strip()
        
        # Analyser le JSON
        evaluation = json.loads(json_str)
        
        # Extraire le score et le feedback
        score = evaluation.get('score', 0)
        feedback = evaluation.get('feedback', "Pas de feedback disponible.")
        
        return score, feedback
    
    except Exception as e:
        logging.error(f"Erreur lors de l'évaluation de la réponse : {e}")
        # Simple fallback evaluation
        return 3, f"Évaluation de secours suite à une erreur. Votre réponse semble partiellement correcte."