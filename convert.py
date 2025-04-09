import win32com.client as win32
import os
import tempfile
import sys

def change_permissions(file_path, permissions):
    try:
        os.chmod(file_path, permissions)
        print(f"Permissions changed for {file_path}")
    except Exception as e:
        print(f"Error changing permissions: {e}")

def convert_docx_to_pdf(docx_path, pdf_path):
    try:
        word = win32.Dispatch("Word.Application")
        doc = word.Documents.Open(docx_path)
        doc.SaveAs(pdf_path, FileFormat=17)  # 17 = pdf
        doc.Close()
        word.Quit()
        return True
    except Exception as e:
        print(f"Error converting docx to pdf: {e}")
        return False

def convert_txt_to_pdf(txt_path, pdf_path):
    try:
        word = win32.Dispatch("Word.Application")
        # Create a temporary docx file
        temp_docx = tempfile.NamedTemporaryFile(suffix='.docx', delete=False).name
        # Open a new document
        doc = word.Documents.Add()
        # Read the text file content
        with open(txt_path, 'r', encoding='utf-8', errors='ignore') as txt_file:
            content = txt_file.read()
        # Insert the content
        doc.Content.Text = content
        # Save as temporary docx
        doc.SaveAs(temp_docx)
        # Save as PDF
        doc.SaveAs(pdf_path, FileFormat=17)  # 17 = pdf
        # Close and clean up
        doc.Close()
        word.Quit()
        # Remove temporary file
        try:
            os.remove(temp_docx)
        except:
            pass
        return True
    except Exception as e:
        print(f"Error converting txt to pdf: {e}")
        return False

def convert_file_to_pdf(input_path, output_path):
    file_extension = os.path.splitext(input_path)[1].lower()
    change_permissions(input_path, 0o777)
    if file_extension == '.docx':
        return convert_docx_to_pdf(input_path, output_path)
    elif file_extension == '.txt':
        return convert_txt_to_pdf(input_path, output_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return False

if __name__ == "__main__":
    # Get input folder from command line argument if provided
    if len(sys.argv) > 1:
        input_folder = os.path.abspath(sys.argv[1])
    else:
        # Use relative path to Resumestr folder in the current directory
        input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resumestr")
    
    # Use the same folder for output
    output_folder = input_folder
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    successful = 0
    failed = 0
    
    for filename in os.listdir(input_folder):
        if filename.endswith((".docx", ".txt")):
            input_path = os.path.join(input_folder, filename)
            pdf_filename = os.path.splitext(filename)[0] + "_converted.pdf"
            output_path = os.path.join(output_folder, pdf_filename)
            print(f"Processing {filename}...")
            if convert_file_to_pdf(input_path, output_path):
                print(f"Successfully converted {filename} to {pdf_filename}")
                successful += 1
            else:
                print(f"Failed to convert {filename}")
                failed += 1
    
    print(f"\nConversion complete: {successful} successful, {failed} failed")
