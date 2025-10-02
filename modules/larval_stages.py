# # import os
# # import tensorflow as tf
# # import numpy as np
# # from PIL import Image

# # MODEL_DIR = 'model'
# # MODEL_NAME = 'model_Larval_Stages.h5'
# # IMAGE_SIZE = (180, 180)

# # larval_stages = [
# #     'day 1', 'day 10-fifth instar', 'day 11', 'day 12', 'day 13', 'day 14',
# #     'day 2-first instar', 'day 3', 'day 4-second instar', 'day 5',
# #     'day 6-third instar', 'day 7', 'day 8-fourth instar', 'day 9'
# # ]

# # def load_model():
# #     """Load Keras model once"""
# #     model_path = os.path.join(MODEL_DIR, MODEL_NAME)
# #     if not os.path.exists(model_path):
# #         return None
# #     return tf.keras.models.load_model(model_path)

# # def ai_larval_stages_classifier(image_file, model):
# #     """Run AI classification on uploaded larval image"""
# #     if model is None:
# #         return None

# #     image = Image.open(image_file)
# #     img_resized = image.resize(IMAGE_SIZE)
# #     img_array = tf.keras.utils.img_to_array(img_resized)
# #     img_array = tf.expand_dims(img_array, 0)

# #     predictions = model.predict(img_array)
# #     result = tf.nn.softmax(predictions[0])

# #     top_indices = np.argsort(result)[::-1][:3]
# #     top_predictions = [
# #         {"class_name": larval_stages[i], "score": float(result[i].numpy()) * 100}
# #         for i in top_indices if i < len(larval_stages)
# #     ]

# #     return {
# #         "class_name": larval_stages[int(np.argmax(result))],
# #         "score": float(np.max(result).numpy()) * 100,
# #         "index": int(np.argmax(result)),
# #         "top_predictions": top_predictions
# #     }

# # def get_larval_stage(species_name: str, larval_stages: int) -> str:
# #     """Returns lifecycle stage given species + days since egg hatched"""
# #     LIFECYCLE_DURATIONS = {
# #         "Butterfly-Clippers": [3, 4, 4, 5, 6, 15],
# #         "Butterfly-Common Jay": [4, 5, 4, 6, 7, 12],
# #         "Butterfly-Common Lime": [3, 3, 4, 4, 5, 14],
# #         "Butterfly-Common Mime": [4, 4, 5, 5, 6, 18],
# #         "Butterfly-Common Mormon": [3, 4, 5, 5, 6, 16],
# #         "Butterfly-Emerald Swallowtail": [4, 4, 5, 6, 7, 15],
# #         "Butterfly-Golden Birdwing": [5, 6, 7, 8, 9, 25],
# #         "Butterfly-Gray Glassy Tiger": [3, 4, 4, 5, 5, 13],
# #         "Butterfly-Great Eggfly": [4, 5, 6, 6, 7, 20],
# #         "Butterfly-Great Yellow Mormon": [3, 4, 5, 6, 7, 17],
# #         "Butterfly-Paper Kite": [3, 4, 5, 5, 6, 19],
# #         "Butterfly-Pink Rose": [4, 5, 5, 6, 7, 15],
# #         "Butterfly-Plain Tiger": [3, 4, 4, 5, 5, 12],
# #         "Butterfly-Red Lacewing": [4, 5, 5, 6, 7, 14],
# #         "Butterfly-Scarlet Mormon": [3, 4, 5, 5, 6, 16],
# #         "Butterfly-Tailed Jay": [4, 5, 5, 6, 7, 13],
# #         "Moth-Atlas": [7, 8, 9, 10, 12, 30],
# #         "Moth-Giant Silk": [6, 7, 8, 9, 10, 25]
# #     }

# #     if species_name not in LIFECYCLE_DURATIONS:
# #         return f"Error: '{species_name}' not in database."

# #     durations = LIFECYCLE_DURATIONS[species_name]
# #     instar_days, pupa_days = durations[:5], durations[5]

# #     cumulative_days = 0
# #     for i, d in enumerate(instar_days, start=1):
# #         cumulative_days += d
# #         if larval_stages <= cumulative_days:
# #             return f"The {species_name} is currently in Instar {i}."

# #     if larval_stages <= cumulative_days + pupa_days:
# #         return f"The {species_name} is a pupa (day {larval_stages - cumulative_days})."

# #     return f"The {species_name} has emerged as an adult."


# from xml.parsers.expat import model
# import streamlit as st
# import pandas as pd
# import os
# import tensorflow as tf
# from PIL import Image
# import numpy as np
# import csv
# import datetime

# # # Define global variables for the AI model
# # MODEL_DIR = 'model'  # Assuming the model is in the 'model' subdirectory
# # MODEL_NAME = 'model_Larval_Stages.h5'
# # IMAGE_SIZE = (180, 180) # Define the expected input size for the model
# # CLASSIFICATION_CSV = 'ai_larval_stages_classification.csv'

