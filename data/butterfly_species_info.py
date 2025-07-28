"""
Comprehensive butterfly species information database
Contains detailed information about butterfly species, lifecycle stages, diseases, and defects
"""

# Butterfly species information with detailed metadata
BUTTERFLY_SPECIES_INFO = {
    "Butterfly-Clippers": {
        "scientific_name": "Parthenos sylvia",
        "family": "Nymphalidae",
        "discovered": "Carl Peter Thunberg, Cramer",
        "year": "1776",
        "description": "Forewing triangular; costa very slightly curved, apex rounded, exterior margin oblique and slightly scalloped, posterior margin short, angle convex",
        "habitat": "Tropical rainforests, secondary forests",
        "wingspan": "80-90mm",
        "conservation_status": "Stable",
        "distribution": "Southeast Asia, Indonesia, Malaysia"
    },
    "Butterfly-Common Jay": {
        "scientific_name": "Graphium doson",
        "family": "Papilionidae",
        "discovered": "C. & R. Felder",
        "year": "1864",
        "description": "Medium-sized swallowtail with distinctive blue-green markings and tail extensions",
        "habitat": "Forest edges, gardens, parks",
        "wingspan": "70-85mm",
        "conservation_status": "Stable",
        "distribution": "India, Southeast Asia, Southern China"
    },
    "Butterfly-Common Lime": {
        "scientific_name": "Papilio demoleus",
        "family": "Papilionidae",
        "discovered": "Linnaeus",
        "year": "1758",
        "description": "The butterfly is tailless and has a wingspan 80–100 mm, the butterfly has a large number of irregular spots on the wing",
        "habitat": "Gardens, citrus groves, urban areas",
        "wingspan": "80-100mm",
        "conservation_status": "Stable",
        "distribution": "Asia, introduced to Caribbean and parts of America"
    },
    "Butterfly-Common Mime": {
        "scientific_name": "Papilio clytia",
        "family": "Papilionidae",
        "discovered": "Linnaeus",
        "year": "1758",
        "description": "It's a black-bodied swallowtail and a good example of Batesian mimicry, meaning it mimics the appearance of other distasteful butterflies",
        "habitat": "Forest areas, woodland edges",
        "wingspan": "85-95mm",
        "conservation_status": "Stable",
        "distribution": "India, Southeast Asia"
    },
    "Butterfly-Common Mormon": {
        "scientific_name": "Papilio polytes",
        "family": "Papilionidae",
        "discovered": "Linnaeus",
        "year": "1758",
        "description": "Large black swallowtail with sexual dimorphism, females often mimic other species",
        "habitat": "Gardens, forest edges, agricultural areas",
        "wingspan": "90-110mm",
        "conservation_status": "Stable",
        "distribution": "India, Southeast Asia, Southern China"
    },
    "Butterfly-Emerald Swallowtail": {
        "scientific_name": "Papilio palinurus",
        "family": "Papilionidae",
        "discovered": "Fabricius",
        "year": "1787",
        "description": "Stunning black butterfly with brilliant emerald green bands and patches",
        "habitat": "Primary and secondary rainforests",
        "wingspan": "80-100mm",
        "conservation_status": "Vulnerable",
        "distribution": "Southeast Asia, Indonesia, Philippines"
    },
    "Butterfly-Golden Birdwing": {
        "scientific_name": "Troides rhadamantus",
        "family": "Papilionidae",
        "discovered": "H. Lucas",
        "year": "1835",
        "description": "Large golden yellow and black birdwing butterfly, one of the largest in the world",
        "habitat": "Primary rainforests, high canopy",
        "wingspan": "150-180mm",
        "conservation_status": "Protected",
        "distribution": "Philippines (endemic)"
    },
    "Butterfly-Gray Glassy Tiger": {
        "scientific_name": "Ideopsis juventa",
        "family": "Nymphalidae",
        "discovered": "Cramer",
        "year": "1777",
        "description": "Semi-transparent wings with gray and white markings, slow graceful flight",
        "habitat": "Forest clearings, edges, gardens",
        "wingspan": "70-85mm",
        "conservation_status": "Stable",
        "distribution": "Southeast Asia, Indonesia"
    },
    "Butterfly-Great Eggfly": {
        "scientific_name": "Hypolimnas bolina",
        "family": "Nymphalidae",
        "discovered": "Linnaeus",
        "year": "1758",
        "description": "Large butterfly with striking sexual dimorphism, males are black with white patches",
        "habitat": "Gardens, forest edges, open areas",
        "wingspan": "85-100mm",
        "conservation_status": "Stable",
        "distribution": "Indo-Pacific region, Australia"
    },
    "Butterfly-Great Yellow Mormon": {
        "scientific_name": "Papilio lowi",
        "family": "Papilionidae",
        "discovered": "Druce",
        "year": "1873",
        "description": "Large yellow and black swallowtail with distinctive wing patterns",
        "habitat": "Primary forests, mountainous regions",
        "wingspan": "120-140mm",
        "conservation_status": "Near Threatened",
        "distribution": "Borneo (endemic)"
    },
    "Butterfly-Paper Kite": {
        "scientific_name": "Idea leuconoe",
        "family": "Nymphalidae",
        "discovered": "Erichson",
        "year": "1834",
        "description": "Large white butterfly with black markings and semi-transparent wings",
        "habitat": "Mangroves, coastal forests, gardens",
        "wingspan": "95-110mm",
        "conservation_status": "Stable",
        "distribution": "Southeast Asia, Taiwan, Southern Japan"
    },
    "Butterfly-Pink Rose": {
        "scientific_name": "Pachliopta kotzebuea",
        "family": "Papilionidae",
        "discovered": "Eschscholtz",
        "year": "1821",
        "description": "Beautiful rose swallowtail with pink and black coloration",
        "habitat": "Forest areas, gardens with host plants",
        "wingspan": "80-90mm",
        "conservation_status": "Stable",
        "distribution": "Philippines (endemic)"
    },
    "Butterfly-Plain Tiger": {
        "scientific_name": "Danaus chrysippus",
        "family": "Nymphalidae",
        "discovered": "Linnaeus",
        "year": "1758",
        "description": "Orange butterfly with black borders and white spots, toxic to predators",
        "habitat": "Open areas, gardens, grasslands",
        "wingspan": "70-80mm",
        "conservation_status": "Stable",
        "distribution": "Africa, Asia, Australia"
    },
    "Butterfly-Red Lacewing": {
        "scientific_name": "Cethosia biblis",
        "family": "Nymphalidae",
        "discovered": "Drury",
        "year": "1773",
        "description": "Stunning red and black butterfly with intricate lacewing patterns",
        "habitat": "Primary rainforests, shaded areas",
        "wingspan": "80-90mm",
        "conservation_status": "Vulnerable",
        "distribution": "India, Southeast Asia"
    },
    "Butterfly-Scarlet Mormon": {
        "scientific_name": "Papilio rumanzovia",
        "family": "Papilionidae",
        "discovered": "Eschscholtz",
        "year": "1821",
        "description": "Large black swallowtail with brilliant red markings",
        "habitat": "Primary forests, mountainous regions",
        "wingspan": "110-130mm",
        "conservation_status": "Protected",
        "distribution": "Philippines (endemic)"
    },
    "Butterfly-Tailed Jay": {
        "scientific_name": "Graphium agamemnon",
        "family": "Papilionidae",
        "discovered": "Linnaeus",
        "year": "1758",
        "description": "Green and black swallowtail with distinctive tails and spotted pattern",
        "habitat": "Gardens, forest edges, parks",
        "wingspan": "80-100mm",
        "conservation_status": "Stable",
        "distribution": "India, Southeast Asia, Australia"
    },
    "Moth-Atlas": {
        "scientific_name": "Attacus atlas",
        "family": "Saturniidae",
        "discovered": "Linnaeus",
        "year": "1758",
        "description": "One of the largest moths in the world with distinctive triangular wing tips",
        "habitat": "Tropical and subtropical forests",
        "wingspan": "200-280mm",
        "conservation_status": "Stable",
        "distribution": "Asia, from India to Indonesia"
    },
    "Moth-Giant Silk": {
        "scientific_name": "Samia cynthia",
        "family": "Saturniidae",
        "discovered": "Drury",
        "year": "1773",
        "description": "Large silk moth with eye spots and feathery antennae",
        "habitat": "Deciduous forests, parks",
        "wingspan": "100-150mm",
        "conservation_status": "Stable",
        "distribution": "Asia, introduced to North America"
    }
}

