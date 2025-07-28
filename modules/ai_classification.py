import streamlit as st
import numpy as np
from PIL import Image
import os
import datetime
from data.butterfly_species_info import BUTTERFLY_SPECIES_INFO, LIFESTAGES_INFO, PUPAE_DEFECTS_INFO, LARVAL_DISEASES_INFO
from utils.image_processing import process_image_for_classification
from utils.csv_handlers import save_to_csv

def ai_classification_app():
    """AI-powered butterfly classification system"""
    st.title("🤖 AI Butterfly Classification System")
    st.caption("CNN-powered analysis for species identification, lifecycle stages, and health assessment")
    
    # Check for model directory
    model_dir = './model'
    if not os.path.exists(model_dir):
        st.error(f"Model directory not found: {model_dir}")
        st.info("Please create the model directory and place your trained models inside:")
        st.code("""
        model/
        ├── model_Butterfly_Species.h5
        ├── model_Life_Stages.h5
        ├── model_Pupae_Defects.h5
        └── model_Larval_Diseases.h5
        """)
        return
    
    # Analysis type selection
    analysis_type = st.selectbox("Analysis Type", [
        "Complete Analysis (All Models)",
        "Species Identification",
        "Lifecycle Stage",
        "Larval Disease Detection",
        "Pupae Defect Analysis"
    ])
    
    # Image upload options
    upload_option = st.radio("Image Source", ["Upload File", "Camera Capture"])
    
    image = None
    if upload_option == "Upload File":
        uploaded_file = st.file_uploader(
            "Upload Butterfly Image", 
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the butterfly/larva/pupa for analysis"
        )
        if uploaded_file:
            image = Image.open(uploaded_file)
    else:
        camera_image = st.camera_input("Take a photo")
        if camera_image:
            image = Image.open(camera_image)
    
    if image:
        # Display uploaded image
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(image, caption="Uploaded Image", use_container_width=True)
        
        with col2:
            # Image preprocessing info
            st.write("**Image Information:**")
            st.write(f"Size: {image.size}")
            st.write(f"Mode: {image.mode}")
            
            # Process button
            if st.button("🔍 Analyze Image", type="primary"):
                with st.spinner("Processing image with AI models..."):
                    results = perform_classification(image, analysis_type)
                    display_results(results)
                    
                    # Save analysis results
                    save_analysis_results(results, analysis_type)
    
    # Model information section
    st.markdown("---")
    display_model_info()
    
    # Recent classifications
    display_recent_classifications()

def perform_classification(image, analysis_type):
    """Perform AI classification based on selected analysis type"""
    results = {}
    
    try:
        # Mock AI results since actual models aren't available
        # In production, this would use actual TensorFlow models
        st.info("🔬 Simulating AI analysis (replace with actual model inference)")
        
        if analysis_type in ["Complete Analysis (All Models)", "Species Identification"]:
            results["species"] = simulate_species_classification()
        
        if analysis_type in ["Complete Analysis (All Models)", "Lifecycle Stage"]:
            results["lifecycle"] = simulate_lifecycle_classification()
        
        if analysis_type in ["Complete Analysis (All Models)", "Larval Disease Detection"]:
            results["diseases"] = simulate_disease_classification()
        
        if analysis_type in ["Complete Analysis (All Models)", "Pupae Defect Analysis"]:
            results["defects"] = simulate_defect_classification()
            
    except Exception as e:
        st.error(f"Classification error: {str(e)}")
        results["error"] = str(e)
    
    return results

def simulate_species_classification():
    """Simulate species classification (replace with actual model)"""
    import random
    species_list = list(BUTTERFLY_SPECIES_INFO.keys())
    predicted_species = random.choice(species_list)
    confidence = random.uniform(0.75, 0.98)
    
    return {
        "predicted_class": predicted_species,
        "confidence": confidence,
        "top_3": [
            {"class": predicted_species, "confidence": confidence},
            {"class": random.choice(species_list), "confidence": random.uniform(0.1, 0.3)},
            {"class": random.choice(species_list), "confidence": random.uniform(0.05, 0.15)}
        ]
    }

def simulate_lifecycle_classification():
    """Simulate lifecycle stage classification"""
    import random
    stages = list(LIFESTAGES_INFO.keys())
    predicted_stage = random.choice(stages)
    confidence = random.uniform(0.8, 0.95)
    
    return {
        "predicted_class": predicted_stage,
        "confidence": confidence,
        "description": LIFESTAGES_INFO[predicted_stage]["stages_info"]
    }

def simulate_disease_classification():
    """Simulate disease classification"""
    import random
    diseases = list(LARVAL_DISEASES_INFO.keys())
    predicted_disease = random.choice(diseases)
    confidence = random.uniform(0.7, 0.92)
    
    return {
        "predicted_class": predicted_disease,
        "confidence": confidence,
        "treatment": LARVAL_DISEASES_INFO[predicted_disease]["treatment_info"]
    }

def simulate_defect_classification():
    """Simulate defect classification"""
    import random
    defects = list(PUPAE_DEFECTS_INFO.keys())
    predicted_defect = random.choice(defects)
    confidence = random.uniform(0.75, 0.90)
    
    return {
        "predicted_class": predicted_defect,
        "confidence": confidence,
        "quality_info": PUPAE_DEFECTS_INFO[predicted_defect]["quality_info"]
    }

