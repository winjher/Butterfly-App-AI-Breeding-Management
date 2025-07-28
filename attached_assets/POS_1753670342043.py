import streamlit as st
import datetime
import random
import pandas as pd
import csv
from PIL import Image
import io
import base64
import os

# --- Configuration ---
PURCHASE_CSV_FILE = 'butterfly_purchases.csv'
BREEDING_CSV_FILE = 'butterfly_breeding_log.csv'

# Sample data for butterfly items - ADDING 'cost'
ITEMS = {
    1: {"name": "Clipper", "price": 23, "cost": 10},
    2: {"name": "Common Jay", "price": 35, "cost": 15},
    3: {"name": "Common Lime", "price": 43, "cost": 20},
    4: {"name": "Common Mime", "price": 65, "cost": 30},
    5: {"name": "Common Mormon", "price": 48, "cost": 22},
    6: {"name": "Emerald Swallowtail", "price": 65, "cost": 32},
    7: {"name": "Gray Glassy Tiger", "price": 78, "cost": 38},
    8: {"name": "Great Eggfly", "price": 89, "cost": 45},
    9: {"name": "Great Yellow Mormon", "price": 71, "cost": 35},
    10: {"name": "Golden Birdwing", "price": 73, "cost": 36},
    11: {"name": "Paper Kite", "price": 81, "cost": 40},
    12: {"name": "Pink Rose", "price": 34, "cost": 16},
    13: {"name": "Plain Tiger", "price": 39, "cost": 18},
    14: {"name": "Red Lacewing", "price": 100, "cost": 50},
    15: {"name": "Scarlet Mormon", "price": 85, "cost": 42},
    16: {"name": "Tailed Jay", "price": 45, "cost": 21},
    17: {"name": "Atlas Moth", "price": 75, "cost": 37},
    18: {"name": "Giant Silk Moth", "price": 80, "cost": 39},
}

# --- Helper Functions ---

def initialize_purchase_csv():
    """Ensures the purchase CSV file exists with the correct headers."""
    try:
        with open(PURCHASE_CSV_FILE, 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Date', 'OR', 'Image_Filename', 'Quantity', 'Classification_Code',
                'Price_Per_Item', 'Cost_Per_Item', 'Subtotal_Revenue', 'Subtotal_Cost', 'Subtotal_Profit'
            ])
    except FileExistsError:
        pass # File already exists

def initialize_breeding_csv():
    """Ensures the breeding log CSV file exists with the correct headers."""
    try:
        with open(BREEDING_CSV_FILE, 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Breeding_Date', 'Parent_1_Code', 'Parent_2_Code', 'Offspring_Count', 
                'Quality_Score', 'Projected_Profit', 'Next_Feeding_Date', 'Notes' 
            ])
    except FileExistsError:
        pass # File already exists

def generate_order_number():
    """Generates a random order number."""
    return random.randint(100000, 999999)

def add_item_to_session_order(item_id, quantity):
    """Adds an item to the current order in Streamlit's session state."""
    if item_id not in ITEMS:
        st.error("Invalid item ID.")
        return

    item_info = ITEMS[item_id]
    st.session_state.current_order.append({
        "item_id": item_id,
        "name": item_info["name"],
        "price": item_info["price"],
        "cost": item_info["cost"], # Added cost
        "quantity": quantity,
        "subtotal_revenue": item_info["price"] * quantity,
        "subtotal_cost": item_info["cost"] * quantity, # Added subtotal cost
        "subtotal_profit": (item_info["price"] - item_info["cost"]) * quantity # Added subtotal profit
    })

def calculate_order_total(order):
    """Calculates the total revenue for a given order."""
    return sum(item["subtotal_revenue"] for item in order)

def save_purchase_data(row_data):
    """Saves purchase data to the CSV file."""
    with open(PURCHASE_CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row_data)

def save_breeding_data(row_data):
    """Saves breeding data to the CSV file."""
    with open(BREEDING_CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row_data)