# # # Define the class names based on your confusion matrix
# # larval_stages_names = ['day 01',
# #                     'day 02-first instar',
# #                     'day 03',
# #                     'day 04-second instar',
# #                     'day 05',
# #                     'day 06-third instar',
# #                     'day 07',
# #                     'day 08-fourth instar',
# #                     'day 09',
# #                     'day 10-fifth instar',
# #                     'day 11',
# #                     'day 12',
# #                     'day 13',
# #                     'day 14']
# # def larval_stages_app():
# #     # st.title("Butterfly & Moth Larval Stages Tracker 🐛🦋")
# #     # st.markdown("This application helps you track the **larval stages** of various butterflies and moths.")
# #     # # Use Streamlit's cache to load the model only once
# #     @st.cache_resource
# #     def load_model(model_name):
# #         """Loads a Keras model from the specified path."""
# #         model_path = os.path.join(MODEL_DIR, model_name)
# #         if not os.path.exists(model_path):
# #             st.error(f"Model not found at: {model_path}. Please ensure the model is saved there.")
# #             return None
# #         try:
# #             model = tf.keras.models.load_model(model_path)
# #             return model
# #         except Exception as e:
# #             st.error(f"Error loading {model_name} Model: {e}")
# #             return None

# #     # The AI classification function
# #     # def classify_images(image_path):
# #     #     input_image = tf.keras.utils.load_img(image_path, target_size=(180,180))
# #     #     input_image_array = tf.keras.utils.img_to_array(input_image)
# #     #     input_image_exp_dim = tf.expand_dims(input_image_array,0)

# #     #     predictions = model.predict(input_image_exp_dim)
# #     #     result = tf.nn.softmax(predictions[0])
# #     #     outcome = 'The Image belongs to ' + larval_stages_names[np.argmax(result)] + ' with a score of '+ str(np.max(result)*100)
# #     #     return outcome
    
# #     def ai_larval_stages_classifier(image_file, model, larval_stages_names):
# #         """
# #         Classifies an uploaded image using the provided AI model.
# #         """
# #         if model is None:
# #             return {"larval_stages_names": "Model Not Loaded", "score": 0.0, "index": -1, "top_predictions": []}

# #         try:
# #             image = Image.open(image_file)
# #             img_resized = image.resize(IMAGE_SIZE)
# #             img_array = tf.keras.utils.img_to_array(img_resized)
# #             img_array = tf.expand_dims(img_array, 0) # Add batch dimension

# #             predictions = model.predict(img_array)
# #             result = tf.nn.softmax(predictions[0])
            
# #             # Get top 3 predictions
# #             top_indices = np.argsort(result)[::-1][:3]
# #             top_predictions = []
# #             for i in top_indices:
# #                 if i < len(larval_stages_names):
# #                     class_name = larval_stages_names[i]
# #                     score = result[i].numpy() * 100
# #                     top_predictions.append({"larval_stages_names": class_name, "score": score})

# #             predicted_class_index = np.argmax(result)
# #             predicted_score = np.max(result).item() * 100

# #             if predicted_class_index < len(larval_stages_names):
# #                 predicted_class_name = larval_stages_names[predicted_class_index]
# #                 result_data = {
# #                     "larval_stages_names": predicted_class_name,
# #                     "score": predicted_score,
# #                     "index": predicted_class_index,
# #                     "top_predictions": top_predictions
# #                 }
# #                 return result_data
# #             elif predicted_class_index == len(larval_stages_names):
# #                 return {"larval_stages_names": "No Larva Detected", "score": predicted_score, "index": predicted_class_index, "top_predictions": top_predictions}
# #             else:
# #                 return {"larval_stages_names": "Unknown Class (Index out of bounds)", "score": 0.0, "index": predicted_class_index, "top_predictions": []}
# #         except Exception as e:
# #             st.error(f"Error during image classification: {e}")
# #             return None 
    
# #     def save_larval_stage_prediction(prediction_result):
# #         """Save larval stage prediction to CSV, creating the file with headers if needed."""
# #         file_exists = os.path.isfile(CLASSIFICATION_CSV)
# #         with open(CLASSIFICATION_CSV, mode='a', newline='', encoding='utf-8') as file:
# #             writer = csv.writer(file)
# #             # Write header if file is new
# #             if not file_exists or os.stat(CLASSIFICATION_CSV).st_size == 0:
# #                 writer.writerow(['timestamp', 'predicted_stage', 'score'])
# #             writer.writerow([
# #                 datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
# #                 prediction_result.get('larval_stages_names', ''),
# #                 f"{prediction_result.get('score', 0):.2f}"
# #             ])
    
