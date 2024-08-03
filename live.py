import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Load initial data
data = pd.read_csv('water_quality_india_2024.csv')

# Set up the figure and axis for the live plot
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('black')  # Set figure background to black
ax.set_facecolor('black')  # Set axis background to black
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.title.set_color('white')

# Initialize line plot
line, = ax.plot([], [], lw=2, color='cyan', label='Access to Clean Water')
ax.set_xlim(data['time'].min(), data['time'].max() + 10)
ax.set_ylim(data['access_to_clean_water'].min() - 10, data['access_to_clean_water'].max() + 10)
ax.set_xlabel('Time')
ax.set_ylabel('Access to Clean Water (%)')
plt.title('Live Water Quality Monitoring', color='white')

# List to hold text annotations
annotations = []

def update_plot(frame):
    """Update the plot with new data up to index frame."""
    x_data = data['time'][:frame+1]
    y_data = data['access_to_clean_water'][:frame+1]
    
    line.set_data(x_data, y_data)
    
    # Remove previous annotations
    for annotation in annotations:
        annotation.remove()
    
    annotations.clear()
    
    # Add new annotations
    for x, y in zip(x_data, y_data):
        annotation = ax.text(x, y, f'{y:.1f}', fontsize=8, color='white', ha='center')
        annotations.append(annotation)
    
    ax.relim()  # Recalculate limits
    ax.autoscale_view()  # Autoscale view to fit new data
    return line,

def generate_live_data():
    """Generate new data for live updates."""
    new_time = data['time'].iloc[-1] + 1
    new_value = data['access_to_clean_water'].iloc[-1] + np.random.normal(loc=0, scale=1)
    new_data = pd.DataFrame({'time': [new_time], 'access_to_clean_water': [new_value]})
    return new_data

def animate(frame):
    """Animate function to update the plot with new data."""
    global data
    new_data = generate_live_data()
    data = pd.concat([data, new_data], ignore_index=True)
    return update_plot(frame)

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=200, interval=1000, blit=True)

plt.show()
