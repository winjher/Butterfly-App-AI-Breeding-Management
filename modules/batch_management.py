# import uuid
# from datetime import datetime, timedelta
# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# # --- External system/database dependencies ---
# from database import create_batch_record, get_user_batches_from_db
# from hostplants import get_host_plants
# from profit_calculator import calculate_batch_profit, get_profit_metrics
# from notifications import send_advance_warning_alert

# # --- Batch Data Model ---
# class CageBatch:
#     """Class to represent a butterfly cage batch"""

#     def __init__(self, species, user_id, stage="egg", initial_count=100):
#         self.cage_id = str(uuid.uuid4())
#         self.species = species
#         self.user_id = user_id
#         self.lifecycle_stage = stage
#         self.initial_count = initial_count
#         self.current_count = initial_count
#         self.start_date = datetime.now()
#         self.survival_rate = 95.0  # Default baseline
#         self.host_plants = get_host_plants(species)
#         self.status = "active"
#         # Cost parameters
#         self.host_plant_cost = 2.0  # per day
#         self.labor_cost = 5.0  # per day
#         self.market_price = 15.0  # per unit
#         self.lifecycle_days = 30  # estimated lifecycle duration
#         # Health tracking
#         self.health_issues = []
#         self.last_inspection = datetime.now()
#         self.foliage_level = 100.0  # percentage

#     def update_stage(self, new_stage):
#         valid_stages = ["egg", "larva", "pupa", "adult"]
#         if new_stage in valid_stages:
#             self.lifecycle_stage = new_stage
#             return True
#         return False

#     def update_survival_rate(self, new_rate):
#         if 0 <= new_rate <= 100:
#             self.survival_rate = new_rate
#             self.current_count = int(self.initial_count * (new_rate / 100))
#             return True
#         return False

#     def add_health_issue(self, issue):
#         self.health_issues.append({
#             'issue': issue,
#             'date': datetime.now(),
#             'resolved': False
#         })

#     def update_foliage_level(self, level):
#         if 0 <= level <= 100:
#             self.foliage_level = level
#             return True
#         return False

#     def get_age_days(self):
#         return (datetime.now() - self.start_date).days

#     def is_critical(self):
#         return (
#             self.foliage_level < 20 or
#             self.survival_rate < 70 or
#             len([issue for issue in self.health_issues if not issue['resolved']]) > 2
#         )

#     def needs_advance_warning(self, minutes_ahead=15):
#         now = datetime.now()
#         warning_time = now + timedelta(minutes=minutes_ahead)
#         last_feeding = getattr(self, 'last_feeding', now - timedelta(hours=8))
#         next_feeding = last_feeding + timedelta(hours=8)
#         if next_feeding <= warning_time:
#             return True, "feeding_due", next_feeding
#         last_cleaning = getattr(self, 'last_cleaning', now - timedelta(hours=24))
#         next_cleaning = last_cleaning + timedelta(hours=24)
#         if next_cleaning <= warning_time:
#             return True, "cleaning_due", next_cleaning
#         next_inspection = self.last_inspection + timedelta(hours=12)
#         if next_inspection <= warning_time:
#             return True, "inspection_due", next_inspection
#         days_in_stage = (now - self.start_date).days
#         stage_durations = {"egg": 7, "larva": 14, "pupa": 10, "adult": 1}
#         expected_duration = stage_durations.get(self.lifecycle_stage, 7)
#         if days_in_stage >= expected_duration - 1:
#             return True, "stage_transition_expected", now + timedelta(days=1)
#         return False, None, None

#     def get_next_task(self):
#         age_days = self.get_age_days()
#         if self.foliage_level < 30:
#             return "Replenish foliage"
#         elif age_days > 7 and self.lifecycle_stage == "egg":
#             return "Check for hatching"
#         elif age_days > 21 and self.lifecycle_stage == "larva":
#             return "Prepare for pupation"
#         elif self.survival_rate < 80:
#             return "Health inspection required"
#         else:
#             return "Routine monitoring"

