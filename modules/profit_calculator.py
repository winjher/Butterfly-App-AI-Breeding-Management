# """
# Profit calculation and optimization engine for butterfly farming operations.
# Calculates profitability based on production costs, survival rates, and market prices.
# """

# from datetime import datetime, timedelta
# from data.butterfly_species_info import get_pupae_quality_score
# def calculate_batch_app():
        
#     def calculate_batch_profit(batch):
#         """Calculate profit for a single batch"""
#         try:
#             # Get batch parameters
#             initial_count = batch.get('initial_count', 0)
#             survival_rate = batch.get('survival_rate', 0) / 100  # Convert to decimal
#             lifecycle_days = batch.get('lifecycle_days', 30)
#             host_plant_cost = batch.get('host_plant_cost', 2.0)
#             labor_cost = batch.get('labor_cost', 5.0)
#             market_price = batch.get('market_price', 15.0)
            
#             # Calculate costs
#             daily_cost = host_plant_cost + labor_cost
#             total_production_cost = daily_cost * lifecycle_days
            
#             # Calculate revenue
#             expected_yield = initial_count * survival_rate
#             total_revenue = expected_yield * market_price
            
#             # Calculate net profit
#             net_profit = total_revenue - total_production_cost
            
#             return net_profit
            
#         except Exception as e:
#             print(f"Error calculating profit: {e}")
#             return 0.0

#     def calculate_detailed_profit_analysis(batch):
#         """Calculate detailed profit analysis with breakdown"""
#         try:
#             initial_count = batch.get('initial_count', 0)
#             survival_rate = batch.get('survival_rate', 0) / 100
#             lifecycle_days = batch.get('lifecycle_days', 30)
#             host_plant_cost_daily = batch.get('host_plant_cost', 2.0)
#             labor_cost_daily = batch.get('labor_cost', 5.0)
#             market_price = batch.get('market_price', 15.0)
#             species = batch.get('species', '')
            
#             # Cost breakdown
#             total_host_plant_cost = host_plant_cost_daily * lifecycle_days
#             total_labor_cost = labor_cost_daily * lifecycle_days
            
#             # Additional costs (equipment, utilities, etc.)
#             equipment_cost = lifecycle_days * 0.5  # $0.50 per day
#             utilities_cost = lifecycle_days * 1.0  # $1.00 per day
            
#             total_production_cost = total_host_plant_cost + total_labor_cost + equipment_cost + utilities_cost
            
#             # Revenue calculation
#             expected_yield = initial_count * survival_rate
#             gross_revenue = expected_yield * market_price
            
#             # Quality adjustments (if pupae defects are considered)
#             quality_adjustment = 1.0  # Default no adjustment
#             adjusted_revenue = gross_revenue * quality_adjustment
            
#             # Profit calculation
#             net_profit = adjusted_revenue - total_production_cost
#             profit_margin = (net_profit / adjusted_revenue * 100) if adjusted_revenue > 0 else 0
            
#             # ROI calculation
#             roi = (net_profit / total_production_cost * 100) if total_production_cost > 0 else 0
            
#             return {
#                 'initial_count': initial_count,
#                 'expected_yield': expected_yield,
#                 'survival_rate_percent': survival_rate * 100,
#                 'lifecycle_days': lifecycle_days,
#                 'costs': {
#                     'host_plant': total_host_plant_cost,
#                     'labor': total_labor_cost,
#                     'equipment': equipment_cost,
#                     'utilities': utilities_cost,
#                     'total': total_production_cost
#                 },
#                 'revenue': {
#                     'gross': gross_revenue,
#                     'adjusted': adjusted_revenue,
#                     'quality_factor': quality_adjustment
#                 },
#                 'profit': {
#                     'net': net_profit,
#                     'margin_percent': profit_margin,
#                     'roi_percent': roi
#                 },
#                 'unit_economics': {
#                     'cost_per_unit': total_production_cost / expected_yield if expected_yield > 0 else 0,
#                     'revenue_per_unit': market_price,
#                     'profit_per_unit': net_profit / expected_yield if expected_yield > 0 else 0
#                 }
#             }
            
#         except Exception as e:
#             print(f"Error in detailed profit analysis: {e}")
#             return None

#     def optimize_batch_parameters(species, target_profit, market_constraints=None):
#         """Optimize batch parameters to achieve target profit"""
#         if market_constraints is None:
#             market_constraints = {
#                 'max_initial_count': 500,
#                 'min_survival_rate': 70,
#                 'max_lifecycle_days': 45,
#                 'market_price_range': (10, 25)
#             }
        
#         best_params = None
#         best_profit = 0
        
#         # Parameter ranges to test
#         count_range = range(50, market_constraints['max_initial_count'] + 1, 50)
#         survival_range = range(market_constraints['min_survival_rate'], 101, 5)
#         price_range = [p for p in range(int(market_constraints['market_price_range'][0]), 
#                                     int(market_constraints['market_price_range'][1]) + 1)]
        
#         for initial_count in count_range:
#             for survival_rate in survival_range:
#                 for market_price in price_range:
#                     # Create test batch
#                     test_batch = {
#                         'initial_count': initial_count,
#                         'survival_rate': survival_rate,
#                         'lifecycle_days': 30,  # Standard lifecycle
#                         'host_plant_cost': 2.0,
#                         'labor_cost': 5.0,
#                         'market_price': market_price,
#                         'species': species
#                     }
                    
#                     profit = calculate_batch_profit(test_batch)
                    
#                     if profit >= target_profit and profit > best_profit:
#                         best_profit = profit
#                         best_params = test_batch.copy()
        