def add_glassmorphism_style():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1547743519-c0c169b1b4a3?fit=crop&w=1920&q=80');
            background-size: cover;
            background-attachment: fixed;
        }
        .stSidebar > div:first-child {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }
        .main .block-container {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-top: 20px;
        }
        h1, h2, h3, h4, h5, h6, .stMarkdown, .stSelectbox, .stNumberInput, .stFileUploader, .stTextInput label, .stSelectbox label, .stNumberInput label {
            color: white !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }
        .stTable, .dataframe {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .stTable th, .stTable td, .dataframe th, .dataframe td {
            color: white;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .stButton button {
            background-color: rgba(69, 170, 242, 0.7);
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: rgba(69, 170, 242, 1);
        }
        .stTextInput > div > div > input, .stSelectbox > div > div > input, .stNumberInput > div > div > input {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 5px;
        }
        .stInfo, .stSuccess, .stWarning {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(5px);
            border-radius: 5px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
            padding: 10px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def generate_receipt_html(order_details, img_path, order_number, total_amount, date_time):
    """Generates an HTML string for a customized receipt."""
    receipt_items_html = ""
    for item in order_details:
        receipt_items_html += f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span>{item['quantity']}x {item['name']}</span>
            <span>${item['subtotal_revenue']:.2f}</span>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Purchase Receipt</title>
        <style>
            body {{
                font-family: 'Courier New', Courier, monospace;
                font-size: 12px;
                width: 80mm;
                margin: 0 auto;
                padding: 10px;
                box-sizing: border-box;
                color: #333;
            }}
            .receipt-container {{
                border: 1px dashed #ccc;
                padding: 10px;
            }}
            h3 {{
                text-align: center;
                margin-bottom: 5px;
                font-size: 14px;
            }}
            .header-info, .footer-info {{
                text-align: center;
                margin-bottom: 10px;
            }}
            .item-list {{
                margin-top: 15px;
                border-top: 1px dashed #ccc;
                padding-top: 10px;
                margin-bottom: 15px;
                border-bottom: 1px dashed #ccc;
                padding-bottom: 10px;
            }}
            .total {{
                display: flex;
                justify-content: space-between;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }}
            .thank-you {{
                text-align: center;
                margin-top: 20px;
                font-style: italic;
            }}
            .receipt-image {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: 10px auto;
            }}
        </style>
    </head>
    <body>
        <div class="receipt-container">
            <h3>Butterfly Haven</h3>
            <div class="header-info">
                <span>Date: {date_time}</span><br>
                <span>Order No: #{order_number}</span>
            </div>
            {'<img src="' + img_path + '" class="receipt-image">' if img_path and img_path != "N/A" else ''}
            <div class="item-list">
                {receipt_items_html}
            </div>
            <div class="total">
                <span>TOTAL:</span>
                <span>${total_amount:.2f}</span>
            </div>
            <div class="thank-you">
                Thank you for your purchase!
            </div>
        </div>
        <script>
            window.onload = function() {{
                window.print();
            }};
        </script>
    </body>
    </html>
    """
    return html_content

def set_background_image(image_path):
    """
    Sets a background image for the Streamlit application using CSS.

    Args:
        image_path (str): The path to the local image file.
    """
    try:
        with open(image_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
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
    except FileNotFoundError:
        st.warning(f"Background image '{image_path}' not found. Please ensure it's in the correct path.")


# --- Streamlit App Layout ---

st.set_page_config(page_title="Point of Sale", layout="wide")

add_glassmorphism_style()

# Ensure 'icon/bg.png' is in the correct path relative to your script
# You might need to create an 'icon' folder and place 'bg.png' inside it.
set_background_image('icon/bg.png')


st.title("🦋 Point of Sale")

# Initialize session state for the current order
if 'current_order' not in st.session_state:
    st.session_state.current_order = []
if 'order_number' not in st.session_state:
    st.session_state.order_number = generate_order_number()
if 'last_purchase_details' not in st.session_state:
    st.session_state.last_purchase_details = None

initialize_purchase_csv()
initialize_breeding_csv()

# --- Navigation Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["🛍️ Purchase System", "📊 Profit Analytics", "🌱 Breeding Log", "📈 Dashboard"])

with tab1:
    st.header(f"Purchase Order: #{st.session_state.order_number}")
    current_date_time = datetime.datetime.now()
    st.write(f"Date: {current_date_time.strftime('%A, %B %d, %Y')}")

    st.subheader("Add Items to Order")

    col1, col2 = st.columns(2)
    with col1:
        selected_item_id = st.selectbox(
            "Select Butterfly Classification Code",
            options=list(ITEMS.keys()),
            format_func=lambda x: f"{x} - {ITEMS[x]['name']} (${ITEMS[x]['price']:.2f})"
        )
    with col2:
        quantity = st.number_input("Quantity", min_value=1, value=1, step=1)

    if st.button("Add to Cart"):
        add_item_to_session_order(selected_item_id, quantity)
        st.success(f"Added {quantity} x {ITEMS[selected_item_id]['name']} to cart!")

    st.markdown("---")

    st.subheader("Your Current Order")

    if st.session_state.current_order:
        order_df = pd.DataFrame(st.session_state.current_order)
        order_df = order_df.rename(columns={
            "name": "Butterfly",
            "price": "Unit Price (Revenue)",
            "cost": "Unit Cost",
            "quantity": "Quantity",
            "subtotal_revenue": "Subtotal Revenue",
            "subtotal_cost": "Subtotal Cost",
            "subtotal_profit": "Subtotal Profit"
        })
        st.table(order_df[["Butterfly", "Unit Price (Revenue)", "Unit Cost", "Quantity", "Subtotal Revenue", "Subtotal Cost", "Subtotal Profit"]])
        
        total_revenue_current_order = calculate_order_total(st.session_state.current_order)
        total_cost_current_order = sum(item["subtotal_cost"] for item in st.session_state.current_order)
        net_profit_current_order = total_revenue_current_order - total_cost_current_order

        st.markdown(f"### Current Order Totals:")
        st.markdown(f"- **Total Revenue:** ${total_revenue_current_order:.2f}")
        st.markdown(f"- **Total Cost:** ${total_cost_current_order:.2f}")
        st.markdown(f"- **Net Profit:** ${net_profit_current_order:.2f}")

    else:
        st.info("Your cart is empty. Add some items above!")

    st.markdown("---")

    st.subheader("Upload Butterfly Image (Optional)")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image_filename = None
    image_base64 = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_container_width=True)
        buffered = io.BytesIO()
        image_format = image.format if image.format else 'PNG'
        image.save(buffered, format=image_format)
        image_base64 = f"data:image/{image_format.lower()};base64,{base64.b64encode(buffered.getvalue()).decode()}"
        image_filename = uploaded_file.name
        st.info(f"Image '{image_filename}' uploaded. (Note: Image is not permanently stored in this demo.)")

    st.markdown("---")

    if st.button("Complete Purchase", type="primary"):
        if st.session_state.current_order:
            total_order_revenue = calculate_order_total(st.session_state.current_order)
            purchase_date_time = datetime.datetime.now()
            
            for item in st.session_state.current_order:
                row_data = [
                    purchase_date_time.strftime('%Y-%m-%d %H:%M:%S'), # Date
                    st.session_state.order_number,                  # OR (Order number)
                    image_filename if image_filename else "N/A",    # Image_Filename
                    item["quantity"],                               # Quantity
                    item["item_id"],                                # Classification_Code
                    item["price"],                                  # Price_Per_Item
                    item["cost"],                                   # Cost_Per_Item
                    item["subtotal_revenue"],                       # Subtotal_Revenue
                    item["subtotal_cost"],                          # Subtotal_Cost
                    item["subtotal_profit"]                         # Subtotal_Profit
                ]
                save_purchase_data(row_data)
            
            st.balloons()
            st.success(f"🎉 Purchase complete for Order #{st.session_state.order_number}! Thank you!")
            st.session_state.last_purchase_details = {
                "order": st.session_state.current_order,
                "order_number": st.session_state.order_number,
                "total_amount": total_order_revenue, # This is total revenue for receipt
                "date_time": purchase_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                "image_base64": image_base64
            }
            st.session_state.current_order = []
            st.session_state.order_number = generate_order_number()
            st.rerun()
        else:
            st.warning("Please add items to your cart before completing the purchase.")

    if st.session_state.last_purchase_details:
        st.markdown("---")
        st.subheader("Receipt Options")
        if st.button("🖨️ Print Last Receipt"):
            receipt_html = generate_receipt_html(
                st.session_state.last_purchase_details["order"],
                st.session_state.last_purchase_details["image_base64"],
                st.session_state.last_purchase_details["order_number"],
                st.session_state.last_purchase_details["total_amount"],
                st.session_state.last_purchase_details["date_time"]
            )
            st.components.v1.html(receipt_html, height=1, width=1, scrolling=False)
            st.info("A print dialog should appear. If not, check your browser's pop-up settings or print manually (Ctrl/Cmd + P).")

    st.markdown("---")
    st.subheader("Purchase History")
    try:
        history_df = pd.read_csv(PURCHASE_CSV_FILE)
        st.dataframe(history_df)
    except FileNotFoundError:
        st.info("No purchase history yet.")
    except pd.errors.EmptyDataError:
        st.info("The purchase history file is empty.")


with tab2:
    st.header("📊 Profit Analytics")
    
    try:
        purchase_data = pd.read_csv(PURCHASE_CSV_FILE)

        # Ensure essential columns exist before proceeding with calculations
        required_purchase_cols = ['Subtotal_Revenue', 'Subtotal_Cost', 'Subtotal_Profit', 'Classification_Code']
        if not all(col in purchase_data.columns for col in required_purchase_cols):
            missing_cols = [col for col in required_purchase_cols if col not in purchase_data.columns]
            st.error(f"Missing essential columns in '{PURCHASE_CSV_FILE}'. Please ensure the file has the following columns: {', '.join(missing_cols)}. "
                     "This might happen if the CSV was created with an older version of the app or manually altered. "
                     "Consider deleting the file (and any other related CSVs like the breeding log) and re-running the app to regenerate it with correct headers.")
            # Use st.stop() to prevent further execution if critical columns are missing
            st.stop()


        total_revenue = purchase_data['Subtotal_Revenue'].sum()
        total_costs = purchase_data['Subtotal_Cost'].sum()
        net_profit = total_revenue - total_costs
        
        profit_margin = (net_profit / total_revenue) * 100 if total_revenue > 0 else 0

        st.markdown(f"### Overall Financial Summary")
        st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
        st.metric(label="Total Costs", value=f"${total_costs:,.2f}")
        st.metric(label="Net Profit", value=f"${net_profit:,.2f}")
        st.metric(label="Profit Margin", value=f"{profit_margin:,.2f}%")

        st.markdown("---")
        st.subheader("Profit by Butterfly Classification")

        profit_by_classification = purchase_data.groupby('Classification_Code').agg(
            Total_Revenue=('Subtotal_Revenue', 'sum'),
            Total_Cost=('Subtotal_Cost', 'sum'),
            Total_Profit=('Subtotal_Profit', 'sum')
        ).reset_index()

        profit_by_classification['Butterfly_Name'] = profit_by_classification['Classification_Code'].map(lambda x: ITEMS.get(x, {}).get('name', 'Unknown'))
        profit_by_classification['Profit_Margin'] = (profit_by_classification['Total_Profit'] / profit_by_classification['Total_Revenue']) * 100
        profit_by_classification = profit_by_classification.fillna(0) # Handle division by zero for profit margin

        st.dataframe(profit_by_classification[['Butterfly_Name', 'Classification_Code', 'Total_Revenue', 'Total_Cost', 'Total_Profit', 'Profit_Margin']].sort_values(by="Total_Profit", ascending=False))

    except FileNotFoundError:
        st.info("No purchase data available for profit analytics yet.")
    except pd.errors.EmptyDataError:
        st.info("The purchase data file is empty. Please make some purchases.")
    except Exception as e:
        st.error(f"An unexpected error occurred while calculating profit analytics: {e}. Please ensure your '{PURCHASE_CSV_FILE}' is correctly formatted and contains the expected columns.")


with tab3:
    st.header("🌱 Breeding Log")

    st.subheader("Record New Breeding Event")

    with st.form("breeding_form"):
        breeding_date = st.date_input("Date of Breeding Event", datetime.date.today())
        
        # Using selectbox for parent codes for better UX
        parent_1_code = st.selectbox(
            "Parent Butterfly 1 (Classification Code)",
            options=list(ITEMS.keys()),
            format_func=lambda x: f"{x} - {ITEMS[x]['name']}",
            key="parent1"
        )
        parent_2_code = st.selectbox(
            "Parent Butterfly 2 (Classification Code)",
            options=list(ITEMS.keys()),
            format_func=lambda x: f"{x} - {ITEMS[x]['name']}",
            key="parent2"
        )
        
        offspring_count = st.number_input("Number of Offspring (Larvae/Eggs)", min_value=0, value=1, step=1)
        
        notes = st.text_area("Notes (e.g., condition, successful hatch rate)")

        submitted = st.form_submit_button("Add Breeding Event")
        if submitted:
            if parent_1_code and parent_2_code:
                # Simulate quality score and projected profit for the new batch
                # In a real app, these might come from user input or more complex logic
                simulated_quality = random.uniform(0.5, 1.0) # Random quality between 50% and 100%
                # Simple projection: 50% of offspring survive to sell, at average item price
                avg_item_price = sum(item['price'] for item in ITEMS.values()) / len(ITEMS)
                simulated_projected_profit = offspring_count * 0.5 * avg_item_price * random.uniform(0.8, 1.2) # Adding some variability

                # Simulate next feeding date (e.g., 7 days from breeding date)
                next_feeding_date = breeding_date + datetime.timedelta(days=7)

                row_data = [
                    breeding_date.strftime('%Y-%m-%d'),
                    parent_1_code,
                    parent_2_code,
                    offspring_count,
                    simulated_quality,        # New: Quality Score
                    simulated_projected_profit, # New: Projected Profit
                    next_feeding_date.strftime('%Y-%m-%d'), # New: Next Feeding Date
                    notes
                ]
                save_breeding_data(row_data)
                st.success("Breeding event recorded successfully!")
            else:
                st.warning("Please select both parent butterflies.")

    st.markdown("---")
    st.subheader("Breeding History")
    
    try:
        breeding_df = pd.read_csv(BREEDING_CSV_FILE)
        
        # Map classification codes to names for better readability
        breeding_df['Parent_1_Name'] = breeding_df['Parent_1_Code'].map(lambda x: ITEMS.get(x, {}).get('name', 'Unknown'))
        breeding_df['Parent_2_Name'] = breeding_df['Parent_2_Code'].map(lambda x: ITEMS.get(x, {}).get('name', 'Unknown'))
        
        # Reorder columns for display
        display_breeding_df = breeding_df[['Breeding_Date', 'Parent_1_Name', 'Parent_2_Name', 'Offspring_Count', 'Quality_Score', 'Projected_Profit', 'Next_Feeding_Date', 'Notes']]
        st.dataframe(display_breeding_df)

        st.markdown("---")
        st.subheader("Breeding Statistics")
        total_offspring = breeding_df['Offspring_Count'].sum()
        st.metric(label="Total Offspring Recorded", value=total_offspring)

        # You can add more detailed breeding statistics here, e.g.,
        # offspring by parent pair, successful breeding rates if you add more data points
        offspring_by_parent = breeding_df.groupby(['Parent_1_Name', 'Parent_2_Name'])['Offspring_Count'].sum().reset_index()
        offspring_by_parent.columns = ['Parent 1', 'Parent 2', 'Total Offspring']
        if not offspring_by_parent.empty:
            st.markdown("##### Offspring by Parent Pair:")
            st.dataframe(offspring_by_parent.sort_values(by="Total Offspring", ascending=False))
        else:
            st.info("No breeding statistics available yet.")


    except FileNotFoundError:
        st.info("No breeding history yet. Record a new event above!")
    except pd.errors.EmptyDataError:
        st.info("The breeding log file is empty. Please add some breeding data.")
    except Exception as e:
        st.error(f"An error occurred while loading breeding history: {e}")

with tab4:
    st.header("📈 Breeding Operations Dashboard")

    try:
        breeding_data_df = pd.read_csv(BREEDING_CSV_FILE)
        
        if not breeding_data_df.empty:
            # Ensure essential columns exist before proceeding with calculations
            required_breeding_cols = ['Quality_Score', 'Projected_Profit', 'Offspring_Count', 'Next_Feeding_Date']
            if not all(col in breeding_data_df.columns for col in required_breeding_cols):
                missing_cols = [col for col in required_breeding_cols if col not in breeding_data_df.columns]
                st.error(f"Missing essential columns in '{BREEDING_CSV_FILE}'. Please ensure the file has the following columns: {', '.join(missing_cols)}. "
                         "This might happen if the CSV was created with an older version of the app or manually altered. "
                         "Consider deleting the file (and any other related CSVs like the purchase history) and re-running the app to regenerate it with correct headers.")
                st.stop()


            # Convert 'Next_Feeding_Date' to datetime for comparison
            breeding_data_df['Next_Feeding_Date'] = pd.to_datetime(breeding_data_df['Next_Feeding_Date'])
            
            # --- Active Batches (considering all recorded as active for simplicity in this demo) ---
            active_batches_count = len(breeding_data_df) # All entries are "active" for now

            # --- Projected Profit ---
            total_projected_profit = breeding_data_df['Projected_Profit'].sum()

            # --- Average Quality ---
            average_quality = breeding_data_df['Quality_Score'].mean() * 100 if active_batches_count > 0 else 0

            # --- Average Offspring per Batch ---
            average_offspring_per_batch = breeding_data_df['Offspring_Count'].mean() if active_batches_count > 0 else 0

            # --- Overdue Feedings ---
            current_date = datetime.datetime.now()
            overdue_feedings_count = breeding_data_df[
                breeding_data_df['Next_Feeding_Date'] < current_date
            ].shape[0]

            col_active_batches, col_avg_offspring, col_proj_profit, col_avg_quality, col_overdue = st.columns(5)

            with col_active_batches:
                st.metric(label="Active Batches", value=active_batches_count)
            with col_avg_offspring:
                st.metric(label="Avg Offspring/Batch", value=f"{average_offspring_per_batch:,.1f}")
            with col_proj_profit:
                st.metric(label="Projected Profit", value=f"${total_projected_profit:,.2f}")
            with col_avg_quality:
                st.metric(label="Average Quality", value=f"{average_quality:,.1f}%")
            with col_overdue:
                st.metric(
                    label="Overdue Feedings",
                    value=overdue_feedings_count,
                    delta=f"{overdue_feedings_count} overdue" if overdue_feedings_count > 0 else "0 overdue",
                    delta_color="inverse" if overdue_feedings_count > 0 else "off"
                )
            
            st.markdown("---")
            st.subheader("Feeding Schedule & Alerts")

            if overdue_feedings_count > 0:
                st.error("🚨 **Urgent: Batches require immediate feeding!**")
                overdue_batches_df = breeding_data_df[breeding_data_df['Next_Feeding_Date'] < current_date].copy()
                overdue_batches_df['Parent_1_Name'] = overdue_batches_df['Parent_1_Code'].map(lambda x: ITEMS.get(x, {}).get('name', 'Unknown'))
                overdue_batches_df['Parent_2_Name'] = overdue_batches_df['Parent_2_Code'].map(lambda x: ITEMS.get(x, {}).get('name', 'Unknown'))
                st.dataframe(overdue_batches_df[['Breeding_Date', 'Parent_1_Name', 'Parent_2_Name', 'Offspring_Count', 'Next_Feeding_Date', 'Notes']])
            else:
                st.info("✅ All batches are on schedule for feeding.")
            
            # Upcoming feedings (next 7 days)
            st.subheader("Upcoming Feedings (Next 7 Days)")
            upcoming_feeding_df = breeding_data_df[
                (breeding_data_df['Next_Feeding_Date'] >= current_date) &
                (breeding_data_df['Next_Feeding_Date'] <= current_date + datetime.timedelta(days=7))
            ].copy()

            if not upcoming_feeding_df.empty:
                upcoming_feeding_df['Parent_1_Name'] = upcoming_feeding_df['Parent_1_Code'].map(lambda x: ITEMS.get(x, {}).get('name', 'Unknown'))
                upcoming_feeding_df['Parent_2_Name'] = upcoming_feeding_df['Parent_2_Code'].map(lambda x: ITEMS.get(x, {}).get('name', 'Unknown'))
                st.dataframe(upcoming_feeding_df[['Breeding_Date', 'Parent_1_Name', 'Parent_2_Name', 'Offspring_Count', 'Next_Feeding_Date']])
            else:
                st.info("No feedings scheduled in the next 7 days.")


        else:
            st.info("No breeding data available to display dashboard metrics. Please add breeding events in the 'Breeding Log' tab.")

    except FileNotFoundError:
        st.info("Breeding log file not found. Please ensure it exists or create new breeding records.")
    except pd.errors.EmptyDataError:
        st.info("The breeding log file is empty. Please add some breeding data.")
    except Exception as e:
        st.error(f"An unexpected error occurred while loading dashboard data: {e}. Please ensure your '{BREEDING_CSV_FILE}' is correctly formatted and contains the expected columns.")