# Host plants and feeding requirements for each species
SPECIES_HOST_PLANTS = {
    'Butterfly-Clippers': {
        'plant': ['Ixora', 'Wild Cucumber', 'Passiflora'],
        'dailyConsumption': 120
    },
    'Butterfly-Common Jay': {
        'plant': ['Avocado Tree', 'Soursop', 'Sugar Apple', 'Amuyon', 'Indian Tree'],
        'dailyConsumption': 160
    },
    'Butterfly-Common Lime': {
        'plant': ['Limeberry', 'Calamondin', 'Pomelo', 'Sweet Orange', 'Calamansi'],
        'dailyConsumption': 140
    },
    'Butterfly-Common Mime': {
        'plant': ['Clover Cinnamon', 'Wild Cinnamon', 'Aristolochia'],
        'dailyConsumption': 150
    },
    'Butterfly-Common Mormon': {
        'plant': ['Limeberry', 'Calamondin', 'Pomelo', 'Sweet Orange', 'Calamansi', 'Lemoncito'],
        'dailyConsumption': 155
    },
    'Butterfly-Emerald Swallowtail': {
        'plant': ['Curry Leafs', 'Pink Lime-Berry Tree', 'Glycosmis'],
        'dailyConsumption': 180
    },
    'Butterfly-Golden Birdwing': {
        'plant': ['Dutchman pipe', 'Indian Birthwort', 'Aristolochia'],
        'dailyConsumption': 200
    },
    'Butterfly-Gray Glassy Tiger': {
        'plant': ['Parsonsia', 'Tylophora', 'Asclepias'],
        'dailyConsumption': 130
    },
    'Butterfly-Great Eggfly': {
        'plant': ['Portulaca', 'Synedrella', 'Asystasia'],
        'dailyConsumption': 145
    },
    'Butterfly-Great Yellow Mormon': {
        'plant': ['Citrus species', 'Murraya', 'Glycosmis'],
        'dailyConsumption': 175
    },
    'Butterfly-Paper Kite': {
        'plant': ['Parsonsia', 'Tylophora', 'Gymnema'],
        'dailyConsumption': 135
    },
    'Butterfly-Pink Rose': {
        'plant': ['Aristolochia', 'Dutchman pipe', 'Birthwort'],
        'dailyConsumption': 165
    },
    'Butterfly-Plain Tiger': {
        'plant': ['Calotropis', 'Asclepias', 'Crown flower'],
        'dailyConsumption': 125
    },
    'Butterfly-Red Lacewing': {
        'plant': ['Passiflora', 'Adenia', 'Passion vine'],
        'dailyConsumption': 170
    },
    'Butterfly-Scarlet Mormon': {
        'plant': ['Aristolochia', 'Dutchman pipe', 'Birthwort'],
        'dailyConsumption': 185
    },
    'Butterfly-Tailed Jay': {
        'plant': ['Polyalthia', 'Annona', 'Sugar apple'],
        'dailyConsumption': 155
    },
    'Moth-Atlas': {
        'plant': ['Rambutan', 'Willow', 'Privet', 'Tree of Heaven'],
        'dailyConsumption': 220
    },
    'Moth-Giant Silk': {
        'plant': ['Ailanthus', 'Cherry', 'Lilac', 'Privet'],
        'dailyConsumption': 190
    }
}

