import fitz  # PyMuPDF

def extract_questions_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    questions = []

    for page in doc:
        text = page.get_text()
        lines = text.split('\n')
        q_text = ""
        options = []
        for line in lines:
            if line.strip().startswith(tuple(str(i) + "." for i in range(1, 100))):
                if q_text:
                    questions.append({"question": q_text.strip(), "options": options})
                    options = []
                q_text = line.strip()
            elif line.strip().startswith(tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")):
                options.append(line.strip())
        # Append last question
        if q_text:
            questions.append({"question": q_text.strip(), "options": options})
    return questions


if __name__ == "__main__":
    pdf_path = "questions/G5-CogAt-Practice-Test-2-Figure-Classification.pdf"
    q_data = extract_questions_from_pdf(pdf_path)
    for q in q_data:
        print(q)