# #     def get_larval_stages(species_name: str, larval_stages_names: int) -> str:
# #         """
# #         Determines the current lifecycle stage of a butterfly or moth based on the number of days.
# #         """
# #         LIFECYCLE_DURATIONS = {
# #             "Butterfly-Clippers": [3, 4, 4, 5, 6, 15],
# #             "Butterfly-Common Jay": [4, 5, 4, 6, 7, 12],
# #             "Butterfly-Common Lime": [2, 2, 2, 2, 2, 14],
# #             "Butterfly-Common Mime": [4, 4, 5, 5, 6, 18],
# #             "Butterfly-Common Mormon": [3, 4, 5, 5, 6, 16],
# #             "Butterfly-Emerald Swallowtail": [4, 4, 5, 6, 7, 15],
# #             "Butterfly-Golden Birdwing": [5, 6, 7, 8, 9, 25],
# #             "Butterfly-Gray Glassy Tiger": [3, 4, 4, 5, 5, 13],
# #             "Butterfly-Great Eggfly": [4, 5, 6, 6, 7, 20],
# #             "Butterfly-Great Yellow Mormon": [3, 4, 5, 6, 7, 17],
# #             "Butterfly-Paper Kite": [3, 4, 5, 5, 6, 19],
# #             "Butterfly-Pink Rose": [4, 5, 5, 6, 7, 15],
# #             "Butterfly-Plain Tiger": [3, 4, 4, 5, 5, 12],
# #             "Butterfly-Red Lacewing": [4, 5, 5, 6, 7, 14],
# #             "Butterfly-Scarlet Mormon": [3, 4, 5, 5, 6, 16],
# #             "Butterfly-Tailed Jay": [4, 5, 5, 6, 7, 13],
# #             "Moth-Atlas": [7, 8, 9, 10, 12, 30],
# #             "Moth-Giant Silk": [6, 7, 8, 9, 10, 25]
# #         }
# #         if species_name not in LIFECYCLE_DURATIONS:
# #             return f"Error: '{species_name}' data not available. Please choose from the provided list."
# #         durations = LIFECYCLE_DURATIONS[species_name]
# #         instar_days = durations[:5]
# #         pupa_days = durations[5]
# #         cumulative_days = 0
# #         for i in range(5):
# #             cumulative_days += instar_days[i]
# #             if larval_stages_names <= cumulative_days:
# #                 return f"The {species_name} is currently in Instar {i + 1}."
# #         pupa_start_day = cumulative_days
# #         pupa_end_day = pupa_start_day + pupa_days
# #         if larval_stages_names <= pupa_end_day:
# #             days_in_pupa = larval_stages_names - pupa_start_day
# #             return f"The {species_name} is a pupa. It has been in this stage for {days_in_pupa} days."
# #         return f"The {species_name} has emerged as an adult."



# #     # --- Streamlit App UI Code ---
# #     st.set_page_config(page_title="Butterfly & Moth Larval Stages Tracker 🦋", layout="wide")
# #     st.title("Butterfly & Moth Larval Stages Tracker 🐛🦋")
# #     st.markdown("This application helps you track the **larval stages** of various butterflies and moths.")

# #     # Load the AI model once at the top level of the script
# #     larval_stages_model = load_model(MODEL_NAME)

# #     # Create tabs
# #     tab1, tab2 = st.tabs(["🧠 AI-Larval Stages Classifier", "🦋 Lifecycle Data"])

# #     # Tab for AI classifier
# #     with tab1:
# #         st.subheader("AI-Larval Stages Classifier")
# #         st.write("Upload an image of a larva to predict its current stage.")
# #         image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
        
# #         if image_file is not None:
# #             st.image(image_file, caption='Uploaded Image', use_container_width=True)
# #             if st.button("Classify Image"):
# #                 with st.spinner('Classifying...'):
# #                     prediction_result = ai_larval_stages_classifier(image_file, larval_stages_model, larval_stages_names=larval_stages_names)
                
# #                 if prediction_result:
# #                     st.success(f"**Predicted Larval Stage:** {prediction_result['larval_stages_names']} with a confidence of {prediction_result['score']:.2f}%")
# #                     st.write("---")
# #                     st.subheader("Top Predictions")
# #                     for pred in prediction_result['top_predictions']:
# #                         st.write(f"- **{pred['larval_stages_names']}**: {pred['score']:.2f}%")

