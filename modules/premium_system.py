import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import csv
import os

DATABASE_FILE = 'users.db'
PREMIUM_FILE = 'premium_subscriptions.csv'
COMMISSION_FILE = 'commissions.csv'
EWALLET_FILE = 'ewallet_transactions.csv'

def initialize_premium_db():
    """Initialize premium system database tables"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Check if columns exist before adding them
    cursor.execute("PRAGMA table_info(users)")
    existing_columns = [column[1] for column in cursor.fetchall()]
    
    # Add premium-related columns to users table if they don't exist
    columns_to_add = [
        ('is_premium', 'BOOLEAN DEFAULT 0'),
        ('premium_start_date', 'DATE'),
        ('premium_end_date', 'DATE'),
        ('total_earnings', 'DECIMAL DEFAULT 0'),
        ('commission_level', 'INTEGER DEFAULT 1'),
        ('ewallet_balance', 'DECIMAL DEFAULT 0'),
        ('signup_bonus_claimed', 'BOOLEAN DEFAULT 0')
    ]
    
    for column_name, column_def in columns_to_add:
        if column_name not in existing_columns:
            try:
                cursor.execute(f'ALTER TABLE users ADD COLUMN {column_name} {column_def}')
                print(f"Added column: {column_name}")
            except sqlite3.OperationalError as e:
                print(f"Error adding column {column_name}: {e}")
    
    conn.commit()
    conn.close()
    
    # Initialize CSV files
    init_premium_csv()
    init_commission_csv()
    init_ewallet_csv()

def init_premium_csv():
    """Initialize premium subscriptions CSV"""
    if not os.path.exists(PREMIUM_FILE):
        with open(PREMIUM_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'username', 'subscription_type', 'start_date', 'end_date', 
                           'monthly_fee', 'payment_status', 'created_at'])

def init_commission_csv():
    """Initialize commissions CSV"""
    if not os.path.exists(COMMISSION_FILE):
        with open(COMMISSION_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'username', 'commission_amount', 'source', 'level', 
                           'earnings_milestone', 'date_earned', 'status'])

def init_ewallet_csv():
    """Initialize ewallet transactions CSV"""
    if not os.path.exists(EWALLET_FILE):
        with open(EWALLET_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'username', 'transaction_type', 'amount', 'description', 
                           'balance_before', 'balance_after', 'timestamp'])

def get_user_premium_status(user_id):
    """Get user's premium status and details"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT is_premium, premium_start_date, premium_end_date, total_earnings, 
               commission_level, ewallet_balance, signup_bonus_claimed
        FROM users WHERE id = ?
    ''', (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'is_premium': bool(result[0]),
            'premium_start_date': result[1],
            'premium_end_date': result[2],
            'total_earnings': float(result[3] or 0),
            'commission_level': int(result[4] or 1),
            'ewallet_balance': float(result[5] or 0),
            'signup_bonus_claimed': bool(result[6])
        }
    return None

def claim_signup_bonus(user_id, username):
    """Claim 200 pesos signup bonus"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Check if bonus already claimed
    status = get_user_premium_status(user_id)
    if status and status['signup_bonus_claimed']:
        return False, "Signup bonus already claimed"
    
    try:
        # Update user balance and mark bonus as claimed
        cursor.execute('''
            UPDATE users SET ewallet_balance = ewallet_balance + 200, signup_bonus_claimed = 1
            WHERE id = ?
        ''', (user_id,))
        
        # Record transaction
        add_ewallet_transaction(user_id, username, 'bonus', 200, 'Signup bonus - Free 200 pesos')
        
        conn.commit()
        conn.close()
        return True, "200 pesos signup bonus added to your ewallet!"
    except Exception as e:
        conn.close()
        return False, f"Error claiming bonus: {str(e)}"

def subscribe_premium(user_id, username, subscription_type="monthly"):
    """Subscribe to premium membership"""
    monthly_fee = 299  # Monthly premium fee in pesos
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=30)
    
    try:
        # Update user premium status
        cursor.execute('''
            UPDATE users SET is_premium = 1, premium_start_date = ?, premium_end_date = ?
            WHERE id = ?
        ''', (start_date, end_date, user_id))
        
        # Record premium subscription
        with open(PREMIUM_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, username, subscription_type, start_date, end_date, 
                           monthly_fee, 'active', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        return False

def add_earnings(user_id, username, amount, source="sales"):
    """Add earnings and check for level 2 qualification"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    try:
        # Update total earnings
        cursor.execute('''
            UPDATE users SET total_earnings = total_earnings + ?
            WHERE id = ?
        ''', (amount, user_id))
        
        # Get updated earnings
        cursor.execute('SELECT total_earnings, commission_level FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        
        if result:
            total_earnings = result[0]
            current_level = result[1]
            
            # Check for level 2 qualification (260k earnings)
            if total_earnings >= 260000 and current_level < 2:
                # Upgrade to level 2
                cursor.execute('UPDATE users SET commission_level = 2 WHERE id = ?', (user_id,))
                
                # Award 20k pesos commission prize
                cursor.execute('UPDATE users SET ewallet_balance = ewallet_balance + 20000 WHERE id = ?', (user_id,))
                
                # Record commission
                with open(COMMISSION_FILE, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([user_id, username, 20000, 'level_upgrade', 2, 260000,
                                   datetime.now().strftime('%Y-%m-%d'), 'approved'])
                
                # Record ewallet transaction
                add_ewallet_transaction(user_id, username, 'commission', 20000, 
                                      'Level 2 Achievement Prize - 20,000 pesos')
                
                conn.commit()
                conn.close()
                return True, "Congratulations! You've reached Level 2 and earned 20,000 pesos!"
        
        conn.commit()
        conn.close()
        return True, f"Earnings updated: +{amount} pesos"
    except Exception as e:
        conn.close()
        return False, f"Error updating earnings: {str(e)}"

def add_ewallet_transaction(user_id, username, transaction_type, amount, description):
    """Add ewallet transaction record"""
    status = get_user_premium_status(user_id)
    balance_before = status['ewallet_balance'] if status else 0
    balance_after = balance_before + amount if transaction_type in ['bonus', 'commission', 'deposit'] else balance_before - amount
    
    with open(EWALLET_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, username, transaction_type, amount, description,
                       balance_before, balance_after, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

def use_ewallet_for_purchase(user_id, username, amount, description="Pupae purchase"):
    """Use ewallet balance for purchases"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    status = get_user_premium_status(user_id)
    if not status or status['ewallet_balance'] < amount:
        return False, "Insufficient ewallet balance"
    
    try:
        # Deduct from ewallet
        cursor.execute('UPDATE users SET ewallet_balance = ewallet_balance - ? WHERE id = ?', 
                      (amount, user_id))
        
        # Record transaction
        add_ewallet_transaction(user_id, username, 'purchase', amount, description)
        
        conn.commit()
        conn.close()
        return True, f"Purchase successful: -{amount} pesos from ewallet"
    except Exception as e:
        conn.close()
        return False, f"Error processing purchase: {str(e)}"

def get_breeder_emails():
    """Get all breeder email addresses for notifications"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT email, username FROM users 
        WHERE role = 'breeder' AND email IS NOT NULL AND email != ''
    ''')
    
    breeders = cursor.fetchall()
    conn.close()
    
    return [(email, username) for email, username in breeders if email]

