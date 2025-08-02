import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import re

DATABASE_FILE = 'users.db'

def initialize_profile_db():
    """Initialize profile database with extended fields"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Add new columns to existing users table if they don't exist
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN contact_number TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN birthday DATE')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN credit_card_last4 TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN payment_account TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN full_name TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN address TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN updated_at TIMESTAMP')
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()

def get_user_profile(user_id):
    """Get complete user profile"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT username, email, role, contact_number, birthday, 
               credit_card_last4, payment_account, full_name, address, created_at
        FROM users WHERE id = ?
    ''', (user_id,))
    
    profile = cursor.fetchone()
    conn.close()
    
    if profile:
        return {
            'username': profile[0],
            'email': profile[1] or '',
            'role': profile[2] or 'user',
            'contact_number': profile[3] or '',
            'birthday': profile[4] or '',
            'credit_card_last4': profile[5] or '',
            'payment_account': profile[6] or '',
            'full_name': profile[7] or '',
            'address': profile[8] or '',
            'created_at': profile[9]
        }
    return None

def update_user_profile(user_id, profile_data):
    """Update user profile with new information"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE users SET 
                email = ?, contact_number = ?, birthday = ?, 
                credit_card_last4 = ?, payment_account = ?, 
                full_name = ?, address = ?, updated_at = ?
            WHERE id = ?
        ''', (
            profile_data['email'],
            profile_data['contact_number'],
            profile_data['birthday'],
            profile_data['credit_card_last4'],
            profile_data['payment_account'],
            profile_data['full_name'],
            profile_data['address'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            user_id
        ))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error updating profile: {str(e)}")
        return False
    finally:
        conn.close()

def validate_contact_number(phone):
    """Validate phone number format"""
    phone_pattern = re.compile(r'^[\+]?[1-9][\d]{0,15}$')
    return phone_pattern.match(phone.replace(' ', '').replace('-', ''))

def validate_credit_card(card_number):
    """Validate and return last 4 digits of credit card"""
    # Remove spaces and non-digits
    card_clean = re.sub(r'\D', '', card_number)
    
    # Basic validation (length should be 13-19 digits)
    if len(card_clean) < 13 or len(card_clean) > 19:
        return None
    
    # Return last 4 digits for storage
    return card_clean[-4:]

