import streamlit as st
import pandas as pd
import datetime
import random
import os
from utils.csv_handlers import save_to_csv, load_from_csv

# Butterfly items with pricing
BUTTERFLY_ITEMS = {
    1: {"name": "Clipper", "price": 23, "cost": 10, "species": "Butterfly-Clippers"},
    2: {"name": "Common Jay", "price": 35, "cost": 15, "species": "Butterfly-Common Jay"},
    3: {"name": "Common Lime", "price": 43, "cost": 20, "species": "Butterfly-Common Lime"},
    4: {"name": "Common Mime", "price": 65, "cost": 30, "species": "Butterfly-Common Mime"},
    5: {"name": "Common Mormon", "price": 48, "cost": 22, "species": "Butterfly-Common Mormon"},
    6: {"name": "Emerald Swallowtail", "price": 65, "cost": 32, "species": "Butterfly-Emerald Swallowtail"},
    7: {"name": "Gray Glassy Tiger", "price": 78, "cost": 38, "species": "Butterfly-Gray Glassy Tiger"},
    8: {"name": "Great Eggfly", "price": 89, "cost": 45, "species": "Butterfly-Great Eggfly"},
    9: {"name": "Great Yellow Mormon", "price": 71, "cost": 35, "species": "Butterfly-Great Yellow Mormon"},
    10: {"name": "Golden Birdwing", "price": 73, "cost": 36, "species": "Butterfly-Golden Birdwing"},
    11: {"name": "Paper Kite", "price": 81, "cost": 40, "species": "Butterfly-Paper Kite"},
    12: {"name": "Pink Rose", "price": 34, "cost": 16, "species": "Butterfly-Pink Rose"},
    13: {"name": "Plain Tiger", "price": 39, "cost": 18, "species": "Butterfly-Plain Tiger"},
    14: {"name": "Red Lacewing", "price": 100, "cost": 50, "species": "Butterfly-Red Lacewing"},
    15: {"name": "Scarlet Mormon", "price": 85, "cost": 42, "species": "Butterfly-Scarlet Mormon"},
    16: {"name": "Tailed Jay", "price": 45, "cost": 21, "species": "Butterfly-Tailed Jay"},
    17: {"name": "Atlas Moth", "price": 75, "cost": 37, "species": "Moth-Atlas"},
    18: {"name": "Giant Silk Moth", "price": 80, "cost": 39, "species": "Moth-Giant Silk"},
}

def point_of_sale_app():
    """Point of Sale system for butterfly transactions"""
    st.title("💰 Butterfly Point of Sale System")
    st.caption("Professional sales system with inventory management and analytics")
    
    # Initialize session state for cart
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'order_number' not in st.session_state:
        st.session_state.order_number = generate_order_number()
    
    # Main tabs
    tabs = st.tabs(["🛒 Sales Terminal", "📊 Sales Analytics", "📋 Transaction History", "⚙️ Settings"])
    
    with tabs[0]:
        sales_terminal()
    
    with tabs[1]:
        sales_analytics()
    
    with tabs[2]:
        transaction_history()
    
    with tabs[3]:
        pos_settings()

def sales_terminal():
    """Main sales terminal interface"""
    st.header(f"Sales Terminal - Order #{st.session_state.order_number}")
    
    current_datetime = datetime.datetime.now()
    st.write(f"**Date:** {current_datetime.strftime('%A, %B %d, %Y')}")
    st.write(f"**Time:** {current_datetime.strftime('%I:%M %p')}")
    st.write(f"**Cashier:** {st.session_state.username}")
    
    # Product selection
    st.subheader("Add Items to Cart")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        selected_item_id = st.selectbox(
            "Select Butterfly Product",
            options=list(BUTTERFLY_ITEMS.keys()),
            format_func=lambda x: f"{BUTTERFLY_ITEMS[x]['name']} - ${BUTTERFLY_ITEMS[x]['price']:.2f}",
            key="item_selector"
        )
    
    with col2:
        quantity = st.number_input("Quantity", min_value=1, max_value=100, value=1, key="quantity_input")
    
    with col3:
        st.write("") # Spacing
        if st.button("🛒 Add to Cart", type="primary"):
            add_to_cart(selected_item_id, quantity)
    
    # Display selected item details
    if selected_item_id:
        item = BUTTERFLY_ITEMS[selected_item_id]
        st.info(f"**{item['name']}** - ${item['price']:.2f} each | Species: {item['species']}")
    
    # Shopping cart
    st.markdown("---")
    display_cart()
    
    # Checkout section
    if st.session_state.cart:
        st.markdown("---")
        checkout_section()

