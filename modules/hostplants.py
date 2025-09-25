# """
# Host plant database and management system for butterfly species.
# Contains information about suitable host plants for each butterfly and moth species.
# """

# from models import BUTTERFLY_SPECIES

# # Host plant database - mapping species to their suitable host plants
# HOST_PLANTS_DB = {
#     'Moth-Atlas': ['Soursop', 'Gmelina', 'Sugar Apple'],
#     'Butterfly-Common Jay': ['Avocado Tree', 'Soursop', 'Sugar Apple', 'Amuyon', 'Indian Tree'],
#     'Butterfly-Common Lime': ['Limeberry', 'Calamondin', 'Pomelo', 'Sweet Orange', 'Calamansi'],
#     'Butterfly-Common Mime': ['Clover Cinnamon', 'Wild Cinnamon'],
#     'Butterfly-Common Mormon': ['Limeberry', 'Calamondin', 'Pomelo', 'Sweet Orange', 'Calamansi', 'Lemoncito'],
#     'Butterfly-Emerald Swallowtail': ['Curry Leafs', 'Pink Lime-Berry Tree'],
#     'Butterfly-Great Eggfly': ['Sweet Potato', 'Water Spinach'],
#     'Butterfly-Great Yellow Mormon': ['Limeberry', 'Calamondin', 'Pomelo', 'Sweet Orange', 'Calamansi'],
#     'Moth-Giant Silk': ['Gmelina Tree'],
#     'Butterfly-Golden Birdwing': ['Dutchman Pipe', 'Indian Birthwort'],
#     'Butterfly-Paper Kite': ['Common Skillpod'],
#     'Butterfly-Pink Rose': ['Dutchman Pipe', 'Indian Birthwort'],
#     'Butterfly-Plain Tiger': ['Crown Flower', 'Giant Milkweed'],
#     'Butterfly-Red Lacewing': ['Wild Bush Passion Fruits'],
#     'Butterfly-Scarlet Mormon': ['Calamondin', 'Pomelo', 'Sweet Orange', 'Calamansi'],
#     'Butterfly-Tailed Jay': ['Avocado Tree', 'Soursop', 'Sugar Apple', 'Amuyon', 'Indian Tree'],
#     'Butterfly-Clippers': ['Wild Cucumber'],
#     'Butterfly-Gray Glassy Tiger': ['Crown Flower', 'Giant Milkweed']  # Similar to Plain Tiger
# }

# # Plant characteristics database
# PLANT_CHARACTERISTICS = {
#     'Soursop': {
#         'scientific_name': 'Annona muricata',
#         'growth_rate': 'Medium',
#         'availability': 'Common',
#         'nutritional_value': 'High',
#         'maintenance': 'Low'
#     },
#     'Gmelina': {
#         'scientific_name': 'Gmelina arborea', 
#         'growth_rate': 'Fast',
#         'availability': 'Common',
#         'nutritional_value': 'High',
#         'maintenance': 'Low'
#     },
#     'Sugar Apple': {
#         'scientific_name': 'Annona squamosa',
#         'growth_rate': 'Medium',
#         'availability': 'Common', 
#         'nutritional_value': 'High',
#         'maintenance': 'Medium'
#     },
#     'Avocado Tree': {
#         'scientific_name': 'Persea americana',
#         'growth_rate': 'Slow',
#         'availability': 'Common',
#         'nutritional_value': 'High',
#         'maintenance': 'Medium'
#     },
#     'Limeberry': {
#         'scientific_name': 'Triphasia trifolia',
#         'growth_rate': 'Medium',
#         'availability': 'Common',
#         'nutritional_value': 'Medium',
#         'maintenance': 'Low'
#     },
#     'Calamondin': {
#         'scientific_name': 'Citrofortunella microcarpa',
#         'growth_rate': 'Medium',
#         'availability': 'Very Common',
#         'nutritional_value': 'High',
#         'maintenance': 'Low'
#     },
#     'Dutchman Pipe': {
#         'scientific_name': 'Aristolochia elegans',
#         'growth_rate': 'Fast',
#         'availability': 'Rare',
#         'nutritional_value': 'High',
#         'maintenance': 'High'
#     },
#     'Crown Flower': {
#         'scientific_name': 'Calotropis gigantea',
#         'growth_rate': 'Fast',
#         'availability': 'Common',
#         'nutritional_value': 'Medium',
#         'maintenance': 'Low'
#     }
# }
# def host_plants_app():
#     """Host Plants Management Interface"""
#     import streamlit as st

#     st.title("🌱 Host Plants Management")

#     st.markdown("""
#     This module provides information about suitable host plants for various butterfly species.
#     You can explore host plants, their characteristics, and calculate foliage demand based on active breeding batches.
#     """)

