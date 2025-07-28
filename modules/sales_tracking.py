import streamlit as st
import pandas as pd
import datetime
import os
from utils.csv_handlers import save_to_csv, load_from_csv

def sales_tracking_app():
    """Sales tracking system for breeders and purchasers"""
    st.title("📊 Sales Tracking System")
    st.caption("Track pupae sales and purchases across the butterfly ecosystem")
    
    # User role tabs
    tabs = st.tabs(["🏪 My Sales", "🛒 My Purchases", "📈 Analytics", "👥 Customer Management"])
    
    with tabs[0]:
        my_sales_section()
    
    with tabs[1]:
        my_purchases_section()
    
    with tabs[2]:
        sales_analytics_section()
    
    with tabs[3]:
        customer_management_section()

def my_sales_section():
    """Track sales made by the current user"""
    st.header("🏪 My Sales Records")
    
    # Add new sale record
    st.subheader("Record New Sale")
    
    with st.form("new_sale_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            buyer_name = st.text_input("Buyer/Customer Name")
            buyer_contact = st.text_input("Buyer Contact (Phone/Email)")
            sale_date = st.date_input("Sale Date", value=datetime.date.today())
        
        with col2:
            butterfly_species = st.selectbox("Butterfly Species", [
                'Butterfly-Clippers', 'Butterfly-Common Jay', 'Butterfly-Common Lime',
                'Butterfly-Common Mime', 'Butterfly-Common Mormon', 'Butterfly-Emerald Swallowtail',
                'Butterfly-Golden Birdwing', 'Butterfly-Great Eggfly', 'Butterfly-Great Yellow Mormon',
                'Butterfly-Gray Glassy Tiger', 'Butterfly-Paper Kite', 'Butterfly-Pink Rose',
                'Butterfly-Plain Tiger', 'Butterfly-Red Lacewing', 'Butterfly-Scarlet Mormon',
                'Butterfly-Tailed Jay', 'Moth-Atlas', 'Moth-Giant Silk'
            ])
            
            pupae_quantity = st.number_input("Pupae Quantity", min_value=1, value=1)
            price_per_unit = st.number_input("Price per Pupa ($)", min_value=0.01, value=5.00, step=0.01)
        
        # Additional details
        stage = st.selectbox("Stage", ["Egg", "Larva", "Pupa", "Adult"])
        quality_grade = st.selectbox("Quality Grade", ["Premium", "Standard", "Basic"])
        payment_method = st.selectbox("Payment Method", ["Cash", "GCash", "Bank Transfer", "Credit Card"])
        notes = st.text_area("Sale Notes")
        
        submit_sale = st.form_submit_button("💰 Record Sale")
        
        if submit_sale and buyer_name:
            # Calculate totals
            total_amount = pupae_quantity * price_per_unit
            
            # Create sale record
            sale_record = {
                'sale_id': f"SALE_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'sale_date': sale_date.strftime('%Y-%m-%d'),
                'seller_username': st.session_state.username,
                'buyer_name': buyer_name,
                'buyer_contact': buyer_contact,
                'species': butterfly_species,
                'stage': stage,
                'quantity': pupae_quantity,
                'price_per_unit': price_per_unit,
                'total_amount': total_amount,
                'quality_grade': quality_grade,
                'payment_method': payment_method,
                'notes': notes,
                'recorded_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Save sale record
            save_to_csv('pupae_sales.csv', sale_record)
            st.success(f"✅ Sale recorded successfully! Total: ${total_amount:.2f}")
            st.rerun()
    
    # Display user's sales
    st.subheader("My Sales History")
    
    sales_df = load_from_csv('pupae_sales.csv')
    
    if not sales_df.empty:
        # Filter for current user's sales
        user_sales = sales_df[sales_df['seller_username'] == st.session_state.username]
        
        if not user_sales.empty:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_sales = len(user_sales)
                st.metric("Total Sales", total_sales)
            
            with col2:
                total_quantity = user_sales['quantity'].sum()
                st.metric("Total Pupae Sold", int(total_quantity))
            
            with col3:
                total_revenue = user_sales['total_amount'].sum()
                st.metric("Total Revenue", f"${total_revenue:.2f}")
            
            with col4:
                avg_price = user_sales['price_per_unit'].mean()
                st.metric("Avg Price/Unit", f"${avg_price:.2f}")
            
            # Sales table with filters
            st.write("### Sales Records")
            
            # Date range filter
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("From Date", value=datetime.date.today() - datetime.timedelta(days=30))
            with col2:
                end_date = st.date_input("To Date", value=datetime.date.today())
            
            # Filter by date
            user_sales['sale_date'] = pd.to_datetime(user_sales['sale_date'])
            filtered_sales = user_sales[
                (user_sales['sale_date'] >= pd.to_datetime(start_date)) &
                (user_sales['sale_date'] <= pd.to_datetime(end_date))
            ]
            
            # Display filtered sales
            if not filtered_sales.empty:
                st.dataframe(filtered_sales.sort_values('sale_date', ascending=False), use_container_width=True)
                
                # Export option
                csv_data = filtered_sales.to_csv(index=False)
                st.download_button(
                    label="📥 Export Sales Data",
                    data=csv_data,
                    file_name=f"my_sales_{start_date}_to_{end_date}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No sales in selected date range.")
        else:
            st.info("No sales recorded yet. Record your first sale above!")
    else:
        st.info("No sales in the system yet.")

def my_purchases_section():
    """Track purchases made by the current user"""
    st.header("🛒 My Purchase Records")
    
    # Add new purchase record
    st.subheader("Record New Purchase")
    
    with st.form("new_purchase_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            seller_name = st.text_input("Seller/Breeder Name")
            seller_contact = st.text_input("Seller Contact")
            purchase_date = st.date_input("Purchase Date", value=datetime.date.today())
        
        with col2:
            butterfly_species = st.selectbox("Butterfly Species", [
                'Butterfly-Clippers', 'Butterfly-Common Jay', 'Butterfly-Common Lime',
                'Butterfly-Common Mime', 'Butterfly-Common Mormon', 'Butterfly-Emerald Swallowtail',
                'Butterfly-Golden Birdwing', 'Butterfly-Great Eggfly', 'Butterfly-Great Yellow Mormon',
                'Butterfly-Gray Glassy Tiger', 'Butterfly-Paper Kite', 'Butterfly-Pink Rose',
                'Butterfly-Plain Tiger', 'Butterfly-Red Lacewing', 'Butterfly-Scarlet Mormon',
                'Butterfly-Tailed Jay', 'Moth-Atlas', 'Moth-Giant Silk'
            ], key="purchase_species")
            
            pupae_quantity = st.number_input("Pupae Quantity", min_value=1, value=1, key="purchase_quantity")
            price_per_unit = st.number_input("Price per Pupa ($)", min_value=0.01, value=5.00, step=0.01, key="purchase_price")
        
        # Additional details
        stage = st.selectbox("Stage", ["Egg", "Larva", "Pupa", "Adult"], key="purchase_stage")
        quality_received = st.selectbox("Quality Received", ["Premium", "Standard", "Basic", "Poor"])
        payment_method = st.selectbox("Payment Method", ["Cash", "GCash", "Bank Transfer", "Credit Card"], key="purchase_payment")
        delivery_method = st.selectbox("Delivery Method", ["Pickup", "Local Delivery", "Shipping", "Meet-up"])
        notes = st.text_area("Purchase Notes", key="purchase_notes")
        
        submit_purchase = st.form_submit_button("🛒 Record Purchase")
        
        if submit_purchase and seller_name:
            # Calculate totals
            total_cost = pupae_quantity * price_per_unit
            
            # Create purchase record
            purchase_record = {
                'purchase_id': f"PURCH_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'purchase_date': purchase_date.strftime('%Y-%m-%d'),
                'buyer_username': st.session_state.username,
                'seller_name': seller_name,
                'seller_contact': seller_contact,
                'species': butterfly_species,
                'stage': stage,
                'quantity': pupae_quantity,
                'price_per_unit': price_per_unit,
                'total_cost': total_cost,
                'quality_received': quality_received,
                'payment_method': payment_method,
                'delivery_method': delivery_method,
                'notes': notes,
                'recorded_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Save purchase record
            save_to_csv('pupae_purchases.csv', purchase_record)
            st.success(f"✅ Purchase recorded successfully! Total: ${total_cost:.2f}")
            st.rerun()
    
    # Display user's purchases
    st.subheader("My Purchase History")
    
    purchases_df = load_from_csv('pupae_purchases.csv')
    
    if not purchases_df.empty:
        # Filter for current user's purchases
        user_purchases = purchases_df[purchases_df['buyer_username'] == st.session_state.username]
        
        if not user_purchases.empty:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_purchases = len(user_purchases)
                st.metric("Total Purchases", total_purchases)
            
            with col2:
                total_quantity = user_purchases['quantity'].sum()
                st.metric("Total Pupae Bought", int(total_quantity))
            
            with col3:
                total_spent = user_purchases['total_cost'].sum()
                st.metric("Total Spent", f"${total_spent:.2f}")
            
            with col4:
                avg_price = user_purchases['price_per_unit'].mean()
                st.metric("Avg Price/Unit", f"${avg_price:.2f}")
            
            # Display purchases table
            st.dataframe(user_purchases.sort_values('purchase_date', ascending=False), use_container_width=True)
            
            # Export option
            csv_data = user_purchases.to_csv(index=False)
            st.download_button(
                label="📥 Export Purchase Data",
                data=csv_data,
                file_name=f"my_purchases_{datetime.date.today()}.csv",
                mime="text/csv"
            )
        else:
            st.info("No purchases recorded yet. Record your first purchase above!")
    else:
        st.info("No purchases in the system yet.")

def sales_analytics_section():
    """Analytics and insights for sales/purchases"""
    st.header("📈 Sales & Purchase Analytics")
    
    # Load data
    sales_df = load_from_csv('pupae_sales.csv')
    purchases_df = load_from_csv('pupae_purchases.csv')
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Analysis Start Date", value=datetime.date.today() - datetime.timedelta(days=30))
    with col2:
        end_date = st.date_input("Analysis End Date", value=datetime.date.today())
    
    # Overall market metrics
    st.subheader("🎯 Market Overview")
    
    if not sales_df.empty and not purchases_df.empty:
        # Filter data by date range
        sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
        purchases_df['purchase_date'] = pd.to_datetime(purchases_df['purchase_date'])
        
        filtered_sales = sales_df[
            (sales_df['sale_date'] >= pd.to_datetime(start_date)) &
            (sales_df['sale_date'] <= pd.to_datetime(end_date))
        ]
        
        filtered_purchases = purchases_df[
            (purchases_df['purchase_date'] >= pd.to_datetime(start_date)) &
            (purchases_df['purchase_date'] <= pd.to_datetime(end_date))
        ]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_transactions = len(filtered_sales) + len(filtered_purchases)
            st.metric("Total Transactions", total_transactions)
        
        with col2:
            total_volume = filtered_sales['quantity'].sum() + filtered_purchases['quantity'].sum()
            st.metric("Total Volume", f"{int(total_volume)} pupae")
        
        with col3:
            total_value = filtered_sales['total_amount'].sum() + filtered_purchases['total_cost'].sum()
            st.metric("Total Market Value", f"${total_value:.2f}")
        
        with col4:
            if not filtered_sales.empty:
                avg_sale_price = filtered_sales['price_per_unit'].mean()
                st.metric("Avg Sale Price", f"${avg_sale_price:.2f}")
        
        # Species popularity
        st.subheader("🦋 Popular Species")
        
        if not filtered_sales.empty:
            species_sales = filtered_sales.groupby('species').agg({
                'quantity': 'sum',
                'total_amount': 'sum',
                'price_per_unit': 'mean'
            }).sort_values('quantity', ascending=False)
            
            st.dataframe(species_sales.head(10), use_container_width=True)
        
        # Price trends
        st.subheader("💰 Price Trends")
        
        if not filtered_sales.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Average Prices by Species**")
                avg_prices = filtered_sales.groupby('species')['price_per_unit'].mean().sort_values(ascending=False)
                st.bar_chart(avg_prices.head(10))
            
            with col2:
                st.write("**Quality Grade Distribution**")
                quality_dist = filtered_sales['quality_grade'].value_counts()
                st.bar_chart(quality_dist)
        
        # User performance (for current user)
        st.subheader("👤 My Performance")
        
        user_sales = filtered_sales[filtered_sales['seller_username'] == st.session_state.username]
        user_purchases = filtered_purchases[filtered_purchases['buyer_username'] == st.session_state.username]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**My Sales Performance**")
            if not user_sales.empty:
                my_revenue = user_sales['total_amount'].sum()
                my_sales_count = len(user_sales)
                my_avg_price = user_sales['price_per_unit'].mean()
                
                st.metric("My Total Revenue", f"${my_revenue:.2f}")
                st.metric("My Sales Count", my_sales_count)
                st.metric("My Avg Price", f"${my_avg_price:.2f}")
            else:
                st.info("No sales data for selected period")
        
        with col2:
            st.write("**My Purchase Performance**")
            if not user_purchases.empty:
                my_spending = user_purchases['total_cost'].sum()
                my_purchase_count = len(user_purchases)
                my_avg_cost = user_purchases['price_per_unit'].mean()
                
                st.metric("My Total Spending", f"${my_spending:.2f}")
                st.metric("My Purchase Count", my_purchase_count)
                st.metric("My Avg Cost", f"${my_avg_cost:.2f}")
            else:
                st.info("No purchase data for selected period")
    
    else:
        st.info("Insufficient data for analysis. Record some sales and purchases first!")

def customer_management_section():
    """Manage customer relationships"""
    st.header("👥 Customer Management")
    
    # Load sales data to get customer information
    sales_df = load_from_csv('pupae_sales.csv')
    
    if not sales_df.empty:
        # Filter for current user's customers
        user_sales = sales_df[sales_df['seller_username'] == st.session_state.username]
        
        if not user_sales.empty:
            # Customer analysis
            st.subheader("📊 Customer Analysis")
            
            customer_stats = user_sales.groupby('buyer_name').agg({
                'quantity': 'sum',
                'total_amount': 'sum',
                'sale_date': 'count'
            }).rename(columns={
                'quantity': 'Total Pupae Bought',
                'total_amount': 'Total Spent',
                'sale_date': 'Number of Orders'
            }).sort_values('Total Spent', ascending=False)
            
            st.dataframe(customer_stats, use_container_width=True)
            
            # Top customers
            st.subheader("🏆 Top Customers")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**By Total Spending**")
                top_spenders = customer_stats.nlargest(5, 'Total Spent')['Total Spent']
                for customer, amount in top_spenders.items():
                    st.write(f"• {customer}: ${amount:.2f}")
            
            with col2:
                st.write("**By Quantity Purchased**")
                top_quantity = customer_stats.nlargest(5, 'Total Pupae Bought')['Total Pupae Bought']
                for customer, qty in top_quantity.items():
                    st.write(f"• {customer}: {int(qty)} pupae")
            
            with col3:
                st.write("**By Order Frequency**")
                top_frequent = customer_stats.nlargest(5, 'Number of Orders')['Number of Orders']
                for customer, orders in top_frequent.items():
                    st.write(f"• {customer}: {int(orders)} orders")
            
            # Customer contact information
            st.subheader("📞 Customer Contacts")
            
            # Get unique customers with contact info
            customer_contacts = user_sales[['buyer_name', 'buyer_contact']].drop_duplicates()
            customer_contacts = customer_contacts[customer_contacts['buyer_contact'] != '']
            
            if not customer_contacts.empty:
                st.dataframe(customer_contacts, use_container_width=True)
                
                # Export customer contacts
                csv_data = customer_contacts.to_csv(index=False)
                st.download_button(
                    label="📥 Export Customer Contacts",
                    data=csv_data,
                    file_name=f"customer_contacts_{datetime.date.today()}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No customer contact information available.")
        
        else:
            st.info("No sales recorded yet. Make some sales to see customer data!")
    
    else:
        st.info("No sales data available.")
