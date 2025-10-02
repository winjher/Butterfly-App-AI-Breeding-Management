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