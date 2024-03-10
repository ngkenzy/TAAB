import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="12th Aviation Battalion",
    page_icon=":bar_chart:",
)

st.title("12th Aviation Battalion")
st.sidebar.success("Select a page above.")

import streamlit as st
import pandas as pd

st.title('UHM Personnel Management Dashboard')

# Define roles and initialize DataFrame
roles = ['PC', 'PC/AMC', 'AMC', 'PI', 'CE']
df = pd.DataFrame(index=roles, columns=['Authorized', 'On Hand', 'Admin/DNIF', 'Loss', 'Staff', 'Leave', 'Available'])

# Input for Authorized row
authorized_input = st.number_input('Authorized for Pilots', min_value=0, value=23, key='authorized_pilots')
authorized_ce = st.number_input('Authorized for CE', min_value=0, value=21, key='authorized_ce')

# Set Authorized values
df.at['PC', 'Authorized'] = df.at['PC/AMC', 'Authorized'] = df.at['AMC', 'Authorized'] = df.at['PI', 'Authorized'] = authorized_input
df.at['CE', 'Authorized'] = authorized_ce

# Collecting inputs for each role using columns to organize inputs
for role in roles:
    st.subheader(role)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        df.at[role, 'On Hand'] = col1.number_input(f'On Hand - {role}', min_value=0, value=0, key=f'on_hand_{role}')
    with col2:
        df.at[role, 'Admin/DNIF'] = col2.number_input(f'Admin/DNIF - {role}', min_value=0, value=0, key=f'admin_dnif_{role}')
    with col3:
        df.at[role, 'Loss'] = col3.number_input(f'Loss - {role}', min_value=0, value=0, key=f'loss_{role}')
    with col4:
        df.at[role, 'Staff'] = col4.number_input(f'Staff - {role}', min_value=0, value=0, key=f'staff_{role}')
    with col5:
        df.at[role, 'Leave'] = col5.number_input(f'Leave - {role}', min_value=0, value=0, key=f'leave_{role}')

# Calculate 'Available' after all inputs
df['Available'] = df['On Hand'] - (df['Admin/DNIF'] + df['Loss'] + df['Staff'] + df['Leave'])

# Display the DataFrame as a table for overview
st.subheader('Personnel Data Overview')
st.table(df)


# Calculate TDA On Hand % and TDA Available % for Pilots and CE
pilot_roles = ['PC', 'PC/AMC', 'AMC', 'PI']
total_on_hand_pilots = df.loc[pilot_roles, 'On Hand'].sum()
total_available_pilots = df.loc[pilot_roles, 'Available'].sum()

tda_on_hand_pilots = (total_on_hand_pilots / authorized_input * 100) if authorized_input > 0 else 0
tda_available_pilots = (total_available_pilots / authorized_input * 100) if authorized_input > 0 else 0

tda_on_hand_ce = (df.at['CE', 'On Hand'] / authorized_ce * 100) if authorized_ce > 0 else 0
tda_available_ce = (df.at['CE', 'Available'] / authorized_ce * 100) if authorized_ce > 0 else 0

# Display Calculated TDA Percentages
st.subheader('TDA On Hand % and TDA Available % for Pilots')
st.write(f'TDA On Hand % for Pilots: {tda_on_hand_pilots:.2f}%')
st.write(f'TDA Available % for Pilots: {tda_available_pilots:.2f}%')

st.subheader('TDA On Hand % and TDA Available % for CE')
st.write(f'TDA On Hand % for CE: {tda_on_hand_ce:.2f}%')
st.write(f'TDA Available % for CE: {tda_available_ce:.2f}%')

# Optional: Display the DataFrame as a table
st.table(df)

st.title("UH/VH-60M Crew Composition Calculator")

# Providing unique keys for each number input to avoid key collision
PC = st.number_input('PC (Pilot in Command)', min_value=0, value=6, key='PC')
PC_AMC = st.number_input('PC/AMC (Pilot/Air Mission Commander)', min_value=0, value=7, key='PC_AMC')
AMC = st.number_input('AMC (Air Mission Commander)', min_value=0, value=0, key='AMC')  # Unused in crew compositions, can be set to zero or allowed for future flexibility
PI = st.number_input('PI (Pilot)', min_value=0, value=9, key='PI')
CE = st.number_input('CE (Crew Engineer)', min_value=0, value=21, key='CE')