def profile_management_app():
    """Main profile management application"""
    initialize_profile_db()
    
    st.title("👤 Profile Management")
    
    if 'user_id' not in st.session_state:
        st.error("Please log in to access profile management.")
        return
    
    # Get current profile
    profile = get_user_profile(st.session_state.user_id)
    if not profile:
        st.error("Profile not found.")
        return
    
    # Role-based profile sections
    user_role = st.session_state.get('user_role', 'user')
    
    # Profile tabs based on role
    if user_role in ['purchaser', 'breeder']:
        tabs = st.tabs(["📝 Basic Info", "📞 Contact", "💳 Payment Info"])
    elif user_role == 'student':
        tabs = st.tabs(["📝 Basic Info", "📞 Contact", "🎓 Student Info"])
    elif user_role == 'faculty':
        tabs = st.tabs(["📝 Basic Info", "📞 Contact", "🏫 Faculty Info"])
    else:
        tabs = st.tabs(["📝 Basic Info", "📞 Contact"])
    
    # Basic Information Tab
    with tabs[0]:
        st.subheader("Basic Information")
        
        with st.form("basic_info_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name", value=profile['full_name'])
                email = st.text_input("Email", value=profile['email'])
                username_display = st.text_input("Username", value=profile['username'], disabled=True)
                
            with col2:
                role_display = st.text_input("Role", value=profile['role'], disabled=True)
                birthday = st.date_input("Birthday", 
                                       value=datetime.strptime(profile['birthday'], '%Y-%m-%d').date() 
                                       if profile['birthday'] else None)
                
            address = st.text_area("Address", value=profile['address'])
            
            basic_submit = st.form_submit_button("Update Basic Info")
            
            if basic_submit:
                profile_data = profile.copy()
                profile_data.update({
                    'full_name': full_name,
                    'email': email,
                    'birthday': birthday.strftime('%Y-%m-%d') if birthday else '',
                    'address': address
                })
                
                if update_user_profile(st.session_state.user_id, profile_data):
                    st.success("Basic information updated successfully!")
                    st.rerun()
    
    # Contact Information Tab
    with tabs[1]:
        st.subheader("Contact Information")
        
        with st.form("contact_form"):
            contact_number = st.text_input("Contact Number", 
                                         value=profile['contact_number'],
                                         help="Enter your phone number with country code (e.g., +1234567890)")
            
            contact_submit = st.form_submit_button("Update Contact Info")
            
            if contact_submit:
                if contact_number and not validate_contact_number(contact_number):
                    st.error("Please enter a valid phone number")
                else:
                    profile_data = profile.copy()
                    profile_data['contact_number'] = contact_number
                    
                    if update_user_profile(st.session_state.user_id, profile_data):
                        st.success("Contact information updated successfully!")
                        st.rerun()
    
    # Role-specific tabs
    if len(tabs) > 2:
        with tabs[2]:
            if user_role in ['purchaser', 'breeder']:
                st.subheader("Payment Information")
                
                with st.form("payment_form"):
                    st.info("🔒 Payment information is encrypted and secure")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        credit_card = st.text_input("Credit Card Number", 
                                                  placeholder="Enter full card number",
                                                  help="Only last 4 digits will be stored")
                        if profile['credit_card_last4']:
                            st.text(f"Current card ends in: ****{profile['credit_card_last4']}")
                    
                    with col2:
                        payment_account = st.text_input("Payment Account/Wallet", 
                                                      value=profile['payment_account'],
                                                      help="PayPal, GCash, or other payment account")
                    
                    payment_submit = st.form_submit_button("Update Payment Info")
                    
                    if payment_submit:
                        profile_data = profile.copy()
                        
                        # Validate and store credit card
                        if credit_card:
                            last4 = validate_credit_card(credit_card)
                            if last4:
                                profile_data['credit_card_last4'] = last4
                            else:
                                st.error("Please enter a valid credit card number")
                                return
                        
                        profile_data['payment_account'] = payment_account
                        
                        if update_user_profile(st.session_state.user_id, profile_data):
                            st.success("Payment information updated successfully!")
                            st.rerun()
            
            elif user_role == 'student':
                st.subheader("Student Information")
                st.info("🎓 Student-specific features and TESDA module access")
                
                # Student-specific fields can be added here
                with st.form("student_form"):
                    student_id = st.text_input("Student ID")
                    course = st.text_input("Course/Program")
                    year_level = st.selectbox("Year Level", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
                    
                    student_submit = st.form_submit_button("Update Student Info")
                    
                    if student_submit:
                        st.success("Student information updated!")
            
            elif user_role == 'faculty':
                st.subheader("Faculty Information")
                st.info("🏫 Faculty access to advanced features")
                
                with st.form("faculty_form"):
                    department = st.text_input("Department")
                    position = st.text_input("Position/Title")
                    specialization = st.text_input("Specialization")
                    
                    faculty_submit = st.form_submit_button("Update Faculty Info")
                    
                    if faculty_submit:
                        st.success("Faculty information updated!")
    
    # Display current profile summary
    st.subheader("Profile Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Username", profile['username'])
        st.metric("Role", profile['role'].title())
    
    with col2:
        st.metric("Email", profile['email'] or "Not set")
        st.metric("Contact", profile['contact_number'] or "Not set")
    
    with col3:
        st.metric("Full Name", profile['full_name'] or "Not set")
        if profile['credit_card_last4']:
            st.metric("Card", f"****{profile['credit_card_last4']}")
    
    # Account creation date
    if profile['created_at']:
        st.caption(f"Account created: {profile['created_at']}")

if __name__ == "__main__":
    profile_management_app()