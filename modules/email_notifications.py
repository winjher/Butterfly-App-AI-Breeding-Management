import streamlit as st
import os
import sys
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from modules.premium_system import get_breeder_emails

def send_premium_notification_email(to_email, username):
    """Send premium upgrade notification email to breeder"""
    
    # Check if SendGrid API key is available
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_key:
        return False, "SendGrid API key not configured"
    
    sg = SendGridAPIClient(sendgrid_key)
    
    # Email content
    subject = "🦋 Upgrade to Premium - Unlock Higher Earnings!"
    
    html_content = f"""
    <html>
    <body>
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #ff6b35;">🦋 Butterfly Breeding Ecosystem</h2>
            
            <p>Dear {username},</p>
            
            <p>We hope your butterfly breeding journey has been rewarding! We're excited to introduce our <strong>Premium Membership</strong> program designed specifically for dedicated breeders like you.</p>
            
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #28a745;">💎 Premium Benefits</h3>
                <ul>
                    <li>✅ Higher commission rates on sales</li>
                    <li>✅ Priority customer support</li>
                    <li>✅ Advanced breeding analytics</li>
                    <li>✅ Exclusive breeder tools and features</li>
                    <li>✅ Access to premium butterfly species</li>
                </ul>
            </div>
            
            <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #856404;">🎯 Earn More with Level 2 Status</h3>
                <p><strong>Reach 260,000 pesos in total earnings and unlock:</strong></p>
                <ul>
                    <li>🏆 <strong>20,000 pesos bonus</strong> added to your ewallet</li>
                    <li>📈 Enhanced commission structure</li>
                    <li>🌟 Elite breeder recognition</li>
                </ul>
            </div>
            
            <div style="background-color: #d1ecf1; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #0c5460;">💰 Monthly Investment</h3>
                <p>Premium membership is available for just <strong>₱299 per month</strong></p>
                <p>This small investment can significantly boost your earning potential!</p>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://your-app-url.replit.app" 
                   style="background-color: #ff6b35; color: white; padding: 15px 30px; 
                          text-decoration: none; border-radius: 5px; font-weight: bold;">
                    Upgrade to Premium Now
                </a>
            </div>
            
            <p>Thank you for being part of our butterfly breeding community. We're committed to helping you succeed and grow your breeding business.</p>
            
            <p>Best regards,<br>
            The Butterfly Breeding Ecosystem Team</p>
            
            <hr style="margin: 30px 0;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to promote our premium membership program. 
                If you no longer wish to receive these notifications, please contact our support team.
            </p>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Dear {username},
    
    We hope your butterfly breeding journey has been rewarding! We're excited to introduce our Premium Membership program.
    
    PREMIUM BENEFITS:
    - Higher commission rates on sales
    - Priority customer support  
    - Advanced breeding analytics
    - Exclusive breeder tools and features
    - Access to premium butterfly species
    
    LEVEL 2 EARNINGS GOAL:
    Reach 260,000 pesos in total earnings and unlock:
    - 20,000 pesos bonus added to your ewallet
    - Enhanced commission structure
    - Elite breeder recognition
    
    Monthly Investment: Just ₱299 per month
    
    Visit our app to upgrade to Premium today!
    
    Best regards,
    The Butterfly Breeding Ecosystem Team
    """
    
    message = Mail(
        from_email=Email("noreply@butterflybreeding.com", "Butterfly Breeding Ecosystem"),
        to_emails=To(to_email),
        subject=subject
    )
    
    message.content = [
        Content("text/plain", text_content),
        Content("text/html", html_content)
    ]
    
    try:
        response = sg.send(message)
        return True, f"Email sent successfully (Status: {response.status_code})"
    except Exception as e:
        return False, f"SendGrid error: {str(e)}"

