import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import pandas as pd
import datetime

def set_background_image(image_path):
    """
    Sets a background image for the Streamlit application using CSS.
    Args:
        image_path (str): The path to the local image file.
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{_get_base64_image(image_path)}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def _get_base64_image(image_path):
    """Helper to convert local image to base64 for CSS background."""
    import base64
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- Apply the background image ---
try:
    set_background_image('icon/bg.png') # Ensure 'icon/bg.png' is in the correct path
except FileNotFoundError:
    st.warning("Background image 'icon/bg.png' not found. Please ensure it's in the correct path.")

# --- Glasmorphism CSS ---
st.markdown(
    """
    <style>
    body {
        color: #333333;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #222222;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .stTextInput label, .stSelectbox label, .stRadio label, .stFileUploader label, .stCameraInput label {
        color: #333333;
        font-weight: bold;
    }
    .stButton>button {
        background-color: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #333333;
        transition: all 0.3s ease;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.3);
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    }
    .col-card {
            flex: 1 1 calc(25% - 20px);
            min-width: 220px;
            max-width: 250px;
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            background-color: #fcfcfc;
            transition: transform 0.2s ease-in-out;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
    }
    .css-pkaj6s { /* Common class for the sidebar parent div */
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin-right: 10px;
    }
    .glasmorphism-card {
        background: rgba(255, 255, 255, 0.25);
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 15px;
        margin-bottom: 15px;
    }
    .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .card h3 {
            color: #4a5568;
            margin-bottom: 20px;
            font-size: 1.4rem;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }

        .stat-card h4 {
            font-size: 2rem;
            margin-bottom: 10px;
        }

        .stat-card p {
            opacity: 0.9;
            font-size: 1.1rem;
        }

        .batch-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }

        .batch-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }

        .batch-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }

        .batch-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .batch-id {
            font-weight: bold;
            color: #4a5568;
            font-size: 1.1rem;
        }

        .lifecycle-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            text-transform: uppercase;
        }

        .lifecycle-egg { background: #ffeaa7; color: #2d3436; }
        .lifecycle-larva { background: #74b9ff; color: white; }
        .lifecycle-pupa { background: #fd79a8; color: white; }
        .lifecycle-adult { background: #00b894; color: white; }

        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }

        .status-healthy { background: #00b894; }
        .status-warning { background: #fdcb6e; }
        .status-critical { background: #e17055; }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #4a5568;
        }

        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }

        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }

        .btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
            margin-right: 10px;
            margin-bottom: 10px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: #718096;
        }

        .btn-danger {
            background: #e53e3e;
        }

        .btn-success {
            background: #38a169;
        }

        .btn-small {
            padding: 8px 16px;
            font-size: 0.9rem;
        }

        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid;
        }

        .alert-success {
            background: #f0fff4;
            border-color: #38a169;
            color: #22543d;
        }

        .alert-warning {
            background: #fffbf0;
            border-color: #d69e2e;
            color: #744210;
        }

        .alert-danger {
            background: #fff5f5;
            border-color: #e53e3e;
            color: #742a2a;
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.3s ease;
        }

        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
        }

        .modal-content {
            background: white;
            margin: 5% auto;
            padding: 30px;
            border-radius: 15px;
            width: 90%;
            max-width: 800px;
            position: relative;
            max-height: 80vh;
            overflow-y: auto;
        }

        .close {
            position: absolute;
            right: 20px;
            top: 20px;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            color: #718096;
        }

        .close:hover {
            color: #4a5568;
        }

        .qr-code {
            text-align: center;
            margin: 20px 0;
        }

        .qr-code img {
            max-width: 200px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .nav-tabs {
                flex-direction: column;
            }
            
            .batch-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border-radius: 8px;
            padding: 15px 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            z-index: 1001;
            max-width: 300px;
            transform: translateX(350px);
            transition: transform 0.3s ease;
        }

        .notification.show {
            transform: translateX(0);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Configuration and Model Loading ---
MODEL_DIR = './model'
IMAGE_SIZE = (180, 180)

if not os.path.exists(MODEL_DIR):
    st.error(f"Model directory not found: {MODEL_DIR}. Please create it and place your models inside.")
    st.stop()

DATA_DIR = './Data'
os.makedirs(DATA_DIR, exist_ok=True)


# --- Define SPECIES_HOST_PLANTS constant ---
SPECIES_HOST_PLANTS = {
    'Butterfly-Clippers': { 'plant': ['Ixora', 'Wild Cucumber'], 'dailyConsumption': 120 },
    'Butterfly-Common Jay': { 'plant': ['Avocado Tree', 'Soursop', 'Sugar Apple', 'Amuyon', 'Indian Tree'], 'dailyConsumption': 160 },
    'Butterfly-Common Lime': { 'plant': ['Limeberry', 'Calamondin', 'Pomelo', 'Sweet Orange', 'Calamansi'], 'dailyConsumption': 140 },
    'Butterfly-Common Mime': { 'plant': ['Clover Cinnamon', 'Wild Cinnamon'], 'dailyConsumption': 150 },
    'Butterfly-Common Mormon': { 'plant': ['Limeberry', 'Calamondin', 'Pomelo', 'Sweet Orange', 'Calamansi', 'Lemoncito'], 'dailyConsumption': 155 },
    'Butterfly-Emerald Swallowtail': { 'plant': ['Curry Leafs', 'Pink Lime-Berry Tree'], 'dailyConsumption': 180 },
    'Butterfly-Golden Birdwing': { 'plant': ['Dutchman pipe', 'Indian Birthwort'], 'dailyConsumption': 200 },
    'Butterfly-Gray Glassy Tiger': { 'plant': ['Parsonsia'], 'dailyConsumption': 130 }, # Corrected to list
    'Butterfly-Great Eggfly': { 'plant': ['Sweet Potato', 'Water Spinach', 'Portulaca'], 'dailyConsumption': 125 },
    'Butterfly-Great Yellow Mormon': { 'plant': ['Limeberry', 'Calamondin', 'Pomelo', 'Sweet Orange', 'Calamansi'], 'dailyConsumption': 165 },
    'Butterfly-Paper Kite': { 'plant': ['Common Skillpod'], 'dailyConsumption': 145 },
    'Butterfly-Plain Tiger': { 'plant': ['Crown flower', 'Giant Milkweed'], 'dailyConsumption': 135 },
    'Butterfly-Red Lacewing': { 'plant': ['Wild Bush Passion Fruits'], 'dailyConsumption': 170 },
    'Butterfly-Scarlet Mormon': { 'plant': ['Calamondin', 'Pomelo', 'Sweet Orange', 'Calamansi'], 'dailyConsumption': 158 },
    'Butterfly-Pink Rose': { 'plant': ['Dutchman pipe', 'Indian Birthwort'], 'dailyConsumption': 185 },
    'Butterfly-Tailed Jay': { 'plant': ['Avocado Tree', 'Soursop', 'Sugar Apple', 'Amuyon', 'Indian Tree'], 'dailyConsumption': 140 },
    'Moth-Atlas': { 'plant': ['Willow'], 'dailyConsumption': 220 }, # Corrected to list
    'Moth-Giant Silk': { 'plant': ['Gmelina Tree', 'Cassia'], 'dailyConsumption': 250 }
}


# --- Load Models (once) ---
@st.cache_resource
def load_model(model_name):
    model_path = os.path.join(MODEL_DIR, model_name)
    if not os.path.exists(model_path):
        st.error(f"Model not found at: {model_path}. Please ensure the model is saved there.")
        return None
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading {model_name} Model: {e}")
        return None

butterfly_species_model = load_model('model_Butterfly_Species.h5')
lifestages_model = load_model('model_Life_Stages.h5')
pupaedefects_model = load_model('model_Pupae_Defects.h5')
larvaldiseases_model = load_model('model_Larval_Diseases.h5') # Changed to h1 to simulate a missing model for testing


# --- Define Class Names and Associated Information for Each Model ---
# Integrate host plant info directly into butterfly_species_info
butterfly_species_info = {
    "Butterfly-Clippers": {"scientific_name": "Parthenos sylvia", "family": "Nymphalidae", "discovered":"Carl Peter Thunberg, Cramer","year":"1776", "description":"Forewing triangular; costa very slightly curved, apex rounded, exterior margin oblique and slightly scalloped, posterior margin short, angle convex; ", "value": 25, **SPECIES_HOST_PLANTS.get('Butterfly-Clippers', {})},
    "Butterfly-Common Jay": {"scientific_name": "Graphium doson", "family": "Papilionidae", "discovered":"C. & R. Felder","year":"1864", "description":"", "value": 30, **SPECIES_HOST_PLANTS.get('Butterfly-Common Jay', {})},
    "Butterfly-Common Lime": {"scientific_name": "Papilio demoleus", "family": "Papilionidae", "discovered":"Linnaeus","year":"1758", "description":"The butterfly is tailless and has a wingspan 80–100 mm,the butterfly has a large number of irregular spots on the wing.", "value": 20, **SPECIES_HOST_PLANTS.get('Butterfly-Common Lime', {})},
    "Butterfly-Common Mime": {"scientific_name": "Papilio clytia", "family": "Papilionidae", "discovered":"Linnaeus","year":"1758", "description":" It's a black-bodied swallowtail and a good example of Batesian mimicry, meaning it mimics the appearance of other distasteful butterflies. ", "value": 28, **SPECIES_HOST_PLANTS.get('Butterfly-Common Mime', {})},
    "Butterfly-Common Mormon": {"scientific_name": "Papilio polytes", "family": "Papilionidae","discovered":"Linnaeus","year":"1758", "description":" ", "value": 28, **SPECIES_HOST_PLANTS.get('Butterfly-Common Mormon', {})},
    "Butterfly-Emerald Swallowtail": {"scientific_name": "Papilio palinurus", "family": "Papilionidae", "discovered":"Fabricius","year":"1787", "description":"", "value": 50, **SPECIES_HOST_PLANTS.get('Butterfly-Emerald Swallowtail', {})},
    "Butterfly-Golden Birdwing": {"scientific_name": "Troides rhadamantus", "family": "Papilionidae", "discovered":"H. Lucas","year":"1835", "description":"", "value": 45, **SPECIES_HOST_PLANTS.get('Butterfly-Golden Birdwing', {})},
    "Butterfly-Gray Glassy Tiger": {"scientific_name": "Ideopsis juventa", "family": "Nymphalidae", "discovered":"Cramer","year":"1777", "description":"", "value": 30, **SPECIES_HOST_PLANTS.get('Butterfly-Gray Glassy Tiger', {})},
    "Butterfly-Great Eggfly": {"scientific_name": "Hypolimnas bolina", "family": "Nymphalidae", "discovered":"Linnaeus","year":"1758", "description":"", "value": 35, **SPECIES_HOST_PLANTS.get('Butterfly-Great Eggfly', {})},
    "Butterfly-Great Yellow Mormon": {"scientific_name": "Papilio lowi", "family": "Papilionidae", "discovered":"Wallace","year":"1865", "description":"", "value": 40, **SPECIES_HOST_PLANTS.get('Butterfly-Great Yellow Mormon', {})},
    "Butterfly-Paper Kite": {"scientific_name": "Idea leuconoe", "family": "Nymphalidae", "discovered":"Rothschild","year":"1895", "description":"", "value": 35, **SPECIES_HOST_PLANTS.get('Butterfly-Paper Kite', {})},
    "Butterfly-Pink Rose": {"scientific_name": "Pachliopta kotzebuea", "family": "Papilionidae", "discovered":"Escholtz","year":"1821", "description":"", "value": 32, **SPECIES_HOST_PLANTS.get('Butterfly-Pink Rose', {})},
    "Butterfly-Plain Tiger": {"scientific_name": "Danaus chrysippus", "family": "Nymphalidae", "discovered":"Hulstaert","year":"1931", "description":"", "value": 25, **SPECIES_HOST_PLANTS.get('Butterfly-Plain Tiger', {})},
    "Butterfly-Red Lacewing": {"scientific_name": "Cethosia biblis", "family": "Nymphalidae", "discovered":"Drury","year":"1773", "description":"", "value": 28, **SPECIES_HOST_PLANTS.get('Butterfly-Red Lacewing', {})},
    "Butterfly-Scarlet Mormon": {"scientific_name": "Papilio rumanzovia", "family": "Papilionidae", "discovered":"Eschscholtz","year":"1821", "description":"", "value": 40, **SPECIES_HOST_PLANTS.get('Butterfly-Scarlet Mormon', {})},
    "Butterfly-Tailed Jay": {"scientific_name": "Graphium agamemnon", "family": "Papilionidae", "discovered":"Linnaeus","year":"1758", "description":"", "value": 30, **SPECIES_HOST_PLANTS.get('Butterfly-Tailed Jay', {})},
    "Moth-Atlas": {"scientific_name": "Attacus atlas", "family": "Saturniidae","discovered":"Linnaeus","year":"1758", "description":"", "value": 45, **SPECIES_HOST_PLANTS.get('Moth-Atlas', {})},
    "Moth-Giant Silk": {"scientific_name": "Samia cynthia", "family": "Saturniidae", "discovered":"Hubner","year":"1819", "description":"", "value": 40, **SPECIES_HOST_PLANTS.get('Moth-Giant Silk', {})},
}
butterfly_species_names = list(butterfly_species_info.keys())

lifestages_info = {
    "Butterfly": {"stages_info": "Reproductive stage, winged insect capable of flight."},
    "Eggs": {"stages_info": "Early developmental stage, typically laid on host plants."},
    "Larvae": {"stages_info": "Caterpillar stage, primary feeding and growth phase."},
    "Pupae": {"stages_info": "Chrysalis (butterfly) or cocoon (moth) stage, metamorphosis occurs."},
}
lifestages_names = list(lifestages_info.keys())

pupaedefects_info = {
    "Ant bites": {"quality_info": "Indicates ant damage, can lead to pupae death or malformation.", "impact_score": 0.3},
    "Deformed body": {"quality_info": "Physical deformities, may indicate poor health or environmental stress.", "impact_score": 0.5},
    "Healthy Pupae": {"quality_info": "No visible defects, good potential for adult emergence.", "impact_score": 1.0},
    "Old Pupa": {"quality_info": "Pupae nearing emergence or past its prime, may be discolored or shriveled.", "impact_score": 0.4},
    "Overbend": {"quality_info": "Abnormal curvature, can impede proper development.", "impact_score": 0.6},
    "Stretch abdomen": {"quality_info": "Abdomen appears stretched or elongated, potentially due to stress or disease.", "impact_score": 0.7},
}
pupaedefects_names = list(pupaedefects_info.keys())

larvaldiseases_info = {
    "Anaphylaxis Infection": {"treatment_info": "Seek entomologist advice; isolate infected larvae. No specific treatment for severe cases.", "impact_score": 0.7},
    "Gnathostomiasis": {"treatment_info": "Parasitic infection. Isolate, remove parasites if visible, improve hygiene.", "impact_score": 0.6},
    "Healthy": {"treatment_info": "Larva appears healthy with no signs of disease.", "impact_score": 1.0},
    "Nucleopolyhedrosis": {"treatment_info": "Highly contagious viral disease. Isolate and destroy infected larvae to prevent spread. Disinfect rearing areas.", "impact_score": 0.9},
}
larvaldiseases_names = list(larvaldiseases_info.keys())


# --- Classification Function ---
def classify_image(image_file, model, class_names, details_dict=None):
    if model is None:
        return None

    try:
        image = Image.open(image_file)
        img_resized = image.resize(IMAGE_SIZE)
        img_array = tf.keras.utils.img_to_array(img_resized)
        img_array = tf.expand_dims(img_array, 0)

        predictions = model.predict(img_array)
        result = tf.nn.softmax(predictions[0])
        
        # Get top 3 predictions for detailed analysis
        top_indices = np.argsort(result)[::-1][:3]
        top_predictions = []
        for i in top_indices:
            if i < len(class_names):
                class_name = class_names[i]
                score = result[i].numpy() * 100
                top_predictions.append({"class_name": class_name, "score": score})

        predicted_class_index = np.argmax(result)
        predicted_score = np.max(result).item() * 100

        if predicted_class_index < len(class_names):
            predicted_class_name = class_names[predicted_class_index]
            result_data = {
                "class_name": predicted_class_name,
                "score": predicted_score,
                "index": predicted_class_index,
                "top_predictions": top_predictions
            }
            if details_dict and predicted_class_name in details_dict:
                result_data.update(details_dict[predicted_class_name])
            return result_data
        else:
            return {"class_name": "Unknown Class (Index out of bounds)", "score": 0.0, "index": predicted_class_index, "top_predictions": []}
    except Exception as e:
        st.error(f"Error during image classification: {e}")
        return None

# --- Functions for Analysis and Recommendations ---

def calculate_health_score_and_grade(classification_result, classifier_type):
    health_score = 0.0
    quality_grade = "N/A"

    if classifier_type == "Larval Diseases":
        if classification_result['class_name'] == "Healthy":
            health_score = 100.0
        elif 'impact_score' in classification_result:
            health_score = (1 - classification_result['impact_score']) * 100
        else:
            health_score = 20.0 # Default for diseases without specific impact_score

        if health_score >= 80: quality_grade = "A+"
        elif health_score >= 60: quality_grade = "B"
        elif health_score >= 40: quality_grade = "C"
        else: quality_grade = "D"

    elif classifier_type == "Pupae Defects":
        if classification_result['class_name'] == "Healthy Pupae":
            health_score = 100.0
        elif 'impact_score' in classification_result:
            health_score = (1 - classification_result['impact_score']) * 100
        else:
            health_score = 50.0 # Default for other defects

        if health_score >= 85: quality_grade = "A+"
        elif health_score >= 70: quality_grade = "B"
        elif health_score >= 50: quality_grade = "C"
        else: quality_grade = "D"
            
    elif classifier_type == "Life Stages":
        health_score = 100.0
        quality_grade = "A+"
        
    elif classifier_type == "Butterfly Species":
        health_score = 100.0
        quality_grade = "A+"
    else: # Added a default case for unexpected classifier types
        st.warning(f"Unknown classifier type '{classifier_type}' for health score calculation.")
        health_score = 0.0
        quality_grade = "N/A"


    return health_score, quality_grade

def get_recommended_actions(classification_result, classifier_type):
    recommendations = []

    if classifier_type == "Larval Diseases":
        class_name = classification_result['class_name']
        if class_name == "Nucleopolyhedrosis":
            recommendations.append("Isolate and destroy infected larvae immediately to prevent widespread contamination. Disinfect all rearing equipment and areas thoroughly.")
        elif class_name == "Anaphylaxis Infection":
            recommendations.append("Consult an entomologist for specific guidance. Isolate affected larvae to prevent potential spread. Consider improving environmental conditions to reduce stress.")
        elif class_name == "Gnathostomiasis":
            recommendations.append("Inspect larvae closely for visible parasites and carefully remove them if found. Improve hygiene practices in the rearing environment to prevent reinfection.")
        elif class_name == "Healthy":
            recommendations.append("Continue current rearing practices. Monitor larvae regularly for any changes in health or behavior.")
        recommendations.append("Maintain optimal temperature and humidity. Ensure proper ventilation and avoid overcrowding.")

    elif classifier_type == "Pupae Defects":
        class_name = classification_result['class_name']
        if class_name == "Ant bites":
            recommendations.append("Implement ant control measures in rearing areas (e.g., ant moats, sticky barriers). Relocate vulnerable pupae to a protected environment.")
        elif class_name == "Deformed body" or class_name == "Overbend" or class_name == "Stretch abdomen":
            recommendations.append("Review environmental conditions (temperature, humidity, substrate). Ensure adequate space and proper hanging conditions for pupation. Cull severely affected pupae to prevent unhealthy adults.")
        elif class_name == "Old Pupa":
            recommendations.append("Monitor closely for emergence. If no emergence after expected period, gently check viability. Note that emergence rate might be lower.")
        elif class_name == "Healthy Pupae":
            recommendations.append("Continue providing stable and optimal environmental conditions. Prepare for adult emergence.")
        recommendations.append("Minimize handling of pupae. Maintain consistent environmental parameters suitable for the species.")

    elif classifier_type == "Butterfly Species":
        species_name = classification_result['class_name']
        if species_name in SPECIES_HOST_PLANTS:
            host_info = SPECIES_HOST_PLANTS[species_name]
            plant_name = ", ".join(host_info['plant']) if isinstance(host_info['plant'], list) else host_info['plant']
            daily_consumption = host_info['dailyConsumption']
            recommendations.append(f"Optimize care for **{species_name}**: Ensure proper **{plant_name}** supply ({daily_consumption}g/day).")
        else:
             recommendations.append(f"Optimize care for **{species_name}**: Research specific host plant and daily consumption requirements.")
        recommendations.append("Provide adequate space and ventilation for adult butterflies. Offer nectar sources (flowers or sugar water) for sustenance.")

    elif classifier_type == "Life Stages":
        class_name = classification_result['class_name']
        if class_name == "Eggs":
            recommendations.append("Maintain appropriate humidity to prevent desiccation. Protect from predators. Monitor for hatching.")
        elif class_name == "Larvae":
            recommendations.append("Ensure a constant supply of fresh host plant leaves. Maintain good hygiene to prevent disease. Monitor growth and prepare for pupation.")
        elif class_name == "Pupae":
            recommendations.append("Keep pupae undisturbed in a stable environment. Maintain humidity to aid emergence. Protect from physical damage and predators.")
        elif class_name == "Butterfly":
            recommendations.append("Provide nectar sources and water. Ensure suitable conditions for mating and egg-laying, if breeding.")
    else: # Added a default case for unexpected classifier types
        recommendations.append(f"No specific recommendations for unknown classifier type: {classifier_type}.")

    return recommendations


# --- Streamlit UI Layout ---
st.title("🦋 Lepretty App")
st.write("Upload an image or capture from your webcam to classify butterflies, their life stages, or identify pupae defects and larval diseases.")

# Sidebar for navigation
st.sidebar.title("Classify")
selected_menu_item = st.sidebar.radio(
    "Go to Menu",
    ["Image Classifiers"]
)

# --- Main Content Area based on Mode Selection ---
if selected_menu_item == "Image Classifiers":
    st.header("🔬 Image Classifiers")
    st.write("Select a classifier to analyze your butterfly images.")

    classifier_choice = st.radio(
        "Choose Classifier Type",
        ["Butterfly Species", "Life Stages", "Pupae Defects", "Larval Diseases"]
    )

    st.markdown("---")

    input_method = st.radio("Choose an input method:", ("Upload Image", "Capture from Webcam"))

    uploaded_file = None
    camera_image = None

    if input_method == "Upload Image":
        uploaded_file = st.file_uploader(f"Upload an image for {classifier_choice} classification...", type=["jpg", "jpeg", "png"])
    elif input_method == "Capture from Webcam":
        camera_image = st.camera_input("Take a picture")

    source_image = None
    if uploaded_file is not None:
        source_image = uploaded_file
    elif camera_image is not None:
        source_image = camera_image

    if source_image is not None:
        st.image(source_image, caption='Image for Classification', use_container_width=True)
        st.write("")
        
        status_placeholder = st.empty()
        status_placeholder.write("Classifying...")

        model_to_use = None
        class_names_to_use = []
        details_to_use = {}
        csv_file_path = None

        if classifier_choice == "Butterfly Species":
            model_to_use = butterfly_species_model
            class_names_to_use = butterfly_species_names
            details_to_use = butterfly_species_info
            csv_file_path = os.path.join(DATA_DIR, "butterfly_species_records.csv")
        elif classifier_choice == "Life Stages":
            model_to_use = lifestages_model
            class_names_to_use = lifestages_names
            details_to_use = lifestages_info
            csv_file_path = os.path.join(DATA_DIR, "life_stages_records.csv")
        elif classifier_choice == "Pupae Defects":
            model_to_use = pupaedefects_model
            class_names_to_use = pupaedefects_names
            details_to_use = pupaedefects_info
            csv_file_path = os.path.join(DATA_DIR, "pupae_defects_records.csv")
        elif classifier_choice == "Larval Diseases":
            model_to_use = larvaldiseases_model
            class_names_to_use = larvaldiseases_names
            details_to_use = larvaldiseases_info
            csv_file_path = os.path.join(DATA_DIR, "larval_diseases_records.csv")

        if model_to_use:
            classification_result = classify_image(source_image, model_to_use, class_names_to_use, details_to_use)
            
            status_placeholder.write("Done!")

            if classification_result and classification_result['class_name'] != "Unknown Class (Index out of bounds)":
                st.success(f"**{classifier_choice} Prediction:** **{classification_result['class_name']}** (Confidence: {classification_result['score']:.2f}%)")

                # Display additional information
                if 'scientific_name' in classification_result:
                    st.write(f"Scientific Name: {classification_result['scientific_name']}")
                    st.write(f"Family: {classification_result['family']}")
                    st.write(f"Discovered by: {classification_result['discovered']}")
                    st.write(f"Year: {classification_result['year']}")
                    if 'description' in classification_result and classification_result['description']:
                        st.write(f"Description: {classification_result['description']}")
                    # Display host plant and daily consumption for species
                    if 'plant' in classification_result:
                        plant_display = ", ".join(classification_result['plant']) if isinstance(classification_result['plant'], list) else classification_result['plant']
                        st.write(f"Host Plant: {plant_display}")
                    if 'dailyConsumption' in classification_result:
                        st.write(f"Daily Consumption: {classification_result['dailyConsumption']}g/day")

                if 'stages_info' in classification_result:
                    st.write(f"Stages Info: {classification_result['stages_info']}")
                if 'quality_info' in classification_result:
                    st.write(f"Quality Info: {classification_result['quality_info']}")
                if 'treatment_info' in classification_result:
                    st.write(f"Treatment Info: {classification_result['treatment_info']}")

                st.markdown("---") # Separator

                # --- Analysis Results Table (Top Predictions) ---
                st.subheader("📊 Analysis Results")
                if classification_result['top_predictions']:
                    top_df_data = []
                    for pred in classification_result['top_predictions']:
                        row = {"Classification": pred['class_name'], "Confidence": f"{pred['score']:.1f}%"}
                        
                        if classifier_choice == "Butterfly Species":
                            if 'value' in butterfly_species_info.get(pred['class_name'], {}):
                                row["Value"] = f"${butterfly_species_info[pred['class_name']]['value']}"
                        
                        elif classifier_choice == "Larval Diseases":
                            if pred['class_name'] in larvaldiseases_info:
                                impact = larvaldiseases_info[pred['class_name']].get('impact_score', 0)
                                row["Impact"] = f"{impact*100:.0f}%"
                        elif classifier_choice == "Pupae Defects":
                            if pred['class_name'] in pupaedefects_info:
                                impact = pupaedefects_info[pred['class_name']].get('impact_score', 0)
                                grade = ""
                                if impact <= 0.2: grade = "A+" # Healthy/very low impact
                                elif impact <= 0.4: grade = "A"
                                elif impact <= 0.6: grade = "B"
                                elif impact <= 0.8: grade = "C"
                                else: grade = "D" # High impact
                                row["Grade"] = grade

                        top_df_data.append(row)
                    
                    st.dataframe(pd.DataFrame(top_df_data), hide_index=True, use_container_width=True)
                else:
                    st.info("No detailed top predictions available.")

                st.markdown("---") # Separator

                # --- Overall Assessment (Health Score & Quality Grade) ---
                st.subheader("📈 Overall Assessment")
                
                # Pass classifier_choice directly
                health_score, quality_grade = calculate_health_score_and_grade(classification_result, classifier_choice)

                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Health Score", value=f"{health_score:.1f}%")
                with col2:
                    st.metric(label="Quality Grade", value=quality_grade)

                st.markdown("---") # Separator

                # --- Recommended Actions ---
                st.subheader("💡 Recommended Actions")
                # Pass classifier_choice directly
                recommendations = get_recommended_actions(classification_result, classifier_choice)
                if recommendations:
                    for i, action in enumerate(recommendations):
                        st.markdown(f"- {action}")
                else:
                    st.info("No specific recommendations available for this classification.")

                # --- Data Logging ---
                date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                location = "Imus, Calabarzon, Philippines" 

                image_filename_for_log = ""
                if uploaded_file is not None:
                    image_filename_for_log = uploaded_file.name
                elif camera_image is not None:
                    image_filename_for_log = f"webcam_capture_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

                log_entry = {
                    "classifier_type": classifier_choice,
                    "class_name": classification_result['class_name'],
                    "score": classification_result['score'],
                    "health_score": health_score,
                    "quality_grade": quality_grade,
                    "date_time": date_time,
                    "location": location,
                    "image_path": image_filename_for_log,
                }
                
                # Add specific details to the log entry
                if 'scientific_name' in classification_result:
                    log_entry["scientific_name"] = classification_result['scientific_name']
                    log_entry["family"] = classification_result['family']
                    log_entry["discovered"] = classification_result["discovered"]
                    log_entry["year"] = classification_result["year"]
                    if 'description' in classification_result:
                        log_entry["description"] = classification_result["description"]
                if 'stages_info' in classification_result:
                    log_entry["stages_info"] = classification_result['stages_info']
                if 'quality_info' in classification_result:
                    log_entry["quality_info"] = classification_result['quality_info']
                if 'treatment_info' in classification_result:
                    log_entry["treatment_info"] = classification_result['treatment_info']
                # Log host plant and daily consumption
                if 'plant' in classification_result:
                    log_entry["host_plant"] = ", ".join(classification_result['plant']) if isinstance(classification_result['plant'], list) else classification_result['plant']
                if 'dailyConsumption' in classification_result:
                    log_entry["daily_consumption_g_day"] = classification_result['dailyConsumption']


                df_log = pd.DataFrame([log_entry])

                if os.path.exists(csv_file_path):
                    df_log.to_csv(csv_file_path, mode='a', header=False, index=False)
                else:
                    df_log.to_csv(csv_file_path, mode='w', header=True, index=False)
                
                st.success(f"Classification result logged to {csv_file_path}")

            else:
                st.error(f"Could not classify the image for {classifier_choice} or prediction was 'Unknown Class'.")
        else:
            st.warning(f"The {classifier_choice} model is not loaded. Please check the model path and ensure the model file exists.")