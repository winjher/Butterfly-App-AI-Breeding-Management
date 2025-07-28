import streamlit as st
import pandas as pd
import datetime

# --- Custom CSS Style Injection ---
st.markdown("""
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
}
.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}
.header {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 30px;
    margin-bottom: 30px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}
.header h1 {
    font-size: 2.5rem;
    color: #4a5568;
    margin-bottom: 10px;
}
.header p {
    color: #718096;
    font-size: 1.1rem;
}
.nav-tabs {
    display: flex;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    padding: 5px;
    margin-bottom: 30px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}
.nav-tab {
    flex: 1;
    background: none;
    border: none;
    padding: 15px 20px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 1rem;
    font-weight: 500;
}
.nav-tab.active {
    background: #667eea;
    color: white;
    box-shadow: 0 3px 10px rgba(102, 126, 234, 0.4);
}
.nav-tab:hover:not(.active) {
    background: rgba(102, 126, 234, 0.1);
}
.tab-content {
    display: none;
}
.tab-content.active {
    display: block;
}
.card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
}
.card h3 {
    color: #4a5568;
    margin-bottom: 20px;
    font-size: 1.4rem;
}
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}
.stat-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 15px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}
.stat-card h4 {
    font-size: 2rem;
    margin-bottom: 10px;
}
.stat-card p {
    opacity: 0.9;
    font-size: 1.1rem;
}
.batch-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
}
.batch-card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
    cursor: pointer;
}
.batch-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #667eea, #764ba2);
}
.batch-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}
.batch-id {
    font-weight: bold;
    color: #4a5568;
    font-size: 1.1rem;
}
.lifecycle-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
}
.lifecycle-egg { background: #ffeaa7; color: #2d3436; }
.lifecycle-larva { background: #74b9ff; color: white; }
.lifecycle-pupa { background: #fd79a8; color: white; }
.lifecycle-adult { background: #00b894; color: white; }
.status-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
}
.status-healthy { background: #00b894; }
.status-warning { background: #fdcb6e; }
.status-critical { background: #e17055; }
.form-group {
    margin-bottom: 20px;
}
.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: #4a5568;
}
.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 12px;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #667eea;
}
.btn {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 500;
    transition: all 0.3s ease;
    margin-right: 10px;
    margin-bottom: 10px;
}
.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}
.btn-secondary {
    background: #718096;
}
.btn-danger {
    background: #e53e3e;
}
.btn-success {
    background: #38a169;
}
.btn-small {
    padding: 8px 16px;
    font-size: 0.9rem;
}
.alert {
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    border-left: 4px solid;
}
.alert-success {
    background: #f0fff4;
    border-color: #38a169;
    color: #22543d;
}
.alert-warning {
    background: #fffbf0;
    border-color: #d69e2e;
    color: #744210;
}
.alert-danger {
    background: #fff5f5;
    border-color: #e53e3e;
    color: #742a2a;
}
.progress-bar {
    width: 100%;
    height: 8px;
    background: #e2e8f0;
    border-radius: 4px;
    overflow: hidden;
    margin: 10px 0;
}
.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea, #764ba2);
    transition: width 0.3s ease;
}
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
}
.modal-content {
    background: white;
    margin: 5% auto;
    padding: 30px;
    border-radius: 15px;
    width: 90%;
    max-width: 800px;
    position: relative;
    max-height: 80vh;
    overflow-y: auto;
}
.close {
    position: absolute;
    right: 20px;
    top: 20px;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
    color: #718096;
}
.close:hover {
    color: #4a5568;
}
.qr-code {
    text-align: center;
    margin: 20px 0;
}
.qr-code img {
    max-width: 200px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}
@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    .header h1 {
        font-size: 2rem;
    }
    .nav-tabs {
        flex-direction: column;
    }
    .batch-grid {
        grid-template-columns: 1fr;
    }
    .stats-grid {
        grid-template-columns: 1fr;
    }
}
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: white;
    border-radius: 8px;
    padding: 15px 20px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    z-index: 1001;
    max-width: 300px;
    transform: translateX(350px);
    transition: transform 0.3s ease;
}
.notification.show {
    transform: translateX(0);
}
</style>
""", unsafe_allow_html=True)

# Sidebar user info and authentication (demo only)
def login():
    st.sidebar.title("Login")
    user = st.sidebar.text_input("Username")
    pw = st.sidebar.text_input("Password", type="password")
    if user and pw:
        st.session_state["user"] = {"name": user, "role": "breeder"}
        st.success(f"Welcome, {user}!")
    else:
        st.warning("Please enter username and password.")

if "user" not in st.session_state:
    login()
    st.stop()

user = st.session_state["user"]

st.set_page_config(page_title="🦋 Butterfly Breeding Management System", layout="wide")

