import streamlit as st
import datetime
from modules.ui_components import display_header, create_info_card, create_notification

def student_dashboard_app():
    """Student Portal with TESDA integration for butterfly production training"""
    display_header("🎓 Student Portal", "Butterfly Production Training - TESDA Integration", "📚")
    
    # Check if user has student role
    if 'user_role' not in st.session_state or st.session_state.user_role != 'student':
        st.warning("⚠️ This section is only available for registered students.")
        st.info("If you are a student, please register with 'student' role to access TESDA modules.")
        return
    
    # Main student dashboard content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Course Enrollment Card
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea, #764ba2); 
            color: white; 
            border-radius: 15px; 
            padding: 25px; 
            text-align: center;
            margin-bottom: 20px;
        ">
            <div style="font-size: 3rem; margin-bottom: 15px;">🏆</div>
            <h4 style="margin: 0 0 15px 0;">Butterfly Production Level II</h4>
            <p style="margin: 15px 0;">Advanced breeding techniques and quality management certification program</p>
            <div style="margin: 20px 0;">
                <div style="background: rgba(255,255,255,0.2); border-radius: 8px; padding: 10px;">
                    <p style="margin: 5px 0;"><strong>Duration:</strong> 80 hours</p>
                    <p style="margin: 5px 0;"><strong>Type:</strong> Blended Learning</p>
                    <p style="margin: 5px 0;"><strong>Certificate:</strong> NC II</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 ENROLL NOW", key="enroll_btn", help="Enroll in Butterfly Production Level II"):
            show_enrollment_modal()
    
    with col2:
        # Scholarship Information Card
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #48bb78, #38a169); 
            color: white; 
            border-radius: 15px; 
            padding: 25px; 
            text-align: center;
            margin-bottom: 20px;
        ">
            <div style="font-size: 3rem; margin-bottom: 15px;">💰</div>
            <h4 style="margin: 0 0 15px 0;">TESDA Scholarship Program</h4>
            <p style="margin: 15px 0;">Get free training with TESDA scholarship opportunities for qualified students</p>
            <div style="margin: 20px 0;">
                <div style="background: rgba(255,255,255,0.2); border-radius: 8px; padding: 10px;">
                    <p style="margin: 5px 0;"><strong>Coverage:</strong> 100% Training Fee</p>
                    <p style="margin: 5px 0;"><strong>Allowance:</strong> Available</p>
                    <p style="margin: 5px 0;"><strong>Requirements:</strong> Basic Education</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("ℹ️ HOW TO APPLY", key="scholarship_btn", help="Learn about scholarship requirements"):
            show_scholarship_modal()
    
    with col3:
        # Career Exploration Card
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #ed8936, #dd6b20); 
            color: white; 
            border-radius: 15px; 
            padding: 25px; 
            text-align: center;
            margin-bottom: 20px;
        ">
            <div style="font-size: 3rem; margin-bottom: 15px;">🧭</div>
            <h4 style="margin: 0 0 15px 0;">Explore Career Paths</h4>
            <p style="margin: 15px 0;">Discover various career opportunities in butterfly farming and biotechnology</p>
            <div style="margin: 20px 0;">
                <div style="background: rgba(255,255,255,0.2); border-radius: 8px; padding: 10px;">
                    <p style="margin: 5px 0;"><strong>Opportunities:</strong> Entrepreneur</p>
                    <p style="margin: 5px 0;"><strong>Industry:</strong> Agriculture</p>
                    <p style="margin: 5px 0;"><strong>Growth:</strong> High Demand</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 EXPLORE", key="career_btn", help="Explore career opportunities"):
            show_career_modal()
    
    # Quick Access Links Section
    st.markdown("---")
    st.subheader("🔗 Quick Access Links")
    
    link_col1, link_col2, link_col3, link_col4 = st.columns(4)
    
    with link_col1:
        st.link_button("🌐 TESDA Official Website", "https://tesda.gov.ph", help="Visit TESDA official website")
    
    with link_col2:
        st.link_button("💻 Online Enrollment Portal", "https://enrollment.tesda.gov.ph", help="Access TESDA enrollment portal")
    
    with link_col3:
        st.link_button("🎓 Scholarship Portal", "https://scholarship.tesda.gov.ph", help="Apply for TESDA scholarships")
    
    with link_col4:
        if st.button("📄 Download Training Guide", key="download_guide"):
            download_training_guide()
    
    # Student Progress Section
    st.markdown("---")
    display_student_progress()
    
    # Learning Resources
    st.markdown("---")
    display_learning_resources()