# Button to calculate crew compositions
if st.button('Calculate Crew Compositions'):
    # Initialize counters for each crew type
    crew_1_PC_1_PI_1_CE = 0
    crew_1_PC_AMC_1_PI_1_CE = 0
    crew_2_PC_AMC_1_CE = 0
    crew_2_PC_1_CE = 0

    # Crew compositions calculation
    while PC >= 1 and PI >= 1 and CE >= 1:
        crew_1_PC_1_PI_1_CE += 1
        PC -= 1
        PI -= 1
        CE -= 1

    while PC_AMC >= 1 and PI >= 1 and CE >= 1:
        crew_1_PC_AMC_1_PI_1_CE += 1
        PC_AMC -= 1
        PI -= 1
        CE -= 1

    while PC >= 2 and CE >= 1:
        crew_2_PC_1_CE += 1
        PC -= 2
        CE -= 1

    while PC_AMC >= 2 and CE >= 1:
        crew_2_PC_AMC_1_CE += 1
        PC_AMC -= 2
        CE -= 1

    # Calculate the maximum number of crews
    max_crews = crew_1_PC_1_PI_1_CE + crew_1_PC_AMC_1_PI_1_CE + crew_2_PC_AMC_1_CE + crew_2_PC_1_CE

    # Results
    result = {
        "max_crews": max_crews,
        "crew_compositions": {
            "1_PC_1_PI_1_CE": crew_1_PC_1_PI_1_CE,
            "1_PC_AMC_1_PI_1_CE": crew_1_PC_AMC_1_PI_1_CE,
            "2_PC_AMC_1_CE": crew_2_PC_AMC_1_CE,
            "2_PC_1_CE": crew_2_PC_1_CE,
        },
        "remaining_personnel": {
            "PC": PC,
            "PC/AMC": PC_AMC,
            "AMC": AMC,
            "PI": PI,
            "CE": CE
        }
    }

    # Displaying the results
    st.subheader("Results")
    st.write("Maximum Number of Crews:", result["max_crews"])
    st.write("Crew Compositions:", result["crew_compositions"])
    st.write("Remaining Personnel:", result["remaining_personnel"])
#########Maintenance
# Set the seed for reproducibility
np.random.seed(0)

# Streamlit app layout for input
st.title("UH/VH-60M Aircraft Maintenance and Availability Calculator")
total_vhm_aircrafts = st.number_input('Total VHM Aircrafts', min_value=1, value=4)
total_uhm_aircrafts = st.number_input('Total UHM Aircrafts', min_value=1, value=4)
vhm_aircrafts_phase_maintenance = st.number_input('VHM Aircrafts in Phase Maintenance', min_value=0, value=1, max_value=total_vhm_aircrafts)
uhm_aircrafts_phase_maintenance = st.number_input('UHM Aircrafts in Phase Maintenance', min_value=0, value=1, max_value=total_uhm_aircrafts)
days = st.number_input('Time Steps', min_value=1, value=30)
simulations = st.number_input('Simulations', min_value=1, value=1000)

# Inputs for maintenance range
vhm_maintenance_min = st.number_input('Minimum VHM on Scheduled/Unscheduled Maintenance', min_value=0, value=0)
vhm_maintenance_max = st.number_input('Maximum VHM Scheduled/Unscheduled Maintenance', min_value=0, value=1)
uhm_maintenance_min = st.number_input('Minimum UHM Scheduled/Unscheduled Maintenance', min_value=0, value=0)
uhm_maintenance_max = st.number_input('Maximum UHM Scheduled/Unscheduled Maintenance', min_value=0, value=1)