# #     # Tab for larval instar data
# #     with tab2:
# #         st.subheader("Species Lifecycle Data")
# #         LIFECYCLE_DURATIONS = {
# #             "Butterfly-Clippers": [3, 4, 4, 5, 6, 15],
# #             "Butterfly-Common Jay": [4, 5, 4, 6, 7, 12],
# #             "Butterfly-Common Lime": [2, 2, 2, 2, 2, 14],
# #             "Butterfly-Common Mime": [4, 4, 5, 5, 6, 18],
# #             "Butterfly-Common Mormon": [3, 4, 5, 5, 6, 16],
# #             "Butterfly-Emerald Swallowtail": [4, 4, 5, 6, 7, 15],
# #             "Butterfly-Golden Birdwing": [5, 6, 7, 8, 9, 25],
# #             "Butterfly-Gray Glassy Tiger": [3, 4, 4, 5, 5, 13],
# #             "Butterfly-Great Eggfly": [4, 5, 6, 6, 7, 20],
# #             "Butterfly-Great Yellow Mormon": [3, 4, 5, 6, 7, 17],
# #             "Butterfly-Paper Kite": [3, 4, 5, 5, 6, 19],
# #             "Butterfly-Pink Rose": [4, 5, 5, 6, 7, 15],
# #             "Butterfly-Plain Tiger": [3, 4, 4, 5, 5, 12],
# #             "Butterfly-Red Lacewing": [4, 5, 5, 6, 7, 14],
# #             "Butterfly-Scarlet Mormon": [3, 4, 5, 5, 6, 16],
# #             "Butterfly-Tailed Jay": [4, 5, 5, 6, 7, 13],
# #             "Moth-Atlas": [7, 8, 9, 10, 12, 30],
# #             "Moth-Giant Silk": [6, 7, 8, 9, 10, 25]
# #         }
# #         data = {
# #             "Species": list(LIFECYCLE_DURATIONS.keys()),
# #             "Instar 1 (days)": [d[0] for d in LIFECYCLE_DURATIONS.values()],
# #             "Instar 2 (days)": [d[1] for d in LIFECYCLE_DURATIONS.values()],
# #             "Instar 3 (days)": [d[2] for d in LIFECYCLE_DURATIONS.values()],
# #             "Instar 4 (days)": [d[3] for d in LIFECYCLE_DURATIONS.values()],
# #             "Instar 5 (days)": [d[4] for d in LIFECYCLE_DURATIONS.values()],
# #             "Pupa (days)": [d[5] for d in LIFECYCLE_DURATIONS.values()],
# #         }
# #         df = pd.DataFrame(data)
# #         st.dataframe(df, use_container_width=True)
# #         st.divider()
# #         st.subheader("Find the Current Stage")
# #         col1, col2 = st.columns(2)
# #         with col1:
# #             species_list = list(LIFECYCLE_DURATIONS.keys())
# #             selected_species = st.selectbox("Select a Species:", species_list)
# #         with col2:
# #             days_passed = st.number_input("Enter the number of days since the egg hatched:", min_value=0, max_value=100, value=1)
# #         if st.button("Check Stage"):
# #             if selected_species and days_passed is not None:
# #                 # CORRECTED LINE
# #                 stage_result = get_larval_stages(selected_species, days_passed)
# #                 st.info(stage_result)
# #             else:
# #                 st.error("Please select a species and enter a valid number of days.")

# #     st.divider()
# #     st.subheader("How It Works")
# #     st.markdown("""
# #     The app uses a fixed dataset of **hypothetical lifecycle durations** for each species. 
# #     It calculates the cumulative number of days for each stage and checks where your entered day falls within that timeline.

# #     - **Instar Stages:** The initial larval stages, where the caterpillar grows and molts.
# #     - **Pupa Stage:** The transformation stage inside a chrysalis or cocoon.
# #     - **Adult Stage:** The final stage, where the butterfly or moth has emerged.

# #     *Note: The data provided is for illustrative purposes and may not reflect actual biological lifecycles.*
# #     """)
# #     st.markdown("---")
# #     st.markdown("Created with ❤️ using Streamlit")
# import os
# import csv
# import datetime
# import streamlit as st
# import pandas as pd
# import tensorflow as tf
# import numpy as np
# from PIL import Image

# # --- Configuration ---
# MODEL_DIR = 'model'
# MODEL_NAME = 'model_Larval_Stages.h5'
# IMAGE_SIZE = (180, 180)
# CLASSIFICATION_CSV = 'ai_larval_stages_classification.csv'

# larval_stages_names = [
#     'day 01',
#     'day 02-first instar',
#     'day 03',
#     'day 04-second instar',
#     'day 05',
#     'day 06-third instar',
#     'day 07',
#     'day 08-fourth instar',
#     'day 09',
#     'day 10-fifth instar',
#     'day 11',
#     'day 12',
#     'day 13',
#     'day 14'
# ]
# def larval_stages_app():
# # --- Utility Functions ---

#     @st.cache_resource
#     def load_model(model_name):
#         """Loads a Keras model from the specified path."""
#         model_path = os.path.join(MODEL_DIR, model_name)
#         if not os.path.exists(model_path):
#             st.error(f"Model not found at: {model_path}. Please ensure the model is saved there.")
#             return None
#         try:
#             model = tf.keras.models.load_model(model_path)
#             return model
#         except Exception as e:
#             st.error(f"Error loading {model_name} Model: {e}")
#             return None

#     def ai_larval_stages_classifier(image_file, model, larval_stages_names):
#         """
#         Classifies an uploaded image using the provided AI model.
#         """
#         if model is None:
#             return {"larval_stages_names": "Model Not Loaded", "score": 0.0, "index": -1, "top_predictions": []}

#         try:
#             image = Image.open(image_file)
#             img_resized = image.resize(IMAGE_SIZE)
#             img_array = tf.keras.utils.img_to_array(img_resized)
#             img_array = tf.expand_dims(img_array, 0) # Add batch dimension

#             predictions = model.predict(img_array)
#             result = tf.nn.softmax(predictions[0])
            
#             # Get top 3 predictions
#             top_indices = np.argsort(result)[::-1][:3]
#             top_predictions = []
#             for i in top_indices:
#                 if i < len(larval_stages_names):
#                     class_name = larval_stages_names[i]
#                     score = result[i].numpy() * 100
#                     top_predictions.append({"larval_stages_names": class_name, "score": score})

