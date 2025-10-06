import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import pandas as pd
import os
from utils.image_processor import preprocess_image
from utils.model_loader import ModelManager
from config.class_labels import CLASS_LABELS

# Configure page
st.set_page_config(
    page_title="LepVision AI Classification",
    page_icon="🦋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'models_loaded' not in st.session_state:
    st.session_state.models_loaded = False
    st.session_state.model_manager = None

def load_models():
    """Load all pre-trained models"""
    if not st.session_state.models_loaded:
        with st.spinner("Loading AI models... This may take a moment."):
            try:
                st.session_state.model_manager = ModelManager()
                st.session_state.models_loaded = True
                st.success("✅ All models loaded successfully!")
            except Exception as e:
                st.error(f"❌ Error loading models: {str(e)}")
                st.error("Please ensure all model files are present in the 'models' directory.")
                return False
    return True

def predict_image(image, model_manager):
    """Make predictions using all applicable models"""
    try:
        # Preprocess image for each model
        processed_image = preprocess_image(image)
        
        results = {}
        
        # Butterfly Species Classification
        try:
            species_pred = model_manager.predict_species(processed_image)
            species_class = np.argmax(species_pred[0])
            species_confidence = float(np.max(species_pred[0]) * 100)
            results['species'] = {
                'prediction': CLASS_LABELS['species'][species_class],
                'confidence': species_confidence,
                'all_scores': {CLASS_LABELS['species'][i]: float(species_pred[0][i] * 100) 
                             for i in range(len(CLASS_LABELS['species']))}
            }
        except Exception as e:
            results['species'] = {'error': str(e)}
        
        # Butterfly Stages Classification
        try:
            stages_pred = model_manager.predict_butterfly_stages(processed_image)
            stages_class = np.argmax(stages_pred[0])
            stages_confidence = float(np.max(stages_pred[0]) * 100)
            results['butterfly_stages'] = {
                'prediction': CLASS_LABELS['butterfly_stages'][stages_class],
                'confidence': stages_confidence,
                'all_scores': {CLASS_LABELS['butterfly_stages'][i]: float(stages_pred[0][i] * 100) 
                             for i in range(len(CLASS_LABELS['butterfly_stages']))}
            }
        except Exception as e:
            results['butterfly_stages'] = {'error': str(e)}
        
        # Larval Diseases Classification
        try:
            diseases_pred = model_manager.predict_larval_diseases(processed_image)
            diseases_class = np.argmax(diseases_pred[0])
            diseases_confidence = float(np.max(diseases_pred[0]) * 100)
            results['larval_diseases'] = {
                'prediction': CLASS_LABELS['larval_diseases'][diseases_class],
                'confidence': diseases_confidence,
                'all_scores': {CLASS_LABELS['larval_diseases'][i]: float(diseases_pred[0][i] * 100) 
                             for i in range(len(CLASS_LABELS['larval_diseases']))}
            }
        except Exception as e:
            results['larval_diseases'] = {'error': str(e)}
        
        # Larval Stages Classification
        try:
            larval_stages_pred = model_manager.predict_larval_stages(processed_image)
            larval_stages_class = np.argmax(larval_stages_pred[0])
            larval_stages_confidence = float(np.max(larval_stages_pred[0]) * 100)
            results['larval_stages'] = {
                'prediction': CLASS_LABELS['larval_stages'][larval_stages_class],
                'confidence': larval_stages_confidence,
                'all_scores': {CLASS_LABELS['larval_stages'][i]: float(larval_stages_pred[0][i] * 100) 
                             for i in range(len(CLASS_LABELS['larval_stages']))}
            }
        except Exception as e:
            results['larval_stages'] = {'error': str(e)}
        
        return results
    
    except Exception as e:
        st.error(f"Error during prediction: {str(e)}")
        return None

def display_results(results, image):
    """Display classification results in an organized dashboard"""
    st.header("🔬 Classification Results")
    
    # Create columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📸 Uploaded Image")
        st.image(image, caption="Input Image", use_column_width=True)
        st.info(f"Image Size: {image.size[0]} x {image.size[1]} pixels")
    
    with col2:
        st.subheader("🤖 AI Predictions")
        
        # Create tabs for different model results
        tab1, tab2, tab3, tab4 = st.tabs([
            "🦋 Species", "📊 Butterfly Stages", "🦠 Larval Diseases", "🐛 Larval Stages"
        ])
        
        with tab1:
            if 'error' in results.get('species', {}):
                st.error(f"Species Classification Error: {results['species']['error']}")
            else:
                species_result = results['species']
                st.metric(
                    label="Predicted Species",
                    value=species_result['prediction'],
                    delta=f"{species_result['confidence']:.2f}% confidence"
                )
                
                # Show top predictions
                st.subheader("Top Predictions")
                sorted_scores = sorted(species_result['all_scores'].items(), 
                                     key=lambda x: x[1], reverse=True)[:5]
                for label, score in sorted_scores:
                    st.write(f"• {label}: {score:.2f}%")
        
        with tab2:
            if 'error' in results.get('butterfly_stages', {}):
                st.error(f"Butterfly Stages Classification Error: {results['butterfly_stages']['error']}")
            else:
                stages_result = results['butterfly_stages']
                st.metric(
                    label="Predicted Stage",
                    value=stages_result['prediction'],
                    delta=f"{stages_result['confidence']:.2f}% confidence"
                )
                
                # Show all predictions
                st.subheader("Stage Probabilities")
                for label, score in stages_result['all_scores'].items():
                    st.progress(score / 100.0)
                    st.write(f"{label}: {score:.2f}%")
        
        with tab3:
            if 'error' in results.get('larval_diseases', {}):
                st.error(f"Larval Diseases Classification Error: {results['larval_diseases']['error']}")
            else:
                diseases_result = results['larval_diseases']
                st.metric(
                    label="Disease Status",
                    value=diseases_result['prediction'],
                    delta=f"{diseases_result['confidence']:.2f}% confidence"
                )
                
                # Show all predictions
                st.subheader("Disease Probabilities")
                for label, score in diseases_result['all_scores'].items():
                    st.progress(score / 100.0)
                    st.write(f"{label}: {score:.2f}%")
        
        with tab4:
            if 'error' in results.get('larval_stages', {}):
                st.error(f"Larval Stages Classification Error: {results['larval_stages']['error']}")
            else:
                larval_result = results['larval_stages']
                st.metric(
                    label="Larval Stage",
                    value=larval_result['prediction'],
                    delta=f"{larval_result['confidence']:.2f}% confidence"
                )
                
                # Show all predictions
                st.subheader("Larval Stage Probabilities")
                for label, score in larval_result['all_scores'].items():
                    st.progress(score / 100.0)
                    st.write(f"{label}: {score:.2f}%")

def main():
    """Main application function"""
    # Header
    st.title("🦋 LepVision AI Classification System")
    st.markdown("""
    **Advanced Lepidopterology Research Tool**
    
    Upload butterfly or larval images for comprehensive AI-powered classification including:
    - Species identification
    - Developmental stage analysis  
    - Disease detection
    - Larval stage classification
    """)
    
    # Sidebar
    st.sidebar.header("📋 System Information")
    st.sidebar.info("""
    **Models Available:**
    - Butterfly Species Classifier
    - Butterfly Stages Classifier  
    - Larval Diseases Detector
    - Larval Stages Classifier
    """)
    
    # Load models
    if not load_models():
        st.stop()
    
    # File upload section
    st.header("📤 Image Upload")
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of a butterfly or larval specimen for classification"
    )
    
    # Drag and drop area styling
    if uploaded_file is None:
        st.info("👆 Please upload an image file (JPG, JPEG, or PNG format)")
        
        # Sample images section
        st.subheader("📚 About the Classification Models")
        st.markdown("""
        **Species Model**: Identifies butterfly species from adult specimens
        
        **Butterfly Stages Model**: Determines developmental stage (egg, larva, pupa, adult)
        
        **Larval Diseases Model**: Detects common diseases in larval specimens
        
        **Larval Stages Model**: Classifies specific larval developmental stages
        """)
    
    else:
        try:
            # Load and display image
            image = Image.open(uploaded_file)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            st.success("✅ Image uploaded successfully!")
            
            # Classification button
            if st.button("🔍 Classify Image", type="primary"):
                with st.spinner("🤖 Running AI classification models..."):
                    results = predict_image(image, st.session_state.model_manager)
                    
                    if results:
                        display_results(results, image)
                    else:
                        st.error("❌ Classification failed. Please try again.")
        
        except Exception as e:
            st.error(f"❌ Error processing image: {str(e)}")
            st.error("Please ensure you've uploaded a valid image file.")

if __name__ == "__main__":
    main()


Species Model: Identifies butterfly species from adult specimens

Butterfly Stages Model: Determines developmental stage (egg, larva, pupa, adult)

Larval Diseases Model: Detects common diseases in larval specimens

Larval Stages Model: Classifies specific larval developmental stages