import fitz  # PyMuPDF
import os
import io
from PIL import Image
import json

def lowercase_camel_case(name):
    parts = name.replace("-", " ").replace("_", " ").split()
    return parts[0].lower() + ''.join(w.capitalize() for w in parts[1:])

def extract_question_and_option_images(pdf_path):
    doc = fitz.open(pdf_path)
    filename_prefix = lowercase_camel_case(os.path.splitext(os.path.basename(pdf_path))[0])

    output_folder = os.path.splitext(pdf_path)[0]
    os.makedirs(output_folder, exist_ok=True)

    results = []
    q_counter = 1

    for page_num, page in enumerate(doc):
        if page_num == 0:  # Skip sample page
            continue

        pix = page.get_pixmap(dpi=300)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))

        width, height = img.size
        section_height = height // 7  # Divide page into 7 equal sections

        # Section ranges
        def section_range(start, end):
            return (0, section_height * start, width, section_height * end)

        # Question 1: sections 2 and 3
        q1_range = section_range(1, 2.5)  # section 2

        q1_question_img = img.crop(q1_range)

        q1_question_path = os.path.join(output_folder, f"{filename_prefix}_{q_counter}_question.png")

        q1_question_img.save(q1_question_path)

        results.append({
            "question": q1_question_path,
            "id": f"{filename_prefix}_{q_counter}"
        })

        q_counter += 1

        # Question 2: sections 4, 5, and 6
        q2_range = section_range(3, 4)
        q2_mid_range = section_range(4, 5)

        q2_question_img = img.crop((0, q2_range[1], width, q2_mid_range[3]))

        q2_question_path = os.path.join(output_folder, f"{filename_prefix}_{q_counter}_question.png")

        q2_question_img.save(q2_question_path)

        results.append({
            "question": q2_question_path,
            "id": f"{filename_prefix}_{q_counter}"
        })

        q_counter += 1

    return results

if __name__ == "__main__":
    pdf_path = "questions/G5-CogAt-Practice-Test-2-Figure-Classification.pdf"
    data = extract_question_and_option_images(pdf_path)

    json_output = json.dumps(data, indent=2)
    #print(json_output)

    json_path = os.path.splitext(pdf_path)[0] + "_questions.json"
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(json_output)