#             predicted_class_index = np.argmax(result)
#             predicted_score = np.max(result).item() * 100

#             if predicted_class_index < len(larval_stages_names):
#                 predicted_class_name = larval_stages_names[predicted_class_index]
#                 result_data = {
#                     "larval_stages_names": predicted_class_name,
#                     "score": predicted_score,
#                     "index": predicted_class_index,
#                     "top_predictions": top_predictions
#                 }
#                 return result_data
#             elif predicted_class_index == len(larval_stages_names):
#                 return {"larval_stages_names": "No Larva Detected", "score": predicted_score, "index": predicted_class_index, "top_predictions": top_predictions}
#             else:
#                 return {"larval_stages_names": "Unknown Class (Index out of bounds)", "score": 0.0, "index": predicted_class_index, "top_predictions": []}
#         except Exception as e:
#             st.error(f"Error during image classification: {e}")
#             return None 

#     def save_larval_stage_prediction(prediction_result):
#         """Save larval stage prediction to CSV, creating the file with headers if needed."""
#         file_exists = os.path.isfile(CLASSIFICATION_CSV)
#         with open(CLASSIFICATION_CSV, mode='a', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             # Write header if file is new
#             if not file_exists or os.stat(CLASSIFICATION_CSV).st_size == 0:
#                 writer.writerow(['timestamp', 'predicted_stage', 'score'])
#             writer.writerow([
#                 datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                 prediction_result.get('larval_stages_names', ''),
#                 f"{prediction_result.get('score', 0):.2f}"
#             ])

#     def get_larval_stages(species_name: str, larval_stages_names: int) -> str:
#         """
#         Determines the current lifecycle stage of a butterfly or moth based on the number of days.
#         """
#         LIFECYCLE_DURATIONS = {
#             "Butterfly-Clippers": [3, 4, 4, 5, 6, 15],
#             "Butterfly-Common Jay": [4, 5, 4, 6, 7, 12],
#             "Butterfly-Common Lime": [2, 2, 2, 2, 2, 14],
#             "Butterfly-Common Mime": [4, 4, 5, 5, 6, 18],
#             "Butterfly-Common Mormon": [3, 4, 5, 5, 6, 16],
#             "Butterfly-Emerald Swallowtail": [4, 4, 5, 6, 7, 15],
#             "Butterfly-Golden Birdwing": [5, 6, 7, 8, 9, 25],
#             "Butterfly-Gray Glassy Tiger": [3, 4, 4, 5, 5, 13],
#             "Butterfly-Great Eggfly": [4, 5, 6, 6, 7, 20],
#             "Butterfly-Great Yellow Mormon": [3, 4, 5, 6, 7, 17],
#             "Butterfly-Paper Kite": [3, 4, 5, 5, 6, 19],
#             "Butterfly-Pink Rose": [4, 5, 5, 6, 7, 15],
#             "Butterfly-Plain Tiger": [3, 4, 4, 5, 5, 12],
#             "Butterfly-Red Lacewing": [4, 5, 5, 6, 7, 14],
#             "Butterfly-Scarlet Mormon": [3, 4, 5, 5, 6, 16],
#             "Butterfly-Tailed Jay": [4, 5, 5, 6, 7, 13],
#             "Moth-Atlas": [7, 8, 9, 10, 12, 30],
#             "Moth-Giant Silk": [6, 7, 8, 9, 10, 25]
#         }
#         if species_name not in LIFECYCLE_DURATIONS:
#             return f"Error: '{species_name}' data not available. Please choose from the provided list."
#         durations = LIFECYCLE_DURATIONS[species_name]
#         instar_days = durations[:5]
#         pupa_days = durations[5]
#         cumulative_days = 0
#         for i in range(5):
#             cumulative_days += instar_days[i]
#             if larval_stages_names <= cumulative_days:
#                 return f"The {species_name} is currently in Instar {i + 1}."
#         pupa_start_day = cumulative_days
#         pupa_end_day = pupa_start_day + pupa_days
#         if larval_stages_names <= pupa_end_day:
#             days_in_pupa = larval_stages_names - pupa_start_day
#             return f"The {species_name} is a pupa. It has been in this stage for {days_in_pupa} days."
#         return f"The {species_name} has emerged as an adult."
    
#     def _display_recent_classifications():
#         """Display recent larval stage classification results from the CSV file."""
#         st.subheader("📊 Recent Larval Stage Classifications")
#         if not os.path.exists(CLASSIFICATION_CSV):
#             st.info("No classifications performed yet. Upload an image to get started!")
#             return

#         df = pd.read_csv(CLASSIFICATION_CSV)
#         if not df.empty:
#             recent = df.tail(10).sort_values('timestamp', ascending=False)
#             st.dataframe(recent, use_container_width=True)

#             st.write("**Classification Statistics:**")
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.metric("Total Classifications", len(df))

#         df = pd.read_csv(CLASSIFICATION_CSV)
#         if not df.empty:
#             recent = df.tail(10).sort_values('timestamp', ascending=False)
#             st.dataframe(recent, use_container_width=True)

