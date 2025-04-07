import pdfplumber
from docx import Document
from spacy.matcher import Matcher
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import spacy
from deep_translator import GoogleTranslator
import os
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import sys

TECH_SKILLS = ["python", "PYTHON DEVELOPER", "Python Developer"]

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'


def add_email_pattern(matcher):
    pattern = [{"text": {"regex": email_pattern}}]
    matcher.add("EMAIL", [pattern])


add_email_pattern(matcher)


def extract_tech_skills(text):
    tech_skills_found = []
    for skill in TECH_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            if len(tech_skills_found) != 1:
                tech_skills_found.append(skill)
            else:
                pass
    return tech_skills_found


def process_resumes(file_path=None, training_file=None):


    with open('entities.txt', 'w') as file:
        file.write("YEAR,EXPERIENCE,MAIL,TECH\n")


    with open('translated.txt', 'w') as file:
        file.write("")

    files = os.listdir(file_path)

    for file_name in files:
        full_path = os.path.join(file_path, file_name)
        if os.path.isfile(full_path):
            _, file_extension = os.path.splitext(full_path)
            text = ""
            if file_extension.lower() == ".docx":
                doc = Document(full_path)
                for paragraph in doc.paragraphs:
                    text += "\n" + paragraph.text

            elif file_extension.lower() == ".pdf":
                with pdfplumber.open(full_path) as pdf:
                    for page in pdf.pages:
                        text1 = page.extract_text()
                        doc = nlp(text1)
                        matches = matcher(doc)
                        h = []


                        if text1 and len(text1.strip()) > 10:
                            try:
                                detected_language = detect(text1)
                                if detected_language != 'en':
                                    text1 = GoogleTranslator(source='auto', target='en').translate(text1)
                                    translated = text1
                                    with open('translated.txt', 'a') as file:
                                        file.write("\n\n\n\n" + translated + "," "\n\n\n\n")
                            except:
                                pass


                        for ent in doc.ents:
                            if ent.label_ == "DATE":
                                years = [year.strip() for year in ent.text.split('-')]
                                for year in years:
                                    if "20" in year:
                                        h.append(year)


                        if h:
                            rl = h[1][-4:]
                            rs = h[1][-4:]
                            for i in h:
                                if int(rs) > int(i[-4:]):
                                    rs = int(i[-4:])
                                if int(rl) < int(i[-4:]):
                                    rl = int(i[-4:])

                                with open('entities.txt', 'a') as file:
                                    file.write(i[-4:] + ";")

                            with open('entities.txt', 'a') as file:
                                file.write(",")
                                totalyears = int(rl) - int(rs)
                                file.write(str(totalyears) + ",")


                        for match_id, start, end in matches:
                            email = doc[start:end].text
                            with open('entities.txt', 'a') as file:
                                file.write(email + ",")


                        tech_skills = extract_tech_skills(text1)
                        with open('entities.txt', 'a') as file:
                            file.write(";".join(tech_skills) + "\n")


    df = pd.read_csv('entities.txt', delimiter=',')
    df.to_csv('output.csv', index=False)


    news_dataset = pd.read_csv(training_file)
    x = news_dataset.drop(columns=["no", "email", "dependend"], axis=1)
    target_values = ['scapy', 'tkinter', 'beautifulsoup', 'tensorflow', 'scikit-learn', 'flask', 'django', 'python']

    column_to_map = 'TECH'
    x[column_to_map] = x[column_to_map].isin(target_values).astype(int)
    y = news_dataset["dependend"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, stratify=y, random_state=1)

    model = LogisticRegression()
    model.fit(x_train, y_train)

    new_data = pd.read_csv('output.csv')
    x_predict = new_data.drop(columns=["YEAR", "MAIL"], axis=1)
    x_predict[column_to_map] = x_predict[column_to_map].isin(target_values).astype(int)
    x_test_predict = model.predict(x_predict)


    new_data["Predicted_Value"] = x_test_predict
    new_data.to_csv('output.csv', index=False)

    return x_test_predict


if __name__ == "__main__":

    resume_dir = sys.argv[1] if len(sys.argv) > 1 else None
    training_file = sys.argv[2] if len(sys.argv) > 2 else None

    process_resumes(resume_dir, training_file)