# Lifecycle stage information
LIFESTAGES_INFO = {
    "Butterfly": {
        "stages_info": "Adult reproductive stage, winged insect capable of flight and mating",
        "duration_days": "7-30",
        "characteristics": "Fully developed wings, reproductive organs, can fly and mate",
        "care_requirements": "Nectar sources, mating space, egg-laying substrates"
    },
    "Eggs": {
        "stages_info": "Early developmental stage, typically laid on host plants",
        "duration_days": "3-7",
        "characteristics": "Small, round or oval, attached to leaves",
        "care_requirements": "Proper humidity, temperature control, protection from predators"
    },
    "Larvae": {
        "stages_info": "Caterpillar stage, primary feeding and growth phase with multiple instars",
        "duration_days": "14-35",
        "characteristics": "Segmented body, growing rapidly, molting several times",
        "care_requirements": "Fresh host plants, clean environment, appropriate density"
    },
    "Pupae": {
        "stages_info": "Chrysalis stage where metamorphosis occurs, non-feeding stage",
        "duration_days": "7-21",
        "characteristics": "Hardened casing, undergoing transformation",
        "care_requirements": "Stable temperature, proper humidity, minimal disturbance"
    }
}

# Pupae defect information and quality assessment
PUPAE_DEFECTS_INFO = {
    "Ant bites": {
        "quality_info": "Indicates ant damage, can lead to pupae death or malformation. Small holes or darkened areas visible.",
        "severity": "High",
        "treatment": "Remove ants, apply protective barriers, isolate affected pupae",
        "prevention": "Ant-proof containers, regular inspection, clean environment"
    },
    "Deformed body": {
        "quality_info": "Physical deformities in pupal structure, may indicate poor health or environmental stress",
        "severity": "Medium to High",
        "treatment": "Monitor closely, maintain optimal conditions, may not be viable",
        "prevention": "Proper nutrition during larval stage, avoid overcrowding"
    },
    "Healthy Pupae": {
        "quality_info": "No visible defects, good potential for successful adult emergence",
        "severity": "None",
        "treatment": "Continue normal care protocols",
        "prevention": "Maintain current practices"
    },
    "Old Pupa": {
        "quality_info": "Pupae past expected emergence time, may be discolored or showing signs of age",
        "severity": "Medium",
        "treatment": "Monitor for delayed emergence, check environmental conditions",
        "prevention": "Accurate record keeping, optimal temperature maintenance"
    },
    "Overbend": {
        "quality_info": "Abnormal curvature in pupal structure, can impede proper development",
        "severity": "Medium",
        "treatment": "Gentle repositioning if possible, monitor development",
        "prevention": "Proper pupation sites, avoid disturbance during pupation"
    },
    "Stretch abdomen": {
        "quality_info": "Abdomen appears stretched or elongated, potentially due to stress or disease",
        "severity": "Medium to High",
        "treatment": "Isolate, monitor for emergence issues, check humidity levels",
        "prevention": "Maintain proper environmental conditions, avoid stress factors"
    }
}