#         return {
#             'optimal_parameters': best_params,
#             'projected_profit': best_profit,
#             'achieves_target': best_profit >= target_profit
#         }

#     def get_profit_metrics(batches):
#         """Calculate aggregate profit metrics for multiple batches"""
#         if not batches:
#             return {
#                 'total_profit': 0,
#                 'avg_profit': 0,
#                 'best_species': 'None',
#                 'worst_species': 'None',
#                 'total_revenue': 0,
#                 'total_costs': 0,
#                 'overall_margin': 0
#             }
        
#         total_profit = 0
#         total_revenue = 0
#         total_costs = 0
#         species_profits = {}
        
#         for batch in batches:
#             profit = calculate_batch_profit(batch)
#             total_profit += profit
            
#             # Calculate revenue and costs for this batch
#             initial_count = batch.get('initial_count', 0)
#             survival_rate = batch.get('survival_rate', 0) / 100
#             lifecycle_days = batch.get('lifecycle_days', 30)
#             host_plant_cost = batch.get('host_plant_cost', 2.0)
#             labor_cost = batch.get('labor_cost', 5.0)
#             market_price = batch.get('market_price', 15.0)
            
#             batch_costs = (host_plant_cost + labor_cost) * lifecycle_days
#             batch_revenue = initial_count * survival_rate * market_price
            
#             total_costs += batch_costs
#             total_revenue += batch_revenue
            
#             # Track by species
#             species = batch.get('species', 'Unknown')
#             if species not in species_profits:
#                 species_profits[species] = []
#             species_profits[species].append(profit)
        
#         # Calculate species averages
#         species_avg_profits = {}
#         for species, profits in species_profits.items():
#             species_avg_profits[species] = sum(profits) / len(profits)
        
#         best_species = max(species_avg_profits.keys(), key=lambda x: species_avg_profits[x]) if species_avg_profits else 'None'
#         worst_species = min(species_avg_profits.keys(), key=lambda x: species_avg_profits[x]) if species_avg_profits else 'None'
        
#         overall_margin = ((total_profit / total_revenue) * 100) if total_revenue > 0 else 0
        
#         return {
#             'total_profit': total_profit,
#             'avg_profit': total_profit / len(batches),
#             'best_species': best_species,
#             'worst_species': worst_species,
#             'total_revenue': total_revenue,
#             'total_costs': total_costs,
#             'overall_margin': overall_margin,
#             'species_breakdown': species_avg_profits
#         }

#     def calculate_break_even_analysis(batch_params):
#         """Calculate break-even point for batch parameters"""
#         try:
#             lifecycle_days = batch_params.get('lifecycle_days', 30)
#             host_plant_cost = batch_params.get('host_plant_cost', 2.0)
#             labor_cost = batch_params.get('labor_cost', 5.0)
#             market_price = batch_params.get('market_price', 15.0)
#             survival_rate = batch_params.get('survival_rate', 95) / 100
            
#             # Daily costs
#             daily_cost = host_plant_cost + labor_cost
#             total_fixed_cost = daily_cost * lifecycle_days
            
#             # Break-even calculation
#             # total_fixed_cost = break_even_units * market_price
#             break_even_units = total_fixed_cost / market_price
            
#             # Convert to initial count needed (accounting for survival rate)
#             break_even_initial_count = break_even_units / survival_rate if survival_rate > 0 else float('inf')
            
#             return {
#                 'break_even_units': break_even_units,
#                 'break_even_initial_count': break_even_initial_count,
#                 'daily_cost': daily_cost,
#                 'total_fixed_cost': total_fixed_cost,
#                 'market_price': market_price,
#                 'survival_rate': survival_rate
#             }
            
#         except Exception as e:
#             print(f"Error in break-even analysis: {e}")
#             return None

#     def project_seasonal_profits(batches, months_ahead=12):
#         """Project profits for upcoming months based on current batches"""
#         monthly_projections = []
        
#         for month in range(months_ahead):
#             month_date = datetime.now() + timedelta(days=30 * month)
            
#             # Assume similar performance to current batches
#             if batches:
#                 avg_profit = sum([calculate_batch_profit(batch) for batch in batches]) / len(batches)
#                 # Add seasonal variation (simplified)
#                 seasonal_multiplier = 1.0 + 0.2 * (month % 12 / 12)  # 20% seasonal variation
#                 projected_profit = avg_profit * seasonal_multiplier
#             else:
#                 projected_profit = 0
            
#             monthly_projections.append({
#                 'month': month_date.strftime('%Y-%m'),
#                 'projected_profit': projected_profit,
#                 'confidence': 0.8 - (month * 0.05)  # Decreasing confidence over time
#             })
        
#         return monthly_projections

#     def calculate_profit_impact_score(batch):
#         """Calculate profit impact score for prioritizing batches"""
#         profit = calculate_batch_profit(batch)
#         survival_rate = batch.get('survival_rate', 0)
#         initial_count = batch.get('initial_count', 0)
        
#         # Normalize factors
#         profit_score = min(profit / 1000, 1.0)  # Normalize to $1000 max
#         survival_score = survival_rate / 100
#         scale_score = min(initial_count / 500, 1.0)  # Normalize to 500 units max
        
#         # Weighted impact score
#         impact_score = (profit_score * 0.5) + (survival_score * 0.3) + (scale_score * 0.2)
        
#         return {
#             'impact_score': impact_score,
#             'profit_contribution': profit_score,
#             'survival_contribution': survival_score,
#             'scale_contribution': scale_score,
#             'priority': 'High' if impact_score > 0.7 else 'Medium' if impact_score > 0.4 else 'Low'
#         }
