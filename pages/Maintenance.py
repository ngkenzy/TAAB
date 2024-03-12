import streamlit as st
import numpy as np

# Function to calculate available aircraft based on crew chiefs and maintenance
def calculate_available_aircraft(on_hands, phase_maintenance, scheduled_maintenance, unscheduled_maintenance):
    available_aircraft = on_hands - phase_maintenance - (scheduled_maintenance + unscheduled_maintenance)
    return max(0, available_aircraft)  # Ensure available aircraft is not negative

# Streamlit UI
st.title('Aircraft Availability Simulation')

# Input fields
on_hands = st.number_input('Aircraft On-Hands', value=24)
phase_maintenance = st.number_input('Phase Maintenance', value=4)
scheduled_maintenance = st.slider('Scheduled Maintenance per Day', 0, 10, 0)
unscheduled_maintenance = st.slider('Unscheduled Maintenance per Day', 0, 10, 0)

# Simulation days
simulation_days = st.slider('Simulation Days', 1, 100, 60)

# Simulation
days = np.arange(1, simulation_days + 1)
available_aircraft_over_time = []

for day in days:
    # Simulate stochastic nature of maintenance
    scheduled_maintenance_today = np.random.randint(0, scheduled_maintenance + 1)
    unscheduled_maintenance_today = np.random.randint(0, unscheduled_maintenance + 1)

    available_aircraft = calculate_available_aircraft(on_hands, phase_maintenance, scheduled_maintenance_today, unscheduled_maintenance_today)
    available_aircraft_over_time.append(available_aircraft)

# Plot histogram for available aircraft distribution
st.subheader('Distribution of Available Aircraft')
st.bar_chart(np.histogram(available_aircraft_over_time, bins=10)[0])

# Summary
st.write(f"Maximum Available Aircraft: {max(available_aircraft_over_time)}")
st.write(f"Minimum Available Aircraft: {min(available_aircraft_over_time)}")
st.write(f"Average Available Aircraft: {np.mean(available_aircraft_over_time)}")
st.write(f"Median Available Aircraft: {np.median(available_aircraft_over_time)}")
