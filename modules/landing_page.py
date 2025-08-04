import streamlit as st
from modules.premium_system import claim_signup_bonus, get_user_premium_status

def show_signup_bonus_banner():
    """Show attractive signup bonus banner on landing page"""
    
    # Only show if user is logged in and hasn't claimed bonus
    if 'user_id' not in st.session_state:
        return
    
    user_id = st.session_state.user_id
    username = st.session_state.username
    status = get_user_premium_status(user_id)
    
    if status and not status['signup_bonus_claimed']:
        # Create attractive banner
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: center;
            color: white;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        ">
            <h2 style="margin: 0; color: white;">🎉 WELCOME BONUS AVAILABLE! 🎉</h2>
            <h3 style="margin: 10px 0; color: #ffeb3b;">FREE ₱200 GCash Bonus</h3>
            <p style="margin: 10px 0; font-size: 18px;">
                Sign up now and get instant ₱200 in your ewallet!<br>
                Perfect for buying your first pupae and starting your butterfly breeding journey.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Claim button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎁 CLAIM MY ₱200 BONUS NOW!", type="primary", use_container_width=True):
                success, message = claim_signup_bonus(user_id, username)
                if success:
                    st.success(message)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(message)

def landing_page_features():
    """Display key features on landing page"""
    
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
        <h1 style="color: #2c3e50; margin-bottom: 10px;">🦋 Butterfly Breeding Ecosystem</h1>
        <p style="font-size: 20px; color: #7f8c8d; margin-bottom: 30px;">
            Your Complete Platform for Butterfly Breeding Success
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 10px 0;
        ">
            <div style="font-size: 48px; margin-bottom: 15px;">💰</div>
            <h3 style="color: #2c3e50; margin-bottom: 15px;">Earn Money</h3>
            <p style="color: #7f8c8d;">
                Breed and sell butterflies with our comprehensive Point of Sale system. 
                Track earnings and reach Level 2 for premium rewards!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 10px 0;
        ">
            <div style="font-size: 48px; margin-bottom: 15px;">🤖</div>
            <h3 style="color: #2c3e50; margin-bottom: 15px;">AI Classification</h3>
            <p style="color: #7f8c8d;">
                Use advanced AI to identify butterfly species, detect diseases, 
                and monitor life stages with professional accuracy.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 10px 0;
        ">
            <div style="font-size: 48px; margin-bottom: 15px;">💎</div>
            <h3 style="color: #2c3e50; margin-bottom: 15px;">Premium Benefits</h3>
            <p style="color: #7f8c8d;">
                Upgrade to premium for higher commissions, priority support, 
                and exclusive features. Reach ₱260k earnings for Level 2 status!
            </p>
        </div>
        """, unsafe_allow_html=True)

def premium_promotion_section():
    """Show premium membership promotion"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 20px;
        margin: 40px 0;
        text-align: center;
        color: white;
    ">
        <h2 style="margin: 0 0 20px 0; color: white;">🚀 Unlock Premium Benefits</h2>
        <div style="display: flex; justify-content: center; gap: 40px; margin: 30px 0;">
            <div>
                <h3 style="color: #ffeb3b;">₱299/month</h3>
                <p>Premium Membership</p>
            </div>
            <div>
                <h3 style="color: #ffeb3b;">₱260,000</h3>
                <p>Level 2 Earnings Goal</p>
            </div>
            <div>
                <h3 style="color: #ffeb3b;">₱20,000</h3>
                <p>Level 2 Achievement Prize</p>
            </div>
        </div>
        <p style="font-size: 18px; margin: 20px 0;">
            Join our premium community and maximize your butterfly breeding potential!
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_earnings_leaderboard():
    """Display top earners leaderboard"""
    
    st.subheader("🏆 Top Breeders Leaderboard")
    
    # This would typically fetch real data from the database
    # For now, showing the structure
    
    sample_data = [
        {"name": "Maria Santos", "level": 2, "earnings": "₱285,000", "status": "Premium"},
        {"name": "Juan Dela Cruz", "level": 2, "earnings": "₱267,500", "status": "Premium"},
        {"name": "Ana Rodriguez", "level": 1, "earnings": "₱189,250", "status": "Premium"},
        {"name": "Carlos Mendoza", "level": 1, "earnings": "₱156,800", "status": "Free"},
        {"name": "Lisa Chen", "level": 1, "earnings": "₱142,300", "status": "Premium"}
    ]
    
    for i, breeder in enumerate(sample_data[:5]):
        if i == 0:
            badge = "🥇"
        elif i == 1:
            badge = "🥈"
        elif i == 2:
            badge = "🥉"
        else:
            badge = f"{i+1}."
        
        level_badge = "👑" if breeder["level"] == 2 else "⭐"
        status_color = "#28a745" if breeder["status"] == "Premium" else "#6c757d"
        
        st.markdown(f"""
        <div style="
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            border-left: 4px solid {status_color};
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <strong>{badge} {breeder['name']}</strong> {level_badge}
                <span style="color: {status_color}; font-size: 12px; margin-left: 10px;">
                    {breeder['status']}
                </span>
            </div>
            <div style="text-align: right;">
                <strong>{breeder['earnings']}</strong><br>
                <small>Level {breeder['level']}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

def enhanced_landing_page():
    """Enhanced landing page with signup bonus and premium features"""
    
    # Show signup bonus banner for logged-in users
    show_signup_bonus_banner()
    
    # Main landing page content
    landing_page_features()
    
    # Premium promotion
    premium_promotion_section()
    
    # Success stories and testimonials
    st.subheader("💬 Success Stories")
    
    testimonials = [
        {
            "name": "Maria Santos",
            "role": "Level 2 Premium Breeder",
            "text": "I reached Level 2 in just 8 months! The ₱20,000 bonus was amazing, and the premium features really helped grow my breeding business.",
            "earnings": "₱285,000 total earnings"
        },
        {
            "name": "Juan Dela Cruz",
            "role": "Premium Breeder",
            "text": "The AI classification feature saved me so much time. I can now identify species and diseases instantly. Premium membership paid for itself!",
            "earnings": "₱267,500 total earnings"
        }
    ]
    
    for testimonial in testimonials:
        st.markdown(f"""
        <div style="
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #28a745;
        ">
            <p style="font-style: italic; margin-bottom: 15px; font-size: 16px;">
                "{testimonial['text']}"
            </p>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{testimonial['name']}</strong><br>
                    <small style="color: #6c757d;">{testimonial['role']}</small>
                </div>
                <div style="text-align: right; color: #28a745;">
                    <strong>{testimonial['earnings']}</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show leaderboard
    show_earnings_leaderboard()

if __name__ == "__main__":
    enhanced_landing_page()