# Larval disease information and treatment protocols
LARVAL_DISEASES_INFO = {
    "Anaphylaxis Infection": {
        "treatment_info": "Severe allergic reaction-like symptoms. Isolate affected larvae immediately. Consult entomologist for specialized treatment.",
        "symptoms": "Rapid swelling, color changes, unusual behavior",
        "contagious": True,
        "mortality_rate": "High",
        "prevention": "Quarantine new stock, maintain hygiene protocols"
    },
    "Gnathostomiasis": {
        "treatment_info": "Parasitic infection affecting digestive system. Remove visible parasites, improve sanitation, treat with appropriate antiparasitic if available.",
        "symptoms": "Visible worms, poor feeding, stunted growth",
        "contagious": True,
        "mortality_rate": "Medium",
        "prevention": "Regular health checks, clean food sources, proper waste management"
    },
    "Healthy": {
        "treatment_info": "Larva appears healthy with no signs of disease. Continue regular monitoring and care.",
        "symptoms": "Normal feeding, regular molting, active movement",
        "contagious": False,
        "mortality_rate": "Low",
        "prevention": "Maintain current care protocols"
    },
    "Nucleopolyhedrosis": {
        "treatment_info": "Highly contagious viral disease. Isolate and destroy infected larvae immediately to prevent spread. Disinfect all equipment and rearing areas.",
        "symptoms": "Sluggish movement, hanging from plants, dark discoloration",
        "contagious": True,
        "mortality_rate": "Very High",
        "prevention": "Strict quarantine, disinfection protocols, avoid overcrowding"
    }
}

