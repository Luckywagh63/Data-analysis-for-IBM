import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load water quality and health outcome data for India villages
water_quality_data = pd.read_csv('water_quality_india.csv')
health_data = pd.read_csv('health_outcomes_india.csv')

# Display the first few rows to ensure data is loaded correctly
print("Water Quality Data:")
print(water_quality_data.head())
print("\nHealth Data:")
print(health_data.head())

# Remove duplicates
water_quality_data.drop_duplicates(inplace=True)
health_data.drop_duplicates(inplace=True)

# Handle missing values
water_quality_data.fillna(method='ffill', inplace=True)
health_data.fillna(method='ffill', inplace=True)

# Standardize units for contaminant levels if needed
if 'contaminant_level' in water_quality_data.columns:
    conversion_factor = 1  # Adjust as necessary
    water_quality_data['contaminant_level'] *= conversion_factor

# Identify areas with the lowest access to clean water
threshold = 50  # Define a threshold for low access
low_access_areas = water_quality_data[water_quality_data['access_to_clean_water'] < threshold]

# Pre- and post-intervention data
pre_intervention = health_data[health_data['intervention'] == 'pre']
post_intervention = health_data[health_data['intervention'] == 'post']

# Check if data exists for comparison
if pre_intervention.empty or post_intervention.empty:
    raise ValueError("No pre or post intervention data available for comparison.")

# Compare pre- and post-intervention data
t_stat, p_value = stats.ttest_ind(pre_intervention['waterborne_disease_cases'], post_intervention['waterborne_disease_cases'])
print(f"T-statistic: {t_stat}, P-value: {p_value}")

if p_value < 0.05:
    print("The intervention had a statistically significant impact on reducing waterborne diseases.")
else:
    print("The intervention did not have a statistically significant impact on reducing waterborne diseases.")

# Set black background
plt.style.use('dark_background')

# Create a figure with multiple subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 12))

# Bar plot for areas with low access to clean water
sns.barplot(x='village', y='access_to_clean_water', data=low_access_areas, color='skyblue', ax=axs[0, 0])
axs[0, 0].set_title('Villages with Low Access to Clean Water in India')
axs[0, 0].set_xlabel('Village')
axs[0, 0].set_ylabel('Access to Clean Water (%)')
axs[0, 0].tick_params(axis='x', rotation=45)

# Pie chart for changes in waterborne disease cases over time
time_period_counts = health_data['time_period'].value_counts()
axs[0, 1].pie(time_period_counts, labels=time_period_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('viridis', len(time_period_counts)))
axs[0, 1].set_title('Changes in Waterborne Disease Cases Over Time')
axs[1, 1].set_title('Changes in Waterborne Disease Cases Over Time')

# Box plot for waterborne disease cases by village
sns.boxplot(data=health_data, x='village', y='waterborne_disease_cases', palette='Set2', ax=axs[1, 0])
axs[1, 0].set_title('Waterborne Disease Cases by Village')
axs[1, 0].set_xlabel('Village')
axs[1, 0].set_ylabel('Waterborne Disease Cases')
axs[1, 0].tick_params(axis='x', rotation=45)

# Summary statistics for health improvement, economic benefits, and educational outcomes
health_improvement = post_intervention['waterborne_disease_cases'].mean() - pre_intervention['waterborne_disease_cases'].mean()
economic_benefits = post_intervention['economic_output'].mean() - pre_intervention['economic_output'].mean()
educational_outcomes = post_intervention['school_attendance'].mean() - pre_intervention['school_attendance'].mean()

summary_data = {
    'Metric': ['Health Improvement', 'Economic Benefits', 'Educational Outcomes'],
    'Value': [health_improvement, economic_benefits, educational_outcomes]
}

summary_df = pd.DataFrame(summary_data)

# Bar plot for summary statistics
sns.barplot(x='Metric', y='Value', data=summary_df, palette='muted', ax=axs[1, 1])
axs[1, 1].set_title('Summary of Project Impact')
axs[1, 1].set_ylabel('Change')

# Adjust layout
plt.tight_layout()

# Show the plots
plt.show()