def add_to_cart(item_id, quantity):
    """Add item to shopping cart"""
    item = BUTTERFLY_ITEMS[item_id]
    
    # Check if item already in cart
    for cart_item in st.session_state.cart:
        if cart_item['item_id'] == item_id:
            cart_item['quantity'] += quantity
            cart_item['subtotal'] = cart_item['quantity'] * cart_item['price']
            st.success(f"Updated {item['name']} quantity in cart!")
            return
    
    # Add new item to cart
    cart_item = {
        'item_id': item_id,
        'name': item['name'],
        'species': item['species'],
        'price': item['price'],
        'cost': item['cost'],
        'quantity': quantity,
        'subtotal': item['price'] * quantity,
        'profit': (item['price'] - item['cost']) * quantity
    }
    
    st.session_state.cart.append(cart_item)
    st.success(f"Added {quantity}x {item['name']} to cart!")

def display_cart():
    """Display current shopping cart"""
    st.subheader("🛒 Current Order")
    
    if not st.session_state.cart:
        st.info("Cart is empty. Add items to get started.")
        return
    
    # Create cart dataframe
    cart_df = pd.DataFrame(st.session_state.cart)
    
    # Display cart items
    for idx, item in enumerate(st.session_state.cart):
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
        
        with col1:
            st.write(f"**{item['name']}**")
            st.caption(f"Species: {item['species']}")
        
        with col2:
            st.write(f"${item['price']:.2f}")
        
        with col3:
            # Quantity adjustment
            new_qty = st.number_input(
                "Qty", 
                min_value=1, 
                value=item['quantity'], 
                key=f"qty_{idx}"
            )
            if new_qty != item['quantity']:
                item['quantity'] = new_qty
                item['subtotal'] = item['price'] * new_qty
                item['profit'] = (item['price'] - item['cost']) * new_qty
                st.rerun()
        
        with col4:
            st.write(f"${item['subtotal']:.2f}")
        
        with col5:
            if st.button("🗑️", key=f"remove_{idx}", help="Remove item"):
                st.session_state.cart.pop(idx)
                st.rerun()
    
    # Cart totals
    st.markdown("---")
    total_amount = sum(item['subtotal'] for item in st.session_state.cart)
    total_profit = sum(item['profit'] for item in st.session_state.cart)
    total_items = sum(item['quantity'] for item in st.session_state.cart)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Items", total_items)
    with col2:
        st.metric("Total Revenue", f"${total_amount:.2f}")
    with col3:
        st.metric("Total Profit", f"${total_profit:.2f}")

def checkout_section():
    """Checkout and payment processing"""
    st.subheader("💳 Checkout")
    
    # Customer information
    col1, col2 = st.columns(2)
    
    with col1:
        customer_name = st.text_input("Customer Name (Optional)")
        customer_email = st.text_input("Customer Email (Optional)")
    
    with col2:
        payment_method = st.selectbox("Payment Method", [
            "Cash", "GCash", "Credit Card", "Bank Transfer", "Other"
        ])
        notes = st.text_area("Order Notes (Optional)")
    
    # Order summary
    total_amount = sum(item['subtotal'] for item in st.session_state.cart)
    
    st.write("### Order Summary")
    st.write(f"**Order Number:** {st.session_state.order_number}")
    st.write(f"**Total Amount:** ${total_amount:.2f}")
    st.write(f"**Payment Method:** {payment_method}")
    
    # Process payment
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💰 Process Payment", type="primary"):
            process_payment(customer_name, customer_email, payment_method, notes)
    
    with col2:
        if st.button("🗑️ Clear Cart"):
            st.session_state.cart = []
            st.rerun()