#             st.write("**Classification Statistics:**")
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.metric("Total Classifications", len(df))
#             with col2:
#                 if 'predicted_stage' in df.columns:
#                     most_common = df['predicted_stage'].mode()[0] if not df['predicted_stage'].mode().empty else "N/A"
#                     st.metric("Most Common Stage", most_common)
#                 else:
#                     st.metric("Most Common Stage", "N/A")
#         else:
#             st.info("No classifications performed yet. Upload an image to get started!")
#     # --- Streamlit App UI Code ---

#     st.set_page_config(page_title="Butterfly & Moth Larval Stages Tracker 🦋", layout="wide")
#     st.title("Butterfly & Moth Larval Stages Tracker 🐛🦋")
#     st.markdown("This application helps you track the **larval stages** of various butterflies and moths.")

#     # Load the AI model once at the top level of the script
#     larval_stages_model = load_model(MODEL_NAME)

#     # Create tabs
#     tab1, tab2 = st.tabs(["🧠 AI-Larval Stages Classifier", "🦋 Lifecycle Data"])

#     # Tab for AI classifier
#     with tab1:
#         st.subheader("AI-Larval Stages Classifier")
#         st.write("Upload an image of a larva to predict its current stage.")
#         image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
        
#         if image_file is not None:
#             st.image(image_file, caption='Uploaded Image', use_container_width=True)
#             if st.button("Classify Image"):
#                 with st.spinner('Classifying...'):
#                     prediction_result = ai_larval_stages_classifier(image_file, larval_stages_model, larval_stages_names=larval_stages_names)
                
#                 if prediction_result:
#                     st.success(f"**Predicted Larval Stage:** {prediction_result['larval_stages_names']} with a confidence of {prediction_result['score']:.2f}%")
#                     save_larval_stage_prediction(prediction_result)
#                     st.write("---")
#                     st.subheader("Top Predictions")
#                     for pred in prediction_result['top_predictions']:
#                         st.write(f"- **{pred['larval_stages_names']}**: {pred['score']:.2f}%")
    
    
#     # Tab for larval instar data
#     with tab2:
#         st.subheader("Species Lifecycle Data")
#         LIFECYCLE_DURATIONS = {
#             "Butterfly-Clippers": [3, 4, 4, 5, 6, 15],
#             "Butterfly-Common Jay": [4, 5, 4, 6, 7, 12],
#             "Butterfly-Common Lime": [2, 2, 2, 2, 2, 14],
#             "Butterfly-Common Mime": [4, 4, 5, 5, 6, 18],
#             "Butterfly-Common Mormon": [3, 4, 5, 5, 6, 16],
#             "Butterfly-Emerald Swallowtail": [4, 4, 5, 6, 7, 15],
#             "Butterfly-Golden Birdwing": [5, 6, 7, 8, 9, 25],
#             "Butterfly-Gray Glassy Tiger": [3, 4, 4, 5, 5, 13],
#             "Butterfly-Great Eggfly": [4, 5, 6, 6, 7, 20],
#             "Butterfly-Great Yellow Mormon": [3, 4, 5, 6, 7, 17],
#             "Butterfly-Paper Kite": [3, 4, 5, 5, 6, 19],
#             "Butterfly-Pink Rose": [4, 5, 5, 6, 7, 15],
#             "Butterfly-Plain Tiger": [3, 4, 4, 5, 5, 12],
#             "Butterfly-Red Lacewing": [4, 5, 5, 6, 7, 14],
#             "Butterfly-Scarlet Mormon": [3, 4, 5, 5, 6, 16],
#             "Butterfly-Tailed Jay": [4, 5, 5, 6, 7, 13],
#             "Moth-Atlas": [7, 8, 9, 10, 12, 30],
#             "Moth-Giant Silk": [6, 7, 8, 9, 10, 25]
#         }
#         data = {
#             "Species": list(LIFECYCLE_DURATIONS.keys()),
#             "Instar 1 (days)": [d[0] for d in LIFECYCLE_DURATIONS.values()],
#             "Instar 2 (days)": [d[1] for d in LIFECYCLE_DURATIONS.values()],
#             "Instar 3 (days)": [d[2] for d in LIFECYCLE_DURATIONS.values()],
#             "Instar 4 (days)": [d[3] for d in LIFECYCLE_DURATIONS.values()],
#             "Instar 5 (days)": [d[4] for d in LIFECYCLE_DURATIONS.values()],
#             "Pupa (days)": [d[5] for d in LIFECYCLE_DURATIONS.values()],
#         }
#         df = pd.DataFrame(data)
#         st.dataframe(df, use_container_width=True)
#         st.divider()
#         st.subheader("Find the Current Stage")
#         col1, col2 = st.columns(2)
#         with col1:
#             species_list = list(LIFECYCLE_DURATIONS.keys())
#             selected_species = st.selectbox("Select a Species:", species_list)
#         with col2:
#             days_passed = st.number_input("Enter the number of days since the egg hatched:", min_value=0, max_value=100, value=1)
#         if st.button("Check Stage"):
#             if selected_species and days_passed is not None:
#                 stage_result = get_larval_stages(selected_species, days_passed)
#                 st.info(stage_result)
#             else:
#                 st.error("Please select a species and enter a valid number of days.")

