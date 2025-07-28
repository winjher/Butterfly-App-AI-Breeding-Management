import streamlit as st
import pandas as pd
import datetime
import os
from utils.csv_handlers import save_to_csv, load_from_csv
from data.butterfly_species_info import BUTTERFLY_SPECIES_INFO, SPECIES_HOST_PLANTS

def breeding_management_app():
    """Main breeding management application"""
    st.title("🦋 Butterfly Breeding Management System")
    st.caption("Advanced breeding optimization with real-time monitoring")
    
    # Navigation tabs
    tabs = st.tabs([
        "Dashboard", 
        "Cage Management", 
        "Task Management", 
        "Breeding Log",
        "Analytics"
    ])
    
    with tabs[0]:
        breeding_dashboard()
    
    with tabs[1]:
        cage_management()
    
    with tabs[2]:
        task_management()
    
    with tabs[3]:
        breeding_log()
    
    with tabs[4]:
        breeding_analytics()

def breeding_dashboard():
    """Breeding dashboard overview"""
    st.header("Breeding Dashboard")
    
    # Load existing batches
    batches_df = load_from_csv('breeding_batches.csv')
    tasks_df = load_from_csv('breeding_tasks.csv')
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_batches = len(batches_df) if not batches_df.empty else 0
        st.metric("Active Batches", active_batches)
    
    with col2:
        total_larvae = batches_df['larva_count'].sum() if not batches_df.empty else 0
        st.metric("Total Larvae", int(total_larvae))
    
    with col3:
        open_tasks = len(tasks_df[tasks_df['status'] == 'pending']) if not tasks_df.empty else 0
        st.metric("Open Tasks", open_tasks)
    
    with col4:
        healthy_batches = len(batches_df[batches_df['health_status'] == 'healthy']) if not batches_df.empty else 0
        st.metric("Healthy Batches", healthy_batches)
    
    # Recent activity
    st.subheader("Recent Batch Activity")
    if not batches_df.empty:
        recent_batches = batches_df.tail(5)
        st.dataframe(recent_batches, use_container_width=True)
    else:
        st.info("No breeding batches yet. Create your first batch in Cage Management.")
    
    # Alerts and notifications
    st.subheader("System Alerts")
    if not tasks_df.empty:
        overdue_tasks = tasks_df[
            (tasks_df['due_date'] < datetime.datetime.now().strftime('%Y-%m-%d')) & 
            (tasks_df['status'] == 'pending')
        ]
        if not overdue_tasks.empty:
            st.error(f"⚠️ {len(overdue_tasks)} overdue tasks require attention!")
        else:
            st.success("✅ All tasks are up to date")
    else:
        st.info("No tasks scheduled")