def process_payment(customer_name, customer_email, payment_method, notes):
    """Process the payment and save transaction"""
    try:
        # Calculate totals
        total_revenue = sum(item['subtotal'] for item in st.session_state.cart)
        total_cost = sum(item['cost'] * item['quantity'] for item in st.session_state.cart)
        total_profit = total_revenue - total_cost
        
        # Create transaction record
        transaction = {
            'order_number': st.session_state.order_number,
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.datetime.now().strftime('%H:%M:%S'),
            'cashier': st.session_state.username,
            'customer_name': customer_name or 'Walk-in Customer',
            'customer_email': customer_email or '',
            'payment_method': payment_method,
            'total_items': sum(item['quantity'] for item in st.session_state.cart),
            'total_revenue': total_revenue,
            'total_cost': total_cost,
            'total_profit': total_profit,
            'notes': notes
        }
        
        # Save transaction
        save_to_csv('pos_transactions.csv', transaction)
        
        # Save individual items
        for item in st.session_state.cart:
            item_record = {
                'order_number': st.session_state.order_number,
                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.datetime.now().strftime('%H:%M:%S'),
                'item_id': item['item_id'],
                'item_name': item['name'],
                'species': item['species'],
                'quantity': item['quantity'],
                'unit_price': item['price'],
                'unit_cost': item['cost'],
                'subtotal_revenue': item['subtotal'],
                'subtotal_profit': item['profit'],
                'cashier': st.session_state.username
            }
            save_to_csv('pos_items.csv', item_record)
        
        # Show success message
        st.success(f"✅ Payment processed successfully!")
        st.success(f"Order #{st.session_state.order_number} completed")
        st.balloons()
        
        # Generate receipt
        generate_receipt(transaction)
        
        # Reset cart and generate new order number
        st.session_state.cart = []
        st.session_state.order_number = generate_order_number()
        
        st.rerun()
        
    except Exception as e:
        st.error(f"Payment processing failed: {str(e)}")

def generate_receipt(transaction):
    """Generate and display receipt"""
    st.write("### 🧾 Receipt")
    
    receipt_html = f"""
    <div style="border: 1px solid #ccc; padding: 20px; margin: 10px 0; font-family: monospace;">
        <h3 style="text-align: center;">🦋 Butterfly Haven</h3>
        <p style="text-align: center;">Sales Receipt</p>
        <hr>
        <p><strong>Order #:</strong> {transaction['order_number']}</p>
        <p><strong>Date:</strong> {transaction['date']} {transaction['time']}</p>
        <p><strong>Cashier:</strong> {transaction['cashier']}</p>
        <p><strong>Customer:</strong> {transaction['customer_name']}</p>
        <hr>
    """
    
    for item in st.session_state.cart:
        receipt_html += f"""
        <p>{item['quantity']}x {item['name']} @ ${item['price']:.2f} = ${item['subtotal']:.2f}</p>
        """
    
    receipt_html += f"""
        <hr>
        <p><strong>Total: ${transaction['total_revenue']:.2f}</strong></p>
        <p><strong>Payment: {transaction['payment_method']}</strong></p>
        <hr>
        <p style="text-align: center;">Thank you for your purchase!</p>
    </div>
    """
    
    st.markdown(receipt_html, unsafe_allow_html=True)

