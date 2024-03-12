import streamlit as st

# Define missions and their requirements
missions = {
    "R": {"aircrews": 1, "aircraft": 1, "type": "24h"},  # Define various types of missions and their requirements
    "TPZ1": {"aircrews": 4, "aircraft": 3, "type": "12h"},  # Day and Night combined
    "TPZ2": {"aircrews": 4, "aircraft": 3, "type": "12h"},  # Day and Night combined
    "JADOC": {"aircrews": 2, "aircraft": 2, "type": "12h"},
    "AMR": {"aircrews": 2, "aircraft": 2, "type": "12h"},
    "Training 1": {"aircrews": 1, "aircraft": 1, "type": "12h"},
    "Training 2": {"aircrews": 1, "aircraft": 1, "type": "12h"},
}

# Define the simulation function
def simulate_daily_operations(total_uhl_aircraft_on_hand, uhl_aircraft_phase_maintenance, uhl_aircrews_available, scheduled_unscheduled_maintenance_range, missions_status, days=60):
    daily_status = []  # List to store daily status
    missions_not_sufficient = []  # List to store days with insufficient missions

    for day in range(days):
        # Initialize or update aircraft maintenance
        aircraft_in_maintenance = uhl_aircraft_phase_maintenance + uhl_aircrews_available[0]  # Using low range for maintenance
        
        # Available resources for the day
        available_aircraft = total_uhl_aircraft_on_hand - aircraft_in_maintenance
        available_aircrews = uhl_aircrews_available[1]  # Use high range for aircrews
        
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
        
        # Store daily status
        daily_status.append({
            "day": day+1, 
            "available_aircraft": available_aircraft, 
            "available_aircrews": available_aircrews,
            "insufficient_missions": insufficient_missions
        })
        
        if insufficient_missions:
            missions_not_sufficient.append((day+1, insufficient_missions))
    
    return daily_status, missions_not_sufficient

# Streamlit app function
def app():
    global missions  # Access global variable missions
    st.title("UHL Aircraft and Aircrew Allocation Simulation")

    # User inputs for initial conditions
    total_uhl_aircraft_on_hand = st.number_input("Total UHL Aircrafts on-hand", value=16, min_value=0)
    uhl_aircraft_phase_maintenance = st.number_input("UHL Aircrafts Phase Maintenance", value=2, min_value=0)
    aircrews_available_low = st.number_input("UHL Aircrews Available Low", value=11, min_value=0)
    aircrews_available_high = st.number_input("UHL Aircrews Available High", value=13, min_value=0)
    scheduled_maintenance_low = st.number_input("Scheduled/Unscheduled Maintenance Low", value=4, min_value=0)
    scheduled_maintenance_high = st.number_input("Scheduled/Unscheduled Maintenance High", value=5, min_value=0)
    
    # Toggle missions
    st.header("Toggle Missions")
    missions_status = {}
    for mission in missions:
        missions_status[mission] = st.checkbox(f"{mission} Mission", True)

    # Run simulation
    if st.button("Run Simulation"):
        result, missions_not_sufficient = simulate_daily_operations(
            total_uhl_aircraft_on_hand, uhl_aircraft_phase_maintenance,
            (scheduled_maintenance_low, scheduled_maintenance_high),
            (aircrews_available_low, aircrews_available_high), 
            missions_status)

        # Display results
        st.write("Daily Status:")
        st.write(result)
        
        # Display missions that are not sufficiently met
        if missions_not_sufficient:
            st.subheader("Insufficient Missions by Day:")
            for day, missions in missions_not_sufficient:
                st.write(f"Day {day}: {', '.join(missions)}")
        else:
            st.write("All missions are sufficiently met throughout the simulation period.")

if __name__ == "__main__":
    app()