#     st.divider()
#     st.subheader("How It Works")
#     st.markdown("""
#     The app uses a fixed dataset of **hypothetical lifecycle durations** for each species. 
#     It calculates the cumulative number of days for each stage and checks where your entered day falls within that timeline.

#     - **Instar Stages:** The initial larval stages, where the caterpillar grows and molts.
#     - **Pupa Stage:** The transformation stage inside a chrysalis or cocoon.
#     - **Adult Stage:** The final stage, where the butterfly or moth has emerged.

#     *Note: The data provided is for illustrative purposes and may not reflect actual biological lifecycles.*
#     """)
#     st.markdown("---")
#     st.markdown("Created with ❤️ using Streamlit")

import os
import csv
import datetime
import streamlit as st
import pandas as pd
import tensorflow as tf
import numpy as np
from PIL import Image
from typing import Dict, Any, List

# --- Configuration Constants ---
MODEL_DIR: str = 'model'
MODEL_NAME: str = 'model_Larval_Stages.h5'
IMAGE_SIZE: tuple = (180, 180)
IMAGE_SIZE = (180, 180)
CLASSIFICATION_CSV: str = 'ai_larval_stages_classification.csv'

# Class names used by the AI model
LARVAL_STAGES_NAMES: List[str] = [
    'day 01', 'day 02-first instar', 'day 03', 'day 04-second instar',
    'day 05', 'day 06-third instar', 'day 07', 'day 08-fourth instar',
    'day 09', 'day 10-fifth instar', 'day 11', 'day 12',
    'day 13', 'day 14'
]

