import spacy
from flask import Flask, render_template, request, jsonify

# Charger le modèle spaCy en français
nlp = spacy.load('fr_core_news_sm')

# Mise à jour du dictionnaire des offres de stage/emploi
job_offers = {
    "python": {
        "stage": {
            "été": "Stage d'Été Développeur Python, Paris, Durée: 3 mois, Type: Présentiel",
            "pfe": "Stage PFE Développeur Python, Paris, Durée: 6 mois, Type: Présentiel"
        },
        "emploi": "Développeur Python, Paris, Salaire: 3000€/mois, Expérience demandée: 2 ans"
    },
    "data scientist": {
        "stage": {
            "été": "Stage d'Été Data Scientist, Remote, Durée: 3 mois, Type: En ligne",
            "pfe": "Stage PFE Data Scientist, Remote, Durée: 6 mois, Type: En ligne"
        },
        "emploi": "Data Scientist, Remote, Salaire: 3500€/mois, Expérience demandée: 3 ans"
    },
    "javascript": {
        "stage": {
            "été": "Stage d'Été Développeur JavaScript, Lyon, Durée: 2 mois, Type: Présentiel",
            "pfe": "Stage PFE Développeur JavaScript, Lyon, Durée: 6 mois, Type: Présentiel"
        },
        "emploi": "Développeur JavaScript, Lyon, Salaire: 2500€/mois, Expérience demandée: 1 an"
    },
    "electronique": {
        "stage": {
            "été": "Stage d'Été Ingénieur Électronique, Toulouse, Durée: 3 mois, Type: Présentiel",
            "pfe": "Stage PFE Ingénieur Électronique, Toulouse, Durée: 6 mois, Type: Présentiel"
        },
        "emploi": "Ingénieur Électronique, Toulouse, Salaire: 3200€/mois, Expérience demandée: 2 ans"
    },
    "bio-mecanique": {
        "stage": {
            "été": "Stage d'Été en Bio-Mécanique, Marseille, Durée: 3 mois, Type: Présentiel",
            "pfe": "Stage PFE en Bio-Mécanique, Marseille, Durée: 6 mois, Type: Présentiel"
        },
        "emploi": "Ingénieur en Bio-Mécanique, Marseille, Salaire: 3400€/mois, Expérience demandée: 2 ans"
    },
    "machine learning": {
        "stage": {
            "été": "Stage d'Été Machine Learning, Bordeaux, Durée: 3 mois, Type: Présentiel",
            "pfe": "Stage PFE Machine Learning, Bordeaux, Durée: 6 mois, Type: Présentiel"
        },
        "emploi": "Spécialiste Machine Learning, Bordeaux, Salaire: 4000€/mois, Expérience demandée: 3 ans"
    }
}

# Ajouter les compétences associées à ces spécialités
predefined_skills = [
    "python", "data scientist", "javascript", "java", "c++", "machine learning", 
    "deep learning", "data science", "electronique", "bio mecanique",
]

# Fonction pour extraire les compétences du texte
def extract_skills_from_text(text):
    doc = nlp(text)
    skills = []
    for token in doc:
        if token.pos_ == "NOUN" and len(token.text) > 3 and token.text.lower() in predefined_skills:
            skills.append(token.text.lower())
    return skills

# Fonction de recommandation d'emplois/stages
def recommend_jobs(skills, request_type, stage_type=None):
    recommendations = []
    for skill in skills:
        if skill in job_offers:
            if request_type == "stage" and stage_type:
                recommendations.append(job_offers[skill]["stage"].get(stage_type, "Aucune offre de stage disponible."))
            elif request_type == "emploi":
                recommendations.append(job_offers[skill]["emploi"])
    if not recommendations:
        return ["Aucune offre disponible pour les compétences détectées."]
    return recommendations

# Initialiser Flask
app = Flask(__name__)

# Route pour afficher la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour traiter la soumission des compétences et recommander des emplois/stages
@app.route('/process_skills', methods=['POST'])
def process_skills():
    try:
        # Récupérer les compétences sélectionnées
        skills_input = request.form['skills']
        skills = skills_input.split(',')  # Séparer les compétences par des virgules
        skills = [skill.strip().lower() for skill in skills]  # Nettoyer les espaces et rendre en minuscules

        # Récupérer le type de demande (stage ou emploi)
        request_type = request.form.get('request_type').lower()

        # Si le type est "stage", récupérer le champ "stage_type". Sinon, l'ignorer.
        stage_type = request.form.get('stage_type') if request_type == "stage" else None

        # Recommander les emplois ou stages en fonction des compétences et du type de demande
        recommended_jobs = recommend_jobs(skills, request_type, stage_type)

        # Rendre la page des recommandations
        return render_template('recommandations.html', recommendations=recommended_jobs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
