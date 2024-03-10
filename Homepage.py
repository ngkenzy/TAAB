import streamlit as st

st.set_page_config(
    page_title="The Army Aviation Brigade Analyzer Tool",
    page_icon=":bar_chart:",
)

st.title("The Army Aviation Brigade Analyzer Tool")
st.sidebar.success("Select a page above.")
#         ______
#         _\ _~-\___
#=  = ==(____AA____D
#             \_____\___________________,-~~~~~~~`-.._
#             /     o O o o o o O O o o o o o o O o  |\_
#             `~-.__        ___..----..                  )
#                   `---~~\___________/------------`````
#                   =  ===(_________)

# Displaying pilot and CE authorized numbers
st.header('Authorized Personnel')

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Pilot Authorized")
    st.write("153M Pilot Authorized: 23")
    st.write("153D Pilot Authorized: 30")

with col2:
    st.subheader("CE Authorized")
    st.write("Total Required: 64")
    st.write("- UH60M: 21")
    st.write("- UH60L: 43")
    st.write("CE TDA: 58 authorized")

with col3:
    st.subheader("Staff Authorized")
    st.write("Total: 17")

# Displaying officer positions
st.header("Officer Positions")
officers = [
    "O2 PLT LDR", "O2 EXECUTIVE OFFICER", "O2 PLT LDR", "O2 PLT LDR",
    "O5 COMMANDER", "O4 EXECUTIVE OFFICER", "O4 S3", "O3 ASST S3",
    "O3 TRAINING OFFICER", "O3 FLT OPERATIONS OFF", "O3 COMMANDER",
    "O3 COMMANDER", "O3 COMMANDER", "O3 COMMANDER", "O3 COMMANDER",
    "O3 ADJUTANT", "O3 S4"
]

# Use for loop to display officers neatly
for officer in officers:
    st.write(officer)