#     def to_dict(self):
#         return {
#             'batch_id': self.cage_id,
#             'species': self.species,
#             'stage': self.lifecycle_stage,
#             'initial_count': self.initial_count,
#             'current_count': self.current_count,
#             'survival_rate': self.survival_rate,
#             'created_date': self.start_date,
#             'status': self.status,
#             'host_plant_cost': self.host_plant_cost,
#             'labor_cost': self.labor_cost,
#             'market_price': self.market_price,
#             'lifecycle_days': self.lifecycle_days,
#             'foliage_level': self.foliage_level,
#             'health_issues': len(self.health_issues)
#         }

# # --- Batch Management Functions ---
# def create_batch(user_id, species, stage, initial_count, survival_rate, **kwargs):
#     try:
#         batch = CageBatch(species, user_id, stage, initial_count)
#         batch.update_survival_rate(survival_rate)
#         for key, value in kwargs.items():
#             if hasattr(batch, key):
#                 setattr(batch, key, value)
#         batch_id = create_batch_record(
#             user_id=user_id,
#             species=species,
#             stage=stage,
#             initial_count=initial_count,
#             survival_rate=survival_rate,
#             **kwargs
#         )
#         return batch_id
#     except Exception as e:
#         raise Exception(f"Failed to create batch: {str(e)}")

# def get_user_batches(user_id):
#     try:
#         return get_user_batches_from_db(user_id)
#     except Exception as e:
#         st.error(f"Error loading batches: {str(e)}")
#         return []

# def get_batch_details(batch_id):
#     return {
#         'batch_id': batch_id,
#         'details_loaded': True
#     }

# def calculate_batch_metrics(batches):
#     if not batches:
#         return {
#             'total_batches': 0,
#             'avg_survival_rate': 0,
#             'total_profit': 0,
#             'active_species': 0
#         }
#     total_survival = sum([batch.get('survival_rate', 0) for batch in batches])
#     avg_survival = total_survival / len(batches)
#     total_profit = 0
#     for batch in batches:
#         production_cost = (batch.get('host_plant_cost', 2) + batch.get('labor_cost', 5)) * batch.get('lifecycle_days', 30)
#         expected_yield = batch.get('initial_count', 0) * (batch.get('survival_rate', 0) / 100)
#         revenue = expected_yield * batch.get('market_price', 15)
#         total_profit += (revenue - production_cost)
#     active_species = len(set([batch.get('species') for batch in batches if batch.get('species')]))
#     return {
#         'total_batches': len(batches),
#         'avg_survival_rate': avg_survival,
#         'total_profit': total_profit,
#         'active_species': active_species
#     }

# def get_critical_batches(batches):
#     critical = []
#     for batch in batches:
#         survival_rate = batch.get('survival_rate', 100)
#         age_days = (datetime.now() - batch.get('created_date', datetime.now())).days
#         if (survival_rate < 70 or (age_days > 35 and batch.get('status') == 'active')):
#             critical.append(batch)
#     return critical

# def update_batch_status(batch_id, new_status):
#     # Update in database (implement as needed)
#     return True

# def generate_batch_report(batch):
#     report = {
#         'batch_id': batch.get('batch_id', ''),
#         'species': batch.get('species', ''),
#         'current_stage': batch.get('stage', ''),
#         'survival_rate': batch.get('survival_rate', 0),
#         'estimated_profit': 0,
#         'recommendations': [],
#         'alerts': []
#     }
#     if batch.get('survival_rate', 100) < 80:
#         report['recommendations'].append("Consider health inspection and treatment")
#         report['alerts'].append("Low survival rate detected")
#     return report