# Breeding difficulty and success rates
BREEDING_DIFFICULTY = {
    "Butterfly-Clippers": {"difficulty": "Medium", "success_rate": 75},
    "Butterfly-Common Jay": {"difficulty": "Easy", "success_rate": 85},
    "Butterfly-Common Lime": {"difficulty": "Easy", "success_rate": 90},
    "Butterfly-Common Mime": {"difficulty": "Medium", "success_rate": 70},
    "Butterfly-Common Mormon": {"difficulty": "Easy", "success_rate": 85},
    "Butterfly-Emerald Swallowtail": {"difficulty": "Hard", "success_rate": 60},
    "Butterfly-Golden Birdwing": {"difficulty": "Very Hard", "success_rate": 45},
    "Butterfly-Gray Glassy Tiger": {"difficulty": "Medium", "success_rate": 75},
    "Butterfly-Great Eggfly": {"difficulty": "Easy", "success_rate": 80},
    "Butterfly-Great Yellow Mormon": {"difficulty": "Hard", "success_rate": 55},
    "Butterfly-Paper Kite": {"difficulty": "Medium", "success_rate": 70},
    "Butterfly-Pink Rose": {"difficulty": "Medium", "success_rate": 75},
    "Butterfly-Plain Tiger": {"difficulty": "Easy", "success_rate": 85},
    "Butterfly-Red Lacewing": {"difficulty": "Hard", "success_rate": 50},
    "Butterfly-Scarlet Mormon": {"difficulty": "Very Hard", "success_rate": 40},
    "Butterfly-Tailed Jay": {"difficulty": "Easy", "success_rate": 80},
    "Moth-Atlas": {"difficulty": "Medium", "success_rate": 70},
    "Moth-Giant Silk": {"difficulty": "Medium", "success_rate": 75}
}

# Environmental requirements for optimal breeding
ENVIRONMENTAL_REQUIREMENTS = {
    "temperature_range": {
        "min": 24,  # Celsius
        "max": 30,
        "optimal": 27
    },
    "humidity_range": {
        "min": 60,  # Percentage
        "max": 85,
        "optimal": 75
    },
    "lighting": {
        "type": "Natural or LED",
        "photoperiod": "12:12 (12 hours light, 12 hours dark)",
        "intensity": "Medium to bright"
    },
    "ventilation": {
        "air_changes_per_hour": 4,
        "circulation": "Gentle, avoid drafts"
    }
}

def get_species_info(species_name):
    """
    Get detailed information about a specific butterfly species
    
    Args:
        species_name (str): Name of the butterfly species
        
    Returns:
        dict: Complete information about the species
    """
    if species_name not in BUTTERFLY_SPECIES_INFO:
        return None
    
    info = BUTTERFLY_SPECIES_INFO[species_name].copy()
    
    # Add host plant information
    if species_name in SPECIES_HOST_PLANTS:
        info['host_plants'] = SPECIES_HOST_PLANTS[species_name]
    
    # Add breeding difficulty
    if species_name in BREEDING_DIFFICULTY:
        info['breeding_info'] = BREEDING_DIFFICULTY[species_name]
    
    return info

def get_all_species_names():
    """Get list of all available butterfly species names"""
    return list(BUTTERFLY_SPECIES_INFO.keys())

def get_species_by_family(family_name):
    """
    Get all species belonging to a specific family
    
    Args:
        family_name (str): Name of the butterfly family
        
    Returns:
        list: List of species names in the family
    """
    return [
        species for species, info in BUTTERFLY_SPECIES_INFO.items()
        if info['family'].lower() == family_name.lower()
    ]

def get_conservation_status_summary():
    """Get summary of conservation status across all species"""
    status_counts = {}
    for species, info in BUTTERFLY_SPECIES_INFO.items():
        status = info['conservation_status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    return status_counts

def calculate_feeding_requirements(species_name, larva_count):
    """
    Calculate daily feeding requirements for a batch
    
    Args:
        species_name (str): Name of the butterfly species
        larva_count (int): Number of larvae
        
    Returns:
        dict: Feeding requirements information
    """
    if species_name not in SPECIES_HOST_PLANTS:
        return None
    
    daily_per_larva = SPECIES_HOST_PLANTS[species_name]['dailyConsumption']
    total_daily = daily_per_larva * larva_count
    
    return {
        'species': species_name,
        'larva_count': larva_count,
        'daily_per_larva_grams': daily_per_larva,
        'total_daily_grams': total_daily,
        'host_plants': SPECIES_HOST_PLANTS[species_name]['plant'],
        'weekly_requirement_kg': round(total_daily * 7 / 1000, 2)
    }
