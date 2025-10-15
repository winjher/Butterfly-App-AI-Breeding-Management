# Butterfly Breeding Ecosystem

## Overview

This is a comprehensive Streamlit-based butterfly breeding management system that integrates multiple business functions including breeding management, AI classification, point of sale, sales tracking, and farm booking systems. The application is designed for butterfly breeders, farm operators, and customers to manage the complete butterfly lifecycle and business operations.

## User Preferences

```
Preferred communication style: Simple, everyday language.
```

## System Architecture

The application follows a modular Streamlit architecture with the following key design decisions:

### Frontend Architecture
- **Framework**: Streamlit with custom glassmorphism styling
- **UI Pattern**: Multi-tab navigation with modular components
- **Styling**: Custom CSS with glassmorphism effects and background image support
- **Responsive Design**: Wide layout configuration for desktop-first experience

### Backend Architecture
- **Database**: Hybrid approach using SQLite for user authentication and CSV files for business data
- **Authentication**: Session-based authentication with SHA256 password hashing
- **Data Persistence**: CSV files for transactional data, SQLite for user management
- **File Organization**: Modular structure with separate modules for each business function

### Data Storage Strategy
- **User Data**: SQLite database (`users.db`) for authentication and user profiles
- **Business Data**: CSV files for flexible data storage and easy export/import
- **Images**: Local file system storage in `icon/` directory
- **Model Data**: Dedicated `model/` directory for AI classification models

## Key Components

### Authentication Module (`modules/auth.py`)
- SHA256 password hashing for security
- Role-based access control (admin/user)
- Session state management
- Default admin account creation

### Profile Management (`modules/profile_management.py`)
- Role-based profile editing with extended user fields
- Contact information, birthday, and address management
- Payment information storage (credit card last 4 digits)
- Student and faculty specific profile sections

### Premium System (`modules/premium_system.py`)
- Premium membership subscription (₱299/month)
- Commission tracking and Level 2 achievement system
- 260,000 pesos earnings milestone for Level 2 status
- 20,000 pesos achievement prize for reaching Level 2
- Ewallet integration with transaction history
- Signup bonus system (200 pesos GCash bonus)

### Email Notifications (`modules/email_notifications.py`)
- SendGrid integration for automated email campaigns
- Premium membership promotion emails to breeders
- Level upgrade congratulations notifications
- Bulk email capabilities for breeder outreach

### Landing Page (`modules/landing_page.py`)
- Enhanced dashboard with signup bonus promotion
- Premium membership benefits showcase
- Success stories and testimonials display
- Top earners leaderboard
- Feature highlights and conversion optimization

### Breeding Management (`modules/breeding_management.py`)
- Cage management system
- Task scheduling and tracking
- Breeding batch monitoring
- Analytics dashboard with real-time metrics

### AI Classification (`modules/ai_classification.py`)
- TensorFlow/Keras integration for butterfly species identification
- Image preprocessing and validation
- Support for multiple image formats
- Classification confidence scoring

### Point of Sale (`modules/point_of_sale.py`)
- Shopping cart functionality
- Order number generation
- Inventory management for 18 butterfly/moth species
- Transaction recording with profit/cost tracking

### Sales Tracking (`modules/sales_tracking.py`)
- Breeder sales management
- Purchase tracking
- Customer relationship management
- Analytics and reporting

### Booking System (`modules/booking_system.py`)
- Farm visit scheduling
- Location mapping with Folium integration
- Capacity management
- Review system

## Data Flow

1. **User Authentication**: Users log in through the auth module, establishing session state
2. **Navigation**: Main app routes users to selected modules based on sidebar navigation
3. **Data Operations**: Each module independently manages its CSV files for data persistence
4. **Image Processing**: AI classification module processes uploaded images through preprocessing pipeline
5. **Reporting**: Data aggregation across modules for analytics and reporting

## External Dependencies

### Core Framework
- **Streamlit**: Primary web application framework
- **Pandas**: Data manipulation and CSV handling
- **SQLite3**: Embedded database for user management

### AI/ML Components
- **TensorFlow**: Machine learning framework for butterfly classification
- **PIL (Pillow)**: Image processing and manipulation
- **NumPy**: Numerical operations for image preprocessing

### UI/Visualization
- **Folium**: Interactive maps for farm locations
- **Streamlit-Folium**: Streamlit integration for map components

### Security & Authentication
- **Hashlib**: Password hashing (SHA256)
- **Bcrypt**: Alternative password hashing (imported but not actively used)