# def check_advance_warnings(user_id, minutes_ahead=15):
#     user_batches = get_user_batches(user_id)
#     warnings_sent = 0
#     for batch_data in user_batches:
#         batch = CageBatch(batch_data['species'], batch_data['user_id'])
#         batch.cage_id = batch_data['batch_id']
#         batch.survival_rate = batch_data.get('survival_rate', 95)
#         batch.lifecycle_stage = batch_data.get('stage', 'unknown')
#         needs_warning, warning_type, scheduled_time = batch.needs_advance_warning(minutes_ahead)
#         if needs_warning:
#             user_email = batch_data.get('user_email', None)
#             success = send_advance_warning_alert(batch_data, user_email, minutes_ahead)
#             if success:
#                 warnings_sent += 1
#     return warnings_sent

# # --- Dashboard Visualization Functions ---
# def create_survival_dashboard(batches):
#     if not batches:
#         return create_empty_chart("No batch data available")
#     df = pd.DataFrame(batches)
#     fig = px.bar(
#         df,
#         x='species',
#         y='survival_rate',
#         color='stage',
#         title='Survival Rates by Species and Stage',
#         labels={'survival_rate': 'Survival Rate (%)', 'species': 'Species', 'stage': 'Lifecycle Stage'}
#     )
#     fig.update_layout(xaxis_tickangle=-45, height=400, showlegend=True, plot_bgcolor='white')
#     fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Target: 80%")
#     return fig

# def create_profit_dashboard(batches):
#     if not batches:
#         return create_empty_chart("No profit data available")
#     profit_data = []
#     for batch in batches:
#         profit = calculate_batch_profit(batch)
#         profit_data.append({
#             'species': batch.get('species', 'Unknown'),
#             'batch_id': batch.get('batch_id', 'Unknown')[:8],
#             'profit': profit,
#             'survival_rate': batch.get('survival_rate', 0),
#             'stage': batch.get('stage', 'Unknown')
#         })
#     df = pd.DataFrame(profit_data)
#     fig = px.scatter(
#         df,
#         x='survival_rate',
#         y='profit',
#         color='species',
#         hover_data=['batch_id'],
#         title='Profit vs Survival Rate Analysis',
#         labels={'survival_rate': 'Survival Rate (%)', 'profit': 'Profit ($)', 'species': 'Species'}
#     )
#     fig.update_layout(height=400, showlegend=True, plot_bgcolor='white')
#     fig.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Break-even")
#     return fig

# def create_species_distribution_chart(batches):
#     if not batches:
#         return create_empty_chart("No species data available")
#     species_counts = {}
#     for batch in batches:
#         species = batch.get('species', 'Unknown')
#         species_counts[species] = species_counts.get(species, 0) + 1
#     fig = px.pie(
#         values=list(species_counts.values()),
#         names=list(species_counts.keys()),
#         title='Batch Distribution by Species'
#     )
#     fig.update_layout(height=400)
#     return fig

# def create_timeline_chart(batches):
#     if not batches:
#         return create_empty_chart("No timeline data available")
#     timeline_data = []
#     for batch in batches:
#         created_date = batch.get('created_date', datetime.now())
#         if isinstance(created_date, str):
#             try:
#                 created_date = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
#             except:
#                 created_date = datetime.now()
#         timeline_data.append({
#             'batch_id': batch.get('batch_id', 'Unknown')[:8],
#             'species': batch.get('species', 'Unknown'),
#             'created_date': created_date,
#             'stage': batch.get('stage', 'Unknown'),
#             'survival_rate': batch.get('survival_rate', 0)
#         })
#     df = pd.DataFrame(timeline_data)
#     df = df.sort_values('created_date')
#     fig = px.scatter(
#         df,
#         x='created_date',
#         y='species',
#         color='stage',
#         size='survival_rate',
#         hover_data=['batch_id', 'survival_rate'],
#         title='Batch Timeline and Progress'
#     )
#     fig.update_layout(height=400, xaxis_title='Creation Date', yaxis_title='Species')
#     return fig

