import PyPDF2
from fuzzywuzzy import fuzz

def process_pdf(pdf_document, search_query):
    results = []

    with open(pdf_document, 'rb') as file:
        reader = PyPDF2.PdfReader(file)


        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            text = text.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')

            # Вычисление сходства строки поиска с текстом страницы
            match_score = fuzz.partial_ratio(search_query.lower(), text.lower())

            # Если сходство выше 50%, добавить результат в список
            if match_score >= 81:
                results.append((page_number, match_score, 'Совпадение'))
            elif 81 > match_score >= 65:
                results.append((page_number, match_score, 'Внимание, необходимо проверить!'))

    return results, search_query