def cage_management():
    """Cage and batch management"""
    st.header("Cage Management")
    
    # Create new batch section
    st.subheader("Create New Breeding Batch")
    
    with st.form("create_batch_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            species = st.selectbox(
                "Butterfly Species", 
                options=list(BUTTERFLY_SPECIES_INFO.keys())
            )
            larva_count = st.number_input("Initial Larva Count", min_value=1, value=10)
            cage_id = st.text_input("Cage ID", value=f"CAGE_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}")
        
        with col2:
            health_status = st.selectbox("Health Status", ["healthy", "warning", "critical"])
            stage = st.selectbox("Current Stage", ["egg", "larva", "pupa", "adult"])
            notes = st.text_area("Notes")
        
        submit_batch = st.form_submit_button("Create Batch")
        
        if submit_batch:
            # Create new batch record
            new_batch = {
                'batch_id': cage_id,
                'species': species,
                'stage': stage,
                'larva_count': larva_count,
                'health_status': health_status,
                'created_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'created_by': st.session_state.username,
                'notes': notes
            }
            
            save_to_csv('breeding_batches.csv', new_batch)
            st.success(f"✅ Batch {cage_id} created successfully!")
            st.rerun()
    
    # Display existing batches
    st.subheader("Active Breeding Batches")
    batches_df = load_from_csv('breeding_batches.csv')
    
    if not batches_df.empty:
        # Batch management interface
        for idx, batch in batches_df.iterrows():
            with st.expander(f"🦋 {batch['batch_id']} - {batch['species']} ({batch['stage']})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Larva Count:** {batch['larva_count']}")
                    st.write(f"**Health Status:** {batch['health_status']}")
                    st.write(f"**Created:** {batch['created_date']}")
                
                with col2:
                    # Update larva count
                    new_count = st.number_input(
                        "Update Count", 
                        value=int(batch['larva_count']), 
                        key=f"count_{idx}"
                    )
                    
                    # Update stage
                    new_stage = st.selectbox(
                        "Update Stage",
                        ["egg", "larva", "pupa", "adult"],
                        index=["egg", "larva", "pupa", "adult"].index(batch['stage']),
                        key=f"stage_{idx}"
                    )
                
                with col3:
                    # Update health status
                    new_health = st.selectbox(
                        "Health Status",
                        ["healthy", "warning", "critical"],
                        index=["healthy", "warning", "critical"].index(batch['health_status']),
                        key=f"health_{idx}"
                    )
                    
                    if st.button(f"Update Batch", key=f"update_{idx}"):
                        # Update the batch
                        batches_df.loc[idx, 'larva_count'] = new_count
                        batches_df.loc[idx, 'stage'] = new_stage
                        batches_df.loc[idx, 'health_status'] = new_health
                        batches_df.loc[idx, 'last_updated'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        # Save updated dataframe
                        batches_df.to_csv('breeding_batches.csv', index=False)
                        st.success("Batch updated!")
                        st.rerun()
                
                # Host plant information
                if batch['species'] in SPECIES_HOST_PLANTS:
                    plant_info = SPECIES_HOST_PLANTS[batch['species']]
                    st.info(f"**Host Plants:** {', '.join(plant_info['plant'])}")
                    st.info(f"**Daily Consumption:** {plant_info['dailyConsumption']}g per larva")
    else:
        st.info("No active batches. Create your first batch above.")

def task_management():
    """Task management system"""
    st.header("Task Management")
    
    # Create new task
    st.subheader("Create New Task")
    
    with st.form("create_task_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            task_title = st.text_input("Task Title")
            task_type = st.selectbox("Task Type", [
                "Feeding", "Pest Control", "Cage Cleaning", "Health Check", 
                "Plant Replacement", "Temperature Check", "Humidity Check", 
                "Breeding Record", "Quality Assessment", "Harvest"
            ])
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        with col2:
            due_date = st.date_input("Due Date", value=datetime.date.today())
            assigned_batch = st.text_input("Batch ID (optional)")
            description = st.text_area("Description")
        
        submit_task = st.form_submit_button("Create Task")
        
        if submit_task and task_title:
            new_task = {
                'task_id': f"TASK_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'title': task_title,
                'type': task_type,
                'priority': priority,
                'due_date': due_date.strftime('%Y-%m-%d'),
                'batch_id': assigned_batch,
                'description': description,
                'status': 'pending',
                'created_by': st.session_state.username,
                'created_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            save_to_csv('breeding_tasks.csv', new_task)
            st.success("✅ Task created successfully!")
            st.rerun()
    
    # Display tasks
    st.subheader("Task List")
    tasks_df = load_from_csv('breeding_tasks.csv')
    
    if not tasks_df.empty:
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "pending", "completed", "cancelled"])
        with col2:
            priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
        with col3:
            type_filter = st.selectbox("Filter by Type", ["All"] + tasks_df['type'].unique().tolist())
        
        # Apply filters
        filtered_tasks = tasks_df.copy()
        if status_filter != "All":
            filtered_tasks = filtered_tasks[filtered_tasks['status'] == status_filter]
        if priority_filter != "All":
            filtered_tasks = filtered_tasks[filtered_tasks['priority'] == priority_filter]
        if type_filter != "All":
            filtered_tasks = filtered_tasks[filtered_tasks['type'] == type_filter]
        
        # Display tasks
        for idx, task in filtered_tasks.iterrows():
            with st.expander(f"📋 {task['title']} - {task['priority']} Priority"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Type:** {task['type']}")
                    st.write(f"**Due Date:** {task['due_date']}")
                    st.write(f"**Status:** {task['status']}")
                    st.write(f"**Batch:** {task.get('batch_id', 'N/A')}")
                
                with col2:
                    st.write(f"**Description:** {task['description']}")
                    
                    # Mark as completed
                    if task['status'] == 'pending':
                        if st.button(f"Mark Complete", key=f"complete_{idx}"):
                            tasks_df.loc[idx, 'status'] = 'completed'
                            tasks_df.loc[idx, 'completed_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            tasks_df.to_csv('breeding_tasks.csv', index=False)
                            st.success("Task marked as completed!")
                            st.rerun()
    else:
        st.info("No tasks created yet.")

def breeding_log():
    """Breeding activity log"""
    st.header("Breeding Activity Log")
    
    # Add log entry
    st.subheader("Add Log Entry")
    
    with st.form("log_entry_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            event_type = st.selectbox("Event Type", [
                "Feeding", "Stage Change", "Health Check", "Mortality", 
                "Temperature Change", "Humidity Change", "Cleaning", "Other"
            ])
            batch_id = st.text_input("Batch ID")
        
        with col2:
            event_description = st.text_area("Event Description")
        
        submit_log = st.form_submit_button("Add Log Entry")
        
        if submit_log and event_description:
            new_log_entry = {
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'event_type': event_type,
                'batch_id': batch_id,
                'description': event_description,
                'logged_by': st.session_state.username
            }
            
            save_to_csv('breeding_log.csv', new_log_entry)
            st.success("✅ Log entry added!")
            st.rerun()
    
    # Display log
    st.subheader("Recent Activity Log")
    log_df = load_from_csv('breeding_log.csv')
    
    if not log_df.empty:
        # Sort by timestamp (most recent first)
        log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])
        log_df = log_df.sort_values('timestamp', ascending=False)
        
        # Display recent entries
        st.dataframe(log_df.head(20), use_container_width=True)
        
        # Download full log
        csv_data = log_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Log",
            data=csv_data,
            file_name=f"breeding_log_{datetime.date.today()}.csv",
            mime="text/csv"
        )
    else:
        st.info("No log entries yet.")

