import streamlit as st
import pandas as pd
import os

# This Python script models the lifecycle stages of various butterflies and moths.
# It tracks the progression through up to five instars, the pupal stage, and emergence as an adult.
def get_larval_stages():
    def get_lifecycle_stage(species_name: str, day_of_lifecycle: int) -> str:
        """
        Determines the current lifecycle stage of a butterfly or moth based on the number of days.

        Args:
            species_name: The name of the butterfly or moth (e.g., "Butterfly-Paper Kite").
            day_of_lifecycle: The number of days that have passed since the egg hatched.

        Returns:
            A string describing the current stage of the insect's lifecycle.
        """

        # Dictionary containing the hypothetical duration (in days) for each stage of each species.
        # The keys are species names, and the values are lists of days for Instar 1 to 5 and Pupa.
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

        # Check if the species name is valid and exists in our data
        if species_name not in LIFECYCLE_DURATIONS:
            return f"Error: '{species_name}' data not available. Please choose from the provided list."

        durations = LIFECYCLE_DURATIONS[species_name]
        instar_days = durations[:5]
        pupa_days = durations[5]

        cumulative_days = 0
        stage = ""

        # Check for each instar stage
        for i in range(5):
            cumulative_days += instar_days[i]
            if day_of_lifecycle < cumulative_days:
                return f"The {species_name} is currently in Instar {i + 1}."

        # Check for the pupa stage
        pupa_start_day = cumulative_days
        pupa_end_day = pupa_start_day + pupa_days
        if day_of_lifecycle < pupa_end_day:
            days_in_pupa = day_of_lifecycle - pupa_start_day
            return f"The {species_name} is a pupa. It has been in this stage for {days_in_pupa} days."

        # If all stages are complete, the insect is an adult
        return f"The {species_name} has emerged as an adult."

    # --- Streamlit App ---
    st.set_page_config(page_title="Butterfly & Moth Lifecycle Tracker 🦋", layout="wide")

    st.title("Butterfly & Moth Lifecycle Tracker 🐛🦋")

    st.markdown("""
    This application helps you track the **lifecycle stage** of various butterflies and moths.
    Simply select a species and a number of days to see its current stage!
    """)

    # Load data from the function's dictionary to a DataFrame for display
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

    st.subheader("Species Lifecycle Data")
    st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("Find the Current Stage")

    # Create two columns for user input
    col1, col2 = st.columns(2)

    with col1:
        species_list = list(LIFECYCLE_DURATIONS.keys())
        selected_species = st.selectbox(
            "Select a Species:",
            species_list
        )

    with col2:
        days_passed = st.number_input(
            "Enter the number of days since the egg hatched:",
            min_value=0,
            max_value=100,
            value=1
        )

    if st.button("Check Stage"):
        if selected_species and days_passed is not None:
            stage_result = get_lifecycle_stage(selected_species, days_passed)
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

    # get_lifecycle_stage(selected_species, days_passed)

    # Add a simple footer
    st.markdown("---")
    st.markdown("Created with ❤️ using Streamlit")