# Lifecycle data: [Instar 1-5 durations (days), Pupa duration (days)]
LIFECYCLE_DURATIONS: Dict[str, List[int]] = {
    "Butterfly-Clippers": [3, 4, 4, 5, 6, 15],
    "Butterfly-Common Jay": [4, 5, 4, 6, 7, 12],
    "Butterfly-Common Lime": [2, 2, 2, 2, 2, 14],
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

# --- Utility Functions ---

@st.cache_resource
def load_model(model_name: str):
    """Loads a Keras model once using Streamlit's cache."""
    model_path = os.path.join(MODEL_DIR, model_name)
    if not os.path.exists(model_path):
        st.error(f"Model not found at: {model_path}.")
        return None
    try:
        return tf.keras.models.load_model(model_path)
    except Exception as e:
        st.error(f"Error loading {model_name} Model: {e}")
        return None

def ai_larval_stages_classifier(image_file, model, larval_stages_names: List[str]) -> Dict[str, Any]:
    """Classifies an uploaded image using the AI model."""
    default_error = {"larval_stages_names": "Model/Classification Error", "score": 0.0, "index": -1, "top_predictions": []}

    if model is None:
        return default_error

    try:
        image = Image.open(image_file)
        img_resized = image.resize(IMAGE_SIZE)
        img_array = tf.keras.utils.img_to_array(img_resized)
        img_array = tf.expand_dims(img_array, 0) # Add batch dimension

        predictions = model.predict(img_array, verbose=0) # Suppress prediction output
        result = tf.nn.softmax(predictions[0]).numpy() # Convert to numpy array once

        # Get top 3 predictions
        top_indices = np.argsort(result)[::-1][:3]
        top_predictions = []
        
        for i in top_indices:
            if i < len(larval_stages_names):
                class_name = larval_stages_names[i]
                score = result[i] * 100
                top_predictions.append({"larval_stages_names": class_name, "score": float(score)}) # Ensure float

        predicted_class_index = np.argmax(result)
        predicted_score = np.max(result).item() * 100

        if predicted_class_index < len(larval_stages_names):
            predicted_class_name = larval_stages_names[predicted_class_index]
            return {
                "larval_stages_names": predicted_class_name,
                "score": float(predicted_score),
                "index": int(predicted_class_index),
                "top_predictions": top_predictions
            }
        else:
            # Handle cases where the index is unexpected (e.g., if a background class was index N)
            return default_error

    except Exception as e:
        st.error(f"Error during image classification: {e}")
        return default_error

def save_larval_stage_prediction(prediction_result: Dict[str, Any]):
    """Save larval stage prediction to CSV."""
    file_exists = os.path.isfile(CLASSIFICATION_CSV)
    
    with open(CLASSIFICATION_CSV, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header if file is new or empty
        if not file_exists or os.stat(CLASSIFICATION_CSV).st_size == 0:
            writer.writerow(['timestamp', 'predicted_stage', 'score'])
            
        writer.writerow([
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            prediction_result.get('larval_stages_names', 'N/A'),
            f"{prediction_result.get('score', 0):.2f}"
        ])

def get_larval_stages(species_name: str, days_passed: int) -> str:
    """
    Determines the current lifecycle stage of a species based on the number of days since hatching.
    """
    if species_name not in LIFECYCLE_DURATIONS:
        return f"Error: '{species_name}' data not available. Please choose from the provided list."
        
    durations = LIFECYCLE_DURATIONS[species_name]
    instar_days = durations[:5]
    pupa_duration = durations[5]
    
    cumulative_days = 0
    # Check Instar stages (5 stages)
    for i in range(5):
        cumulative_days += instar_days[i]
        if days_passed <= cumulative_days:
            return f"The {species_name} is currently in **Instar {i + 1}**."
            
    # Check Pupa stage
    pupa_start_day = cumulative_days
    pupa_end_day = pupa_start_day + pupa_duration
    
    if days_passed <= pupa_end_day:
        days_in_pupa = days_passed - pupa_start_day
        return f"The {species_name} is a **pupa**. It has been in this stage for **{days_in_pupa}** days."
        
    # Must be adult stage
    return f"The {species_name} has **emerged as an adult**."

def _display_recent_classifications():
    """Display recent larval stage classification results from the CSV file."""
    st.subheader("📊 Recent Larval Stage Classifications")
    if not os.path.exists(CLASSIFICATION_CSV):
        st.info("No classifications performed yet. Upload an image to get started!")
        return

    df = pd.read_csv(CLASSIFICATION_CSV)
    if not df.empty:
        # Sort and display the 10 most recent classifications
        recent = df.sort_values('timestamp', ascending=False).head(10)
        st.dataframe(recent, use_container_width=True)

        st.write("**Classification Statistics:**")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Classifications", len(df))
        
        with col2:
            if 'predicted_stage' in df.columns:
                most_common = df['predicted_stage'].mode().iloc[0] if not df['predicted_stage'].mode().empty else "N/A"
                st.metric("Most Common Stage", most_common)
            else:
                st.metric("Most Common Stage", "N/A")
    else:
        st.info("No classifications performed yet. Upload an image to get started!")

# --- Main Streamlit App ---

def larval_stages_app():
    """Main function to run the Streamlit application."""
    
    st.set_page_config(page_title="Butterfly & Moth Larval Stages Tracker 🦋", layout="wide")
    st.title("Butterfly & Moth Larval Stages Tracker 🐛🦋")
    st.markdown("This application helps you track the **larval stages** of various butterflies and moths.")

    # Load the AI model
    larval_stages_model = load_model(MODEL_NAME)

    # Create tabs
    tab1, tab2 = st.tabs(["🧠 AI-Larval Stages Classifier", "🦋 Lifecycle Data"])

    # Tab 1: AI classifier
    with tab1:
        st.subheader("AI-Larval Stages Classifier")
        st.write("Upload an image of a larva to predict its current stage.")
        image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
        
        if image_file is not None:
            st.image(image_file, caption='Uploaded Image', use_container_width=True)
            if st.button("Classify Image", key="classify_btn"):
                if larval_stages_model:
                    with st.spinner('Classifying...'):
                        prediction_result = ai_larval_stages_classifier(image_file, larval_stages_model, LARVAL_STAGES_NAMES)
                    
                    if prediction_result and prediction_result.get('score', 0) > 0:
                        st.success(f"**Predicted Larval Stage:** {prediction_result['larval_stages_names']} with a confidence of {prediction_result['score']:.2f}%")
                        save_larval_stage_prediction(prediction_result)
                        
                        st.write("---")
                        st.subheader("Top Predictions")
                        # Display top 3 predictions in a structured list
                        for pred in prediction_result['top_predictions']:
                            st.write(f"- **{pred['larval_stages_names']}**: {pred['score']:.2f}%")
                    else:
                        st.warning("Classification failed or model returned an unknown class.")
                else:
                    st.error("Model could not be loaded. Please check the model directory.")
        
        st.divider()
        _display_recent_classifications() # Call the display function

    # Tab 2: Lifecycle data
    with tab2:
        st.subheader("Species Lifecycle Data Table")
        
        # Convert the dictionary to a DataFrame for display
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
        st.subheader("Find the Current Stage by Day Count")
        
        col1, col2 = st.columns(2)
        with col1:
            species_list = list(LIFECYCLE_DURATIONS.keys())
            selected_species = st.selectbox("Select a Species:", species_list)
        with col2:
            days_passed = st.number_input("Enter the number of days since the egg hatched:", min_value=0, max_value=100, value=1)
            
        if st.button("Check Stage", key="check_stage_btn"):
            if selected_species and days_passed is not None:
                stage_result = get_larval_stages(selected_species, days_passed)
                st.info(stage_result)
            else:
                st.error("Please select a species and enter a valid number of days.")

    st.divider()
    st.subheader("How The Lifecycle Tracker Works")
    st.markdown("""
    The app calculates the cumulative number of days for each stage based on a **fixed dataset of lifecycle durations**.
    
    - **Instar Stages:** The initial larval stages, where the caterpillar grows and molts.
    - **Pupa Stage:** The transformation stage inside a chrysalis or cocoon.
    - **Adult Stage:** The final stage, where the butterfly or moth has emerged.

    *Note: The data provided is for illustrative purposes and may not reflect actual biological lifecycles.*
    """)
    st.markdown("---")
    st.markdown("Created with ❤️ using Streamlit")

if __name__ == '__main__':
    larval_stages_app()