#     # Example usage
#     species = st.selectbox("Select Butterfly Species", get_species_list())
#     if species:
#         st.subheader(f"Host Plants for {species}")
#         host_plants = get_host_plants(species)
#         if host_plants:
#             for plant in host_plants:
#                 characteristics = get_plant_characteristics(plant)
#                 st.markdown(f"**{plant}**")
#                 st.write(characteristics)
#         else:
#             st.write("No host plants found for this species.")
# def get_host_plants(species):
#     """Get host plants for a specific butterfly species"""
#     return HOST_PLANTS_DB.get(species, [])

# def get_species_list():
#     """Get list of all supported butterfly species"""
#     return BUTTERFLY_SPECIES

# def get_all_host_plants():
#     """Get list of all host plants in database"""
#     all_plants = set()
#     for plants in HOST_PLANTS_DB.values():
#         all_plants.update(plants)
#     return sorted(list(all_plants))

# def get_plant_characteristics(plant_name):
#     """Get characteristics of a specific plant"""
#     return PLANT_CHARACTERISTICS.get(plant_name, {})

# def get_species_by_plant(plant_name):
#     """Get butterfly species that use a specific host plant"""
#     species_list = []
#     for species, plants in HOST_PLANTS_DB.items():
#         if plant_name in plants:
#             species_list.append(species)
#     return species_list

# def calculate_daily_foliage_demand(batches):
#     """Calculate daily foliage demand for active batches"""
#     total_demand = {}
    
#     # Consumption rates per larva per day (in grams)
#     CONSUMPTION_RATES = {
#         'egg': 0,
#         'larva': 5.0,  # 5g per larva per day
#         'pupa': 0,
#         'adult': 1.0   # 1g per adult per day (nectar plants)
#     }
    
#     for batch in batches:
#         if batch.get('status') != 'active':
#             continue
            
#         species = batch.get('species', '')
#         stage = batch.get('stage', 'larva')
#         current_count = batch.get('current_count', 0)
        
#         # Get consumption rate for current stage
#         consumption_per_individual = CONSUMPTION_RATES.get(stage, 0)
        
#         if consumption_per_individual > 0:
#             # Get host plants for this species
#             host_plants = get_host_plants(species)
            
#             # Assume equal distribution among host plants
#             plants_count = len(host_plants) if host_plants else 1
#             demand_per_plant = (current_count * consumption_per_individual) / plants_count
            
#             for plant in host_plants:
#                 if plant not in total_demand:
#                     total_demand[plant] = 0
#                 total_demand[plant] += demand_per_plant
    
#     return total_demand

# def get_plant_availability_score(plant_name):
#     """Get availability score for a plant (0-1 scale)"""
#     characteristics = get_plant_characteristics(plant_name)
#     availability = characteristics.get('availability', 'Unknown')
    
#     availability_scores = {
#         'Very Common': 1.0,
#         'Common': 0.8,
#         'Moderate': 0.6,
#         'Rare': 0.3,
#         'Very Rare': 0.1,
#         'Unknown': 0.5
#     }
    
#     return availability_scores.get(availability, 0.5)

# def recommend_alternative_plants(species, unavailable_plants):
#     """Recommend alternative plants when preferred ones are unavailable"""
#     all_plants = get_host_plants(species)
#     available_plants = [plant for plant in all_plants if plant not in unavailable_plants]
    
#     # Sort by availability score
#     available_plants.sort(key=get_plant_availability_score, reverse=True)
    
#     return available_plants

# def generate_plant_schedule(batches, planning_days=30):
#     """Generate planting schedule based on batch requirements"""
#     schedule = {}
    
#     for day in range(planning_days):
#         schedule[day] = calculate_daily_foliage_demand(batches)
    
#     return schedule

# def validate_host_plant_compatibility(species, plant_name):
#     """Validate if a plant is compatible with a butterfly species"""
#     compatible_plants = get_host_plants(species)
#     return plant_name in compatible_plants

# def get_plant_growth_timeline(plant_name):
#     """Get estimated growth timeline for a plant"""
#     characteristics = get_plant_characteristics(plant_name)
#     growth_rate = characteristics.get('growth_rate', 'Medium')
    
#     # Growth timelines in days
#     growth_timelines = {
#         'Fast': 30,      # 1 month to maturity
#         'Medium': 60,    # 2 months to maturity  
#         'Slow': 120      # 4 months to maturity
#     }
    
#     return growth_timelines.get(growth_rate, 60)

# def calculate_planting_requirements(projected_demand, plant_name):
#     """Calculate how many plants need to be planted to meet demand"""
#     characteristics = get_plant_characteristics(plant_name)
    
#     # Assume average yield per mature plant (grams per day)
#     average_yield = {
#         'Fast': 100,
#         'Medium': 150,
#         'Slow': 200
#     }
    
#     growth_rate = characteristics.get('growth_rate', 'Medium')
#     yield_per_plant = average_yield.get(growth_rate, 150)
    
#     plants_needed = max(1, int(projected_demand / yield_per_plant) + 1)
    
#     return {
#         'plants_needed': plants_needed,
#         'yield_per_plant': yield_per_plant,
#         'total_yield': plants_needed * yield_per_plant,
#         'growth_timeline': get_plant_growth_timeline(plant_name)
#     }