# Button to run simulation
if st.button('Run Calculation'):
    # Calculate initial available aircrafts
    available_vhm_aircrafts = total_vhm_aircrafts - vhm_aircrafts_phase_maintenance
    available_uhm_aircrafts = total_uhm_aircrafts - uhm_aircrafts_phase_maintenance

    # Initialize arrays to store results
    vhm_down_for_maintenance_daily = np.zeros(days)
    uhm_down_for_maintenance_daily = np.zeros(days)
    vhm_available_daily = np.zeros(days)
    uhm_available_daily = np.zeros(days)

    # Run simulations
    for _ in range(simulations):
        for day in range(days):
            # Random maintenance for each aircraft type within specified range
            vhm_maintenance = np.random.randint(vhm_maintenance_min, vhm_maintenance_max + 1)  # Inclusive range
            uhm_maintenance = np.random.randint(uhm_maintenance_min, uhm_maintenance_max + 1)  # Inclusive range

            # Calculate available aircrafts after maintenance
            vhm_available = max(0, available_vhm_aircrafts - vhm_maintenance)
            uhm_available = max(0, available_uhm_aircrafts - uhm_maintenance)

            # Accumulate results
            vhm_down_for_maintenance_daily[day] += vhm_maintenance
            uhm_down_for_maintenance_daily[day] += uhm_maintenance
            vhm_available_daily[day] += vhm_available
            uhm_available_daily[day] += uhm_available

    # Calculate averages
    vhm_down_for_maintenance_daily_avg = vhm_down_for_maintenance_daily / simulations
    uhm_down_for_maintenance_daily_avg = uhm_down_for_maintenance_daily / simulations
    vhm_available_daily_avg = vhm_available_daily / simulations
    uhm_available_daily_avg = uhm_available_daily / simulations

    # Plot results
    days_range = np.arange(1, days + 1)
    plt.figure(figsize=(14, 8))

    plt.plot(days_range, vhm_down_for_maintenance_daily_avg, label="VHM Down for Maintenance", marker='o')
    plt.plot(days_range, uhm_down_for_maintenance_daily_avg, label="UHM Down for Maintenance", marker='x')
    plt.plot(days_range, vhm_available_daily_avg, label="VHM Available", linestyle='--')
    plt.plot(days_range, uhm_available_daily_avg, label="UHM Available", linestyle='--')

    plt.title("Aircraft Maintenance and Availability over 30 Days")
    plt.xlabel("Day")
    plt.ylabel("Number of Aircraft")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    st.pyplot(plt)

    #############################


st.title("UH/VH-60M Mission Allocation Simulator")

# Inputs for available resources
aircrews = st.number_input('Available Aircrews', min_value=1, value=11, key='aircrews')
uhm_aircrafts = st.number_input('Available UHM Aircrafts', min_value=0, value=2, key='uhm_aircrafts')
vhm_aircrafts = st.number_input('Available VHM Aircrafts', min_value=0, value=3, key='vhm_aircrafts')

# Checkbox to turn 'ATLAS' mission on or off
atlas_enabled = st.checkbox("'ATLAS' Mission Enabled", value=True)

# Inputs for 'ATLAS' mission requirements, only shown if 'ATLAS' is enabled
if atlas_enabled:
    atlas_aircrews = st.number_input("'ATLAS' Aircrews Required", min_value=1, value=3, key='atlas_aircrews')
    atlas_aircrafts = st.number_input("'ATLAS' Aircrafts Required", min_value=1, value=3, key='atlas_aircrafts')

# Missions requirements with 'ATLAS' being conditional
missions = {
    'SDM Day': {'aircrews': 2, 'aircrafts': 2, 'spare': 1},
    'SDM Night': {'aircrews': 2, 'aircrafts': 0, 'spare': 0},
    'J4': {'aircrews': 2, 'aircrafts': 2, 'spare': 1},
    'DOVER': {'aircrews': 2, 'aircrafts': 2},
    'Training': {'aircrews': 1, 'aircrafts': 1}
}

# Add 'ATLAS' to missions if enabled
if atlas_enabled:
    missions['ATLAS'] = {'aircrews': atlas_aircrews, 'aircrafts': atlas_aircrafts}

def allocate_resources(aircrews, uhm_aircrafts, vhm_aircrafts, missions):
    completed_missions = {}
    available_resources = {'aircrews': aircrews, 'uhm_aircrafts': uhm_aircrafts, 'vhm_aircrafts': vhm_aircrafts}

    for mission, requirements in missions.items():
        if (available_resources['aircrews'] >= requirements['aircrews'] and
            (available_resources['uhm_aircrafts'] + available_resources['vhm_aircrafts']) >= requirements['aircrafts']):
            available_resources['aircrews'] -= requirements['aircrews']
            aircraft_needed = requirements['aircrafts']
            spare_needed = requirements.get('spare', 0)

            if spare_needed > 0:
                if available_resources['uhm_aircrafts'] >= spare_needed:
                    available_resources['uhm_aircrafts'] -= spare_needed
                elif available_resources['vhm_aircrafts'] >= spare_needed:
                    available_resources['vhm_aircrafts'] -= spare_needed
                else:
                    continue

            while aircraft_needed > 0:
                if available_resources['uhm_aircrafts'] > 0:
                    available_resources['uhm_aircrafts'] -= 1
                elif available_resources['vhm_aircrafts'] > 0:
                    available_resources['vhm_aircrafts'] -= 1
                aircraft_needed -= 1

            completed_missions[mission] = True
        else:
            completed_missions[mission] = False

    return completed_missions, available_resources

