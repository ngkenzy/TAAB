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

st.title('UHL Personnel Management Dashboard')

# Define roles and initialize DataFrame
roles = ['PC', 'PC/AMC', 'AMC', 'PI', 'CE']
df = pd.DataFrame(index=roles, columns=['Authorized', 'On Hand', 'Admin/DNIF', 'Loss', 'Staff', 'Leave', 'Available'])

# Input for Authorized row
authorized_input = st.number_input('Authorized for Pilots', min_value=0, value=30, key='authorized_pilots')
authorized_ce = st.number_input('Authorized for CE', min_value=0, value=43, key='authorized_ce')

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

def calculate_crew_compositions(PC, PC_AMC, AMC, PI, CE):
    # Initialize counters for each crew type
    crew_1_PC_1_PI_1_CE = 0
    crew_1_PC_AMC_1_PI_1_CE = 0
    crew_2_PC_AMC_1_CE = 0
    crew_2_PC_1_CE = 0

    # Crew compositions
    # 1 PC, 1 PI, 1 CE
    while PC >= 1 and PI >= 1 and CE >= 1:
        crew_1_PC_1_PI_1_CE += 1
        PC -= 1
        PI -= 1
        CE -= 1

    # 1 PC/AMC, 1 PI, 1 CE
    while PC_AMC >= 1 and PI >= 1 and CE >= 1:
        crew_1_PC_AMC_1_PI_1_CE += 1
        PC_AMC -= 1
        PI -= 1
        CE -= 1

    # 2 PC, 1 CE
    while PC >= 2 and CE >= 1:
        crew_2_PC_1_CE += 1
        PC -= 2
        CE -= 1

    # 2 PC/AMC, 1 CE
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
            "CE": CE-1
        }
    }

    return result

# Streamlit app layout
st.title('UH-60L Crew Composition Calculator')

# User inputs
PC = st.number_input('PC (Pilot in Command)', min_value=0, value=4)
PC_AMC = st.number_input('PC/AMC (Pilot/Air Mission Commander)', min_value=0, value=10)
AMC = st.number_input('AMC (Air Mission Commander)', min_value=0, value=0)  # Unused in crew compositions, can be set to zero or allowed for future flexibility
PI = st.number_input('PI (Pilot)', min_value=0, value=12)
CE = st.number_input('CE (Crew Engineer)', min_value=0, value=20)

# Calculate the crew compositions with the user's inputs
results = calculate_crew_compositions(PC, PC_AMC, AMC, PI, CE)

# Display the results
st.subheader('Maximum Number of Crews')
st.write(results["max_crews"])

st.subheader('Crew Compositions')
st.write(results["crew_compositions"])

st.subheader('Remaining Personnel')
st.write(results["remaining_personnel"])


def perform_maintenance_simulation(total_aircraft, phase_maintenance, iterations, days, maintenance_min, maintenance_max, maintenance_avg_min, maintenance_avg_max):
    np.random.seed(42)  # For reproducibility
    daily_maintenance = np.zeros((days, iterations))
    daily_available = np.zeros((days, iterations))

    for iteration in range(iterations):
        for day in range(days):
            daily_maintenance_count = np.random.randint(maintenance_avg_min, maintenance_avg_max+1)
            daily_maintenance[day, iteration] = daily_maintenance_count
            daily_available[day, iteration] = total_aircraft - phase_maintenance - daily_maintenance_count

    avg_daily_maintenance = np.mean(daily_maintenance, axis=1)
    avg_daily_available = np.mean(daily_available, axis=1)

    return avg_daily_maintenance, avg_daily_available


# Streamlit app layout
st.title('UH-60L Crew Composition and Aircraft Maintenance Calculator')

# Crew Composition Inputs
# Place your crew composition inputs here

