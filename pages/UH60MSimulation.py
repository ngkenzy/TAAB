import streamlit as st
import numpy as np
import pandas as pd
from random import randint
import plotly.graph_objects as go

# Define missions and their requirements (flexible allocation)
missions = {
    "SDM Day": {"aircrews": 2, "aircraft": {"VHM": 2}, "type": "12h"},
    "SDM Night": {"aircrews": 2, "aircraft": {"UHM": 2}, "type": "12h"},
    "J4": {"aircrews": 2, "aircraft": {"VHM": 1, "UHM": 1}, "type": "12h (Mon-Fri)"},  # Can be VHM, UHM, or both
    "DOVER": {"aircrews": 2, "aircraft": {"UHM": 2}, "type": "12h"},  # Can be VHM, UHM, or none (any type)
    "OSA": {"aircrews": 1, "aircraft": {"UHM": 1}, "type": "12h"},
    "Training 1": {"aircrews": 1, "aircraft": {"VHM": 1}, "type": "12h"},
}

# Define the simulation function
def simulate_daily_operations(total_vhm_aircraft, total_uhm_aircraft, vhm_phase_maintenance, uhm_phase_maintenance,
                               vhm_maintenance_range, uhm_maintenance_range, aircrew_availability_range,
                               missions_status, days=60):
    daily_status = []
    missions_not_sufficient = []
    missions_met = {mission: 0 for mission in missions}

    for day in range(days):
        # Initialize or update aircraft maintenance
        vhm_maintenance = randint(*vhm_maintenance_range)
        uhm_maintenance = randint(*uhm_maintenance_range)

        # Available resources for the day
        available_vhm = max(total_vhm_aircraft - vhm_phase_maintenance - vhm_maintenance, 0)
        available_uhm = max(total_uhm_aircraft - uhm_phase_maintenance - uhm_maintenance, 0)
        available_aircrews = randint(*aircrew_availability_range)

        # Check mission sufficiency
        insufficient_missions = []
        for mission, status in missions_status.items():
            if status:  # If mission is active
                req_aircrews = missions[mission]["aircrews"]
                req_vhm = 0
                req_uhm = 0

                # Check if mission specifies aircraft requirements
                aircraft_req = missions[mission].get("aircraft", {})
                req_vhm = aircraft_req.get("VHM", 0)
                req_uhm = aircraft_req.get("UHM", 0)

                # Check if resources are sufficient for the mission
                if available_aircrews >= req_aircrews and (available_vhm >= req_vhm or available_uhm >= req_uhm):
                    available_aircrews -= req_aircrews
                    available_vhm -= req_vhm
                    available_uhm -= req_uhm
                    missions_met[mission] += 1
                else:
                    insufficient_missions.append(mission)

        daily_status.append({
            "day": day + 1,
            "available_vhm": available_vhm,
            "available_uhm": available_uhm,
            "available_aircrews": available_aircrews,
        })

        if insufficient_missions:
            missions_not_sufficient.append((day + 1, insufficient_missions))

    return pd.DataFrame(daily_status), missions_not_sufficient, missions_met

# Streamlit app function
def app():
    global missions

    st.title("VHM/UHM Aircraft and Aircrew Allocation Simulation")

    # User inputs for initial conditions
    st.sidebar.header("Initial Conditions")
    total_vhm_aircraft = st.sidebar.number_input("Total VHM Aircrafts on-hand", value=4, min_value=0)
    total_uhm_aircraft = st.sidebar.number_input("Total UHM Aircrafts on-hand", value=4, min_value=0)
    vhm_phase_maintenance = st.sidebar.number_input("VHM Aircrafts Phase Maintenance", value=1, min_value=0)
    uhm_phase_maintenance = st.sidebar.number_input("UHM Aircrafts Phase Maintenance", value=1, min_value=0)
    vhm_maintenance_low = st.sidebar.number_input("VHM Scheduled/Unscheduled Maintenance Low", value=0, min_value=0)
    vhm_maintenance_high = st.sidebar.number_input("VHM Scheduled/Unscheduled Maintenance High", value=1, min_value=0)
    uhm_maintenance_low = st.sidebar.number_input("UHM Scheduled/Unscheduled Maintenance Low", value=0, min_value=0)
    uhm_maintenance_high = st.sidebar.number_input("UHM Scheduled/Unscheduled Maintenance High", value=1, min_value=0)
    aircrew_availability_low = st.sidebar.number_input("Total Aircrews Available Low", value=0, min_value=0)
    aircrew_availability_high = st.sidebar.number_input("Total Aircrews Available High", value=8, min_value=0)

    # Toggle missions
    st.header("Toggle Missions")
    missions_status = {mission: st.checkbox(f"{mission} Mission", True) for mission in missions}

    # Run simulation
    if st.button("Run Simulation"):
        result, missions_not_sufficient, missions_met = simulate_daily_operations(
            total_vhm_aircraft, total_uhm_aircraft, vhm_phase_maintenance, uhm_phase_maintenance,
            (vhm_maintenance_low, vhm_maintenance_high), (uhm_maintenance_low, uhm_maintenance_high),
            (aircrew_availability_low, aircrew_availability_high), missions_status)
        
        # Plotting the results
        st.line_chart(result.set_index("day")[["available_vhm", "available_uhm", "available_aircrews"]])

        # Display missions that are not sufficiently met
        if missions_not_sufficient:
            st.subheader("Insufficient Missions by Day")
            for day, missions in missions_not_sufficient:
                st.write(f"Day {day}: {', '.join(missions)}")
        else:
            st.write("All missions are sufficiently met throughout the simulation period.")

        # Display total missions met
        st.subheader("Total Missions Met")
        for mission, days_met in missions_met.items():
            days_not_met = result.shape[0] - days_met
            percentage_met = (days_met / result.shape[0]) * 100
            percentage_not_met = (days_not_met / result.shape[0]) * 100
            st.write(f"{mission}: {percentage_met:.2f}% Met, {percentage_not_met:.2f}% Not Met")

        # Plotting the percentage of missions met vs not met
        fig = go.Figure(data=[
            go.Bar(name='Met', x=list(missions_met.keys()), y=[(days_met / result.shape[0]) * 100 for days_met in missions_met.values()]),
            go.Bar(name='Not Met', x=list(missions_met.keys()), y=[((result.shape[0] - days_met) / result.shape[0]) * 100 for days_met in missions_met.values()])
        ])
        fig.update_layout(barmode='stack', title='Percentage of Missions Met vs Not Met')
        st.plotly_chart(fig)

# Call the app function to run the Streamlit app
if __name__ == "__main__":
    app()
