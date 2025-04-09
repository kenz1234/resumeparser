import streamlit as st
import pandas as pd
import os
import sys
import subprocess
import tempfile


def upload_resume_files():
    """
    Use Streamlit to upload multiple resume files
    """
    uploaded_files = st.file_uploader("Upload Resume Files", 
                                      type=["pdf", "docx", "txt"],
                                      accept_multiple_files=True)

    if uploaded_files:
        # Create a temporary directory to store the uploaded files
        temp_dir = tempfile.mkdtemp()
        st.session_state['temp_resume_dir'] = temp_dir

        st.write(f"Uploaded {len(uploaded_files)} resume files:")
        
        # Save each uploaded file to the temporary directory
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.write(uploaded_file.name)

        return temp_dir
    
    return None


def select_training_dataset():
    """
    Use Streamlit to upload a training dataset CSV file
    """
    uploaded_file = st.file_uploader("Upload training dataset CSV", type=["csv"])

    if uploaded_file:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        temp_file.write(uploaded_file.getbuffer())

        try:
            df = pd.read_csv(temp_file.name)
            st.write(f"Training dataset preview ({len(df)} records):")
            st.dataframe(df.head())
            return temp_file.name
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
            os.unlink(temp_file.name)

    return None


def run_resume_processing(resume_dir, training_file):
    """
    Run the resume processing script and capture its output
    """
    try:
        result = subprocess.run([sys.executable, 'resume_processing.py', resume_dir, training_file],
                                capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)


def main():
    st.title("Wayne Enterprises: Resume Sorting Process")

    st.sidebar.header("Resume Processing Workflow")

    # Initialize session state if needed
    if 'temp_resume_dir' not in st.session_state:
        st.session_state['temp_resume_dir'] = None

    st.header("1. Upload Resume Files")
    uploaded_resume_dir = upload_resume_files()

    st.header("2. Converting txt or word files to PDF")
    if uploaded_resume_dir and st.button("Click here to Convert"):
        with st.spinner('Converting...'):
            subprocess.run([sys.executable, 'convert.py', uploaded_resume_dir])
        st.success("Uploaded files converted into PDF successfully!")

    st.header("3. Select Training Dataset")
    selected_training_file = select_training_dataset()

    st.header("4. Process these Resumes")
    resume_dir_to_process = uploaded_resume_dir or st.session_state.get('temp_resume_dir')
    
    if resume_dir_to_process and selected_training_file and st.button("Click here to process"):
        with st.spinner('Processing resumes...'):
            stdout, stderr = run_resume_processing(resume_dir_to_process, selected_training_file)

            if stderr:
                st.error(f"Error occurred: {stderr}")
            else:
                st.success("Resume processing completed!")

    st.header("5. Candidate Results")
    try:
        results_df = pd.read_csv('output.csv')
        st.dataframe(results_df)

        selected_candidates = results_df[results_df['Predicted_Value'] == 1]
        st.subheader("Selected Candidates")
        st.dataframe(selected_candidates)

    except FileNotFoundError:
        st.warning("No results available. Please process resumes first.")

    st.title("6. Translated File")
    try:
        with open("translated.txt", "r", encoding="latin-1") as file:
            content = file.read()
            st.text_area("File Contents:", content, height=300)
    except FileNotFoundError:
        st.error("File 'translated.txt' not found. Please make sure the file exists in the directory.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    st.header("7. Send Interview Invitations")
    if st.button("Send Emails to Selected Candidates"):
        with st.spinner('Sending emails...'):
            subprocess.run([sys.executable, 'email_sender.py'])
        st.success("Emails sent to selected candidates!")


if __name__ == "__main__":
    main()