# Aircraft Maintenance Inputs
total_aircraft = st.number_input('Total Aircraft', min_value=1, value=16)
phase_maintenance = st.number_input('Aircraft in Phase Maintenance', min_value=0, value=2)
iterations = st.number_input('Iterations for Simulation', min_value=100, value=1000)
days = st.number_input('Days to Simulate', min_value=1, value=30)
maintenance_min = st.number_input('Minimum Maintenance Duration (Days)', min_value=0, value=1)
maintenance_max = st.number_input('Maximum Maintenance Duration (Days)', min_value=maintenance_min, value=12)
maintenance_avg_min = st.number_input('Minimum Average Maintenance (Days)', min_value=maintenance_min, value=3)
maintenance_avg_max = st.number_input('Maximum Average Maintenance (Days)', min_value=maintenance_avg_min, value=6)

# Calculations
# Include your crew composition calculation call here if needed

# Aircraft Maintenance Simulation
avg_daily_maintenance, avg_daily_available = perform_maintenance_simulation(total_aircraft, phase_maintenance, iterations, days, maintenance_min, maintenance_max, maintenance_avg_min, maintenance_avg_max)

# Display Results for Crew Composition
# Include your crew composition results display here

# Display Results for Aircraft Maintenance Simulation
st.subheader('Aircraft Maintenance Simulation Results')
st.line_chart(avg_daily_maintenance, width=0, height=0, use_container_width=True)
st.write("Average Daily Maintenance")
st.line_chart(avg_daily_available, width=0, height=0, use_container_width=True)
st.write("Average Daily Availability")



import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def allocate_missions(total_aircrews, total_aircrafts, include_jadoc, jadoc_aircrews, jadoc_aircrafts):
    # Missions requirements
    missions = {
        'R': {'aircrews': 1, 'aircrafts': 1},
        'TPZ1 Day': {'aircrews': 2, 'aircrafts': 3},  # Including spare
        'TPZ1 Night': {'aircrews': 2, 'aircrafts': 0},  # Shared with TPZ1 Day
        'TPZ2 Day': {'aircrews': 2, 'aircrafts': 3},  # Including spare
        'TPZ2 Night': {'aircrews': 2, 'aircrafts': 0},  # Shared with TPZ2 Day
        'AMR': {'aircrews': 2, 'aircrafts': 2},
        'Training 1': {'aircrews': 1, 'aircrafts': 1},
        'Training 2': {'aircrews': 1, 'aircrafts': 1},
    }

    # Optionally include JADOC mission
    if include_jadoc:
        missions['JADOC'] = {'aircrews': jadoc_aircrews, 'aircrafts': jadoc_aircrafts}

    completed_missions = {}
    incomplete_missions = {}

    for mission, req in missions.items():
        if total_aircrews >= req['aircrews'] and total_aircrafts >= req['aircrafts']:
            completed_missions[mission] = req
            total_aircrews -= req['aircrews']
            total_aircrafts -= req['aircrafts']
        else:
            incomplete_missions[mission] = req

    remaining_resources = {
        'UHL Aircrews': total_aircrews,
        'UHL Aircrafts': total_aircrafts
    }

    return completed_missions, incomplete_missions, remaining_resources

# Streamlit app layout
st.title('Crew Composition, Aircraft Maintenance, and Mission Allocation Calculator')

# Inputs for mission allocation
total_aircrews_input = st.number_input('Total Aircrews', min_value=1, value=13)
total_aircrafts_input = st.number_input('Total Aircrafts', min_value=1, value=10)
include_jadoc = st.checkbox('Include JADOC Mission', value=False)

# Inputs for JADOC mission requirements, shown if JADOC is included
jadoc_aircrews, jadoc_aircrafts = 3, 3  # Defaults
if include_jadoc:
    jadoc_aircrews = st.number_input('JADOC Aircrews Required', min_value=1, value=3, key='jadoc_aircrews')
    jadoc_aircrafts = st.number_input('JADOC Aircrafts Required', min_value=1, value=3, key='jadoc_aircrafts')

# Perform mission allocation based on inputs
completed_missions, incomplete_missions, remaining_resources = allocate_missions(total_aircrews_input, total_aircrafts_input, include_jadoc, jadoc_aircrews, jadoc_aircrafts)

