import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from random import randint

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
        available_vhm = total_vhm_aircraft - vhm_phase_maintenance - vhm_maintenance
        available_uhm = total_uhm_aircraft - uhm_phase_maintenance - uhm_maintenance
        available_aircrews = randint(*aircrew_availability_range)

        # Check mission sufficiency
        insufficient_missions = []
        for mission, status in missions_status.items():
            if status:  # If mission is active
                req_aircrews = missions[mission]["aircrews"]
                req_vhm = 0
                req_uhm = 0

                # Check if mission specifies aircraft requirements (handle different cases)
                aircraft_req = missions[mission].get("aircraft")
                if aircraft_req:
                    if "VHM" in aircraft_req:
                        req_vhm = aircraft_req["VHM"]
                    if "UHM" in aircraft_req:
                        req_uhm = aircraft_req["UHM"]
                else:
                    # Mission allows any type (VHM, UHM, or none)
                    continue  # Skip to the next mission

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
    global missions  # This line is typically unnecessary for reading a global variable, but added for clarity.
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
        fig, axs = plt.subplots(3, 1, sharex=True, figsize=(8, 10))  # Create three subplots for aircraft, aircrew, and missions

        axs[0].plot(result["day"], result["available_vhm"], label="Available VHM")
        axs[0].plot(result["day"], result["available_uhm"], label="Available UHM")
        axs[0].set_ylabel("Number Available (Aircraft)")
        axs[0].legend()
        axs[0].set_title("Daily Availability of VHM and UHM Aircraft")

        axs[1].plot(result["day"], result["available_aircrews"], label="Available Aircrews")
        axs[1].set_xlabel("Day")
        axs[1].set_ylabel("Number Available (Aircrews)")
        axs[1].legend()
        axs[1].set_title("Daily Availability of Aircrews")

        missions_labels = list(missions_met.keys())
        missions_values = list(missions_met.values())
        bar_plot = axs[2].barh(missions_labels, missions_values, color='skyblue')
        axs[2].set_xlabel('Number of Days')
        axs[2].set_ylabel('Missions')
        axs[2].set_title('Total Missions Met')

        for i, (mission, days_met) in enumerate(missions_met.items()):
            days_not_met = result.shape[0] - days_met
            percentage_met = (days_met / result.shape[0]) * 100
            percentage_not_met = (days_not_met / result.shape[0]) * 100
            st.write(f"{mission}: {percentage_met:.2f}% Met, {percentage_not_met:.2f}% Not Met")

            # Annotate the bar plot with percentages
            axs[2].text(days_met, i, f'{percentage_met:.2f}%', va='center')

        fig.suptitle("Daily Availability of Resources and Total Missions Met")  # Add a supertitle for all plots
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