st.title("🦋 Butterfly Breeding Management System")
st.caption("Advanced CNN-powered breeding optimization with real-time monitoring")

# Tabs
tabs = [
    "Dashboard",
    "Cage Management",
    "AI Classification",
    "Marketplace",
    "Task Management",
    "Profit Analytics",
    "Breeding Log",
    "Settings"
]
tab = st.sidebar.radio("Navigate", tabs)

# Dummy data
species_list = ["Papilio demoleus", "Danaus chrysippus", "Troides helena"]
batches = [
    {"id": "B001", "species": "Papilio demoleus", "stage": "Larva", "larva_count": 50, "status": "healthy", "phone": "+1234567890"},
    {"id": "B002", "species": "Danaus chrysippus", "stage": "Pupa", "larva_count": 30, "status": "warning", "phone": "+9876543210"},
]
tasks = [
    {"title": "Feed batch B001", "type": "feeding", "priority": "high", "due": datetime.datetime.now() + datetime.timedelta(hours=2)},
    {"title": "Clean Cage B002", "type": "cage_cleaning", "priority": "medium", "due": datetime.datetime.now() + datetime.timedelta(days=1)},
]
breeding_log = [
    {"datetime": "2025-06-26 14:00", "event": "Fed batch B001"},
    {"datetime": "2025-06-27 09:20", "event": "Batch B002 entered pupa stage"}
]

if tab == "Dashboard":
    st.header("Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Batches", len(batches))
    col2.metric("Total Larvae", sum(b['larva_count'] for b in batches))
    col3.metric("Open Tasks", len(tasks))
    st.subheader("Active Alerts")
    st.info("All systems nominal. No critical alerts.")
    st.subheader("Recent Batch Activity")
    st.table(pd.DataFrame(breeding_log))

elif tab == "Cage Management":
    st.header("Cage Management")
    st.subheader("Create New Cage Batch")
    with st.form("create_batch"):
        species = st.selectbox("Species", species_list)
        larva_count = st.number_input("Larva Count", min_value=1)
        phone = st.text_input("Phone Number")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Create Batch")
        if submitted:
            st.success(f"Batch created: {species} ({larva_count} larvae)")
    st.subheader("Active Cage Batches")
    st.table(pd.DataFrame(batches))

elif tab == "AI Classification":
    st.header("CNN Image Classification")
    st.write("Upload images for AI-powered analysis of butterfly species, lifecycle stages, larval diseases, and pupae defects.")
    analysis_type = st.selectbox("Analysis Type", [
        "Complete Analysis (All Models)",
        "Species Identification",
        "Lifecycle Stage",
        "Larval Disease Detection",
        "Pupae Defect Analysis"
    ])
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        st.info("Pretend AI analysis results: (demo)")
        st.json({"species": "Papilio demoleus", "stage": "Larva", "disease": "None", "defects": "None"})
    st.subheader("Model Information")
    st.write("CNN Models: All loaded and ready.")

elif tab == "Marketplace":
    st.header("Butterfly Marketplace")
    st.write("Buy and sell butterfly specimens from verified breeders with secure GCash payments.")
    st.info("Marketplace feature coming soon.")
    st.subheader("My Orders")
    st.write("Orders will appear here.")

elif tab == "Task Management":
    st.header("Task Management")
    st.subheader("Create New Task")
    with st.form("create_task"):
        task_title = st.text_input("Task Title")
        task_type = st.selectbox("Task Type", [
            "Feeding", "Pest Control", "Cage Cleaning", "Health Check", "Plant Replacement",
            "Temperature Check", "Humidity Check", "Breeding Record", "Quality Assessment", "Harvest"
        ])
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        due_date = st.date_input("Due Date", value=datetime.date.today())
        desc = st.text_area("Description")
        task_submit = st.form_submit_button("Create Task")
        if task_submit:
            st.success(f"Task created: {task_title}")
    st.subheader("Task List")
    st.table(pd.DataFrame(tasks))

elif tab == "Profit Analytics":
    st.header("Profit Overview")
    st.info("Profit analytics and species performance coming soon.")

elif tab == "Breeding Log":
    st.header("Activity Log")
    st.table(pd.DataFrame(breeding_log))

elif tab == "Settings":
    st.header("Settings")
    st.subheader("SMS Configuration")
    test_phone = st.text_input("Test Phone Number")
    test_message = st.text_area("Test Message", value="🦋 Test message from Butterfly Breeding Management System!")
    if st.button("Send Test SMS"):
        st.success(f"Test SMS sent to {test_phone} (simulation)")
    st.subheader("Data Management")
    st.button("Export Data")
    st.button("Check Feeding Schedule")

st.sidebar.markdown("---")
if st.sidebar.button("Logout"):
    del st.session_state["user"]
    st.experimental_rerun()