### Utilities
- **Base64**: Image encoding for CSS background integration
- **DateTime**: Timestamp management across all modules
- **OS**: File system operations and directory management

## Deployment Strategy

### Development Setup
- Single-file entry point (`app.py`) for easy deployment
- Modular architecture allows for independent testing of components
- CSV-based data storage eliminates complex database setup requirements

### Production Considerations
- **Database Migration**: Current CSV approach may need PostgreSQL migration for scalability
- **File Storage**: Local image storage should migrate to cloud storage (AWS S3, etc.)
- **Model Storage**: TensorFlow models require proper versioning and deployment strategy
- **Session Management**: Current in-memory sessions need persistent storage for production

### Scalability Notes
- CSV files work well for small to medium datasets but may need database migration
- Current architecture supports horizontal scaling through database abstraction layer
- Image processing pipeline can be offloaded to separate microservice if needed

The application prioritizes ease of deployment and maintenance while providing comprehensive business functionality for butterfly breeding operations.


modules = ["python-3.11", "web"]

[nix]
channel = "stable-25_05"
packages = ["cargo", "freetype", "glibcLocales", "lcms2", "libiconv", "libimagequant", "libjpeg", "libtiff", "libwebp", "libxcrypt", "openjpeg", "rustc", "tcl", "tk", "zlib"]

[deployment]
deploymentTarget = "autoscale"
run = ["streamlit", "run", "app.py", "--server.port", "5000"]

[workflows]
runButton = "Project"

[[workflows.workflow]]
name = "Project"
mode = "parallel"
author = "agent"

[[workflows.workflow.tasks]]
task = "workflow.run"
args = "Streamlit Server"

[[workflows.workflow]]
name = "Streamlit Server"
author = "agent"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "streamlit run app.py --server.port 5000"
waitForPort = 5000

[[ports]]
localPort = 5000
externalPort = 80

[agent]
integrations = ["python_sendgrid==1.0.0"]

database.py
import os
import sqlite3
import pandas as pd

def initialize_databases():
    """Initialize all required databases and CSV files"""
    
    # Create necessary directories
    directories = ['Data', 'model', 'icon']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Initialize SQLite database for users
    initialize_user_database()
    
    # Initialize premium system after user database
    from modules.premium_system import initialize_premium_db
    from modules.profile_management import initialize_profile_db
    initialize_premium_db()
    initialize_profile_db()
    
    # Initialize CSV file structures
    initialize_csv_files()