def premium_system_app():
    """Premium system management interface"""
    initialize_premium_db()
    
    st.title("💎 Premium Membership System")
    
    if 'user_id' not in st.session_state:
        st.error("Please log in to access premium features.")
        return
    
    user_id = st.session_state.user_id
    username = st.session_state.username
    status = get_user_premium_status(user_id)
    
    if not status:
        st.error("Unable to load user status.")
        return
    
    # Signup bonus section
    if not status['signup_bonus_claimed']:
        st.success("🎁 Welcome Bonus Available!")
        st.info("Claim your FREE 200 pesos GCash bonus to start buying pupae!")
        
        if st.button("Claim 200 Pesos Bonus"):
            success, message = claim_signup_bonus(user_id, username)
            if success:
                st.success(message)
                st.balloons()
                st.rerun()
            else:
                st.error(message)
    
    # Display current status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        premium_status = "Premium" if status['is_premium'] else "Free"
        st.metric("Membership", premium_status)
    
    with col2:
        st.metric("Commission Level", f"Level {status['commission_level']}")
    
    with col3:
        st.metric("Total Earnings", f"₱{status['total_earnings']:,.2f}")
    
    with col4:
        st.metric("Ewallet Balance", f"₱{status['ewallet_balance']:,.2f}")
    
    # Level progress
    if status['commission_level'] < 2:
        progress = min(status['total_earnings'] / 260000, 1.0)
        remaining = 260000 - status['total_earnings']
        
        st.subheader("🎯 Level 2 Progress")
        st.progress(progress)
        st.write(f"Progress: ₱{status['total_earnings']:,.2f} / ₱260,000")
        
        if remaining > 0:
            st.info(f"Earn ₱{remaining:,.2f} more to reach Level 2 and get 20,000 pesos prize!")
        else:
            st.success("Congratulations! You've qualified for Level 2!")
    
    # Premium subscription
    if not status['is_premium']:
        st.subheader("🚀 Upgrade to Premium")
        st.write("**Premium Benefits:**")
        st.write("- Higher commission rates")
        st.write("- Priority support")
        st.write("- Advanced analytics")
        st.write("- Exclusive breeder features")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("Monthly Premium: ₱299/month")
        
        with col2:
            if st.button("Subscribe to Premium"):
                if subscribe_premium(user_id, username):
                    st.success("Premium subscription activated!")
                    st.rerun()
                else:
                    st.error("Failed to activate premium subscription")
    else:
        st.success(f"Premium Active until: {status['premium_end_date']}")
    
    # Ewallet transactions
    st.subheader("💰 Ewallet Transactions")
    
    if os.path.exists(EWALLET_FILE):
        df = pd.read_csv(EWALLET_FILE)
        user_transactions = df[df['user_id'] == user_id].sort_values(by='timestamp', ascending=False)
        
        if not user_transactions.empty:
            st.dataframe(user_transactions[['transaction_type', 'amount', 'description', 'balance_after', 'timestamp']], use_container_width=True)
        else:
            st.info("No transactions yet")
    
    # Commission history
    st.subheader("🏆 Commission History")
    
    if os.path.exists(COMMISSION_FILE):
        df = pd.read_csv(COMMISSION_FILE)
        user_commissions = df[df['user_id'] == user_id].sort_values(by='date_earned', ascending=False)
        
        if not user_commissions.empty:
            st.dataframe(user_commissions[['commission_amount', 'source', 'level', 'earnings_milestone', 'date_earned', 'status']], use_container_width=True)
        else:
            st.info("No commissions earned yet")

