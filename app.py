import streamlit as st
import os
from modules.auth import handle_authentication
from modules.breeding_management import breeding_management_app
from modules.ai_classification import ai_classification_app
from modules.point_of_sale import point_of_sale_app
from modules.sales_tracking import sales_tracking_app
from modules.booking_system import booking_system_app
from modules.student_dashboard import student_dashboard_app
from modules.purchaser_profile import purchaser_profile_app
from modules.profile_management import profile_management_app
from modules.premium_system import premium_system_app, admin_premium_management
from modules.email_notifications import email_notifications_app
from modules.landing_page import enhanced_landing_page
from modules.database import initialize_databases
from modules.ui_components import apply_glassmorphism_style, set_background_image

# Page configuration
st.set_page_config(
    page_title="🦋 Butterfly Breeding Ecosystem",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize databases and directories
initialize_databases()

# Apply styling
apply_glassmorphism_style()
try:
    set_background_image('icon/bg.png')
except:
    pass  # Background image is optional

def main():
    """Main application entry point"""
    
    # Handle authentication
    if not handle_authentication():
        return
    
    # Main navigation
    st.sidebar.title("🦋 Butterfly Ecosystem")
    st.sidebar.write(f"Welcome, **{st.session_state.username}**!")
    
    # Navigation menu with role-based access
    apps = {
        "🏠 Dashboard": "dashboard",
        "👤 My Profile": "profile",
        "💎 Premium System": "premium",
        "🦋 Breeding Management": "breeding",
        "🤖 AI Classification": "ai_classification",
        "💰 Point of Sale": "pos",
        "📊 Sales Tracking": "sales_tracking",
        "🌍 Farm Booking": "booking"
    }
    
    # Add admin-only features
    if st.session_state.get('user_role') == 'admin':
        apps["🔧 Premium Admin"] = "premium_admin"
        apps["📧 Email Notifications"] = "email_notifications"
    
    # Add role-specific dashboards
    if st.session_state.get('user_role') == 'student':
        apps["🎓 Student Dashboard"] = "student_dashboard"
    
    if st.session_state.get('user_role') == 'purchaser':
        apps["🛒 Purchaser Profile"] = "purchaser_profile"
    
    # Role-based feature highlighting
    if st.session_state.get('user_role') in ['breeder', 'faculty']:
        st.sidebar.info("🔬 You have access to advanced breeding features")
    elif st.session_state.get('user_role') == 'purchaser':
        st.sidebar.info("🛒 Enhanced purchasing features available")
    elif st.session_state.get('user_role') == 'student':
        st.sidebar.success("📚 Student Dashboard with TESDA modules available")
    elif st.session_state.get('user_role') == 'enthusiast/tourist':
        st.sidebar.info("🦋 Tourism and booking features optimized for you")
    
    selected_app = st.sidebar.selectbox("Select Application", list(apps.keys()))
    
    # Logout button
    if st.sidebar.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Route to selected application
    app_key = apps[selected_app]
    
    if app_key == "dashboard":
        dashboard_app()
    elif app_key == "profile":
        profile_management_app()
    elif app_key == "premium":
        premium_system_app()
    elif app_key == "premium_admin":
        admin_premium_management()
    elif app_key == "email_notifications":
        email_notifications_app()
    elif app_key == "breeding":
        breeding_management_app()
    elif app_key == "ai_classification":
        ai_classification_app()
    elif app_key == "pos":
        point_of_sale_app()
    elif app_key == "sales_tracking":
        sales_tracking_app()
    elif app_key == "booking":
        booking_system_app()
    elif app_key == "student_dashboard":
        student_dashboard_app()
    elif app_key == "purchaser_profile":
        purchaser_profile_app()

def dashboard_app():
    """Dashboard overview of the entire ecosystem"""
    
    # Show enhanced landing page with signup bonus
    enhanced_landing_page()

def get_active_batches_count():
    """Get count of active breeding batches"""
    try:
        import pandas as pd
        if os.path.exists('breeding_batches.csv'):
            df = pd.read_csv('breeding_batches.csv')
            return len(df)
    except:
        pass
    return 0

def get_species_count():
    """Get count of butterfly species"""
    from data.butterfly_species_info import BUTTERFLY_SPECIES_INFO
    return len(BUTTERFLY_SPECIES_INFO)

def get_monthly_sales():
    """Get monthly sales count"""
    try:
        import pandas as pd
        from datetime import datetime, timedelta
        if os.path.exists('butterfly_purchases.csv'):
            df = pd.read_csv('butterfly_purchases.csv')
            # Filter for current month
            current_month = datetime.now().replace(day=1)
            df['Date'] = pd.to_datetime(df['Date'])
            monthly_sales = df[df['Date'] >= current_month]
            return len(monthly_sales)
    except:
        pass
    return 0

def get_booking_count():
    """Get farm booking count"""
    try:
        import pandas as pd
        if os.path.exists('farm_bookings.csv'):
            df = pd.read_csv('farm_bookings.csv')
            return len(df)
    except:
        pass
    return 0

if __name__ == "__main__":
    main()