# def create_health_metrics_dashboard(batches):
#     if not batches:
#         return create_empty_chart("No health data available")
#     fig = make_subplots(
#         rows=2, cols=2,
#         subplot_titles=('Survival Rate Distribution', 'Stage Distribution', 'Health Score by Species', 'Alert Status'),
#         specs=[[{"type": "histogram"}, {"type": "pie"}],
#                [{"type": "bar"}, {"type": "bar"}]]
#     )
#     survival_rates = [batch.get('survival_rate', 0) for batch in batches]
#     fig.add_trace(go.Histogram(x=survival_rates, name='Survival Rate', nbinsx=10), row=1, col=1)
#     stage_counts = {}
#     for batch in batches:
#         stage = batch.get('stage', 'Unknown')
#         stage_counts[stage] = stage_counts.get(stage, 0) + 1
#     fig.add_trace(go.Pie(labels=list(stage_counts.keys()), values=list(stage_counts.values()), name='Stages'), row=1, col=2)
#     species_health = {}
#     for batch in batches:
#         species = batch.get('species', 'Unknown')
#         if species not in species_health:
#             species_health[species] = []
#         species_health[species].append(batch.get('survival_rate', 0))
#     species_avg_health = {species: np.mean(rates) for species, rates in species_health.items()}
#     fig.add_trace(go.Bar(x=list(species_avg_health.keys()), y=list(species_avg_health.values()), name='Avg Health Score'), row=2, col=1)
#     alert_counts = {
#         'Healthy (>80%)': len([b for b in batches if b.get('survival_rate', 0) > 80]),
#         'Warning (60-80%)': len([b for b in batches if 60 <= b.get('survival_rate', 0) <= 80]),
#         'Critical (<60%)': len([b for b in batches if b.get('survival_rate', 0) < 60])
#     }
#     fig.add_trace(go.Bar(x=list(alert_counts.keys()), y=list(alert_counts.values()), name='Alert Status', marker_color=['green', 'orange', 'red']), row=2, col=2)
#     fig.update_layout(height=600, showlegend=False)
#     return fig

# def create_profit_trend_chart(batches, days_back=30):
#     if not batches:
#         return create_empty_chart("No profit trend data available")
#     end_date = datetime.now().date()
#     start_date = end_date - timedelta(days=days_back)
#     daily_profits = {}
#     current_date = start_date
#     while current_date <= end_date:
#         daily_profits[current_date] = 0
#         current_date += timedelta(days=1)
#     for batch in batches:
#         created_date = batch.get('created_date', datetime.now())
#         if isinstance(created_date, str):
#             try:
#                 created_date = datetime.fromisoformat(created_date.replace('Z', '+00:00')).date()
#             except:
#                 created_date = datetime.now().date()
#         elif hasattr(created_date, 'date'):
#             created_date = created_date.date()
#         if start_date <= created_date <= end_date:
#             profit = calculate_batch_profit(batch)
#             daily_profits[created_date] += profit
#     df = pd.DataFrame([
#         {'date': date, 'profit': profit}
#         for date, profit in daily_profits.items()
#     ])
#     fig = px.line(
#         df,
#         x='date',
#         y='profit',
#         title=f'Daily Profit Trend (Last {days_back} days)',
#         labels={'profit': 'Daily Profit ($)', 'date': 'Date'}
#     )
#     fig.update_layout(height=400)
#     return fig

# def create_kpi_cards_data(batches):
#     if not batches:
#         return {
#             'total_batches': 0,
#             'avg_survival': 0,
#             'total_profit': 0,
#             'active_species': 0,
#             'critical_batches': 0
#         }
#     total_batches = len(batches)
#     avg_survival = sum([batch.get('survival_rate', 0) for batch in batches]) / total_batches
#     total_profit = sum([calculate_batch_profit(batch) for batch in batches])
#     active_species = len(set([batch.get('species') for batch in batches]))
#     critical_batches = len([batch for batch in batches if batch.get('survival_rate', 0) < 70])
#     return {
#         'total_batches': total_batches,
#         'avg_survival': avg_survival,
#         'total_profit': total_profit,
#         'active_species': active_species,
#         'critical_batches': critical_batches
#     }

