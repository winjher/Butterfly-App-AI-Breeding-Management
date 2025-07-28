import streamlit as st
import pandas as pd
import datetime
from utils.csv_handlers import save_to_csv, load_from_csv
from modules.ui_components import display_header, create_metric_card, create_info_card

def purchaser_profile_app():
    """Enhanced purchaser profile and purchase management system"""
    display_header("🛒 Purchaser Profile", "Enhanced shopping experience for butterfly enthusiasts", "💳")
    
    # Check if user has purchaser role
    if 'user_role' not in st.session_state or st.session_state.user_role != 'purchaser':
        st.warning("⚠️ This section is optimized for registered purchasers.")
        st.info("Register with 'purchaser' role to access enhanced purchasing features.")
        return
    
    # Purchaser dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Purchase Dashboard", "🛍️ Quick Order", "📋 Order History", "👤 Profile Settings"])
    
    with tab1:
        display_purchase_dashboard()
    
    with tab2:
        display_quick_order_system()
    
    with tab3:
        display_order_history()
    
    with tab4:
        display_profile_settings()

def display_purchase_dashboard():
    """Display purchaser dashboard with metrics and recommendations"""
    st.subheader("📊 Your Purchase Overview")
    
    # Load purchase history
    purchase_history = load_from_csv('purchase_history.csv')
    
    # Calculate metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = len(purchase_history) if not purchase_history.empty else 0
        create_metric_card("Total Orders", str(total_orders))
    
    with col2:
        total_spent = purchase_history['total_amount'].sum() if not purchase_history.empty and 'total_amount' in purchase_history.columns else 0
        create_metric_card("Total Spent", f"₱{total_spent:,.2f}")
    
    with col3:
        avg_order = total_spent / total_orders if total_orders > 0 else 0
        create_metric_card("Avg Order Value", f"₱{avg_order:,.2f}")
    
    with col4:
        this_month_orders = 0
        if not purchase_history.empty and 'purchase_date' in purchase_history.columns:
            current_month = datetime.datetime.now().strftime('%Y-%m')
            this_month_orders = len(purchase_history[purchase_history['purchase_date'].str.startswith(current_month)])
        create_metric_card("This Month", str(this_month_orders))
    
    # Favorite species
    st.subheader("🦋 Your Favorite Species")
    if not purchase_history.empty and 'species' in purchase_history.columns:
        species_counts = purchase_history['species'].value_counts().head(5)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(species_counts)
        with col2:
            st.write("**Top Purchases:**")
            for species, count in species_counts.items():
                st.write(f"• {species}: {count} orders")
    else:
        st.info("No purchase history found. Start shopping to see your preferences!")
    
    # Recommendations
    st.subheader("💡 Recommended for You")
    display_recommendations()

def display_quick_order_system():
    """Enhanced quick order system for frequent purchasers"""
    st.subheader("🛍️ Quick Order System")
    
    # Butterfly species inventory
    butterfly_species = {
        'Butterfly-Common Lime': {'price': 150, 'stock': 25, 'description': 'Beautiful citrus butterfly, perfect for gardens'},
        'Butterfly-Common Mormon': {'price': 200, 'stock': 15, 'description': 'Large black swallowtail with stunning patterns'},
        'Butterfly-Paper Kite': {'price': 180, 'stock': 20, 'description': 'Elegant white butterfly with black markings'},
        'Butterfly-Emerald Swallowtail': {'price': 300, 'stock': 8, 'description': 'Rare green butterfly, collector\'s favorite'},
        'Butterfly-Golden Birdwing': {'price': 500, 'stock': 3, 'description': 'Premium species, very rare and beautiful'},
        'Butterfly-Plain Tiger': {'price': 120, 'stock': 30, 'description': 'Hardy species, great for beginners'},
        'Moth-Atlas': {'price': 250, 'stock': 12, 'description': 'One of the largest moths in the world'},
        'Butterfly-Red Lacewing': {'price': 220, 'stock': 10, 'description': 'Stunning red patterns, eye-catching display'}
    }
    
    # Quick order form
    with st.form("quick_order_form"):
        st.write("**Select Species and Quantities:**")
        
        order_items = []
        total_amount = 0
        
        for species, info in butterfly_species.items():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"**{species}**")
                st.caption(info['description'])
            
            with col2:
                st.write(f"₱{info['price']}")
            
            with col3:
                stock_color = "🟢" if info['stock'] > 10 else "🟡" if info['stock'] > 5 else "🔴"
                st.write(f"{stock_color} {info['stock']}")
            
            with col4:
                quantity = st.number_input(
                    f"Qty", 
                    min_value=0, 
                    max_value=info['stock'], 
                    value=0, 
                    key=f"qty_{species}"
                )
                
                if quantity > 0:
                    item_total = quantity * info['price']
                    order_items.append({
                        'species': species,
                        'quantity': quantity,
                        'unit_price': info['price'],
                        'total': item_total
                    })
                    total_amount += item_total
        
        # Order summary
        if order_items:
            st.subheader("📋 Order Summary")
            summary_df = pd.DataFrame(order_items)
            st.dataframe(summary_df, use_container_width=True)
            
            st.markdown(f"### **Total Amount: ₱{total_amount:,.2f}**")
            
            # Additional options
            col1, col2 = st.columns(2)
            with col1:
                delivery_option = st.selectbox("Delivery Option", 
                                             ["Standard (5-7 days)", "Express (2-3 days)", "Premium (Next day)"])
                special_instructions = st.text_area("Special Instructions", 
                                                  placeholder="Any special handling requests...")
            
            with col2:
                payment_method = st.selectbox("Payment Method", 
                                            ["Cash on Delivery", "GCash", "Bank Transfer", "Credit Card"])
                delivery_address = st.text_area("Delivery Address", 
                                               placeholder="Complete delivery address...")
        
        # Submit order
        submit_order = st.form_submit_button("🛒 Place Order", type="primary")
        
        if submit_order and order_items:
            if delivery_address:
                process_quick_order(order_items, total_amount, delivery_option, payment_method, 
                                  delivery_address, special_instructions)
            else:
                st.error("Please provide delivery address")

