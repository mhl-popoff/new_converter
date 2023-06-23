# Импорт PyMuPDF для модуля Python
import fitz

def process_pdf(pdf_document):
    output_file = "text/output.txt"

    doc = fitz.open(pdf_document)

    # Извлекаем и сохраняем текст в файле TXT
    with open(output_file, "w", encoding="utf-8") as stream:
        for page in doc:
            page_text = page.get_text("text").replace('\xa0', ' ')
            stream.write(page_text)
             
             