def readable_output(completed_missions, available_resources):
    # Missions Summary
    completed_summary = "\n".join([f"- {mission}: {'Completed' if status else 'Not Completed'}" for mission, status in completed_missions.items()])
    missions_summary = f"Mission Completion Summary:\n{completed_summary}"

    # Resources Summary
    resources_summary = f"Remaining Resources Summary:\n- Aircrews: {available_resources['aircrews']}\n" \
                        f"- UHM Aircrafts: {available_resources['uhm_aircrafts']}\n" \
                        f"- VHM Aircrafts: {available_resources['vhm_aircrafts']}"

    return missions_summary, resources_summary

# Button to run simulation and plot allocations
if st.button('Allocate Resources'):
    completed_missions, available_resources = allocate_resources(aircrews, uhm_aircrafts, vhm_aircrafts, missions)
    
    def plot_allocations(completed_missions, available_resources):
        fig, axs = plt.subplots(1, 2, figsize=(14, 4))
        
        # Completed Missions
        missions_status = ['Completed' if status else 'Not Completed' for status in completed_missions.values()]
        axs[0].bar(completed_missions.keys(), missions_status)
        axs[0].tick_params(axis='x', rotation=45)
        axs[0].set_title("Mission Completion Status")

        # Available Resources
        resource_names = ['Aircrews', 'UHM Aircrafts', 'VHM Aircrafts']
        resource_values = [available_resources['aircrews'], available_resources['uhm_aircrafts'], available_resources['vhm_aircrafts']]
        axs[1].bar(resource_names, resource_values, color=['blue', 'orange', 'green'])
        axs[1].set_title("Available Resources After Allocation")

        plt.tight_layout()
        return fig

    fig = plot_allocations(completed_missions, available_resources)
    st.pyplot(fig)

    missions_summary, resources_summary = readable_output(completed_missions, available_resources)
    st.text(missions_summary)
    st.text(resources_summary)

    ##########################


st.title("Mission Allocation Simulator with Dynamic Inputs")

# Constants
DAYS = 30
MISSIONS = ['SDM Day', 'SDM Night', 'J4', 'DOVER', 'Training']  # ATLAS will be added conditionally
MISSION_REQUIREMENTS = {
    'SDM Day': {'aircrew': 2, 'aircraft': 2},
    'SDM Night': {'aircrew': 2, 'aircraft': 1},
    'J4': {'aircrew': 2, 'aircraft': 3},
    'DOVER': {'aircrew': 2, 'aircraft': 2},
    'Training': {'aircrew': 1, 'aircraft': 1},
}

# Ensure all st.number_input widgets have a unique key parameter
AIRCREW_MIN = st.number_input('Minimum Aircrews Available Daily', min_value=1, value=8, key='aircrew_min')
AIRCREW_MAX = st.number_input('Maximum Aircrews Available Daily', min_value=AIRCREW_MIN, value=11, key='aircrew_max')
UHM_AIRCRAFT_TOTAL = st.number_input('Total UHM Aircrafts', min_value=1, value=4, key='uhm_aircraft_total')
VHM_AIRCRAFT_TOTAL = st.number_input('Total VHM Aircrafts', min_value=1, value=4, key='vhm_aircraft_total')
VHM_PHASE_MAINTENANCE = st.number_input('VHM Aircrafts in Phase Maintenance', min_value=0, value=1, key='vhm_phase_maintenance')
UHM_PHASE_MAINTENANCE = st.number_input('UHM Aircrafts in Phase Maintenance', min_value=0, value=1, key='uhm_phase_maintenance')
MAINTENANCE_MIN, MAINTENANCE_MAX = st.slider('Scheduled and Unschedule Maintenance Range for Both UHM and VHM Aircrafts', 0, 5, (0, 2), key='maintenance_range')