# def create_comparison_chart(batches, metric='survival_rate'):
#     if not batches:
#         return create_empty_chart(f"No {metric} data available")
#     species_data = {}
#     for batch in batches:
#         species = batch.get('species', 'Unknown')
#         if species not in species_data:
#             species_data[species] = []
#         if metric == 'profit':
#             value = calculate_batch_profit(batch)
#         else:
#             value = batch.get(metric, 0)
#         species_data[species].append(value)
#     species_averages = {
#         species: np.mean(values)
#         for species, values in species_data.items()
#     }
#     fig = px.bar(
#         x=list(species_averages.keys()),
#         y=list(species_averages.values()),
#         title=f'Average {metric.replace("_", " ").title()} by Species'
#     )
#     fig.update_layout(height=400, xaxis_tickangle=-45)
#     return fig

# def create_empty_chart(message):
#     fig = go.Figure()
#     fig.add_annotation(
#         text=message,
#         xref="paper", yref="paper",
#         x=0.5, y=0.5,
#         xanchor='center', yanchor='middle',
#         showarrow=False,
#         font=dict(size=16, color="gray")
#     )
#     fig.update_layout(
#         height=400,
#         xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
#         yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
#         plot_bgcolor='white'
#     )
#     return fig

# def create_performance_summary_chart(batches):
#     if not batches:
#         return create_empty_chart("No performance data available")
#     metrics = get_profit_metrics(batches)
#     fig = make_subplots(
#         rows=2, cols=2,
#         specs=[[{"type": "indicator"}, {"type": "indicator"}],
#                [{"type": "indicator"}, {"type": "indicator"}]],
#         subplot_titles=('Avg Survival Rate', 'Profit Margin', 'Batch Efficiency', 'Species Diversity')
#     )
#     avg_survival = sum([b.get('survival_rate', 0) for b in batches]) / len(batches)
#     fig.add_trace(
#         go.Indicator(
#             mode="gauge+number",
#             value=avg_survival,
#             title={'text': "Survival Rate (%)"},
#             gauge={'axis': {'range': [0, 100]},
#                    'bar': {'color': "green" if avg_survival > 80 else "orange" if avg_survival > 60 else "red"},
#                    'steps': [{'range': [0, 60], 'color': "lightgray"},
#                             {'range': [60, 80], 'color': "gray"}],
#                    'threshold': {'line': {'color': "red", 'width': 4},
#                                'thickness': 0.75, 'value': 80}}
#         ),
#         row=1, col=1
#     )
#     profit_margin = metrics.get('overall_margin', 0)
#     fig.add_trace(
#         go.Indicator(
#             mode="gauge+number",
#             value=profit_margin,
#             title={'text': "Profit Margin (%)"},
#             gauge={'axis': {'range': [0, 50]},
#                    'bar': {'color': "green" if profit_margin > 20 else "orange" if profit_margin > 10 else "red"}}
#         ),
#         row=1, col=2
#     )
#     efficiency = len([b for b in batches if b.get('survival_rate', 0) > 80]) / len(batches) * 100
#     fig.add_trace(
#         go.Indicator(
#             mode="gauge+number",
#             value=efficiency,
#             title={'text': "Batch Efficiency (%)"},
#             gauge={'axis': {'range': [0, 100]},
#                    'bar': {'color': "green" if efficiency > 70 else "orange" if efficiency > 50 else "red"}}
#         ),
#         row=2, col=1
#     )
#     species_count = len(set([b.get('species') for b in batches]))
#     fig.add_trace(
#         go.Indicator(
#             mode="number",
#             value=species_count,
#             title={'text': "Active Species"},
#             number={'font': {'size': 40}}
#         ),
#         row=2, col=2
#     )
#     fig.update_layout(height=500)
#     return fig