def breeding_analytics():
    """Breeding analytics and insights"""
    st.header("Breeding Analytics")
    
    # Load data
    batches_df = load_from_csv('breeding_batches.csv')
    log_df = load_from_csv('breeding_log.csv')
    
    if not batches_df.empty:
        # Species distribution
        st.subheader("Species Distribution")
        species_counts = batches_df['species'].value_counts()
        st.bar_chart(species_counts)
        
        # Stage distribution
        st.subheader("Lifecycle Stage Distribution")
        stage_counts = batches_df['stage'].value_counts()
        st.bar_chart(stage_counts)
        
        # Health status overview
        st.subheader("Health Status Overview")
        health_counts = batches_df['health_status'].value_counts()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Healthy Batches", health_counts.get('healthy', 0))
        with col2:
            st.metric("Warning Status", health_counts.get('warning', 0))
        with col3:
            st.metric("Critical Status", health_counts.get('critical', 0))
        
        # Productivity metrics
        st.subheader("Productivity Metrics")
        total_larvae = batches_df['larva_count'].sum()
        avg_batch_size = batches_df['larva_count'].mean()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Larvae", int(total_larvae))
        with col2:
            st.metric("Average Batch Size", f"{avg_batch_size:.1f}")
        
        # Detailed batch table
        st.subheader("Detailed Batch Information")
        st.dataframe(batches_df, use_container_width=True)
        
    else:
        st.info("No breeding data available for analysis.")
