import streamlit as st
import base64
import os

def apply_glassmorphism_style():
    """Apply glassmorphism styling to the Streamlit application"""
    st.markdown(
        """
        <style>
        /* General glassmorphism styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 20px;
        }

        /* Sidebar styling */
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 16px;
        }

        /* Card styling */
        .card {
            background: rgba(255, 255, 255, 0.25);
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            padding: 15px;
            margin-bottom: 15px;
        }

        /* Button styling */
        .stButton>button {
            background-color: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
            border-radius: 8px;
        }

        .stButton>button:hover {
            background-color: rgba(255, 255, 255, 0.3);
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        }

        /* Input field styling */
        .stTextInput>div>div>input,
        .stSelectbox>div>div>input,
        .stNumberInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 5px;
        }

        /* Metric styling */
        .metric-container {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        /* Alert styling */
        .stAlert {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(5px);
            border-radius: 5px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        /* Data frame styling */
        .stDataFrame {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        /* Expander styling */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 5px;
            margin: 2px;
        }

        .stTabs [aria-selected="true"] {
            background: rgba(255, 255, 255, 0.3) !important;
        }

        /* Form styling */
        .stForm {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        /* Success/Warning/Error message styling */
        .stSuccess, .stWarning, .stError, .stInfo {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(5px);
            border-radius: 5px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def set_background_image(image_path):
    """
    Set a background image for the Streamlit application
    
    Args:
        image_path (str): Path to the background image file
    """
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            st.warning(f"Background image '{image_path}' not found.")
            return
        
        # Convert image to base64
        with open(image_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        
        # Apply background image CSS
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{img_base64}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.warning(f"Could not load background image: {str(e)}")

def create_metric_card(title, value, delta=None, delta_color="normal"):
    """
    Create a styled metric card with glassmorphism effect
    
    Args:
        title (str): The metric title
        value (str): The metric value
        delta (str, optional): The delta value
        delta_color (str): Color of delta ('normal', 'inverse')
    """
    delta_html = ""
    if delta:
        color = "#28a745" if delta_color == "normal" else "#dc3545"
        delta_html = f'<div style="color: {color}; font-size: 0.8rem; margin-top: 5px;">{delta}</div>'
    
    card_html = f"""
    <div class="metric-container">
        <div style="font-size: 0.8rem; color: #666; margin-bottom: 5px;">{title}</div>
        <div style="font-size: 1.5rem; font-weight: bold; color: #333;">{value}</div>
        {delta_html}
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def create_status_badge(status, status_type="default"):
    """
    Create a status badge with appropriate styling
    
    Args:
        status (str): Status text
        status_type (str): Type of status ('success', 'warning', 'error', 'info', 'default')
    """
    colors = {
        'success': '#28a745',
        'warning': '#ffc107', 
        'error': '#dc3545',
        'info': '#17a2b8',
        'default': '#6c757d'
    }
    
    color = colors.get(status_type, colors['default'])
    
    badge_html = f"""
    <span style="
        background-color: {color};
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-block;
        margin: 2px;
    ">
        {status}
    </span>
    """
    
    return badge_html

def create_info_card(title, content, icon="ℹ️"):
    """
    Create an information card with glassmorphism styling
    
    Args:
        title (str): Card title
        content (str): Card content
        icon (str): Icon for the card
    """
    card_html = f"""
    <div style="
        background: rgba(255, 255, 255, 0.25);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    ">
        <h4 style="margin: 0 0 10px 0; color: #333;">
            {icon} {title}
        </h4>
        <p style="margin: 0; color: #555; line-height: 1.5;">
            {content}
        </p>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def create_progress_bar(progress, label="Progress"):
    """
    Create a styled progress bar
    
    Args:
        progress (float): Progress value between 0 and 1
        label (str): Label for the progress bar
    """
    progress_percent = int(progress * 100)
    
    progress_html = f"""
    <div style="margin: 15px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span style="font-size: 0.9rem; color: #333;">{label}</span>
            <span style="font-size: 0.9rem; color: #666;">{progress_percent}%</span>
        </div>
        <div style="
            width: 100%;
            height: 10px;
            background-color: rgba(255, 255, 255, 0.3);
            border-radius: 5px;
            overflow: hidden;
        ">
            <div style="
                width: {progress_percent}%;
                height: 100%;
                background: linear-gradient(90deg, #667eea, #764ba2);
                border-radius: 5px;
                transition: width 0.3s ease;
            "></div>
        </div>
    </div>
    """
    
    st.markdown(progress_html, unsafe_allow_html=True)

def display_header(title, subtitle="", icon="🦋"):
    """
    Display a styled header with glassmorphism effect
    
    Args:
        title (str): Main title
        subtitle (str): Subtitle text
        icon (str): Icon for the header
    """
    subtitle_html = f'<p style="color: #666; font-size: 1.1rem; margin: 10px 0 0 0;">{subtitle}</p>' if subtitle else ""
    
    header_html = f"""
    <div style="
        background: rgba(255, 255, 255, 0.25);
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 30px;
        text-align: center;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">
        <h1 style="
            font-size: 2.5rem;
            color: #333;
            margin: 0;
        ">{icon} {title}</h1>
        {subtitle_html}
    </div>
    """
    
    st.markdown(header_html, unsafe_allow_html=True)

def create_notification(message, notification_type="info", auto_dismiss=True):
    """
    Create a notification message
    
    Args:
        message (str): Notification message
        notification_type (str): Type of notification ('success', 'warning', 'error', 'info')
        auto_dismiss (bool): Whether to auto-dismiss the notification
    """
    colors = {
        'success': '#d4edda',
        'warning': '#fff3cd',
        'error': '#f8d7da',
        'info': '#d1ecf1'
    }
    
    icons = {
        'success': '✅',
        'warning': '⚠️',
        'error': '❌',
        'info': 'ℹ️'
    }
    
    bg_color = colors.get(notification_type, colors['info'])
    icon = icons.get(notification_type, icons['info'])
    
    notification_html = f"""
    <div style="
        background-color: {bg_color};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #333;
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
    ">
        <strong>{icon} {message}</strong>
    </div>
    """
    
    st.markdown(notification_html, unsafe_allow_html=True)

def create_data_table(df, title="Data Table"):
    """
    Create a styled data table with glassmorphism effect
    
    Args:
        df (pandas.DataFrame): Data to display
        title (str): Table title
    """
    if df.empty:
        st.info(f"No data available for {title}")
        return
    
    st.markdown(f"### {title}")
    
    # Custom styling for the dataframe
    st.markdown("""
    <style>
    .dataframe {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(df, use_container_width=True)