def show_enrollment_modal():
    """Display enrollment information modal"""
    with st.expander("📝 Course Enrollment - Butterfly Production Level II", expanded=True):
        st.markdown("""
        ### Course Overview
        The Butterfly Production Level II certification program provides comprehensive training in:
        
        **Core Modules:**
        - Advanced breeding techniques
        - Quality management systems
        - Disease prevention and control
        - Business planning and marketing
        - Sustainable farming practices
        
        **Prerequisites:**
        - Basic education (high school graduate or equivalent)
        - Interest in agriculture and biotechnology
        
        **Certification:**
        Upon completion, students receive TESDA NC II certification in Butterfly Production.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name", key="enroll_name")
            st.text_input("Contact Number", key="enroll_contact")
            st.selectbox("Educational Background", 
                        ["High School Graduate", "College Graduate", "Vocational Graduate", "Others"],
                        key="enroll_education")
        
        with col2:
            st.text_input("Email Address", key="enroll_email")
            st.date_input("Preferred Start Date", key="enroll_date")
            st.selectbox("Learning Mode", 
                        ["Face-to-face", "Online", "Blended Learning"],
                        key="enroll_mode")
        
        if st.button("Submit Enrollment Application", key="submit_enrollment"):
            st.success("✅ Enrollment application submitted successfully! You will receive confirmation within 3 business days.")
            create_notification("Enrollment application submitted", "success")

def show_scholarship_modal():
    """Display scholarship information modal"""
    with st.expander("💰 TESDA Scholarship Program Information", expanded=True):
        st.markdown("""
        ### Available Scholarships
        
        **1. TESDA-TWSP (Training for Work Scholarship Program)**
        - 100% training fee coverage
        - Training materials allowance
        - Assessment and certification fee
        
        **2. Private Education Student Financial Assistance (PESFA)**
        - For students in private training institutions
        - Covers tuition and other fees
        
        **Requirements:**
        - Filipino citizen
        - High school graduate or equivalent
        - Family income below poverty threshold
        - Passing the scholarship examination
        
        **Application Process:**
        1. Visit nearest TESDA office
        2. Submit required documents
        3. Take scholarship examination
        4. Wait for results and interview
        5. Enroll in accredited training center
        """)
        
        if st.button("Download Scholarship Application Form", key="download_scholarship"):
            st.info("📄 Scholarship application form download initiated.")

def show_career_modal():
    """Display career exploration modal"""
    with st.expander("🧭 Career Opportunities in Butterfly Production", expanded=True):
        st.markdown("""
        ### Career Paths
        
        **1. Butterfly Farm Entrepreneur**
        - Start your own butterfly breeding facility
        - Supply butterflies to exhibits and educational centers
        - Average income: ₱50,000 - ₱200,000+ monthly
        
        **2. Agricultural Technician**
        - Work in research institutions
        - Assist in breeding programs
        - Salary range: ₱18,000 - ₱35,000 monthly
        
        **3. Tourism Guide/Educator**
        - Lead butterfly garden tours
        - Educational program coordinator
        - Income: ₱15,000 - ₱30,000 monthly
        
        **4. Quality Control Specialist**
        - Ensure breeding standards
        - Health monitoring and assessment
        - Salary: ₱20,000 - ₱40,000 monthly
        
        ### Industry Growth
        - 15-20% annual growth in eco-tourism
        - Increasing demand for educational programs
        - Export opportunities to international markets
        """)

def download_training_guide():
    """Simulate training guide download"""
    st.info("📄 Training Guide for Butterfly Production NC II - Download initiated")
    
    # Create downloadable content
    training_content = """
    BUTTERFLY PRODUCTION TRAINING GUIDE
    =====================================
    
    Module 1: Introduction to Butterfly Biology
    Module 2: Breeding Techniques and Best Practices  
    Module 3: Disease Prevention and Health Management
    Module 4: Quality Control and Assessment
    Module 5: Business Planning and Marketing
    Module 6: Sustainable Farming Practices
    
    This guide contains comprehensive information for successful butterfly production.
    """
    
    st.download_button(
        label="📥 Download PDF Guide",
        data=training_content,
        file_name="butterfly_production_guide.txt",
        mime="text/plain"
    )

def display_student_progress():
    """Display student learning progress"""
    st.subheader("📊 Your Learning Progress")
    
    # Mock progress data
    progress_data = {
        "Introduction to Butterfly Biology": 100,
        "Breeding Techniques": 75,
        "Disease Prevention": 60,
        "Quality Control": 30,
        "Business Planning": 0,
        "Sustainable Practices": 0
    }
    
    for module, progress in progress_data.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{module}**")
            st.progress(progress / 100)
        with col2:
            st.write(f"{progress}%")

def display_learning_resources():
    """Display available learning resources"""
    st.subheader("📚 Learning Resources")
    
    resources = [
        {
            "title": "Butterfly Species Identification Guide",
            "type": "PDF",
            "description": "Comprehensive guide to common butterfly species in the Philippines"
        },
        {
            "title": "Breeding Setup Video Tutorial",
            "type": "Video",
            "description": "Step-by-step guide to setting up breeding cages"
        },
        {
            "title": "Disease Recognition Charts",
            "type": "Images",
            "description": "Visual guide to identifying common butterfly diseases"
        },
        {
            "title": "Business Plan Template",
            "type": "Document",
            "description": "Template for creating a butterfly farm business plan"
        }
    ]
    
    for resource in resources:
        with st.expander(f"📄 {resource['title']} ({resource['type']})"):
            st.write(resource['description'])
            st.button(f"Access {resource['title']}", key=f"access_{resource['title'].replace(' ', '_')}")