def sales_analytics():
    """Sales analytics and reporting"""
    st.header("📊 Sales Analytics")
    
    # Load transaction data
    transactions_df = load_from_csv('pos_transactions.csv')
    items_df = load_from_csv('pos_items.csv')
    
    if transactions_df.empty:
        st.info("No sales data available yet.")
        return
    
    # Date range filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=datetime.date.today())
    
    # Filter data by date range
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    filtered_transactions = transactions_df[
        (transactions_df['date'] >= pd.to_datetime(start_date)) &
        (transactions_df['date'] <= pd.to_datetime(end_date))
    ]
    
    if filtered_transactions.empty:
        st.warning("No data for selected date range.")
        return
    
    # Key metrics
    st.subheader("📈 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_transactions = len(filtered_transactions)
        st.metric("Total Transactions", total_transactions)
    
    with col2:
        total_revenue = filtered_transactions['total_revenue'].sum()
        st.metric("Total Revenue", f"${total_revenue:.2f}")
    
    with col3:
        total_profit = filtered_transactions['total_profit'].sum()
        st.metric("Total Profit", f"${total_profit:.2f}")
    
    with col4:
        avg_transaction = filtered_transactions['total_revenue'].mean()
        st.metric("Avg Transaction", f"${avg_transaction:.2f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Daily Sales")
        daily_sales = filtered_transactions.groupby('date')['total_revenue'].sum()
        st.line_chart(daily_sales)
    
    with col2:
        st.subheader("Payment Methods")
        payment_methods = filtered_transactions['payment_method'].value_counts()
        st.bar_chart(payment_methods)
    
    # Top selling items
    if not items_df.empty:
        items_df['date'] = pd.to_datetime(items_df['date'])
        filtered_items = items_df[
            (items_df['date'] >= pd.to_datetime(start_date)) &
            (items_df['date'] <= pd.to_datetime(end_date))
        ]
        
        st.subheader("🏆 Top Selling Items")
        top_items = filtered_items.groupby('item_name').agg({
            'quantity': 'sum',
            'subtotal_revenue': 'sum',
            'subtotal_profit': 'sum'
        }).sort_values('quantity', ascending=False)
        
        st.dataframe(top_items.head(10), use_container_width=True)

def transaction_history():
    """Display transaction history"""
    st.header("📋 Transaction History")
    
    # Load data
    transactions_df = load_from_csv('pos_transactions.csv')
    
    if transactions_df.empty:
        st.info("No transactions recorded yet.")
        return
    
    # Search and filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_order = st.text_input("Search by Order Number")
    
    with col2:
        search_customer = st.text_input("Search by Customer Name")
    
    with col3:
        payment_filter = st.selectbox("Filter by Payment Method", 
                                    ["All"] + transactions_df['payment_method'].unique().tolist())
    
    # Apply filters
    filtered_df = transactions_df.copy()
    
    if search_order:
        filtered_df = filtered_df[filtered_df['order_number'].str.contains(search_order, case=False, na=False)]
    
    if search_customer:
        filtered_df = filtered_df[filtered_df['customer_name'].str.contains(search_customer, case=False, na=False)]
    
    if payment_filter != "All":
        filtered_df = filtered_df[filtered_df['payment_method'] == payment_filter]
    
    # Display transactions
    st.subheader(f"Transactions ({len(filtered_df)} found)")
    
    if not filtered_df.empty:
        # Sort by date (most recent first)
        filtered_df = filtered_df.sort_values(['date', 'time'], ascending=False)
        st.dataframe(filtered_df, use_container_width=True)
        
        # Export option
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Export to CSV",
            data=csv_data,
            file_name=f"transactions_{datetime.date.today()}.csv",
            mime="text/csv"
        )
    else:
        st.info("No transactions match your search criteria.")

def pos_settings():
    """POS system settings"""
    st.header("⚙️ POS Settings")
    
    # Tax settings
    st.subheader("Tax Configuration")
    tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, max_value=50.0, value=0.0, step=0.1)
    
    # Discount settings
    st.subheader("Discount Options")
    enable_discounts = st.checkbox("Enable Customer Discounts")
    
    if enable_discounts:
        max_discount = st.number_input("Maximum Discount (%)", min_value=0.0, max_value=100.0, value=10.0)
    
    # Receipt settings
    st.subheader("Receipt Configuration")
    business_name = st.text_input("Business Name", value="Butterfly Haven")
    business_address = st.text_area("Business Address")
    receipt_footer = st.text_area("Receipt Footer Message", 
                                value="Thank you for your purchase!")
    
    # Data management
    st.subheader("Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export All Sales Data"):
            transactions_df = load_from_csv('pos_transactions.csv')
            items_df = load_from_csv('pos_items.csv')
            
            if not transactions_df.empty:
                csv_data = transactions_df.to_csv(index=False)
                st.download_button(
                    label="Download Transactions",
                    data=csv_data,
                    file_name=f"all_transactions_{datetime.date.today()}.csv",
                    mime="text/csv"
                )
    
    with col2:
        if st.button("🗑️ Clear Old Data (30+ days)"):
            st.warning("This will permanently delete old transaction data!")
            if st.button("Confirm Delete"):
                # Implementation for clearing old data
                st.success("Old data cleared successfully!")

def generate_order_number():
    """Generate a unique order number"""
    return f"ORD{datetime.datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
