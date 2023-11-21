import streamlit as st
import cv2
import face_recognition
import pickle

# Function to encode and save face data to a file during registration
def encode_and_save_face_registration(frame, name, aadhar, voter_id, ward, encoding_file='registration_data.pkl'):
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    if len(face_encodings) > 0:
        encoding_data = {'name': name, 'aadhar': aadhar, 'voter_id': voter_id, 'ward': ward, 'encoding': face_encodings[0]}
        try:
            with open(encoding_file, 'rb') as file:
                existing_data = pickle.load(file)
                existing_data.append(encoding_data)
            with open(encoding_file, 'wb') as file:
                pickle.dump(existing_data, file)
            st.success(f"Registration Successful for {name}!")
        except FileNotFoundError:
            with open(encoding_file, 'wb') as file:
                pickle.dump([encoding_data], file)
            st.success(f"Registration Successful for {name}!")
    else:
        st.warning("No face found in the frame during registration.")

# Function to recognize a face and verify details during login
def recognize_face_login(frame, entered_aadhar, entered_voter_id, entered_ward, encoding_file='registration_data.pkl'):
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    if len(face_encodings) > 0:
        with open(encoding_file, 'rb') as file:
            registered_data = pickle.load(file)

        for data in registered_data:
            known_encoding = data['encoding']
            result = face_recognition.compare_faces([known_encoding], face_encodings[0])

            if result[0]:
                # Face recognized, now check other details
                if (
                    entered_aadhar == data['aadhar']
                    and entered_voter_id == data['voter_id']
                    and entered_ward == data['ward']
                ):
                    return f"Welcome back, {data['name']}!"
                else:
                    return "Details do not match. Please check your information."

        return "Face not recognized. Please try again or register if you are a new user."
    else:
        return "No face found in the frame during login."

# Create a session state to manage the state between pages
class SessionState:
    def __init__(self):
        self.page = "Home"
        self.name = ""
        self.aadhar_number = ""
        self.voter_id_number = ""
        self.ward_number = ""

# Streamlit app
state = SessionState()

# Page functions
def registration_page():
    st.title("Registration Page")

    # Input fields for registration
    state.name = st.text_input("Enter Your Name:")
    state.aadhar_number = st.text_input("Enter Aadhar Number:")
    state.voter_id_number = st.text_input("Enter Voter ID Number:")
    state.ward_number = st.text_input("Enter Ward Number:")

    # Open a video capture object for registration
    video_capture_registration = cv2.VideoCapture(0)  # Use 0 for default camera, you may need to change this number

    # Placeholder for displaying the video stream during registration
    video_placeholder_registration = st.empty()

    # Button to capture a frame and perform face encoding during registration
    if st.button("Capture Frame for Registration"):
        ret, frame_registration = video_capture_registration.read()
        video_placeholder_registration.image(frame_registration, channels="BGR")

        # Perform face encoding and save registration data
        encode_and_save_face_registration(frame_registration, state.name, state.aadhar_number, state.voter_id_number, state.ward_number)

    # Release the video capture object for registration
    video_capture_registration.release()

def login_page():
    st.title("Login Page")

    # Input fields for login
    entered_aadhar_number = st.text_input("Enter Aadhar Number for Login:")
    entered_voter_id_number = st.text_input("Enter Voter ID Number for Login:")
    entered_ward_number = st.text_input("Enter Ward Number for Login:")

    # Open a video capture object for login
    video_capture_login = cv2.VideoCapture(0)  # Use 0 for default camera, you may need to change this number

    # Placeholder for displaying the video stream during login
    video_placeholder_login = st.empty()

    # Button to capture a frame and perform face recognition during login
    if st.button("Perform Face Recognition for Login"):
        ret, frame_login = video_capture_login.read()
        video_placeholder_login.image(frame_login, channels="BGR")

        # Perform face recognition and verify details for login
        login_result = recognize_face_login(frame_login, entered_aadhar_number, entered_voter_id_number, entered_ward_number)
        st.info(login_result)

    # Release the video capture object for login (This line should be executed when the app stops)
    video_capture_login.release()

# Navigation
st.sidebar.title("Navigation")
pages = ["Home", "Registration", "Login"]
state.page = st.sidebar.radio("Go to", pages)

# Render pages
if state.page == "Registration":
    registration_page()
elif state.page == "Login":
    login_page()
else:
    st.title("Home Page")
    st.write("Welcome to the Home Page!")

# Save state for next time
state.sync()
