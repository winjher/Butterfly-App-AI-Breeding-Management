import streamlit as st
import sqlite3
import hashlib
import os
from datetime import datetime

DATABASE_FILE = 'users.db'

def initialize_auth_db():
    """Initialize the authentication database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create default admin user if not exists
    admin_password = hashlib.sha256("admin123".encode()).hexdigest()
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, role) 
        VALUES (?, ?, ?)
    ''', ("admin", admin_password, "admin"))
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    """Verify user credentials"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    hashed_password = hash_password(password)
    cursor.execute(
        "SELECT id, username, role FROM users WHERE username = ? AND password = ?",
        (username, hashed_password)
    )
    
    user = cursor.fetchone()
    conn.close()
    
    return user

def create_user(username, password, email="", role="user"):
    """Create a new user account"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    try:
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            (username, hashed_password, email, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def handle_authentication():
    """Handle user authentication flow"""
    initialize_auth_db()
    
    # Check if user is already logged in
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        return True
    
    # Login/Register tabs
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Butterfly Ecosystem")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Login")
            
            if login_submitted:
                if username and password:
                    user = verify_user(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user[0]
                        st.session_state.username = user[1]
                        st.session_state.user_role = user[2]
                        st.success(f"Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.error("Please enter both username and password")
    
    with tab2:
        st.subheader("Create New Account")
        
        with st.form("register_form"):
            new_username = st.text_input("Choose Username")
            new_email = st.text_input("Email (optional)")
            role = st.selectbox("Role (optional)", 
                              options=["user", "breeder", "purchaser", "enthusiast/tourist", "student", "faculty"],
                              index=0,
                              help="Select your role to access specific features")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            register_submitted = st.form_submit_button("Register")
            
            if register_submitted:
                if new_username and new_password:
                    if new_password == confirm_password:
                        if create_user(new_username, new_password, new_email, role):
                            st.success("Account created successfully! Please login.")
                        else:
                            st.error("Username already exists")
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in required fields")
    
    return False
