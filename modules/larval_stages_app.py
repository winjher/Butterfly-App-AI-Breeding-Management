import streamlit as st
import pandas as pd
from modules.larval_stages import load_model, ai_larval_stages_classifier, get_larval_stage

st.title("🦋 Larval Stages Tracker")

model = load_model()

tab1, tab2 = st.tabs(["🧠 AI Classifier", "🦋 Lifecycle Data"])

with tab1:
    image_file = st.file_uploader("Upload Larval Image", type=["jpg", "png", "jpeg"])
    if image_file and st.button("Classify Image"):
        with st.spinner("Classifying..."):
            result = ai_larval_stages_classifier(image_file, model)
        if result:
            st.success(f"Predicted: {result['class_name']} ({result['score']:.2f}%)")
            st.write("Top 3 predictions:")
            for pred in result["top_predictions"]:
                st.write(f"- {pred['class_name']}: {pred['score']:.2f}%")

with tab2:
    st.subheader("Check Stage by Species & Days")
    species = st.selectbox("Select Species", ["Butterfly-Common Lime", "Butterfly-Clippers", "Moth-Atlas"])
    days = st.number_input("Days since egg hatched", min_value=0, max_value=100, value=1)
    if st.button("Get Stage"):
        stage = get_larval_stage(species, days)
        st.info(stage)