def display_order_history():
    """Display comprehensive order history for purchasers"""
    st.subheader("📋 Your Order History")
    
    purchase_history = load_from_csv('purchase_history.csv')
    
    if purchase_history.empty:
        st.info("No purchase history found. Place your first order to see it here!")
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        date_filter = st.selectbox("Time Period", 
                                 ["All Time", "Last 30 days", "Last 90 days", "This Year"])
    with col2:
        status_filter = st.selectbox("Order Status", 
                                   ["All", "Pending", "Processing", "Shipped", "Delivered", "Cancelled"])
    with col3:
        species_filter = st.selectbox("Species", 
                                    ["All Species"] + list(purchase_history['species'].unique()) 
                                    if 'species' in purchase_history.columns else ["All Species"])
    
    # Apply filters
    filtered_history = apply_order_filters(purchase_history, date_filter, status_filter, species_filter)
    
    # Display orders
    if not filtered_history.empty:
        for _, order in filtered_history.iterrows():
            with st.expander(f"Order #{order.get('order_id', 'N/A')} - {order.get('purchase_date', 'N/A')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Species:** {order.get('species', 'N/A')}")
                    st.write(f"**Quantity:** {order.get('quantity', 'N/A')}")
                    st.write(f"**Amount:** ₱{order.get('total_amount', 0):,.2f}")
                
                with col2:
                    status = order.get('status', 'Unknown')
                    status_color = get_status_color(status)
                    st.markdown(f"**Status:** {status_color} {status}")
                    st.write(f"**Payment:** {order.get('payment_method', 'N/A')}")
                    st.write(f"**Delivery:** {order.get('delivery_option', 'N/A')}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"📋 View Details", key=f"details_{order.get('order_id', 'N/A')}"):
                        show_order_details(order)
                with col2:
                    if status in ['Pending', 'Processing']:
                        if st.button(f"❌ Cancel Order", key=f"cancel_{order.get('order_id', 'N/A')}"):
                            cancel_order(order.get('order_id'))
                with col3:
                    if st.button(f"🔄 Reorder", key=f"reorder_{order.get('order_id', 'N/A')}"):
                        reorder_items(order)

def display_profile_settings():
    """Display and manage purchaser profile settings"""
    st.subheader("👤 Profile Settings")
    
    # Load current profile
    profile_data = load_purchaser_profile()
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Personal Information**")
            full_name = st.text_input("Full Name", value=profile_data.get('full_name', ''))
            email = st.text_input("Email", value=profile_data.get('email', ''))
            phone = st.text_input("Phone Number", value=profile_data.get('phone', ''))
            
            st.write("**Preferences**")
            preferred_species = st.multiselect("Preferred Species", 
                                             ["Butterfly-Common Lime", "Butterfly-Common Mormon", 
                                              "Butterfly-Paper Kite", "Butterfly-Emerald Swallowtail"],
                                             default=profile_data.get('preferred_species', []))
        
        with col2:
            st.write("**Delivery Information**")
            default_address = st.text_area("Default Delivery Address", 
                                         value=profile_data.get('default_address', ''))
            preferred_delivery = st.selectbox("Preferred Delivery Option", 
                                            ["Standard", "Express", "Premium"],
                                            index=["Standard", "Express", "Premium"].index(
                                                profile_data.get('preferred_delivery', 'Standard')))
            
            st.write("**Notifications**")
            email_notifications = st.checkbox("Email Notifications", 
                                            value=profile_data.get('email_notifications', True))
            sms_notifications = st.checkbox("SMS Notifications", 
                                          value=profile_data.get('sms_notifications', False))
        
        if st.form_submit_button("💾 Save Profile", type="primary"):
            save_profile_data = {
                'username': st.session_state.username,
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'preferred_species': preferred_species,
                'default_address': default_address,
                'preferred_delivery': preferred_delivery,
                'email_notifications': email_notifications,
                'sms_notifications': sms_notifications,
                'updated_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            save_to_csv('purchaser_profiles.csv', save_profile_data)
            st.success("✅ Profile updated successfully!")

def display_recommendations():
    """Display personalized recommendations for purchasers"""
    recommendations = [
        {
            'species': 'Butterfly-Emerald Swallowtail',
            'reason': 'Based on your preference for colorful species',
            'price': 300,
            'discount': '10% off for returning customers'
        },
        {
            'species': 'Moth-Atlas',
            'reason': 'Popular among collectors like you',
            'price': 250,
            'discount': 'Free shipping on orders over ₱500'
        },
        {
            'species': 'Butterfly-Red Lacewing',
            'reason': 'New arrival, perfect for your collection',
            'price': 220,
            'discount': 'Early bird special - 15% off'
        }
    ]
    
    for rec in recommendations:
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**{rec['species']}**")
                st.caption(rec['reason'])
            
            with col2:
                st.write(f"₱{rec['price']}")
                st.success(rec['discount'])
            
            with col3:
                if st.button("➕ Add", key=f"add_{rec['species']}"):
                    st.session_state[f"quick_add_{rec['species']}"] = True

def process_quick_order(order_items, total_amount, delivery_option, payment_method, 
                       delivery_address, special_instructions):
    """Process the quick order submission"""
    order_id = f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    for item in order_items:
        order_data = {
            'order_id': order_id,
            'username': st.session_state.username,
            'species': item['species'],
            'quantity': item['quantity'],
            'unit_price': item['unit_price'],
            'total_amount': item['total'],
            'delivery_option': delivery_option,
            'payment_method': payment_method,
            'delivery_address': delivery_address,
            'special_instructions': special_instructions,
            'status': 'Pending',
            'purchase_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        save_to_csv('purchase_history.csv', order_data)
    
    st.success(f"✅ Order {order_id} placed successfully!")
    st.info(f"Total amount: ₱{total_amount:,.2f}")
    st.balloons()

def apply_order_filters(purchase_history, date_filter, status_filter, species_filter):
    """Apply filters to purchase history"""
    filtered_df = purchase_history.copy()
    
    # Date filter
    if date_filter != "All Time":
        # Implementation for date filtering
        pass
    
    # Status filter
    if status_filter != "All" and 'status' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['status'] == status_filter]
    
    # Species filter
    if species_filter != "All Species" and 'species' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['species'] == species_filter]
    
    return filtered_df

def get_status_color(status):
    """Get color indicator for order status"""
    colors = {
        'Pending': '🟡',
        'Processing': '🔵',
        'Shipped': '🟠',
        'Delivered': '🟢',
        'Cancelled': '🔴'
    }
    return colors.get(status, '⚪')

def load_purchaser_profile():
    """Load purchaser profile data"""
    profiles = load_from_csv('purchaser_profiles.csv')
    if not profiles.empty and 'username' in profiles.columns:
        user_profile = profiles[profiles['username'] == st.session_state.username]
        if not user_profile.empty:
            return user_profile.iloc[0].to_dict()
    return {}

def show_order_details(order):
    """Show detailed order information"""
    st.info(f"Detailed view for Order #{order.get('order_id', 'N/A')} - Feature coming soon!")

def cancel_order(order_id):
    """Cancel an existing order"""
    st.warning(f"Order {order_id} cancellation requested - Processing...")

def reorder_items(order):
    """Reorder items from previous order"""
    st.info("Adding items to cart for reorder...")