# Display mission allocation results
st.subheader('Mission Allocation Results')
st.write("Completed Missions:", list(completed_missions.keys()))
st.write("Incomplete Missions:", list(incomplete_missions.keys()))
st.write("Remaining Resources:", remaining_resources)

# Visualization omitted for brevity. Add your plotting code here.
st.title('Crew Composition, Aircraft Maintenance, and Mission Allocation Calculator')

# Mission Allocation Inputs
total_aircrews_input = st.number_input('Total Aircrews', min_value=1, value=13, key='UH60L_total_aircrews')
total_aircrafts_input = st.number_input('Total Aircrafts', min_value=1, value=10, key='UH60L_total_aircrafts')
jadoc_enabled = st.checkbox('Include JADOC Mission', value=True)

# If JADOC is enabled, provide inputs for its requirements
if jadoc_enabled:
    jadoc_aircrews = st.number_input('JADOC Aircrews Required', min_value=1, value=2, key='jadoc_aircrews')
    jadoc_aircrafts = st.number_input('JADOC Aircrafts Required', min_value=1, value=2, key='jadoc_aircrafts')

def allocate_missions(total_aircrews, total_aircrafts, include_jadoc, jadoc_req=None):
    # Missions requirements with conditional JADOC
    missions = {
        'R': {'aircrews': 1, 'aircrafts': 1},
        'TPZ1 Day': {'aircrews': 2, 'aircrafts': 3},
        'TPZ1 Night': {'aircrews': 2, 'aircrafts': 0},
        'TPZ2 Day': {'aircrews': 2, 'aircrafts': 3},
        'TPZ2 Night': {'aircrews': 2, 'aircrafts': 0},
        'AMR': {'aircrews': 2, 'aircrafts': 2},
        'Training 1': {'aircrews': 1, 'aircrafts': 1},
        'Training 2': {'aircrews': 1, 'aircrafts': 1},
    }
    if include_jadoc and jadoc_req:
        missions['JADOC'] = jadoc_req

    completed_missions = {}
    incomplete_missions = {}

    for mission, req in missions.items():
        if total_aircrews >= req['aircrews'] and total_aircrafts >= req['aircrafts']:
            completed_missions[mission] = req
            total_aircrews -= req['aircrews']
            total_aircrafts -= req['aircrafts']
        else:
            incomplete_missions[mission] = req

    remaining_resources = {
        'UHL Aircrews': total_aircrews,
        'UHL Aircrafts': total_aircrafts
    }

    return completed_missions, incomplete_missions, remaining_resources

# Perform Mission Allocation
if jadoc_enabled:
    jadoc_req = {'aircrews': jadoc_aircrews, 'aircrafts': jadoc_aircrafts}
else:
    jadoc_req = None
completed_missions, incomplete_missions, remaining_resources = allocate_missions(total_aircrews_input, total_aircrafts_input, jadoc_enabled, jadoc_req)

# Display Mission Allocation Results
st.subheader('Mission Allocation Results')
st.write("Completed Missions:", list(completed_missions.keys()))
st.write("Incomplete Missions:", list(incomplete_missions.keys()))
st.write("Remaining Resources:", remaining_resources)

# Visualization
fig, axs = plt.subplots(1, 3, figsize=(21, 7))

# Completed missions visualization
axs[0].bar(completed_missions.keys(), [val['aircrews'] for val in completed_missions.values()], label='Aircrews')
axs[0].bar(completed_missions.keys(), [val['aircrafts'] for val in completed_missions.values()], bottom=[val['aircrews'] for val in completed_missions.values()], label='Aircrafts')
axs[0].set_title('Completed Missions')
axs[0].tick_params(labelrotation=45)
axs[0].legend()

# Incomplete missions visualization
axs[1].bar(incomplete_missions.keys(), [1 for _ in incomplete_missions.values()], color='red', label='Incomplete')
axs[1].set_title('Incomplete Missions')
axs[1].tick_params(labelrotation=45)
axs[1].legend()

# Remaining resources visualization
resource_keys = list(remaining_resources.keys())
resource_values = list(remaining_resources.values())
axs[2].bar(resource_keys, resource_values, color=['blue', 'orange'])
axs[2].set_title('Remaining Resources')

