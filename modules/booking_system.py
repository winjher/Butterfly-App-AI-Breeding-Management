import streamlit as st
import pandas as pd
import datetime
import folium
from streamlit_folium import st_folium
from utils.csv_handlers import save_to_csv, load_from_csv

def booking_system_app():
    """Farm visit booking system"""
    st.title("🌍 Butterfly Farm Booking System")
    st.caption("Book visits to butterfly farms and breeding facilities")
    
    # Main tabs
    tabs = st.tabs(["🎫 Book Visit", "📅 My Bookings", "🏞️ Farm Locations", "⭐ Reviews"])
    
    with tabs[0]:
        book_visit_section()
    
    with tabs[1]:
        my_bookings_section()
    
    with tabs[2]:
        farm_locations_section()
    
    with tabs[3]:
        reviews_section()

def book_visit_section():
    """Book a new farm visit"""
    st.header("🎫 Book Farm Visit")
    
    # Available farms (mock data)
    farms = {
        "Lorica's Butterfly Breeding Farm": {
            "location": "Bunganay, Boac, Marinduque, Philippines",
            "coordinates": [13.391627752131035, 121.83732779599431],
            "description": "Premier butterfly breeding facility with guided tours",
            "price_per_person": 150,
            "max_capacity": 20,
            "specialties": ["Tropical butterflies", "Educational tours", "Photography sessions"]
        },
        "JCM Butterfly Breeding Farm": {
            "location": "Cawit, Boac, Marinduque, Philippines",
            "coordinates": [16.4023, 120.5960],
            "description": "Premier butterfly breeding facility with guided tours",
            "price_per_person": 150,
            "max_capacity": 20,
            "specialties": ["Tropical butterflies", "Educational tours", "Photography sessions"]
        },
        "Marl Insects Farm": {
            "location": "Caganhao, Boac, Marinduque, Philippines",
            "coordinates": [13.402601213675057, 121.82643398620317],
            "description": "Premier butterfly breeding facility with guided tours",
            "price_per_person": 150,
            "max_capacity": 20,
            "specialties": ["Tropical butterflies", "Educational tours", "Photography sessions"]
        },
        "Lyra-Ysabelle Butterfly": {
            "location": "Cawit, Boac, Marinduque, Philippines",
            "coordinates": [13.380662651692896, 121.82747508250148],
            "description": "Premier butterfly breeding facility with guided tours",
            "price_per_person": 150,
            "max_capacity": 20,
            "specialties": ["Tropical butterflies", "Educational tours", "Photography sessions"]
        },
        "Saluciana Integrated and Butterfly Farm": {
            "location": "Sta. Cruz, Marinduque, Philippines",
            "coordinates": [13.43847474827148, 122.0971865954574],
            "description": "Premier butterfly breeding facility with guided tours",
            "price_per_person": 150,
            "max_capacity": 20,
            "specialties": ["Tropical butterflies", "Educational tours", "Photography sessions"]
        },
        "Butterfly Paradise Farm": {
            "location": "Baguio City, Philippines",
            "coordinates": [16.4023, 120.5960],
            "description": "Premier butterfly breeding facility with guided tours",
            "price_per_person": 150,
            "max_capacity": 20,
            "specialties": ["Tropical butterflies", "Educational tours", "Photography sessions"]
        },
        "Rainbow Wings Sanctuary": {
            "location": "Tagaytay, Philippines", 
            "coordinates": [14.1059, 120.9627],
            "description": "Conservation-focused butterfly sanctuary",
            "price_per_person": 120,
            "max_capacity": 15,
            "specialties": ["Conservation education", "Native species", "Research tours"]
        },
        "Monarch Breeding Center": {
            "location": "Los Baños, Laguna",
            "coordinates": [14.1693, 121.2376],
            "description": "Scientific breeding facility with research programs",
            "price_per_person": 200,
            "max_capacity": 12,
            "specialties": ["Research tours", "Breeding techniques", "Student programs"]
        }
    }
    
    # Farm selection
    st.subheader("Select Farm")
    selected_farm = st.selectbox("Choose Farm", list(farms.keys()))
    
    if selected_farm:
        farm_info = farms[selected_farm]
        
        # Display farm information
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**Location:** {farm_info['location']}")
            st.write(f"**Description:** {farm_info['description']}")
            st.write(f"**Price:** ₱{farm_info['price_per_person']} per person")
            st.write(f"**Max Capacity:** {farm_info['max_capacity']} visitors")
            
            st.write("**Specialties:**")
            for specialty in farm_info['specialties']:
                st.write(f"• {specialty}")
        
        with col2:
            # Simple map placeholder
            st.write("**Location Map**")
            st.info("📍 " + farm_info['location'])
            # In a real implementation, you could use folium or another mapping library
            
        st.markdown("---")
        
        # Booking form
        st.subheader("Book Your Visit")
        
        with st.form("booking_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                visit_date = st.date_input(
                    "Visit Date", 
                    min_value=datetime.date.today() + datetime.timedelta(days=1),
                    value=datetime.date.today() + datetime.timedelta(days=7)
                )
                
                visit_time = st.selectbox("Preferred Time", [
                    "09:00 AM - 11:00 AM",
                    "11:00 AM - 01:00 PM", 
                    "01:00 PM - 03:00 PM",
                    "03:00 PM - 05:00 PM"
                ])
                
                num_visitors = st.number_input(
                    "Number of Visitors", 
                    min_value=1, 
                    max_value=farm_info['max_capacity'], 
                    value=1
                )
            
            with col2:
                contact_name = st.text_input("Contact Name")
                contact_phone = st.text_input("Phone Number")
                contact_email = st.text_input("Email Address")
                
                visit_purpose = st.selectbox("Purpose of Visit", [
                    "Educational Tour",
                    "Photography",
                    "Research",
                    "School Field Trip",
                    "Family Outing",
                    "Other"
                ])
            
            special_requests = st.text_area("Special Requests or Notes")
            
            # Calculate total cost
            total_cost = num_visitors * farm_info['price_per_person']
            st.write(f"**Total Cost:** ₱{total_cost}")
            
            # Terms and conditions
            agree_terms = st.checkbox("I agree to the terms and conditions")
            
            submit_booking = st.form_submit_button("📅 Submit Booking Request")
            
            if submit_booking:
                if contact_name and contact_phone and agree_terms:
                    # Create booking record
                    booking_record = {
                        'booking_id': f"BK{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                        'farm_name': selected_farm,
                        'farm_location': farm_info['location'],
                        'visitor_name': contact_name,
                        'visitor_phone': contact_phone,
                        'visitor_email': contact_email,
                        'visit_date': visit_date.strftime('%Y-%m-%d'),
                        'visit_time': visit_time,
                        'num_visitors': num_visitors,
                        'visit_purpose': visit_purpose,
                        'total_cost': total_cost,
                        'special_requests': special_requests,
                        'booking_status': 'Pending',
                        'booked_by': st.session_state.username,
                        'booking_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Save booking
                    save_to_csv('farm_bookings.csv', booking_record)
                    
                    st.success("✅ Booking request submitted successfully!")
                    st.info(f"Booking ID: {booking_record['booking_id']}")
                    st.info("You will receive a confirmation within 24 hours.")
                    
                    # Show booking summary
                    st.write("### Booking Summary")
                    st.write(f"**Farm:** {selected_farm}")
                    st.write(f"**Date:** {visit_date}")
                    st.write(f"**Time:** {visit_time}")
                    st.write(f"**Visitors:** {num_visitors}")
                    st.write(f"**Total Cost:** ₱{total_cost}")
                    
                    st.rerun()
                else:
                    st.error("Please fill in all required fields and agree to terms.")

def my_bookings_section():
    """Display user's bookings"""
    st.header("📅 My Bookings")
    
    # Load user's bookings
    bookings_df = load_from_csv('farm_bookings.csv')
    
    if not bookings_df.empty:
        user_bookings = bookings_df[bookings_df['booked_by'] == st.session_state.username]
        
        if not user_bookings.empty:
            # Booking statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_bookings = len(user_bookings)
                st.metric("Total Bookings", total_bookings)
            
            with col2:
                confirmed_bookings = len(user_bookings[user_bookings['booking_status'] == 'Confirmed'])
                st.metric("Confirmed", confirmed_bookings)
            
            with col3:
                pending_bookings = len(user_bookings[user_bookings['booking_status'] == 'Pending'])
                st.metric("Pending", pending_bookings)
            
            with col4:
                total_spent = user_bookings['total_cost'].sum()
                st.metric("Total Spent", f"₱{total_spent}")
            
            # Display bookings
            st.subheader("Booking History")
            
            # Status filter
            status_filter = st.selectbox("Filter by Status", 
                                       ["All"] + user_bookings['booking_status'].unique().tolist())
            
            if status_filter != "All":
                filtered_bookings = user_bookings[user_bookings['booking_status'] == status_filter]
            else:
                filtered_bookings = user_bookings
            
            # Display each booking
            for idx, booking in filtered_bookings.iterrows():
                with st.expander(f"🎫 {booking['booking_id']} - {booking['farm_name']} ({booking['booking_status']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Farm:** {booking['farm_name']}")
                        st.write(f"**Location:** {booking['farm_location']}")
                        st.write(f"**Date:** {booking['visit_date']}")
                        st.write(f"**Time:** {booking['visit_time']}")
                        st.write(f"**Visitors:** {booking['num_visitors']}")
                    
                    with col2:
                        st.write(f"**Purpose:** {booking['visit_purpose']}")
                        st.write(f"**Total Cost:** ₱{booking['total_cost']}")
                        st.write(f"**Status:** {booking['booking_status']}")
                        st.write(f"**Booked:** {booking['booking_date']}")
                    
                    if booking['special_requests']:
                        st.write(f"**Special Requests:** {booking['special_requests']}")
                    
                    # Action buttons
                    if booking['booking_status'] == 'Pending':
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"Cancel Booking", key=f"cancel_{idx}"):
                                # Update booking status
                                bookings_df.loc[idx, 'booking_status'] = 'Cancelled'
                                bookings_df.to_csv('farm_bookings.csv', index=False)
                                st.success("Booking cancelled successfully!")
                                st.rerun()
                        
                        with col2:
                            if st.button(f"Modify Booking", key=f"modify_{idx}"):
                                st.info("Contact the farm directly to modify your booking.")
            
            # Export bookings
            csv_data = filtered_bookings.to_csv(index=False)
            st.download_button(
                label="📥 Export Bookings",
                data=csv_data,
                file_name=f"my_bookings_{datetime.date.today()}.csv",
                mime="text/csv"
            )
        
        else:
            st.info("No bookings found. Book your first farm visit!")
    
    else:
        st.info("No bookings in the system yet.")

