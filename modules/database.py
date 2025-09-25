import os
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import hashlib
import uuid
from datetime import datetime

# --- Database Connection ---
def database_app():
    """Database management and operations for the butterfly breeding application."""
    pass
def get_db_connection():
    """Get PostgreSQL database connection using environment variables."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("PGHOST", "localhost"),
            database=os.getenv("PGDATABASE", "butterfly_db"),
            user=os.getenv("PGUSER", "postgres"),
            password=os.getenv("PGPASSWORD", ""),
            port=os.getenv("PGPORT", "5432")
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# --- Utility Functions ---

def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

# --- Initialization ---

def init_database():
    """Initialize database tables and create admin user if needed."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        # Users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(64) NOT NULL,
                role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'breeder', 'faculty', 'student', 'enthusiast', 'other')),
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        # Batches table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS batches (
                id SERIAL PRIMARY KEY,
                batch_id TEXT UNIQUE NOT NULL,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                species VARCHAR(100) NOT NULL,
                stage VARCHAR(20) NOT NULL CHECK (stage IN ('egg', 'larva', 'pupa', 'adult')),
                initial_count INTEGER NOT NULL,
                current_count INTEGER,
                survival_rate DECIMAL(5,2) DEFAULT 95.0,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'failed')),
                host_plant_cost DECIMAL(10,2) DEFAULT 2.0,
                labor_cost DECIMAL(10,2) DEFAULT 5.0,
                market_price DECIMAL(10,2) DEFAULT 15.0,
                lifecycle_days INTEGER DEFAULT 30,
                notes TEXT
            )
        """)
        # Classifications table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS classifications (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                image_path VARCHAR(255) NOT NULL,
                model_type VARCHAR(50) NOT NULL,
                prediction VARCHAR(100) NOT NULL,
                confidence DECIMAL(5,4) NOT NULL,
                classification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Create admin user if not exists
        cur.execute("SELECT COUNT(*) FROM users WHERE email = 'admin@butterfly.com'")
        result = cur.fetchone()
        if result and result[0] == 0:
            admin_password = hash_password("admin123")
            cur.execute("""
                INSERT INTO users (username, email, password_hash, role)
                VALUES ('admin', 'admin@butterfly.com', %s, 'admin')
            """, (admin_password,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

# --- User Management ---

def create_user(username, email, password, role):
    """Create a new user."""
    conn = get_db_connection()
    if not conn:
        raise Exception("Database connection failed")
    try:
        cur = conn.cursor()
        password_hash = hash_password(password)
        cur.execute("""
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (username, email, password_hash, role))
        result = cur.fetchone()
        user_id = result[0] if result else None
        conn.commit()
        cur.close()
        conn.close()
        return user_id
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        raise Exception(f"Error creating user: {e}")

def get_user_by_email(email):
    """Get user by email."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s AND is_active = TRUE", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return dict(user) if user else None
    except Exception as e:
        print(f"Error getting user: {e}")
        if conn:
            conn.close()
        return None

def update_user_last_login(user_id):
    """Update user's last login timestamp."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE users SET last_login = CURRENT_TIMESTAMP 
            WHERE id = %s
        """, (user_id,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating last login: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

# --- Classification Management ---

def save_classification(user_id, image_path, model_type, prediction, confidence):
    """Save classification result to database."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO classifications (user_id, image_path, model_type, prediction, confidence)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, image_path, model_type, prediction, confidence))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving classification: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

# --- Batch Management ---

def create_batch_record(user_id, species, stage, initial_count, survival_rate, **kwargs):
    """Create a new batch record."""
    conn = get_db_connection()
    if not conn:
        raise Exception("Database connection failed")
    try:
        cur = conn.cursor()
        batch_id = str(uuid.uuid4())
        cur.execute("""
            INSERT INTO batches (batch_id, user_id, species, stage, initial_count, 
                               current_count, survival_rate, host_plant_cost, 
                               labor_cost, market_price, lifecycle_days)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING batch_id
        """, (
            batch_id, user_id, species, stage, initial_count, 
            initial_count, survival_rate,
            kwargs.get('host_plant_cost', 2.0),
            kwargs.get('labor_cost', 5.0), 
            kwargs.get('market_price', 15.0),
            kwargs.get('lifecycle_days', 30)
        ))
        result = cur.fetchone()
        returned_batch_id = result[0] if result else batch_id
        conn.commit()
        cur.close()
        conn.close()
        return str(returned_batch_id)
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        raise Exception(f"Error creating batch: {e}")

def get_user_batches_from_db(user_id):
    """Get all batches for a user."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT * FROM batches 
            WHERE user_id = %s 
            ORDER BY created_date DESC
        """, (user_id,))
        batches = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(batch) for batch in batches]
    except Exception as e:
        print(f"Error getting batches: {e}")
        if conn:
            conn.close()
        return []

# --- CSV and Backup Utilities ---

def initialize_csv_files():
    """Initialize all required CSV files with proper headers."""
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

def backup_data():
    """Create backup of all data."""
    import shutil
    import datetime
    backup_dir = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
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
    """Reset all CSV files (WARNING: This will delete all data)."""
    csv_files = [
        'breeding_batches.csv', 'breeding_tasks.csv', 'breeding_log.csv',
        'ai_classifications.csv', 'pos_transactions.csv', 'pos_items.csv',
        'pupae_sales.csv', 'pupae_purchases.csv', 'farm_bookings.csv',
        'farm_reviews.csv'
    ]
    for filename in csv_files:
        if os.path.exists(filename):
            os.remove(filename)
    initialize_csv_files()
setup_databases = init_database