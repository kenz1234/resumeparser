import streamlit as st
import pandas as pd
import os
import sys
import subprocess
import tempfile
from pathlib import Path

st.set_page_config(
    page_title="Wayne Enterprises: Resume Sorting Process",
    page_icon="📄",
    layout="wide"
)

TEMP_DIR = Path(os.getcwd()) / "temp_resumes"
OUTPUT_FILE = Path(os.getcwd()) / "output.csv"
TRANSLATED_FILE = Path(os.getcwd()) / "translated.txt"

def upload_resume_files():
    """
    Use Streamlit to upload resume files directly
    """
    uploaded_files = st.file_uploader("Upload Resume Files", 
                                    accept_multiple_files=True,
                                    type=['pdf', 'docx', 'txt'])
    
    if uploaded_files:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.success(f"Successfully uploaded {len(uploaded_files)} resume files")
        

        os.makedirs(TEMP_DIR, exist_ok=True)
        with st.expander("View uploaded files", expanded=False):
            for uploaded_file in uploaded_files:
                st.write(f"- {uploaded_file.name}")

                file_path = os.path.join(TEMP_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
        
        return TEMP_DIR
    
    return None

def upload_training_dataset():
    """
    Use Streamlit to upload a training dataset CSV file
    """
    uploaded_file = st.file_uploader("Upload training dataset CSV", type=["csv"])

    if uploaded_file:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        temp_file.write(uploaded_file.getbuffer())
        temp_file.close()

        try:
  
            df = pd.read_csv(temp_file.name)
            with st.expander("Training dataset preview", expanded=False):
                st.dataframe(df.head(5))
                st.info(f"Total records: {len(df)}")
            return temp_file.name
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    return None

def convert_files():
    """
    Convert txt and docx files to PDF
    """
    try:
        result = subprocess.run([sys.executable, 'convert.py'], 
                               capture_output=True, text=True, check=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except subprocess.CalledProcessError as e:
        return False, f"Process error: {e}"
    except FileNotFoundError:
        return False, "Convert script not found. Please ensure 'convert.py' exists in the directory."
    except Exception as e:
        return False, f"Unexpected error: {e}"

def run_resume_processing(resume_dir, training_file):
    """
    Run the resume processing script and capture its output
    """
    try:
        result = subprocess.run(
            [sys.executable, 'resume_processing.py', str(resume_dir), training_file],
            capture_output=True, text=True, check=True
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except subprocess.CalledProcessError as e:
        return False, f"Process error: {e}"
    except FileNotFoundError:
        return False, "Resume processing script not found. Please ensure 'resume_processing.py' exists in the directory."
    except Exception as e:
        return False, f"Unexpected error: {e}"

def send_invitation_emails():
    """
    Send interview invitations to selected candidates
    """
    try:
        if not os.path.exists(OUTPUT_FILE):
            return False, "No results available. Please process resumes first."
            

        results_df = pd.read_csv(OUTPUT_FILE)
        selected_candidates = results_df[results_df['Predicted_Value'] == 1]
        
        if len(selected_candidates) == 0:
            return False, "No candidates were selected to receive emails."
            
        result = subprocess.run(
            [sys.executable, 'email_sender.py'],
            capture_output=True, text=True, check=True
        )
        if result.returncode == 0:
            return True, f"Successfully sent emails to {len(selected_candidates)} candidates."
        else:
            return False, result.stderr
    except subprocess.CalledProcessError as e:
        return False, f"Process error: {e}"
    except FileNotFoundError:
        return False, "Email sender script not found. Please ensure 'email_sender.py' exists in the directory."
    except Exception as e:
        return False, f"Unexpected error: {e}"

def display_results():
    """
    Display the results of resume processing
    """
    try:
        if not os.path.exists(OUTPUT_FILE):
            st.warning("No results available. Please process resumes first.")
            return False
            
        results_df = pd.read_csv(OUTPUT_FILE)
        

        tab1, tab2 = st.tabs(["All Candidates", "Selected Candidates"])
        
        with tab1:
            st.dataframe(
                results_df,
                use_container_width=True,
                hide_index=True
            )
        
        with tab2:
            selected_candidates = results_df[results_df['Predicted_Value'] == 1]
            if len(selected_candidates) > 0:
                st.dataframe(
                    selected_candidates,
                    use_container_width=True,
                    hide_index=True
                )
                st.success(f"Found {len(selected_candidates)} qualified candidates")
            else:
                st.warning("No candidates met the selection criteria")
        
        return True
    except Exception as e:
        st.error(f"Error displaying results: {e}")
        return False

def display_translated_content():
    """
    Display the contents of the translated file
    """
    try:
        if not os.path.exists(TRANSLATED_FILE):
            st.warning("File 'translated.txt' not found. Please make sure the file exists in the directory.")
            return False
            
        with open(TRANSLATED_FILE, "r", encoding="utf-8") as file:
            try:
                content = file.read()
            except UnicodeDecodeError:
 
                with open(TRANSLATED_FILE, "r", encoding="latin-1") as file2:
                    content = file2.read()
                    
        st.text_area("File Contents:", content, height=300)
        return True
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        return False

def main():

    
    if 'upload_complete' not in st.session_state:
        st.session_state.upload_complete = False
    if 'conversion_complete' not in st.session_state:
        st.session_state.conversion_complete = False
    if 'training_complete' not in st.session_state:
        st.session_state.training_complete = False
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", 
                            ["Upload & Process", "View Results", "Send Invitations"],
                            index=0)
    
    st.sidebar.markdown("---")
    st.sidebar.info("Wayne Enterprises HR Department")

    if page == "Upload & Process":

        st.markdown('<p class="step-header">Step 1: Upload Resume Files</p>', unsafe_allow_html=True)
        resume_dir = upload_resume_files()
        if resume_dir:
            st.session_state.upload_complete = True

        st.markdown('<p class="step-header">Step 2: Convert Files to PDF</p>', unsafe_allow_html=True)
        convert_btn = st.button("Convert Files", 
                               disabled=not st.session_state.upload_complete,
                               use_container_width=True)
        
        if convert_btn:
            with st.spinner('Converting files...'):
                success, message = convert_files()
                if success:
                    st.success("Files converted successfully!")
                    st.session_state.conversion_complete = True
                else:
                    st.error(f"Conversion failed: {message}")


        st.markdown('<p class="step-header">Step 3: Upload Training Dataset</p>', unsafe_allow_html=True)
        training_file = upload_training_dataset()
        if training_file:
            st.session_state.training_complete = True

   
        st.markdown('<p class="step-header">Step 4: Process Resumes</p>', unsafe_allow_html=True)
        process_ready = st.session_state.upload_complete and st.session_state.training_complete
        
        process_btn = st.button("Process Resumes", 
                              disabled=not process_ready,
                              use_container_width=True)
        
        if process_btn and resume_dir and training_file:
            with st.spinner('Processing resumes... This may take a while'):
                success, message = run_resume_processing(resume_dir, training_file)
                if success:
                    st.success("Resume processing completed successfully!")
                    st.session_state.processing_complete = True
                    st.balloons()
                else:
                    st.error(f"Processing failed: {message}")

    elif page == "View Results":

        st.markdown('<p class="step-header">Step 5: Candidate Results</p>', unsafe_allow_html=True)
        display_results()
        

        st.markdown('<p class="step-header">Step 6: Translated Content</p>', unsafe_allow_html=True)
        display_translated_content()

    elif page == "Send Invitations":

        st.markdown('<p class="step-header">Step 7: Send Interview Invitations</p>', unsafe_allow_html=True)
  
        if st.button("Send Emails to Selected Candidates", use_container_width=True):
            confirm = st.warning("Are you sure you want to send emails to all selected candidates?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, send emails"):
                    with st.spinner('Sending emails...'):
                        success, message = send_invitation_emails()
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
            with col2:
                if st.button("Cancel"):
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
