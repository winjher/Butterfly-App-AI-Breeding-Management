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
