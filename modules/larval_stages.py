# import os
# import tensorflow as tf
# import numpy as np
# from PIL import Image

# MODEL_DIR = 'model'
# MODEL_NAME = 'model_Larval_Stages.h5'
# IMAGE_SIZE = (180, 180)

# larval_stages = [
#     'day 1', 'day 10-fifth instar', 'day 11', 'day 12', 'day 13', 'day 14',
#     'day 2-first instar', 'day 3', 'day 4-second instar', 'day 5',
#     'day 6-third instar', 'day 7', 'day 8-fourth instar', 'day 9'
# ]

# def load_model():
#     """Load Keras model once"""
#     model_path = os.path.join(MODEL_DIR, MODEL_NAME)
#     if not os.path.exists(model_path):
#         return None
#     return tf.keras.models.load_model(model_path)

# def ai_larval_stages_classifier(image_file, model):
#     """Run AI classification on uploaded larval image"""
#     if model is None:
#         return None

#     image = Image.open(image_file)
#     img_resized = image.resize(IMAGE_SIZE)
#     img_array = tf.keras.utils.img_to_array(img_resized)
#     img_array = tf.expand_dims(img_array, 0)

#     predictions = model.predict(img_array)
#     result = tf.nn.softmax(predictions[0])

#     top_indices = np.argsort(result)[::-1][:3]
#     top_predictions = [
#         {"class_name": larval_stages[i], "score": float(result[i].numpy()) * 100}
#         for i in top_indices if i < len(larval_stages)
#     ]

#     return {
#         "class_name": larval_stages[int(np.argmax(result))],
#         "score": float(np.max(result).numpy()) * 100,
#         "index": int(np.argmax(result)),
#         "top_predictions": top_predictions
#     }

# def get_larval_stage(species_name: str, larval_stages: int) -> str:
#     """Returns lifecycle stage given species + days since egg hatched"""
#     LIFECYCLE_DURATIONS = {
#         "Butterfly-Clippers": [3, 4, 4, 5, 6, 15],
#         "Butterfly-Common Jay": [4, 5, 4, 6, 7, 12],
#         "Butterfly-Common Lime": [3, 3, 4, 4, 5, 14],
#         "Butterfly-Common Mime": [4, 4, 5, 5, 6, 18],
#         "Butterfly-Common Mormon": [3, 4, 5, 5, 6, 16],
#         "Butterfly-Emerald Swallowtail": [4, 4, 5, 6, 7, 15],
#         "Butterfly-Golden Birdwing": [5, 6, 7, 8, 9, 25],
#         "Butterfly-Gray Glassy Tiger": [3, 4, 4, 5, 5, 13],
#         "Butterfly-Great Eggfly": [4, 5, 6, 6, 7, 20],
#         "Butterfly-Great Yellow Mormon": [3, 4, 5, 6, 7, 17],
#         "Butterfly-Paper Kite": [3, 4, 5, 5, 6, 19],
#         "Butterfly-Pink Rose": [4, 5, 5, 6, 7, 15],
#         "Butterfly-Plain Tiger": [3, 4, 4, 5, 5, 12],
#         "Butterfly-Red Lacewing": [4, 5, 5, 6, 7, 14],
#         "Butterfly-Scarlet Mormon": [3, 4, 5, 5, 6, 16],
#         "Butterfly-Tailed Jay": [4, 5, 5, 6, 7, 13],
#         "Moth-Atlas": [7, 8, 9, 10, 12, 30],
#         "Moth-Giant Silk": [6, 7, 8, 9, 10, 25]
#     }

#     if species_name not in LIFECYCLE_DURATIONS:
#         return f"Error: '{species_name}' not in database."

#     durations = LIFECYCLE_DURATIONS[species_name]
#     instar_days, pupa_days = durations[:5], durations[5]

#     cumulative_days = 0
#     for i, d in enumerate(instar_days, start=1):
#         cumulative_days += d
#         if larval_stages <= cumulative_days:
#             return f"The {species_name} is currently in Instar {i}."

#     if larval_stages <= cumulative_days + pupa_days:
#         return f"The {species_name} is a pupa (day {larval_stages - cumulative_days})."

#     return f"The {species_name} has emerged as an adult."


import streamlit as st
import pandas as pd
import os
import tensorflow as tf
from PIL import Image
import numpy as np

# Define global variables for the AI model
MODEL_DIR = 'model'  # Assuming the model is in the 'model' subdirectory
MODEL_NAME = 'model_Larval_Stages.h5'
IMAGE_SIZE = (180, 180) # Define the expected input size for the model
CLASSIFICATION_CSV = 'ai_larval_stages.csv'

