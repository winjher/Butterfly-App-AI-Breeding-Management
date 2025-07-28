import streamlit as st
import os
from modules.auth import handle_authentication
from modules.breeding_management import breeding_management_app
from modules.ai_classification import ai_classification_app
from modules.point_of_sale import point_of_sale_app
from modules.sales_tracking import sales_tracking_app
from modules.booking_system import booking_system_app
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
    
    # Navigation menu
    apps = {
        "🏠 Dashboard": "dashboard",
        "🦋 Breeding Management": "breeding",
        "🤖 AI Classification": "ai_classification",
        "💰 Point of Sale": "pos",
        "📊 Sales Tracking": "sales_tracking",
        "🌍 Farm Booking": "booking"
    }
    
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

def dashboard_app():
    """Dashboard overview of the entire ecosystem"""
    st.title("🏠 Butterfly Ecosystem Dashboard")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Batches", get_active_batches_count())
    with col2:
        st.metric("Total Species", get_species_count())
    with col3:
        st.metric("Sales This Month", get_monthly_sales())
    with col4:
        st.metric("Farm Bookings", get_booking_count())
    
    # Recent activity
    st.subheader("Recent Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Recent Breeding Activities**")
        # Show recent breeding log entries
        st.info("Check Breeding Management for detailed logs")
    
    with col2:
        st.write("**Recent Sales**")
        # Show recent sales
        st.info("Check Sales Tracking for detailed records")
    
    # Quick actions
    st.subheader("Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🦋 New Breeding Batch"):
            st.session_state.quick_action = "new_batch"
            st.rerun()
    
    with col2:
        if st.button("🤖 Classify Image"):
            st.session_state.quick_action = "classify"
            st.rerun()
    
    with col3:
        if st.button("💰 Record Sale"):
            st.session_state.quick_action = "sale"
            st.rerun()

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