def display_results(results):
    """Display classification results"""
    st.subheader("🔬 Analysis Results")
    
    if "error" in results:
        st.error(f"Analysis failed: {results['error']}")
        return
    
    # Species identification results
    if "species" in results:
        st.write("### 🦋 Species Identification")
        species_result = results["species"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"**Predicted Species:** {species_result['predicted_class']}")
            st.write(f"**Confidence:** {species_result['confidence']:.1%}")
            
            # Display species information
            if species_result['predicted_class'] in BUTTERFLY_SPECIES_INFO:
                species_info = BUTTERFLY_SPECIES_INFO[species_result['predicted_class']]
                st.write(f"**Scientific Name:** {species_info['scientific_name']}")
                st.write(f"**Family:** {species_info['family']}")
                
        with col2:
            st.write("**Top 3 Predictions:**")
            for i, pred in enumerate(species_result['top_3'], 1):
                st.write(f"{i}. {pred['class']} ({pred['confidence']:.1%})")
    
    # Lifecycle stage results
    if "lifecycle" in results:
        st.write("### 🔄 Lifecycle Stage")
        lifecycle_result = results["lifecycle"]
        
        st.info(f"**Stage:** {lifecycle_result['predicted_class']} ({lifecycle_result['confidence']:.1%})")
        st.write(f"**Description:** {lifecycle_result['description']}")
    
    # Disease detection results
    if "diseases" in results:
        st.write("### 🏥 Disease Detection")
        disease_result = results["diseases"]
        
        if disease_result['predicted_class'] == "Healthy":
            st.success(f"✅ {disease_result['predicted_class']} ({disease_result['confidence']:.1%})")
        else:
            st.warning(f"⚠️ {disease_result['predicted_class']} detected ({disease_result['confidence']:.1%})")
        
        st.write(f"**Treatment Information:** {disease_result['treatment']}")
    
    # Defect analysis results
    if "defects" in results:
        st.write("### 🔍 Quality Assessment")
        defect_result = results["defects"]
        
        if defect_result['predicted_class'] == "Healthy Pupae":
            st.success(f"✅ {defect_result['predicted_class']} ({defect_result['confidence']:.1%})")
        else:
            st.warning(f"⚠️ {defect_result['predicted_class']} detected ({defect_result['confidence']:.1%})")
        
        st.write(f"**Quality Information:** {defect_result['quality_info']}")

def save_analysis_results(results, analysis_type):
    """Save classification results to CSV"""
    import datetime
    
    # Prepare data for saving
    analysis_data = {
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'analysis_type': analysis_type,
        'user': st.session_state.username,
    }
    
    # Add specific results
    if "species" in results:
        analysis_data.update({
            'predicted_species': results["species"]["predicted_class"],
            'species_confidence': results["species"]["confidence"]
        })
    
    if "lifecycle" in results:
        analysis_data.update({
            'predicted_stage': results["lifecycle"]["predicted_class"],
            'stage_confidence': results["lifecycle"]["confidence"]
        })
    
    if "diseases" in results:
        analysis_data.update({
            'predicted_disease': results["diseases"]["predicted_class"],
            'disease_confidence': results["diseases"]["confidence"]
        })
    
    if "defects" in results:
        analysis_data.update({
            'predicted_defect': results["defects"]["predicted_class"],
            'defect_confidence': results["defects"]["confidence"]
        })
    
    save_to_csv('ai_classifications.csv', analysis_data)

def display_model_info():
    """Display model information and status"""
    st.subheader("🤖 Model Information")
    
    models = [
        "model_Butterfly_Species.h5",
        "model_Life_Stages.h5", 
        "model_Pupae_Defects.h5",
        "model_Larval_Diseases.h5"
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Available Models:**")
        for model in models:
            model_path = f"./model/{model}"
            if os.path.exists(model_path):
                st.success(f"✅ {model}")
            else:
                st.error(f"❌ {model} (Missing)")
    
    with col2:
        st.write("**Model Capabilities:**")
        st.write("🦋 Species: 18 butterfly/moth species")
        st.write("🔄 Stages: 4 lifecycle stages")
        st.write("🏥 Diseases: 4 larval disease types")
        st.write("🔍 Defects: 6 pupae defect types")

def display_recent_classifications():
    """Display recent classification results"""
    st.subheader("📊 Recent Classifications")
    
    from utils.csv_handlers import load_from_csv
    
    classifications_df = load_from_csv('ai_classifications.csv')
    
    if not classifications_df.empty:
        # Display recent classifications
        recent_classifications = classifications_df.tail(10).sort_values('timestamp', ascending=False)
        st.dataframe(recent_classifications, use_container_width=True)
        
        # Classification statistics
        st.write("**Classification Statistics:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_classifications = len(classifications_df)
            st.metric("Total Classifications", total_classifications)
        
        with col2:
            if 'predicted_species' in classifications_df.columns:
                unique_species = classifications_df['predicted_species'].nunique()
                st.metric("Species Identified", unique_species)
        
        with col3:
            today = datetime.date.today().strftime('%Y-%m-%d')
            today_classifications = len(classifications_df[classifications_df['timestamp'].str.startswith(today)])
            st.metric("Today's Classifications", today_classifications)
    else:
        st.info("No classifications performed yet. Upload an image to get started!")
