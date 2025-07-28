import streamlit as st
import pandas as pd
import os
import sqlite3
from datetime import datetime
from bcrypt import hashpw, checkpw, gensalt # For password hashing
import folium
from streamlit_folium import st_folium
import math # For distance calculation

# --- Configuration ---
DATABASE_FILE = 'users.db' # SQLite database for user accounts
SALES_CSV_FILE = 'sales_records.csv' # CSV for sales data
BOOKINGS_CSV_FILE = 'booking_records.csv' # CSV for booking data

# --- Geographic Data for Marinduque (Simplified for demonstration) ---
# Approximate coordinates for town centers and example barangays
MARINDUQUE_DATA = {
    "Boac": {
        "coords": (13.4589, 121.8596),
        "barangays": {
            "Isok I": (13.4600, 121.8600),
            "Maligaya": (13.4550, 121.8650),
            "Poras": (13.4500, 121.8550),
            "Santol": (13.4620, 121.8580)
        }
    },
    "Gasan": {
        "coords": (13.3100, 121.8500),
        "barangays": {
            "Bamban": (13.3050, 121.8450),
            "Pinugusan": (13.3150, 121.8520),
            "Antipolo": (13.3000, 121.8550),
            "Tabi": (13.3120, 121.8480)
        }
    },
    "Buenavista": {
        "coords": (13.2500, 121.9333),
        "barangays": {
            "Bagacay": (13.2550, 121.9300),
            "Indan": (13.2450, 121.9350),
            "Malbog": (13.2520, 121.9320),
            "Tungib": (13.2480, 121.9380)
        }
    },
    "Mogpog": {
        "coords": (13.5000, 121.8833),
        "barangays": {
            "Anapog-Sibucao": (13.5050, 121.8800),
            "Balanacan": (13.4950, 121.8850),
            "Gitnang Bayan": (13.5020, 121.8830),
            "Capayang": (13.4980, 121.8810)
        }
    },
    "Santa Cruz": {
        "coords": (13.4500, 122.0167),
        "barangays": {
            "Mabuhay": (13.4550, 122.0150),
            "Tagum": (13.4450, 122.0180),
            "Kasilian": (13.4520, 122.0160),
            "Hupi": (13.4480, 122.0170)
        }
    },
    "Torrijos": {
        "coords": (13.3333, 122.0667),
        "barangays": {
            "Cagpo": (13.3380, 122.0650),
            "Maranlig": (13.3280, 122.0680),
            "Sibuyao": (13.3350, 122.0670),
            "Bangbang": (13.3300, 122.0640)
        }
    }
}

BUTTERFLY_FARM_LOCATION = (13.3200, 121.8600) # Example location near Gasan
BUTTERFLY_FARM_NAME = "Marinduque Butterfly Farm"

# --- Fare Calculation Parameters (example values) ---
BASE_FARE = 50.00  # PHP
RATE_PER_KM = 15.00 # PHP
RATE_PER_MINUTE_TRAVEL = 2.00 # PHP
SURCHARGE_FLAT = 20.00 # PHP (e.g., for peak hours, special handling)
AVERAGE_SPEED_KMPH = 30 # km/h for calculating travel time

# --- Database Functions for User Management ---
def init_db():
    """Initializes the SQLite database and creates the users table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password):
    """Adds a new user to the database after hashing the password."""
    hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("Username already exists!")
        return False
    finally:
        conn.close()

def verify_user(username, password):
    """Verifies a user's password against the hashed password in the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_hashed_password = result[0].encode('utf-8')
        return checkpw(password.encode('utf-8'), stored_hashed_password)
    return False

# --- CSV Functions for Sales Data ---
def save_sale_to_csv(breeder, buyer, quantity, species):
    """Saves a single sale record to the CSV file, including the breeder."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_record = {
        'Timestamp': timestamp,
        'Breeder/Seller': breeder,
        'Purchaser Name': buyer,
        'Quantity': quantity,
        'Species': species
    }
    new_df = pd.DataFrame([new_record])

    if not os.path.exists(SALES_CSV_FILE):
        new_df.to_csv(SALES_CSV_FILE, index=False)
    else:
        new_df.to_csv(SALES_CSV_FILE, mode='a', header=False, index=False)

def load_sales_from_csv(breeder=None):
    """
    Loads all sale records from the CSV file.
    If a breeder is provided, filters the sales for that specific breeder.
    """
    if os.path.exists(SALES_CSV_FILE):
        df = pd.read_csv(SALES_CSV_FILE)
        if breeder:
            return df[df['Breeder/Seller'] == breeder]
        return df # Return all if no breeder specified (e.g., for admin view)
    return pd.DataFrame(columns=['Timestamp', 'Breeder/Seller', 'Purchaser Name', 'Quantity', 'Species'])

# --- CSV Functions for Booking Data ---
def save_booking_to_csv(username, town, barangay, booking_date, adults, children, base_fare, distance_cost, time_cost, surcharges, total_fare, distance_km, travel_time_minutes):
    """Saves a single booking record to the CSV file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_record = {
        'Timestamp': timestamp,
        'Booked By': username,
        'Origin Town': town,
        'Origin Barangay': barangay,
        'Destination': BUTTERFLY_FARM_NAME,
        'Booking Date': booking_date.strftime("%Y-%m-%d"),
        'Adults': adults,
        'Children': children,
        'Distance (km)': f"{distance_km:.2f}",
        'Travel Time (min)': f"{travel_time_minutes:.0f}",
        'Base Fare (PHP)': f"{base_fare:.2f}",
        'Distance Cost (PHP)': f"{distance_cost:.2f}",
        'Time Cost (PHP)': f"{time_cost:.2f}",
        'Surcharges (PHP)': f"{surcharges:.2f}",
        'Total Fare (PHP)': f"{total_fare:.2f}"
    }
    new_df = pd.DataFrame([new_record])

    if not os.path.exists(BOOKINGS_CSV_FILE):
        new_df.to_csv(BOOKINGS_CSV_FILE, index=False)
    else:
        new_df.to_csv(BOOKINGS_CSV_FILE, mode='a', header=False, index=False)

