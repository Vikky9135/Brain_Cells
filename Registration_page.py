import streamlit as st

def main():
    st.title("Voting System Registration")

    adhar_number = st.text_input("Adhar Number:")
    voter_id = st.text_input("Voter ID Number:")
    ward_number = st.text_input("Ward Number:")

    if st.button("Submit"):
        if adhar_number and voter_id and ward_number:
            st.success("Registration Successful!")
        else:
            st.error("Please fill in all the details.")

if __name__ == "__main__":
    main()