def admin_premium_management():
    """Admin interface for premium system management"""
    st.title("🔧 Premium System Admin")
    
    if st.session_state.get('user_role') != 'admin':
        st.error("Admin access required")
        return
    
    tabs = st.tabs(["📊 Overview", "📧 Email Notifications", "💰 Commissions"])
    
    with tabs[0]:
        st.subheader("System Overview")
        
        # Premium users count
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_premium = 1')
        premium_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE commission_level = 2')
        level2_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(ewallet_balance) FROM users')
        total_ewallet = cursor.fetchone()[0] or 0
        
        conn.close()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Premium Users", premium_count)
        with col2:
            st.metric("Level 2 Breeders", level2_count)
        with col3:
            st.metric("Total Ewallet Balance", f"₱{total_ewallet:,.2f}")
    
    with tabs[1]:
        st.subheader("Email Notifications to Breeders")
        
        breeders = get_breeder_emails()
        st.write(f"Found {len(breeders)} breeders with email addresses")
        
        if breeders:
            for email, username in breeders:
                st.write(f"- {username}: {email}")
            
            st.info("📧 Email notification feature requires SendGrid API key configuration")
            
            if st.button("Send Premium Promotion Emails"):
                st.success(f"Would send premium promotion emails to {len(breeders)} breeders")
    
    with tabs[2]:
        st.subheader("Commission Management")
        
        if os.path.exists(COMMISSION_FILE):
            df = pd.read_csv(COMMISSION_FILE)
            st.dataframe(df)
        else:
            st.info("No commission data available")

if __name__ == "__main__":
    premium_system_app()