# ATLAS mission toggle and requirements input
atlas_enabled = st.checkbox("Include 'ATLAS' Mission", value=True)
if atlas_enabled:
    MISSIONS.append('ATLAS')
    atlas_aircrew = st.number_input("'ATLAS' Mission Aircrews Required", min_value=1, value=3, key='atlas_aircrew')
    atlas_aircraft = st.number_input("'ATLAS' Mission Aircrafts Required", min_value=1, value=3, key='atlas_aircraft')
    MISSION_REQUIREMENTS['ATLAS'] = {'aircrew': atlas_aircrew, 'aircraft': atlas_aircraft}

def run_simulation():
    # Results Storage
    mission_completion = {mission: [] for mission in MISSIONS}
    aircrew_availability = []
    uhm_vhm_availability = []

    # Simulation
    for day in range(DAYS):
        aircrews = np.random.randint(AIRCREW_MIN, AIRCREW_MAX + 1)
        uhm_maintenance = np.random.randint(MAINTENANCE_MIN, MAINTENANCE_MAX + 1) + UHM_PHASE_MAINTENANCE
        vhm_maintenance = np.random.randint(MAINTENANCE_MIN, MAINTENANCE_MAX + 1) + VHM_PHASE_MAINTENANCE

        uhm_available = UHM_AIRCRAFT_TOTAL - uhm_maintenance
        vhm_available = VHM_AIRCRAFT_TOTAL - vhm_maintenance

        for mission in MISSIONS:
            req_aircrew = MISSION_REQUIREMENTS[mission]['aircrew']
            req_aircraft = MISSION_REQUIREMENTS[mission]['aircraft']

            if aircrews >= req_aircrew and (uhm_available + vhm_available) >= req_aircraft:
                mission_completion[mission].append(1)
                aircrews -= req_aircrew
                allocated_aircraft = min(req_aircraft, uhm_available)
                uhm_available -= allocated_aircraft
                vhm_available -= (req_aircraft - allocated_aircraft)
            else:
                mission_completion[mission].append(0)

        aircrew_availability.append(aircrews)
        uhm_vhm_availability.append(uhm_available + vhm_available)

    return mission_completion, aircrew_availability, uhm_vhm_availability

if st.button('Run The VH/UH-60M Simulation'):
    mission_completion, aircrew_availability, uhm_vhm_availability = run_simulation()

    # Plotting
    plt.figure(figsize=(14, 10))

    # Mission Completion Visualization
    plt.subplot(2, 1, 1)
    for mission, completion in mission_completion.items():
        plt.plot(completion, label=mission)
    plt.title('Mission Completion Status Over 30 Days')
    plt.ylabel('Completion Status (1=Yes, 0=No)')
    plt.xlabel('Day')
    plt.xticks(range(0, DAYS, 1))
    plt.legend()

    # Resource Availability Visualization
    plt.subplot(2, 1, 2)
    plt.plot(aircrew_availability, label='Aircrew Availability')
    plt.plot(uhm_vhm_availability, label='UHM + VHM Aircraft Availability')
    plt.title('Resource Availability After Allocation')
    plt.ylabel('Available Resources')
    plt.xlabel('Day')
    plt.xticks(range(0, DAYS, 1))
    plt.legend()

    plt.tight_layout()
    st.pyplot(plt)


# Assuming the rest of your Streamlit app and simulation setup is defined above

if st.button('Display Output'):
    mission_completion, aircrew_availability, uhm_vhm_availability = run_simulation()

    # Calculate Mission Completion Percentages
    mission_completion_percentages = {mission: (sum(completion) / DAYS) * 100 for mission, completion in mission_completion.items()}

    # Calculate Average Resource Availability
    average_aircrew_availability = sum(aircrew_availability) / DAYS
    average_uhm_vhm_availability = sum(uhm_vhm_availability) / DAYS

    # Display Mission Completion Percentages
    st.subheader("Mission Completion Percentages Over 30 Days:")
    for mission, percentage in mission_completion_percentages.items():
        st.write(f"- {mission}: {percentage:.2f}%")

    # Display Average Resource Availability After Allocation
    st.subheader("Average Resource Availability After Allocation:")
    st.write(f"- Average remaining aircrew availability: {average_aircrew_availability:.2f}")
    st.write(f"- Average remaining UHM + VHM aircraft availability: {average_uhm_vhm_availability:.2f}")

    # Plotting code from before goes here