# Define the class names based on your confusion matrix
larval_stages = [
    'day 1', 'day 2-first instar', 'day 3', 'day 4-second instar', 'day 5',
    'day 6-third instar', 'day 7', 'day 8-fourth instar', 'day 9','day 10-fifth instar', 
    'day 11', 'day 12', 'day 13', 'day 14',
]
def larval_stages_app():
    # st.title("Butterfly & Moth Larval Stages Tracker 🐛🦋")
    # st.markdown("This application helps you track the **larval stages** of various butterflies and moths.")
    # # Use Streamlit's cache to load the model only once
    @st.cache_resource
    def load_model(model_name):
        """Loads a Keras model from the specified path."""
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

    # The AI classification function
    def ai_larval_stages_classifier(image_file, model, larval_stages):
        """
        Classifies an uploaded image using the provided AI model.
        """
        if model is None:
            return {"class_name": "Model Not Loaded", "score": 0.0, "index": -1, "top_predictions": []}

        try:
            image = Image.open(image_file)
            img_resized = image.resize(IMAGE_SIZE)
            img_array = tf.keras.utils.img_to_array(img_resized)
            img_array = tf.expand_dims(img_array, 0) # Add batch dimension

            predictions = model.predict(img_array)
            result = tf.nn.softmax(predictions[0])
            
            # Get top 3 predictions
            top_indices = np.argsort(result)[::-1][:3]
            top_predictions = []
            for i in top_indices:
                if i < len(larval_stages):
                    class_name = larval_stages[i]
                    score = result[i].numpy() * 100
                    top_predictions.append({"class_name": class_name, "score": score})

            predicted_class_index = np.argmax(result)
            predicted_score = np.max(result).item() * 100

            if predicted_class_index < len(larval_stages):
                predicted_class_name = larval_stages[predicted_class_index]
                result_data = {
                    "class_name": predicted_class_name,
                    "score": predicted_score,
                    "index": predicted_class_index,
                    "top_predictions": top_predictions
                }
                return result_data
            else:
                return {"class_name": "Unknown Class (Index out of bounds)", "score": 0.0, "index": predicted_class_index, "top_predictions": []}
        except Exception as e:
            st.error(f"Error during image classification: {e}")
            return None

    def get_larval_stages(species_name: str, larval_stages: int) -> str:
        """
        Determines the current lifecycle stage of a butterfly or moth based on the number of days.
        """
        LIFECYCLE_DURATIONS = {
            "Butterfly-Clippers": [3, 4, 4, 5, 6, 15],
            "Butterfly-Common Jay": [4, 5, 4, 6, 7, 12],
            "Butterfly-Common Lime": [3, 3, 4, 4, 5, 14],
            "Butterfly-Common Mime": [4, 4, 5, 5, 6, 18],
            "Butterfly-Common Mormon": [3, 4, 5, 5, 6, 16],
            "Butterfly-Emerald Swallowtail": [4, 4, 5, 6, 7, 15],
            "Butterfly-Golden Birdwing": [5, 6, 7, 8, 9, 25],
            "Butterfly-Gray Glassy Tiger": [3, 4, 4, 5, 5, 13],
            "Butterfly-Great Eggfly": [4, 5, 6, 6, 7, 20],
            "Butterfly-Great Yellow Mormon": [3, 4, 5, 6, 7, 17],
            "Butterfly-Paper Kite": [3, 4, 5, 5, 6, 19],
            "Butterfly-Pink Rose": [4, 5, 5, 6, 7, 15],
            "Butterfly-Plain Tiger": [3, 4, 4, 5, 5, 12],
            "Butterfly-Red Lacewing": [4, 5, 5, 6, 7, 14],
            "Butterfly-Scarlet Mormon": [3, 4, 5, 5, 6, 16],
            "Butterfly-Tailed Jay": [4, 5, 5, 6, 7, 13],
            "Moth-Atlas": [7, 8, 9, 10, 12, 30],
            "Moth-Giant Silk": [6, 7, 8, 9, 10, 25]
        }
        if species_name not in LIFECYCLE_DURATIONS:
            return f"Error: '{species_name}' data not available. Please choose from the provided list."
        durations = LIFECYCLE_DURATIONS[species_name]
        instar_days = durations[:5]
        pupa_days = durations[5]
        cumulative_days = 0
        for i in range(5):
            cumulative_days += instar_days[i]
            if larval_stages <= cumulative_days:
                return f"The {species_name} is currently in Instar {i + 1}."
        pupa_start_day = cumulative_days
        pupa_end_day = pupa_start_day + pupa_days
        if larval_stages <= pupa_end_day:
            days_in_pupa = larval_stages - pupa_start_day
            return f"The {species_name} is a pupa. It has been in this stage for {days_in_pupa} days."
        return f"The {species_name} has emerged as an adult."

    # --- Streamlit App UI Code ---
    st.set_page_config(page_title="Butterfly & Moth Larval Stages Tracker 🦋", layout="wide")
    st.title("Butterfly & Moth Larval Stages Tracker 🐛🦋")
    st.markdown("This application helps you track the **larval stages** of various butterflies and moths.")

    # Load the AI model once at the top level of the script
    larval_stages_model = load_model(MODEL_NAME)

    # Create tabs
    tab1, tab2 = st.tabs(["🧠 AI-Larval Stages Classifier", "🦋 Lifecycle Data"])

    # Tab for AI classifier
    with tab1:
        st.subheader("AI-Larval Stages Classifier")
        st.write("Upload an image of a larva to predict its current stage.")
        image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
        
        if image_file is not None:
            st.image(image_file, caption='Uploaded Image', use_container_width=True)
            if st.button("Classify Image"):
                with st.spinner('Classifying...'):
                    prediction_result = ai_larval_stages_classifier(image_file, larval_stages_model, larval_stages)
                
                if prediction_result:
                    st.success(f"**Predicted Larval Stage:** {prediction_result['class_name']} with a confidence of {prediction_result['score']:.2f}%")
                    st.write("---")
                    st.subheader("Top Predictions")
                    for pred in prediction_result['top_predictions']:
                        st.write(f"- **{pred['class_name']}**: {pred['score']:.2f}%")

    # Tab for larval instar data
    with tab2:
        st.subheader("Species Lifecycle Data")
        LIFECYCLE_DURATIONS = {
            "Butterfly-Clippers": [3, 4, 4, 5, 6, 15],
            "Butterfly-Common Jay": [4, 5, 4, 6, 7, 12],
            "Butterfly-Common Lime": [3, 3, 4, 4, 5, 14],
            "Butterfly-Common Mime": [4, 4, 5, 5, 6, 18],
            "Butterfly-Common Mormon": [3, 4, 5, 5, 6, 16],
            "Butterfly-Emerald Swallowtail": [4, 4, 5, 6, 7, 15],
            "Butterfly-Golden Birdwing": [5, 6, 7, 8, 9, 25],
            "Butterfly-Gray Glassy Tiger": [3, 4, 4, 5, 5, 13],
            "Butterfly-Great Eggfly": [4, 5, 6, 6, 7, 20],
            "Butterfly-Great Yellow Mormon": [3, 4, 5, 6, 7, 17],
            "Butterfly-Paper Kite": [3, 4, 5, 5, 6, 19],
            "Butterfly-Pink Rose": [4, 5, 5, 6, 7, 15],
            "Butterfly-Plain Tiger": [3, 4, 4, 5, 5, 12],
            "Butterfly-Red Lacewing": [4, 5, 5, 6, 7, 14],
            "Butterfly-Scarlet Mormon": [3, 4, 5, 5, 6, 16],
            "Butterfly-Tailed Jay": [4, 5, 5, 6, 7, 13],
            "Moth-Atlas": [7, 8, 9, 10, 12, 30],
            "Moth-Giant Silk": [6, 7, 8, 9, 10, 25]
        }
        data = {
            "Species": list(LIFECYCLE_DURATIONS.keys()),
            "Instar 1 (days)": [d[0] for d in LIFECYCLE_DURATIONS.values()],
            "Instar 2 (days)": [d[1] for d in LIFECYCLE_DURATIONS.values()],
            "Instar 3 (days)": [d[2] for d in LIFECYCLE_DURATIONS.values()],
            "Instar 4 (days)": [d[3] for d in LIFECYCLE_DURATIONS.values()],
            "Instar 5 (days)": [d[4] for d in LIFECYCLE_DURATIONS.values()],
            "Pupa (days)": [d[5] for d in LIFECYCLE_DURATIONS.values()],
        }
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        st.divider()
        st.subheader("Find the Current Stage")
        col1, col2 = st.columns(2)
        with col1:
            species_list = list(LIFECYCLE_DURATIONS.keys())
            selected_species = st.selectbox("Select a Species:", species_list)
        with col2:
            days_passed = st.number_input("Enter the number of days since the egg hatched:", min_value=0, max_value=100, value=1)
        if st.button("Check Stage"):
            if selected_species and days_passed is not None:
                # CORRECTED LINE
                stage_result = get_larval_stages(selected_species, days_passed)
                st.info(stage_result)
            else:
                st.error("Please select a species and enter a valid number of days.")

    st.divider()
    st.subheader("How It Works")
    st.markdown("""
    The app uses a fixed dataset of **hypothetical lifecycle durations** for each species. 
    It calculates the cumulative number of days for each stage and checks where your entered day falls within that timeline.

    - **Instar Stages:** The initial larval stages, where the caterpillar grows and molts.
    - **Pupa Stage:** The transformation stage inside a chrysalis or cocoon.
    - **Adult Stage:** The final stage, where the butterfly or moth has emerged.

    *Note: The data provided is for illustrative purposes and may not reflect actual biological lifecycles.*
    """)
    st.markdown("---")
    st.markdown("Created with ❤️ using Streamlit")