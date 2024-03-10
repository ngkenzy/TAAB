import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from random import randint

# Define missions and their requirements
missions = {
    "R": {"aircrews": 1, "aircraft": 1, "type": "24h"},
    "TPZ1": {"aircrews": 4, "aircraft": 3, "type": "12h"},  # Day and Night combined
    "TPZ2": {"aircrews": 4, "aircraft": 3, "type": "12h"},  # Day and Night combined
    "JADOC": {"aircrews": 2, "aircraft": 2, "type": "12h"},
    "AMR": {"aircrews": 2, "aircraft": 2, "type": "12h"},
    "Training 1": {"aircrews": 1, "aircraft": 1, "type": "12h"},
    "Training 2": {"aircrews": 1, "aircraft": 1, "type": "12h"},
}

# Define the simulation function
def simulate_daily_operations(total_uhl_aircraft_on_hand, uhl_aircraft_phase_maintenance, uhl_aircrews_available, scheduled_unscheduled_maintenance_range, missions_status, days=60):
    daily_status = []
    missions_not_sufficient = []

    for day in range(days):
        # Initialize or update aircraft maintenance
        aircraft_in_maintenance = uhl_aircraft_phase_maintenance + randint(*scheduled_unscheduled_maintenance_range)
        
        # Available resources for the day
        available_aircraft = total_uhl_aircraft_on_hand - aircraft_in_maintenance
        available_aircrews = randint(*uhl_aircrews_available)  # Stochastic aircrew availability
        
        # Check mission sufficiency
        insufficient_missions = []
        for mission, status in missions_status.items():
            if status:  # If mission is active
                req_aircrews = missions[mission]["aircrews"]
                req_aircraft = missions[mission]["aircraft"]
                
                # Check if resources are sufficient for the mission
                if available_aircrews >= req_aircrews and available_aircraft >= req_aircraft:
                    available_aircrews -= req_aircrews
                    available_aircraft -= req_aircraft
                else:
                    insufficient_missions.append(mission)
        
        daily_status.append({
            "day": day+1, 
            "available_aircraft": available_aircraft, 
            "available_aircrews": available_aircrews,
            "insufficient_missions": insufficient_missions
        })
        
        if insufficient_missions:
            missions_not_sufficient.append((day+1, insufficient_missions))
    
    return pd.DataFrame(daily_status), missions_not_sufficient

# Streamlit app function
def app():
    global missions  # This line is typically unnecessary for reading a global variable, but added for clarity.
    st.title("UHL Aircraft and Aircrew Allocation Simulation")

    # User inputs for initial conditions
    st.sidebar.header("Initial Conditions")
    total_uhl_aircraft_on_hand = st.sidebar.number_input("Total UHL Aircrafts on-hand", value=16, min_value=0)
    uhl_aircraft_phase_maintenance = st.sidebar.number_input("UHL Aircrafts Phase Maintenance", value=2, min_value=0)
    aircrews_available_low = st.sidebar.number_input("UHL Aircrews Available Low", value=11, min_value=0)
    aircrews_available_high = st.sidebar.number_input("UHL Aircrews Available High", value=13, min_value=0)
    scheduled_maintenance_low = st.sidebar.number_input("Scheduled/Unscheduled Maintenance Low", value=4, min_value=0)
    scheduled_maintenance_high = st.sidebar.number_input("Scheduled/Unscheduled Maintenance High", value=5, min_value=0)
    
    # Toggle missions
    st.header("Toggle Missions")
    missions_status = {mission: st.checkbox(f"{mission} Mission", True) for mission in missions}

    # Run simulation
    if st.button("Run Simulation"):
        result, missions_not_sufficient = simulate_daily_operations(
            total_uhl_aircraft_on_hand, uhl_aircraft_phase_maintenance,
            (aircrews_available_low, aircrews_available_high),
            (scheduled_maintenance_low, scheduled_maintenance_high), 
            missions_status)

        # Plotting the results
        fig, ax = plt.subplots()
        ax.plot(result["day"], result["available_aircraft"], label="Available Aircraft")
        ax.plot(result["day"], result["available_aircrews"], label="Available Aircrews", linestyle="--")
        ax.set_xlabel("Day")
        ax.set_ylabel("Number Available")
        ax.set_title("Daily Availability of Aircraft and Aircrews")
        ax.legend()
        st.pyplot(fig)

        # Calculate mission status percentages
        total_days = len(result)
        missions_status_counts = {mission: 0 for mission in missions}
        for _, row in result.iterrows():
            for mission in row["insufficient_missions"]:
                missions_status_counts[mission] += 1
        
        # Plotting the average status (met and not met) for each mission
        fig, ax = plt.subplots()
        mission_labels = list(missions_status_counts.keys())
        met_percentages = [((total_days - count) / total_days) * 100 for count in missions_status_counts.values()]
        not_met_percentages = [(count / total_days) * 100 for count in missions_status_counts.values()]

        ax.barh(mission_labels, met_percentages, label="Met")
        ax.barh(mission_labels, not_met_percentages, left=met_percentages, label="Not Met")

        ax.set_xlabel("Percentage")
        ax.set_title("Average Mission Status")
        ax.legend()
        st.pyplot(fig)

        # Display missions that are not sufficiently met
        if missions_not_sufficient:
            st.subheader("Insufficient Missions by Day")
            for day, missions in missions_not_sufficient:
                st.write(f"Day {day}: {', '.join(missions)}")
        else:
            st.write("All missions are sufficiently met throughout the simulation period.")

if __name__ == "__main__":
    app()