def farm_locations_section():
    """Display farm locations and information"""
    st.header("🏞️ Farm Locations")
    
    # Farm information (expanded)
    farms_info = {
        "Butterfly Paradise Farm": {
            "location": "Baguio City, Philippines",
            "coordinates": [16.4023, 120.5960],
            "description": "Premier butterfly breeding facility with guided tours and educational programs",
            "price_per_person": 150,
            "max_capacity": 20,
            "specialties": ["Tropical butterflies", "Educational tours", "Photography sessions"],
            "operating_hours": "8:00 AM - 5:00 PM",
            "contact": "+63 917 123 4567",
            "email": "info@butterflyparadise.ph",
            "rating": 4.8,
            "facilities": ["Visitor Center", "Gift Shop", "Restaurant", "Parking"]
        },
        "Rainbow Wings Sanctuary": {
            "location": "Tagaytay, Philippines",
            "coordinates": [14.1059, 120.9627],
            "description": "Conservation-focused butterfly sanctuary dedicated to protecting native species",
            "price_per_person": 120,
            "max_capacity": 15,
            "specialties": ["Conservation education", "Native species", "Research tours"],
            "operating_hours": "9:00 AM - 4:00 PM",
            "contact": "+63 918 234 5678",
            "email": "contact@rainbowwings.ph",
            "rating": 4.6,
            "facilities": ["Research Lab", "Nature Trail", "Outdoor Classroom"]
        },
        "Monarch Breeding Center": {
            "location": "Los Baños, Laguna",
            "coordinates": [14.1693, 121.2376],
            "description": "Scientific breeding facility with advanced research programs and university partnerships",
            "price_per_person": 200,
            "max_capacity": 12,
            "specialties": ["Research tours", "Breeding techniques", "Student programs"],
            "operating_hours": "10:00 AM - 3:00 PM (By appointment)",
            "contact": "+63 919 345 6789",
            "email": "research@monarchcenter.ph",
            "rating": 4.9,
            "facilities": ["Research Facility", "Laboratory", "Conference Room", "Library"]
        }
    }
    
    # Display each farm
    for farm_name, farm_info in farms_info.items():
        with st.expander(f"🦋 {farm_name} ⭐ {farm_info['rating']}/5.0"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**📍 Location:** {farm_info['location']}")
                st.write(f"**📝 Description:** {farm_info['description']}")
                st.write(f"**💰 Price:** ₱{farm_info['price_per_person']} per person")
                st.write(f"**👥 Capacity:** {farm_info['max_capacity']} visitors")
                st.write(f"**🕐 Hours:** {farm_info['operating_hours']}")
                
                st.write("**🎯 Specialties:**")
                for specialty in farm_info['specialties']:
                    st.write(f"• {specialty}")
                
                st.write("**🏢 Facilities:**")
                for facility in farm_info['facilities']:
                    st.write(f"• {facility}")
            
            with col2:
                st.write("**📞 Contact Information:**")
                st.write(f"Phone: {farm_info['contact']}")
                st.write(f"Email: {farm_info['email']}")
                
                st.write("**📊 Quick Stats:**")
                st.metric("Rating", f"{farm_info['rating']}/5.0")
                st.metric("Max Visitors", farm_info['max_capacity'])
                
                # Quick booking button
                if st.button(f"📅 Book Visit", key=f"book_{farm_name}"):
                    st.session_state.selected_farm = farm_name
                    st.info(f"Go to 'Book Visit' tab to complete booking for {farm_name}")
    
    # Interactive map (placeholder)
    st.subheader("🗺️ Farm Locations Map")
    st.info("Interactive map showing all butterfly farm locations would be displayed here using Folium or similar mapping library")
    
    # For demonstration, show a simple location list
    st.write("**Farm Coordinates:**")
    for farm_name, farm_info in farms_info.items():
        lat, lon = farm_info['coordinates']
        st.write(f"• {farm_name}: {lat:.4f}, {lon:.4f}")

def reviews_section():
    """Farm reviews and ratings system"""
    st.header("⭐ Farm Reviews")
    
    # Add new review
    st.subheader("Write a Review")
    
    # Load user's bookings to see which farms they've visited
    bookings_df = load_from_csv('farm_bookings.csv')
    user_bookings = bookings_df[
        (bookings_df['booked_by'] == st.session_state.username) & 
        (bookings_df['booking_status'] == 'Confirmed')
    ] if not bookings_df.empty else pd.DataFrame()
    
    if not user_bookings.empty:
        visited_farms = user_bookings['farm_name'].unique().tolist()
        
        with st.form("review_form"):
            farm_to_review = st.selectbox("Select Farm to Review", visited_farms)
            rating = st.selectbox("Rating", [5, 4, 3, 2, 1], format_func=lambda x: f"{x} ⭐")
            review_title = st.text_input("Review Title")
            review_text = st.text_area("Your Review")
            
            # Review categories
            col1, col2 = st.columns(2)
            with col1:
                facilities_rating = st.selectbox("Facilities Rating", [5, 4, 3, 2, 1], key="facilities")
                staff_rating = st.selectbox("Staff Rating", [5, 4, 3, 2, 1], key="staff")
            
            with col2:
                value_rating = st.selectbox("Value for Money", [5, 4, 3, 2, 1], key="value")
                experience_rating = st.selectbox("Overall Experience", [5, 4, 3, 2, 1], key="experience")
            
            submit_review = st.form_submit_button("📝 Submit Review")
            
            if submit_review and review_title and review_text:
                # Create review record
                review_record = {
                    'review_id': f"REV{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'farm_name': farm_to_review,
                    'reviewer': st.session_state.username,
                    'rating': rating,
                    'review_title': review_title,
                    'review_text': review_text,
                    'facilities_rating': facilities_rating,
                    'staff_rating': staff_rating,
                    'value_rating': value_rating,
                    'experience_rating': experience_rating,
                    'review_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Save review
                save_to_csv('farm_reviews.csv', review_record)
                st.success("✅ Review submitted successfully!")
                st.rerun()
    else:
        st.info("You can only review farms you have visited. Book and complete a visit first!")
    
    # Display existing reviews
    st.subheader("Recent Reviews")
    
    reviews_df = load_from_csv('farm_reviews.csv')
    
    if not reviews_df.empty:
        # Review statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_reviews = len(reviews_df)
            st.metric("Total Reviews", total_reviews)
        
        with col2:
            avg_rating = reviews_df['rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.1f} ⭐")
        
        with col3:
            recent_reviews = len(reviews_df[reviews_df['review_date'] >= (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')])
            st.metric("Reviews This Month", recent_reviews)
        
        # Farm filter
        farm_filter = st.selectbox("Filter by Farm", ["All Farms"] + reviews_df['farm_name'].unique().tolist())
        
        if farm_filter != "All Farms":
            filtered_reviews = reviews_df[reviews_df['farm_name'] == farm_filter]
        else:
            filtered_reviews = reviews_df
        
        # Display reviews
        filtered_reviews = filtered_reviews.sort_values('review_date', ascending=False)
        
        for idx, review in filtered_reviews.head(10).iterrows():
            with st.expander(f"⭐ {review['rating']}/5 - {review['review_title']} (by {review['reviewer']})"):
                st.write(f"**Farm:** {review['farm_name']}")
                st.write(f"**Date:** {review['review_date']}")
                st.write(f"**Review:** {review['review_text']}")
                
                # Detailed ratings
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Facilities", f"{review['facilities_rating']}/5")
                with col2:
                    st.metric("Staff", f"{review['staff_rating']}/5")
                with col3:
                    st.metric("Value", f"{review['value_rating']}/5")
                with col4:
                    st.metric("Experience", f"{review['experience_rating']}/5")
        
        # Export reviews
        if not filtered_reviews.empty:
            csv_data = filtered_reviews.to_csv(index=False)
            st.download_button(
                label="📥 Export Reviews",
                data=csv_data,
                file_name=f"farm_reviews_{datetime.date.today()}.csv",
                mime="text/csv"
            )
    
    else:
        st.info("No reviews yet. Be the first to review a farm!")