plt.tight_layout()
st.pyplot(fig)

def calculate_mission_allocations(total_aircrews, total_aircrafts):
    # Missions dictionary as provided
    missions = {
        'R': {'aircrews': 1, 'aircrafts': 1},
        'TPZ1 Day': {'aircrews': 2, 'aircrafts': 3},  # Including spare
        'TPZ1 Night': {'aircrews': 2, 'aircrafts': 0},  # Shared with TPZ1 Day
        'TPZ2 Day': {'aircrews': 2, 'aircrafts': 3},  # Including spare
        'TPZ2 Night': {'aircrews': 2, 'aircrafts': 0},  # Shared with TPZ2 Day
        'JADOC': {'aircrews': 2, 'aircrafts': 2},  # JADOC Turn OFF
        'AMR': {'aircrews': 2, 'aircrafts': 2},
        'Training 1': {'aircrews': 1, 'aircrafts': 1},
        'Training 2': {'aircrews': 1, 'aircrafts': 1},
    }
    
    completed_missions = {}
    incomplete_missions = {}

    for mission, req in missions.items():
        if total_aircrews >= req['aircrews'] and total_aircrafts >= req['aircrafts']:
            completed_missions[mission] = req
            total_aircrews -= req['aircrews']
            total_aircrafts -= req['aircrafts']
        else:
            incomplete_missions[mission] = req
    
    # Remaining resources
    remaining_resources = {
        'UHL Aircrews': total_aircrews,
        'UHL Aircrafts': total_aircrafts
    }
    
    return completed_missions, incomplete_missions, remaining_resources

def perform_30_day_simulation(aircrew_range, aircraft_range, days=30):
    results = {
        'day': [],
        'completed_missions': [],
        'incomplete_missions': [],
        'remaining_aircrews': [],
        'remaining_aircrafts': []
    }
    
    for day in range(1, days + 1):
        aircrews = np.random.randint(aircrew_range[0], aircrew_range[1] + 1)
        aircrafts = np.random.randint(aircraft_range[0], aircraft_range[1] + 1)
        
        completed_missions, incomplete_missions, remaining_resources = calculate_mission_allocations(aircrews, aircrafts)
        
        # Record results
        results['day'].append(day)
        results['completed_missions'].append(len(completed_missions))
        results['incomplete_missions'].append(len(incomplete_missions))
        results['remaining_aircrews'].append(remaining_resources['UHL Aircrews'])
        results['remaining_aircrafts'].append(remaining_resources['UHL Aircrafts'])
    
    return results


#####################

# Streamlit App Layout
st.title('Mission Allocation and 30-Day Simulation')

# Inputs for total resources and ranges for simulation
total_aircrews_input = st.number_input('Total Aircrews', value=13)
total_aircrafts_input = st.number_input('Total Aircrafts', value=10)
aircrew_range_min = st.number_input('Minimum Aircrews Available Daily', value=11, min_value=0)
aircrew_range_max = st.number_input('Maximum Aircrews Available Daily', value=13, min_value=0)
aircraft_range_min = st.number_input('Minimum Aircrafts Available Daily', value=9, min_value=0)
aircraft_range_max = st.number_input('Maximum Aircrafts Available Daily', value=12, min_value=0)

# Perform simulation
simulation_results = perform_30_day_simulation((aircrew_range_min, aircrew_range_max), (aircraft_range_min, aircraft_range_max))

# Plotting the results
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# Completed missions
axs[0, 0].plot(simulation_results['day'], simulation_results['completed_missions'], marker='o', linestyle='-')
axs[0, 0].set_title('Completed Missions per Day')
axs[0, 0].set_xlabel('Day')
axs[0, 0].set_ylabel('Number of Completed Missions')

# Incomplete missions
axs[0, 1].plot(simulation_results['day'], simulation_results['incomplete_missions'], marker='o', linestyle='-', color='red')
axs[0, 1].set_title('Incomplete Missions per Day')
axs[0, 1].set_xlabel('Day')
axs[0, 1].set_ylabel('Number of Incomplete Missions')