def initialize_user_database():
    """Initialize the user authentication database"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Create default admin user
    import hashlib
    admin_password = hashlib.sha256("admin123".encode()).hexdigest()
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, role) 
        VALUES (?, ?, ?)
    ''', ("admin", admin_password, "admin"))
    
    conn.commit()
    conn.close()

def initialize_csv_files():
    """Initialize all required CSV files with proper headers"""
    
    csv_files = {
        'breeding_batches.csv': [
            'batch_id', 'species', 'stage', 'larva_count', 'health_status',
            'created_date', 'created_by', 'notes', 'last_updated'
        ],
        'breeding_tasks.csv': [
            'task_id', 'title', 'type', 'priority', 'due_date', 'batch_id',
            'description', 'status', 'created_by', 'created_date', 'completed_date'
        ],
        'breeding_log.csv': [
            'timestamp', 'event_type', 'batch_id', 'description', 'logged_by'
        ],
        'ai_classifications.csv': [
            'timestamp', 'analysis_type', 'user', 'predicted_species',
            'species_confidence', 'predicted_stage', 'stage_confidence',
            'predicted_disease', 'disease_confidence', 'predicted_defect', 'defect_confidence'
        ],
        'pos_transactions.csv': [
            'order_number', 'date', 'time', 'cashier', 'customer_name',
            'customer_email', 'payment_method', 'total_items', 'total_revenue',
            'total_cost', 'total_profit', 'notes'
        ],
        'pos_items.csv': [
            'order_number', 'date', 'time', 'item_id', 'item_name', 'species',
            'quantity', 'unit_price', 'unit_cost', 'subtotal_revenue',
            'subtotal_profit', 'cashier'
        ],
        'pupae_sales.csv': [
            'sale_id', 'sale_date', 'seller_username', 'buyer_name', 'buyer_contact',
            'species', 'stage', 'quantity', 'price_per_unit', 'total_amount',
            'quality_grade', 'payment_method', 'notes', 'recorded_at'
        ],
        'pupae_purchases.csv': [
            'purchase_id', 'purchase_date', 'buyer_username', 'seller_name',
            'seller_contact', 'species', 'stage', 'quantity', 'price_per_unit',
            'total_cost', 'quality_received', 'payment_method', 'delivery_method',
            'notes', 'recorded_at'
        ],
        'farm_bookings.csv': [
            'booking_id', 'farm_name', 'farm_location', 'visitor_name',
            'visitor_phone', 'visitor_email', 'visit_date', 'visit_time',
            'num_visitors', 'visit_purpose', 'total_cost', 'special_requests',
            'booking_status', 'booked_by', 'booking_date'
        ],
        'farm_reviews.csv': [
            'review_id', 'farm_name', 'reviewer', 'rating', 'review_title',
            'review_text', 'facilities_rating', 'staff_rating', 'value_rating',
            'experience_rating', 'review_date'
        ]
    }
    
    for filename, headers in csv_files.items():
        if not os.path.exists(filename):
            df = pd.DataFrame(columns=headers)
            df.to_csv(filename, index=False)

def get_database_info():
    """Get information about database tables and CSV files"""
    info = {
        'database_tables': [],
        'csv_files': [],
        'total_records': 0
    }
    
    # Check SQLite database
    if os.path.exists('users.db'):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            info['database_tables'].append({
                'name': table_name,
                'records': count
            })
            info['total_records'] += count
        
        conn.close()
    
    # Check CSV files
    csv_files = [
        'breeding_batches.csv', 'breeding_tasks.csv', 'breeding_log.csv',
        'ai_classifications.csv', 'pos_transactions.csv', 'pos_items.csv',
        'pupae_sales.csv', 'pupae_purchases.csv', 'farm_bookings.csv',
        'farm_reviews.csv'
    ]
    
    for filename in csv_files:
        if os.path.exists(filename):
            try:
                df = pd.read_csv(filename)
                info['csv_files'].append({
                    'name': filename,
                    'records': len(df),
                    'size_kb': round(os.path.getsize(filename) / 1024, 2)
                })
                info['total_records'] += len(df)
            except:
                info['csv_files'].append({
                    'name': filename,
                    'records': 0,
                    'size_kb': 0
                })
    
    return info

def backup_data():
    """Create backup of all data"""
    import shutil
    import datetime
    
    backup_dir = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup SQLite database
    if os.path.exists('users.db'):
        shutil.copy2('users.db', os.path.join(backup_dir, 'users.db'))
    
    # Backup CSV files
    csv_files = [
        'breeding_batches.csv', 'breeding_tasks.csv', 'breeding_log.csv',
        'ai_classifications.csv', 'pos_transactions.csv', 'pos_items.csv',
        'pupae_sales.csv', 'pupae_purchases.csv', 'farm_bookings.csv',
        'farm_reviews.csv'
    ]
    
    for filename in csv_files:
        if os.path.exists(filename):
            shutil.copy2(filename, os.path.join(backup_dir, filename))
    
    return backup_dir

def reset_database():
    """Reset all databases (WARNING: This will delete all data)"""
    
    # Remove SQLite database
    if os.path.exists('users.db'):
        os.remove('users.db')
    
    # Remove CSV files
    csv_files = [
        'breeding_batches.csv', 'breeding_tasks.csv', 'breeding_log.csv',
        'ai_classifications.csv', 'pos_transactions.csv', 'pos_items.csv',
        'pupae_sales.csv', 'pupae_purchases.csv', 'farm_bookings.csv',
        'farm_reviews.csv'
    ]
    
    for filename in csv_files:
        if os.path.exists(filename):
            os.remove(filename)
    
    # Reinitialize
    initialize_databases()

toml
[project]
name = "repl-nix-workspace"
version = "0.1.0"
description = "Add your description here"
requires-python = ">=3.11"
dependencies = [
    "folium>=0.20.0",
    "streamlit-folium>=0.25.0",
    "streamlit>=1.47.1",
    "sendgrid>=6.12.4",
]
[project]


ai_classifiction
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import os
import datetime
import tensorflow as tf
from io import BytesIO

# --- Assuming these modules exist in your project structure ---
from data.butterfly_species_info import BUTTERFLY_SPECIES_INFO, LIFESTAGES_INFO, PUPAE_DEFECTS_INFO, LARVAL_DISEASES_INFO, SPECIES_HOST_PLANTS,LARVAL_STAGES_INFO, BREEDING_DIFFICULTY
from utils.csv_handlers import save_to_csv, load_from_csv

# --- Configuration Constants ---
MODEL_DIR = './model'
IMAGE_SIZE = (180, 180)
CLASSIFICATION_CSV = 'ai_classifications.csv'

# --- Model Loading with Caching ---
# import streamlit as st
# import os

# @st.cache_resource
# def load_model_safe(MODEL_DIR, model_name):
#     import tensorflow as tf
#     try:
#         model_path = os.path.join(MODEL_DIR, model_name)
#         if not os.path.exists(model_path):
#             raise FileNotFoundError(f"Model file not found: {model_path}")
#         model = tf.keras.models.load_model(model_path)
#         return model
#     except Exception as e:
#         st.error(f"❌ Failed to load model: {e}")
#         return None

@st.cache_resource
def load_model(model_name):
    """Load a TensorFlow model and cache it to prevent re-loading."""
    model_path = os.path.join(MODEL_DIR, model_name)
    if not os.path.exists(model_path):
        st.error(f"Model not found at: {model_path}. Please ensure the model is saved there.")
        return None
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading {model_name}: {e}")
        return None
# --- CSV Handlers with Error Handling ---
def load_from_csv(filename):
    """Load a CSV file into a pandas DataFrame, skipping bad lines."""
    if os.path.exists(filename):
        try:
            return pd.read_csv(filename, on_bad_lines='skip')
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()
# --- Main Application Class ---

class ButterflyApp:
    def __init__(self):
        # st.set_page_config(page_title="AI Butterfly Classification", page_icon="🦋", layout="wide")
        self._initialize_session_state()
        self._models = self._load_all_models()
        self._class_info = self._get_class_info()
        self._check_model_directory()

    def _initialize_session_state(self):
        """Initializes session state variables for the app."""
        if 'image' not in st.session_state:
            st.session_state.image = None
        if 'analysis_type' not in st.session_state:
            st.session_state.analysis_type = "Complete Analysis (All Models)"
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = None
        if 'username' not in st.session_state:
            st.session_state.username = "Guest User"

    def _load_all_models(self):
        """Loads all AI models into a dictionary."""
        return {
            'butterfly_species_model': load_model('model_Butterfly_Species.h5'),
            'lifestages_model': load_model('model_Life_Stages.h5'),
            'larvaldiseases_model': load_model('model_Larval_Diseases.h5'),
            'pupaedefects_model': load_model('model_Pupae_Defects.h5'),
            'larvalstages_model': load_model('model_Larval_Stages.h5'),
        }

    def _get_class_info(self):
        """Returns class names and information for all models from data files."""
        return {
            'butterfly_species_info': BUTTERFLY_SPECIES_INFO,
            'butterfly_species_names': list(BUTTERFLY_SPECIES_INFO.keys()),
            'lifestages_info': LIFESTAGES_INFO,
            'lifestages_names': list(LIFESTAGES_INFO.keys()),
            'pupaedefects_info': PUPAE_DEFECTS_INFO,
            'pupaedefects_names': list(PUPAE_DEFECTS_INFO.keys()),
            'larvaldiseases_info': LARVAL_DISEASES_INFO,
            'larvaldiseases_names': list(LARVAL_DISEASES_INFO.keys()),
            'hostplants_species_names': list(SPECIES_HOST_PLANTS.keys()),
            'hostplants_species_info': SPECIES_HOST_PLANTS,
            'larval_stages_names': list(LARVAL_STAGES_INFO.keys()),
            'larval_stages_info': LARVAL_STAGES_INFO,
        }

    def _check_model_directory(self):
        """Checks if the model directory exists."""
        if not os.path.exists(MODEL_DIR):
            st.error(f"Model directory not found: {MODEL_DIR}")
            st.info("Please create the directory and place your trained models inside.")
            st.stop()  # Stop the app if models are missing

    def run(self):
        """Runs the main Streamlit application logic."""
        st.title("🤖 AI Butterfly Classification System")
        st.caption("CNN-powered analysis for species identification, lifecycle stages, and health assessment")

        self._display_main_ui()
        
        st.markdown("---")
        self._display_info_sections()

    def _display_main_ui(self):
        """Displays the main UI for image upload and analysis."""
        st.session_state.analysis_type = st.selectbox("Analysis Type", [
            "Complete Analysis (All Models)", "Species Identification", "Lifecycle Stage",
            "Larval Disease Detection", "Pupae Defect Analysis"
        ])
        
        upload_option = st.radio("Image Source", ["Upload File", "Camera Capture"])
        
        if upload_option == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload Butterfly Image", type=["jpg", "jpeg", "png"],
                help="Upload a clear image of the butterfly/larva/pupa for analysis"
            )
            if uploaded_file:
                st.session_state.image = Image.open(uploaded_file)
        else:
            camera_image = st.camera_input("Take a photo")
            if camera_image:
                st.session_state.image = Image.open(camera_image)

        if st.session_state.image:
            self._display_image_and_analysis_button()

    def _display_image_and_analysis_button(self):
        """Displays the uploaded image and the 'Analyze' button."""
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(st.session_state.image, caption="Uploaded Image", use_container_width=True)
        
        with col2:
            st.write("**Image Information:**")
            st.write(f"Size: {st.session_state.image.size}")
            st.write(f"Mode: {st.session_state.image.mode}")
            
            if st.button("🔍 Analyze Image", type="primary"):
                self._handle_analysis()

        if st.session_state.analysis_results:
            self._display_results(st.session_state.analysis_results)

    def _handle_analysis(self):
        """Performs the classification and updates session state."""
        with st.spinner("Processing image with AI models..."):
            results = self._perform_classification()
            st.session_state.analysis_results = results
            
            if "error" not in results:
                self._save_analysis_results(results)

    def _perform_classification(self):
        """Performs AI classification based on the selected type using loaded models."""
        results = {}
        try:
            # Convert PIL image to file-like object for classification
            img_buffer = BytesIO()
            st.session_state.image.save(img_buffer, format='PNG')
            
            analysis_type = st.session_state.analysis_type
            
            if analysis_type in ["Complete Analysis (All Models)", "Species Identification"]:
                img_buffer.seek(0)
                species_result = self._classify_image(
                    img_buffer, self._models['butterfly_species_model'], 
                    self._class_info['butterfly_species_names'], self._class_info['butterfly_species_info']

                )
                if species_result:
                    results["species"] = {
                        "predicted_class": species_result['class_name'],
                        "confidence": species_result['score'] / 100,
                        "top_3": [{"class": pred['class_name'], "confidence": pred['score'] / 100} for pred in species_result['top_predictions']],
                        "details": species_result, 

                    }
            
            if analysis_type in ["Complete Analysis (All Models)", "Lifecycle Stage"]:
                img_buffer.seek(0)
                stage_result = self._classify_image(
                    img_buffer, self._models['lifestages_model'], 
                    self._class_info['lifestages_names'], self._class_info['lifestages_info']
                )
                if stage_result:
                    results["lifecycle"] = {
                        "predicted_class": stage_result['class_name'],
                        "confidence": stage_result['score'] / 100,
                        "description": stage_result.get('stages_info', 'No description available'),
                        "details": stage_result
                    }
            
            if analysis_type in ["Complete Analysis (All Models)", "Larval Disease Detection"]:
                img_buffer.seek(0)
                disease_result = self._classify_image(
                    img_buffer, self._models['larvaldiseases_model'], 
                    self._class_info['larvaldiseases_names'], self._class_info['larvaldiseases_info']
                )
                if disease_result:
                    results["diseases"] = {
                        "predicted_class": disease_result['class_name'],
                        "confidence": disease_result['score'] / 100,
                        "treatment": disease_result.get('treatment_info', 'No treatment information available'),
                        "details": disease_result
                    }
            
            if analysis_type in ["Complete Analysis (All Models)", "Pupae Defect Analysis"]:
                img_buffer.seek(0)
                defect_result = self._classify_image(
                    img_buffer, self._models['pupaedefects_model'], 
                    self._class_info['pupaedefects_names'], self._class_info['pupaedefects_info']
                )
                if defect_result:
                    results["defects"] = {
                        "predicted_class": defect_result['class_name'],
                        "confidence": defect_result['score'] / 100,
                        "quality_info": defect_result.get('quality_info', 'No quality information available'),
                        "details": defect_result
                    }
            if analysis_type in ["Complete Analysis (All Models)", "Larval Stages"]:
                img_buffer.seek(0)
                larval_stage = self._classify_image(
                    img_buffer, self._models['larvalstages_model'], 
                    self._class_info['larvalstages_names'], self._class_info['larvalstages_info']
                )
                if larval_stage:
                    results["larval_stage"] = {
                        "predicted_class": larval_stage['class_name'],
                        "confidence": larval_stage['score'] / 100,
                        "details": larval_stage
                    }
                       
        except Exception as e:
            st.error(f"Classification error: {str(e)}")
            results["error"] = str(e)
        
        return results

    def _classify_image(self, image_file, model, class_names, details_dict=None):
        """Classify image using a specific TensorFlow model."""
        if model is None:
            return None

        try:
            image = Image.open(image_file)
            img_resized = image.resize(IMAGE_SIZE)
            img_array = tf.keras.utils.img_to_array(img_resized)
            img_array = tf.expand_dims(img_array, 0)

            predictions = model.predict(img_array)
            result = tf.nn.softmax(predictions[0])
            
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
                    "top_predictions": top_predictions,
                    "model_details": details_dict,
                }
                if details_dict and predicted_class_name in details_dict:
                    result_data.update(details_dict[predicted_class_name])
                return result_data
            else:
                return {"class_name": "Unknown Class", "score": 0.0, "index": predicted_class_index, "top_predictions": []}
        except Exception as e:
            st.error(f"Error during image classification: {e}")
            return None

    def _display_results(self, results):
        """Displays all classification results in the main UI."""
        st.subheader("🔬 Analysis Results")
        if "error" in results:
            st.error(f"Analysis failed: {results['error']}")
            return
        
        if "species" in results:
            self._display_species_results(results["species"])
        
        if "lifecycle" in results:
            self._display_lifecycle_results(results["lifecycle"])
        
        if "diseases" in results:
            self._display_disease_results(results["diseases"])
        
        if "defects" in results:
            self._display_defect_results(results["defects"])

    def _display_species_results(self, species_result):
        st.markdown("---")
        st.write("### 🦋 Species Identification")
        col1, col2 = st.columns(2)
        with col1:
            
            st.success(f"**Predicted Species:** {species_result['predicted_class']}")
            st.write(f"**Confidence:** {species_result['confidence']:.1%}")
            details = species_result.get('details', {})
            st.write(f"**Scientific Name:** {details.get('scientific_name', 'Unknown')}")
            st.write(f"**Family:** {details.get('family', 'Unknown')}")
            st.write(f"**Discovered By:** {details.get('discovered', 'Unknown')} ({details.get('year', 'N/A')})")
            st.write(f"**Habitat:** {details.get('habitat', 'Unknown')}")
            st.write(f"**Description:** {details.get('description', 'Unknown')}")
            plants = details.get('plant')
            if plants:
                if isinstance(plants, list):
                    st.write("**Host Plants:**")
                    for plant in plants:
                        st.write(f"- {plant}")
                else:
                    st.write(f"**Host Plants:** {plants}")
            else:
                st.write("**Host Plants:** Unknown")
            st.write(f"**Host Plants:** {details.get('plant', 'Unknown')}")
            #st.write(f"**Daily Consumption:** {details.get('dailyConsumption', 0)}g")
            #st.write(f"**Estimated Value:** ₱{details.get('value', 0.0):.2f}")

        with col2:
            st.write("**Top 3 Predictions:**")
            for i, pred in enumerate(species_result['top_3'], 1):
                st.write(f"{i}. {pred['class']} ({pred['confidence']:.1%})")
            st.write("**Top 3 Predictions:**")
            top3 = species_result['top_3']
            # Prepare data for the chart
            chart_data = pd.DataFrame({
                "Species": [pred['class'] for pred in top3],
                "Confidence": [pred['confidence']*100 for pred in top3]  # Convert to percentage
            })
            st.bar_chart(chart_data.set_index("Species"))

            # Optionally, still show the text list
            for i, pred in enumerate(top3, 1):
                st.write(f"{i}. {pred['class']} ({pred['confidence']:.1%})")
            health_score, quality_grade = self._calculate_health_score_and_grade(species_result, "Butterfly Species")
            st.write(f"**Quality Grade:** {quality_grade}")
            
            recommendations = self._get_recommended_actions(species_result, "Butterfly Species")
            if recommendations:
                st.write("**Recommendations:**")
                for rec in recommendations:
                    st.write(f"• {rec}")

    def _display_lifecycle_results(self, lifecycle_result):
        st.markdown("---")
        st.write("### 🔄 Lifecycle Stage")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Stage:** {lifecycle_result['predicted_class']} ({lifecycle_result['confidence']:.1%})")
            st.write(f"**Description:** {lifecycle_result['description']}")
            st.write(f"**Duration:** {lifecycle_result.get('duration', 'N/A')} days")
        with col2:
            recommendations = self._get_recommended_actions(lifecycle_result, "Life Stages")
            if recommendations:
                st.write("**Care Recommendations:**")
                for rec in recommendations:
                    st.write(f"• {rec}")

    def _display_disease_results(self, disease_result):
        st.markdown("---")
        st.write("### 🏥 Disease Detection")
        col1, col2 = st.columns(2)
        with col1:
            if disease_result['predicted_class'] == "Healthy":
                st.success(f"✅ {disease_result['predicted_class']} ({disease_result['confidence']:.1%})")
            else:
                st.warning(f"⚠️ {disease_result['predicted_class']} detected ({disease_result['confidence']:.1%})")
            st.write(f"**Treatment Information:** {disease_result.get('treatment', 'N/A')}")
            st.write(f"**Symptoms:** {disease_result.get('symptoms', 'N/A')}")
            st.write(f"**Spread Method:** {disease_result.get('spread', 'N/A')}")
            st.write(f"**Prevention:** {disease_result.get('prevention', 'N/A')}")
            st.write(f"**Prevention:** {disease_result.get('prevention', 'N/A')}")
            st.write(f"**Mortality Rate:** {disease_result.get('mortality_rate', 0.0):.1%}")
            st.write(f"**Contagious:** {'Yes' if disease_result.get('contagious', False) else 'No'}")
        
        with col2:
            health_score, quality_grade = self._calculate_health_score_and_grade(disease_result, "Larval Diseases")
            st.metric("Health Score", f"{health_score:.1f}%")
            st.write(f"**Quality Grade:** {quality_grade}")
            
            recommendations = self._get_recommended_actions(disease_result, "Larval Diseases")
            if recommendations:
                st.write("**Recommendations:**")
                for rec in recommendations:
                    st.write(f"• {rec}")

    def _display_defect_results(self, defect_result):
        st.markdown("---")
        st.write("### 🔍 Quality Assessment")
        col1, col2 = st.columns(2)
        with col1:
            if defect_result['predicted_class'] == "Healthy Pupae":
                st.success(f"✅ {defect_result['predicted_class']} ({defect_result['confidence']:.1%})")
            else:
                st.warning(f"⚠️ {defect_result['predicted_class']} detected ({defect_result['confidence']:.1%})")
            st.write(f"**Quality Information:** {defect_result['quality_info']}")
        
        with col2:
            health_score, quality_grade = self._calculate_health_score_and_grade(defect_result, "Pupae Defects")
            st.metric("Health Score", f"{health_score:.1f}%")
            st.write(f"**Quality Grade:** {quality_grade}")
            
            recommendations = self._get_recommended_actions(defect_result, "Pupae Defects")
            if recommendations:
                st.write("**Recommendations:**")
                for rec in recommendations:
                    st.write(f"• {rec}")

    def _calculate_health_score_and_grade(self, classification_result, classifier_type):
        """Calculate health score and quality grade based on classification results."""
        health_score = 100.0
        quality_grade = "A+"
        
        details = classification_result.get('details', {})
        impact_score = details.get('impact_score')
        
        if impact_score is not None:
            health_score = (1 - impact_score) * 100
        
        if health_score >= 85: quality_grade = "A+"
        elif health_score >= 70: quality_grade = "B"
        elif health_score >= 50: quality_grade = "C"
        else: quality_grade = "D"

        if classification_result['predicted_class'] == "Healthy" or classification_result['predicted_class'] == "Healthy Pupae":
             health_score = 100.0
             quality_grade = "A+"
             
        return health_score, quality_grade

    def _get_recommended_actions(self, classification_result, classifier_type):
        """Get recommended actions based on the classification results."""
        recommendations = []
        class_name = classification_result['predicted_class']
        
        # Recommendations for Larval Diseases
        if classifier_type == "Larval Diseases":
            rec_info = LARVAL_DISEASES_INFO.get(class_name, {})
            if rec_info:
                recommendations.append(rec_info.get('treatment_info'))
            
        # Recommendations for Pupae Defects
        elif classifier_type == "Pupae Defects":
            rec_info = PUPAE_DEFECTS_INFO.get(class_name, {})
            if rec_info:
                recommendations.append(rec_info.get('quality_info'))

        # Recommendations for Species & Lifecycle
        else:
            if class_name in BUTTERFLY_SPECIES_INFO:
                details = BUTTERFLY_SPECIES_INFO.get(class_name)
                if details and details.get('plant'):
                    plants = ", ".join(details['plant']) if isinstance(details['plant'], list) else details['plant']
                    recommendations.append(f"Ensure a steady supply of host plants like **{plants}**.")
            
            if class_name in LIFESTAGES_INFO:
                details = LIFESTAGES_INFO.get(class_name)
                if details:
                    recommendations.append(details.get('stages_info'))
        
        # Add general recommendations
        recommendations.append("Maintain optimal temperature and humidity. Ensure proper ventilation and avoid overcrowding.")
        
        return [rec for rec in recommendations if rec]

    def _save_analysis_results(self, results):
        """Save classification results to CSV."""
        analysis_data = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_type': st.session_state.analysis_type,
            'user': st.session_state.username,
            'predicted_species': results.get("species", {}).get("predicted_class", ""),
            'species_confidence': results.get("species", {}).get("confidence", ""),
            'predicted_stage': results.get("lifecycle", {}).get("predicted_class", ""),
            'stage_confidence': results.get("lifecycle", {}).get("confidence", ""),
            'predicted_disease': results.get("diseases", {}).get("predicted_class", ""),
            'disease_confidence': results.get("diseases", {}).get("confidence", ""),
            'predicted_defect': results.get("defects", {}).get("predicted_class", ""),
            'defect_confidence': results.get("defects", {}).get("confidence", ""),
            'predicted_larval_stage': results.get("larval_stage", {}).get("predicted_class", ""),
            'larval_stage_confidence': results.get("larval_stage", {}).get("confidence", ""),
         }
        
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
        if "larval_stage" in results:
            analysis_data.update({
                'predicted_larval_stage': results["larval_stage"]["predicted_class"],
                'larval_stage_confidence': results["larval_stage"]["confidence"],
                
            })
        # Append to CSV
        save_to_csv(CLASSIFICATION_CSV, analysis_data)
        df = pd.DataFrame([analysis_data])
        df.to_csv(CLASSIFICATION_CSV, index=False)
        
    def _display_info_sections(self):
        """Displays sections for model information and recent classifications."""
        self._display_model_info()
        st.markdown("---")
        self._display_recent_classifications()

    def _display_model_info(self):
        """Display model information and status."""
        st.subheader("🤖 Model Information")
        models = [
            "model_Butterfly_Species.h5", "model_Life_Stages.h5", 
            "model_Larval_Diseases.h5", "model_Pupae_Defects.h5",
            "model_Larval_Stages.h5"
        ]
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Available Models:**")
            for model_name in models:
                model_path = os.path.join(MODEL_DIR, model_name)
                if os.path.exists(model_path):
                    st.success(f"✅ {model_name}")
                else:
                    st.error(f"❌ {model_name} (Missing)")
        
        with col2:
            st.write("**Model Capabilities:**")
            st.write("🦋 **Species:** 18 butterfly/moth species")
            st.write("🔄 **Stages:** 4 lifecycle stages")
            st.write("🏥 **Diseases:** 4 larval disease types")
            st.write("🔍 **Defects:** 6 pupae defect types")
            st.write("🐛 **Larval Stages:** 14 larval stages")

    def _display_recent_classifications(self):
        """Display recent classification results from the CSV file."""
        st.subheader("📊 Recent Classifications")
        classifications_df = load_from_csv(CLASSIFICATION_CSV)

        if not classifications_df.empty:
            recent_classifications = classifications_df.tail(10).sort_values('timestamp', ascending=False)
            st.dataframe(recent_classifications, use_container_width=True)

            st.write("**Classification Statistics:**")
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            with col1:
                st.metric("Total Classifications", len(classifications_df))
            with col2:
                # Count non-empty species classifications
                species_count = classifications_df['predicted_species'].notna().sum()
                st.metric("Species Identified", species_count)
            with col3:
                # Count non-empty life stage classifications
                stage_count = classifications_df['predicted_stage'].notna().sum()
                st.metric("Life Stages Classified", stage_count)
            with col4:
                # Count non-empty larval disease classifications
                disease_count = classifications_df['predicted_disease'].notna().sum()
                st.metric("Larval Diseases Classified", disease_count)
            with col5:
                # Count non-empty pupae defect classifications
                defect_count = classifications_df['predicted_defect'].notna().sum()
                st.metric("Pupae Defects Classified", defect_count)
            with col6:
                today = datetime.date.today().strftime('%Y-%m-%d')
                today_classifications = len(classifications_df[classifications_df['timestamp'].astype(str).str.startswith(today)])
                st.metric("Today's Classifications", today_classifications)
        else:
            st.info("No classifications performed yet. Upload an image to get started!")
        


def ai_classification_app():
    app = ButterflyApp()
    app.run()
 
# if __name__ == '__main__':
#     app = ButterflyApp()
#     app.run()