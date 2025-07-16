import easyocr
import spacy
import re
import json

# Initialize OCR and NLP globally for performance
reader = easyocr.Reader(['en'])
nlp = spacy.load("en_core_web_sm")

def process_medical_document(image_path):
    # OCR
    results = reader.readtext(image_path)
    ocr_text = " ".join([text for (_, text, _) in results])

    # NLP
    doc = nlp(ocr_text)

    # Extract patient name
    patient_name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            patient_name = ent.text
            break

    # Extract age
    age_match = re.search(r'Age[:\-]?\s*(\d+)', ocr_text, re.IGNORECASE)
    age = age_match.group(1) if age_match else None

    # Extract gender
    gender_match = re.search(r'Gender[:\-]?\s*(Male|Female)', ocr_text, re.IGNORECASE)
    gender = gender_match.group(1) if gender_match else None

    # Extract medicines
    medicines = []
    medicine_pattern = re.compile(r'([A-Za-z]+)\s+(\d+mg)\s+([a-z\s]+)', re.IGNORECASE)
    for match in medicine_pattern.finditer(ocr_text):
        med_name = match.group(1)
        dosage = match.group(2)
        frequency = match.group(3).strip()
        medicines.append({
            "name": med_name,
            "dosage": dosage,
            "frequency": frequency
        })

    # Final structured output
    output = {
        "patient_name": patient_name,
        "age": age,
        "gender": gender,
        "medicines": medicines
    }

    return output