# Remaining aircrews
axs[1, 0].plot(simulation_results['day'], simulation_results['remaining_aircrews'], marker='o', linestyle='-', color='green')
axs[1, 0].set_title('Remaining Aircrews per Day')
axs[1, 0].set_xlabel('Day')
axs[1, 0].set_ylabel('Number of Remaining Aircrews')

# Remaining aircrafts
axs[1, 1].plot(simulation_results['day'], simulation_results['remaining_aircrafts'], marker='o', linestyle='-', color='purple')
axs[1, 1].set_title('Remaining Aircrafts per Day')
axs[1, 1].set_xlabel('Day')
axs[1, 1].set_ylabel('Number of Remaining Aircrafts')

plt.tight_layout()

st.pyplot(fig)

def calculate_mission_allocations(total_aircrews, total_aircrafts, missions):
    completed_missions = {}
    incomplete_missions = {}
    for mission, req in missions.items():
        if total_aircrews >= req['aircrews'] and total_aircrafts >= req['aircrafts']:
            completed_missions[mission] = req
            total_aircrews -= req['aircrews']
            total_aircrafts -= req['aircrafts']
        else:
            incomplete_missions[mission] = req
    remaining_resources = {'UHL Aircrews': total_aircrews, 'UHL Aircrafts': total_aircrafts}
    return completed_missions, incomplete_missions, remaining_resources

def perform_30_day_simulation(aircrew_range, aircraft_range, include_jadoc=True, days=30):
    missions = {
        'R': {'aircrews': 1, 'aircrafts': 1},
        'TPZ1 Day': {'aircrews': 2, 'aircrafts': 3},
        'TPZ1 Night': {'aircrews': 2, 'aircrafts': 0},
        'TPZ2 Day': {'aircrews': 2, 'aircrafts': 3},
        'TPZ2 Night': {'aircrews': 2, 'aircrafts': 0},
        'AMR': {'aircrews': 2, 'aircrafts': 2},
        'Training 1': {'aircrews': 1, 'aircrafts': 1},
        'Training 2': {'aircrews': 1, 'aircrafts': 1},
    }
    
    # Conditionally include JADOC based on the toggle
    if include_jadoc:
        missions['JADOC'] = {'aircrews': 2, 'aircrafts': 2}  # Adjust these numbers as per requirements

    mission_completions = {mission: 0 for mission in missions.keys()}
    mission_incompletions = {mission: 0 for mission in missions.keys()}

    for day in range(1, days + 1):
        aircrews = np.random.randint(aircrew_range[0], aircrew_range[1] + 1)
        aircrafts = np.random.randint(aircraft_range[0], aircraft_range[1] + 1)
        
        completed_missions, incomplete_missions, _ = calculate_mission_allocations(aircrews, aircrafts, missions)
        
        for mission in completed_missions:
            mission_completions[mission] += 1
        
        for mission in incomplete_missions:
            mission_incompletions[mission] += 1

    average_completions = {mission: completions / days for mission, completions in mission_completions.items()}
    average_incompletions = {mission: incompletions / days for mission, incompletions in mission_incompletions.items()}
    
    return average_completions, average_incompletions

# Streamlit App Layout
st.title('Mission Allocation and 30-Day Simulation')


# Perform simulation
average_completions, average_incompletions = perform_30_day_simulation((aircrew_range_min, aircrew_range_max), (aircraft_range_min, aircraft_range_max))

# Convert dictionary to two columns for Streamlit
completion_df = pd.DataFrame(list(average_completions.items()), columns=['Mission', 'Average Completions'])
incompletion_df = pd.DataFrame(list(average_incompletions.items()), columns=['Mission', 'Average Incompletions'])

# Plotting the results with Streamlit
st.subheader('Average Mission Completions over 30 Days')
st.bar_chart(completion_df.set_index('Mission'))

st.subheader('Average Mission Incompletions over 30 Days')
st.bar_chart(incompletion_df.set_index('Mission'))


