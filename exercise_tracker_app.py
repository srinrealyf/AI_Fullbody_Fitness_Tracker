# exercise_tracker_app.py
import streamlit as st
import subprocess

# Function to run the selected exercise tracker
def run_tracker(exercise):
    python_executable = "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3"  # Replace this with the full path to your Python executable

    if exercise == "Push-Ups":
        subprocess.Popen([python_executable, "pushups_tracker.py"])
    elif exercise == "Sit-Ups":
        subprocess.Popen([python_executable, "situps_tracker.py"])

# Streamlit app
def main():
    st.title("AI Exercise Tracker App")

    # User input for exercise selection
    exercise_choice = st.radio("Select Exercise", ["Push-Ups", "Sit-Ups"])

    # Run the selected exercise tracker
    if st.button("Start Tracking"):
        st.write(f"Tracking {exercise_choice}... Please wait.")
        run_tracker(exercise_choice)

if __name__ == "__main__":
    main()