def load_bookings_from_csv(username=None):
    """
    Loads all booking records from the CSV file.
    If a username is provided, filters the bookings for that specific user.
    """
    if os.path.exists(BOOKINGS_CSV_FILE):
        df = pd.read_csv(BOOKINGS_CSV_FILE)
        if username:
            return df[df['Booked By'] == username]
        return df
    return pd.DataFrame(columns=[
        'Timestamp', 'Booked By', 'Origin Town', 'Origin Barangay', 'Destination',
        'Booking Date', 'Adults', 'Children', 'Distance (km)', 'Travel Time (min)',
        'Base Fare (PHP)', 'Distance Cost (PHP)', 'Time Cost (PHP)', 'Surcharges (PHP)', 'Total Fare (PHP)'
    ])

# --- Helper Function for Distance Calculation (Haversine formula) ---
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# --- Streamlit App Layout ---
def login_page():
    """Displays the login and signup forms."""
    st.sidebar.subheader("Login / Sign Up")
    choice = st.sidebar.radio("Go to", ["Login", "Sign Up"])

    if choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.sidebar.success(f"Welcome, {username}!")
                st.rerun() # Rerun to switch to the main app
            else:
                st.sidebar.error("Invalid Username or Password")

    elif choice == "Sign Up":
        new_username = st.sidebar.text_input("New Username")
        new_password = st.sidebar.text_input("New Password", type="password")
        confirm_password = st.sidebar.text_input("Confirm Password", type="password")

        if st.sidebar.button("Sign Up"):
            if new_password == confirm_password:
                if add_user(new_username, new_password):
                    st.sidebar.success("Account created! Please login.")
                else:
                    # Error handled by add_user already
                    pass
            else:
                st.sidebar.error("Passwords do not match.")