def send_level_upgrade_notification(to_email, username, level, prize_amount):
    """Send congratulations email for level upgrade"""
    
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_key:
        return False, "SendGrid API key not configured"
    
    sg = SendGridAPIClient(sendgrid_key)
    
    subject = f"🎉 Congratulations! You've Reached Level {level}!"
    
    html_content = f"""
    <html>
    <body>
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #28a745;">🎉 CONGRATULATIONS {username.upper()}!</h2>
            
            <div style="background-color: #d4edda; padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0;">
                <h1 style="color: #155724; margin: 0;">🏆 LEVEL {level} ACHIEVED!</h1>
                <h2 style="color: #155724; margin: 10px 0;">₱{prize_amount:,} PRIZE AWARDED!</h2>
            </div>
            
            <p>Dear {username},</p>
            
            <p>We are thrilled to congratulate you on reaching <strong>Level {level}</strong> in our Butterfly Breeding Ecosystem!</p>
            
            <p>Your dedication and hard work have paid off. You've successfully earned 260,000 pesos in total sales, demonstrating your expertise as a premier butterfly breeder.</p>
            
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #ff6b35;">🎁 Your Rewards:</h3>
                <ul>
                    <li>💰 <strong>₱{prize_amount:,} bonus</strong> added to your ewallet</li>
                    <li>🌟 Elite Level {level} breeder status</li>
                    <li>📈 Enhanced commission rates</li>
                    <li>🏅 Recognition in our breeder community</li>
                </ul>
            </div>
            
            <p>Your ₱{prize_amount:,} prize has been automatically added to your ewallet and is ready to use for purchasing pupae or can be withdrawn through your preferred payment method.</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://your-app-url.replit.app" 
                   style="background-color: #28a745; color: white; padding: 15px 30px; 
                          text-decoration: none; border-radius: 5px; font-weight: bold;">
                    View Your Ewallet Balance
                </a>
            </div>
            
            <p>Thank you for being an outstanding member of our butterfly breeding community. We look forward to supporting your continued success!</p>
            
            <p>Warmest congratulations,<br>
            The Butterfly Breeding Ecosystem Team</p>
        </div>
    </body>
    </html>
    """
    
    message = Mail(
        from_email=Email("noreply@butterflybreeding.com", "Butterfly Breeding Ecosystem"),
        to_emails=To(to_email),
        subject=subject
    )
    
    message.content = Content("text/html", html_content)
    
    try:
        response = sg.send(message)
        return True, f"Congratulations email sent (Status: {response.status_code})"
    except Exception as e:
        return False, f"SendGrid error: {str(e)}"

def bulk_send_premium_notifications():
    """Send premium notifications to all breeders"""
    
    breeders = get_breeder_emails()
    if not breeders:
        return 0, "No breeder emails found"
    
    sent_count = 0
    failed_count = 0
    
    for email, username in breeders:
        success, message = send_premium_notification_email(email, username)
        if success:
            sent_count += 1
        else:
            failed_count += 1
    
    return sent_count, f"Sent {sent_count} emails, {failed_count} failed"

def email_notifications_app():
    """Email notifications management interface"""
    st.title("📧 Email Notifications")
    
    if st.session_state.get('user_role') != 'admin':
        st.error("Admin access required")
        return
    
    # Check SendGrid configuration
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_key:
        st.error("SendGrid API key not configured. Please add SENDGRID_API_KEY to environment variables.")
        st.info("Contact your administrator to configure email notifications.")
        return
    
    st.success("✅ SendGrid configured and ready")
    
    tabs = st.tabs(["📤 Send Notifications", "📊 Email Status"])
    
    with tabs[0]:
        st.subheader("Premium Membership Notifications")
        
        breeders = get_breeder_emails()
        st.info(f"Found {len(breeders)} breeders with email addresses")
        
        if breeders:
            st.write("**Breeder Email List:**")
            for email, username in breeders:
                st.write(f"- {username}: {email}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📧 Send Premium Notifications", type="primary"):
                    with st.spinner("Sending emails..."):
                        sent_count, message = bulk_send_premium_notifications()
                        if sent_count > 0:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")
            
            with col2:
                st.info("This will send premium upgrade notifications to all breeders")
        else:
            st.warning("No breeders with email addresses found")
    
    with tabs[1]:
        st.subheader("Email System Status")
        
        # Test email functionality
        if st.button("Test Email Configuration"):
            test_success, test_message = send_premium_notification_email(
                "test@example.com", "TestUser"
            )
            if test_success:
                st.success("✅ Email system working correctly")
            else:
                st.error(f"❌ Email test failed: {test_message}")

if __name__ == "__main__":
    email_notifications_app()