def main_app():
    """The main application logic after a user is logged in."""
    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        del st.session_state.username
        st.rerun() # Rerun to go back to login page

    st.title(f"Welcome, {st.session_state.username}!")

    tab1, tab2 = st.tabs(["🦋 Butterfly Farm Booking", "🐛 Pupae Sales Tracker"])

    with tab1:
        st.header("Book Your Trip to Marinduque Butterfly Farm!")
        st.write("Select your origin and book your visit. Fare will be calculated automatically.")

        col1, col2 = st.columns(2)

        with col1:
            selected_town = st.selectbox("Select your Town:", list(MARINDUQUE_DATA.keys()))
            
            # Get barangays for the selected town
            barangays_in_town = MARINDUQUE_DATA[selected_town]["barangays"]
            selected_barangay = st.selectbox("Select your Barangay:", list(barangays_in_town.keys()))

            origin_coords = barangays_in_town[selected_barangay]
            
            st.markdown("---")
            st.subheader("Trip Details")
            booking_date = st.date_input("Select Booking Date:", min_value=datetime.today().date())
            num_adults = st.number_input("Number of Adults:", min_value=1, value=1)
            num_children = st.number_input("Number of Children:", min_value=0, value=0)

        with col2:
            st.subheader("Marinduque Map")
            # Create a Folium map centered on Marinduque
            m = folium.Map(location=[13.4, 121.9], zoom_start=10)

            # Add marker for Butterfly Farm
            folium.Marker(
                location=BUTTERFLY_FARM_LOCATION,
                popup=BUTTERFLY_FARM_NAME,
                icon=folium.Icon(color='green', icon='leaf', prefix='fa')
            ).add_to(m)

            # Add marker for the selected origin
            folium.Marker(
                location=origin_coords,
                popup=f"Your Origin: {selected_barangay}, {selected_town}",
                icon=folium.Icon(color='blue', icon='home', prefix='fa')
            ).add_to(m)

            # Draw a line between origin and destination
            folium.PolyLine([origin_coords, BUTTERFLY_FARM_LOCATION], color="red", weight=2.5, opacity=1).add_to(m)

            # Display the map
            st_folium(m, width=600, height=400) # Ensure map is responsive

        # Calculate fare
        distance_km = haversine_distance(origin_coords[0], origin_coords[1], BUTTERFLY_FARM_LOCATION[0], BUTTERFLY_FARM_LOCATION[1])
        travel_time_minutes = (distance_km / AVERAGE_SPEED_KMPH) * 60

        # Fare components
        fare_base = BASE_FARE
        fare_distance_cost = distance_km * RATE_PER_KM
        fare_time_cost = travel_time_minutes * RATE_PER_MINUTE_TRAVEL
        fare_surcharges = SURCHARGE_FLAT # Example flat surcharge

        total_fare = fare_base + fare_distance_cost + fare_time_cost + fare_surcharges

        st.markdown("---")
        st.subheader("Payment Details")
        st.write(f"**Origin:** {selected_barangay}, {selected_town}")
        st.write(f"**Destination:** {BUTTERFLY_FARM_NAME}")
        st.write(f"**Estimated Distance:** `{distance_km:.2f}` km")
        st.write(f"**Estimated Travel Time:** `{travel_time_minutes:.0f}` minutes")
        st.write(f"**Base Fare:** `PHP {fare_base:.2f}`")
        st.write(f"**Distance Cost:** `PHP {fare_distance_cost:.2f}` (`{RATE_PER_KM:.2f}` PHP/km)")
        st.write(f"**Time Cost:** `PHP {fare_time_cost:.2f}` (`{RATE_PER_MINUTE_TRAVEL:.2f}` PHP/min)")
        st.write(f"**Surcharges:** `PHP {fare_surcharges:.2f}`")
        st.markdown(f"**Total Fare:** `PHP {total_fare:.2f}`")

        if st.button("Confirm Booking"):
            save_booking_to_csv(
                st.session_state.username, selected_town, selected_barangay,
                booking_date, num_adults, num_children,
                fare_base, fare_distance_cost, fare_time_cost, fare_surcharges, total_fare,
                distance_km, travel_time_minutes
            )
            st.success(f"Booking confirmed for {booking_date.strftime('%Y-%m-%d')}! Total fare: PHP {total_fare:.2f}")
            st.rerun()

        st.markdown("---")
        st.subheader(f"Your Past Bookings ({st.session_state.username})")
        bookings_df = load_bookings_from_csv(st.session_state.username)
        if not bookings_df.empty:
            st.dataframe(bookings_df.sort_values(by='Timestamp', ascending=False))
        else:
            st.info("No bookings recorded yet. Make a new booking above!")

    with tab2:
        st.header(f"Pupae Sales Tracker for {st.session_state.username}")
        st.header("Enter Sale Information")

        buyer_name = st.text_input("Purchaser/Buyer Name:")

        all_species = [
            'Butterfly-Clippers', 'Butterfly-Common Jay', 'Butterfly-Common Lime',
            'Butterfly-Common Mime', 'Butterfly-Common Mormon', 'Butterfly-Emerald Swallowtail',
            'Butterfly-Golden Birdwing', 'Butterfly-Great Eggfly', 'Butterfly-Great Yellow Mormon',
            'Butterfly-Grey Glassy Tiger', 'Butterfly-Paper Kite', 'Butterfly-Pink Rose',
            'Butterfly-Plain Tiger', 'Butterfly-Red Lacewing', 'Butterfly-Scarlet Mormon',
            'Butterfly-Tailed Jay', 'Moth_Atlas', 'Moth-GiantSilk',
        ]

        pupae_quantity = st.number_input("Quantity of Pupae:", min_value=1, value=10)
        pupae_species = st.selectbox("Species:", all_species)

        st.write("---")

        if st.button("Record Sale"):
            if buyer_name:
                save_sale_to_csv(st.session_state.username, buyer_name, pupae_quantity, pupae_species)
                st.success(f"Sale Recorded for: **{buyer_name}** and saved!")
                st.rerun() # Refresh the displayed sales
            else:
                st.warning("Please enter the **Purchaser/Buyer Name** before recording the sale.")

        st.write("---")
        st.subheader(f"Your Recent Sales ({st.session_state.username})")

        sales_df = load_sales_from_csv(st.session_state.username) # Load only current user's sales
        if not sales_df.empty:
            st.dataframe(sales_df.sort_values(by='Timestamp', ascending=False))
        else:
            st.info("No sales recorded yet. Start by entering a new sale above!")

def main():
    """Main entry point of the Streamlit application."""
    init_db() # Ensure database is initialized

    # Initialize session state for login if not already present
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        main_app()
    else:
        login_page()

if __name__ == "__main__":
    main()

