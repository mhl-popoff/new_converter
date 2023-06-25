import os
import PyPDF2
from celery import Celery
from fuzzywuzzy import fuzz
from shutil import copyfile

app = Celery('tasks', broker='redis://localhost:6379/0')

def copy_file(source_file, destination_file):
    if os.path.exists(destination_file):
        os.remove(destination_file)
    copyfile(source_file, destination_file)
@app.task
def process_pdf_task(pdf_document, search_query, file_name):
    results = []
    success_list = []  # верные документы
    general_list = []  # общее количество документов
    with open(pdf_document, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            text = text.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
            match_score = fuzz.partial_ratio(search_query.lower(), text.lower())
            count_success = 0
            count_general = 0
            if match_score >= 81:
                results.append((page_number, match_score, 'Допустимо'))
                count_success += 1
                count_general += 1
            elif 81 > match_score >= 65:
                results.append((page_number, match_score, 'Внимание, необходимо проверить!'))
                count_general += 1
            success_list.append(count_success)
            general_list.append(count_general)
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    output_file = os.path.join(results_dir, f"{file_name}_results.html")
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write(f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<h1>Объект капитального строительства: {search_query}</h1><br>""")
        if not results:
            output.write("<h3>В этом документе совпадений не найдено.</h3>")
        else:
            for i, result in enumerate(results, start=1):
                page_number, match_score, comment = result
                if comment == 'Допустимо':
                    output.write(
                        f"<li class='green'>{i}. Найдено совпадение на странице {page_number} - процент сходства {match_score}% - <b>{comment}</b> - <a href={'../media/' + pdf_document.split('/')[-1]}>Подробнее...</a></li>")
                elif comment == 'Внимание, необходимо проверить!':
                    output.write(
                        f"<li class='red'>{i}. Найдено совпадение на странице {page_number} - процент сходства {match_score}% - <b>{comment}</b> - <a href={'../media/' + pdf_document.split('/')[-1]}>Подробнее...</a></li>")









# <h1>Объект капитального строительства: {search_query}</h1><br>""")
#         if not results:
#             output.write("<h3>В этом документе совпадений не найдено.</h3>")
#         else:
#             for i, result in enumerate(results, start=1):
#                 page_number, match_score, comment = result
#                 output.write(f"<li>{i}. Найдено совпадение на странице {page_number} - процент сходства {match_score}% - <b>{comment}</b> - <a href={'../media/' + pdf_document.split('/')[-1]}>Подробнее...</a></li>")


# import os
# import PyPDF2
# from celery import Celery
# from fuzzywuzzy import fuzz

# app = Celery('tasks', broker='redis://localhost:6379/0')

# @app.task
# def process_pdf_task(pdf_document, search_query, file_name):
#     with open(pdf_document, 'rb') as file:
#         results = []
#         reader = PyPDF2.PdfReader(file)
#         for page_number, page in enumerate(reader.pages, start=1):
#             text = page.extract_text()
#             text = text.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
#             match_score = fuzz.partial_ratio(search_query.lower(), text.lower())
#             if match_score >= 81:
#                 results.append((page_number, match_score, 'Допустимое совпадение'))
#             elif 81 > match_score >= 65:
#                 results.append((page_number, match_score, 'Внимание, необходимо проверить!'))
#     results_dir = "results"
#     if not os.path.exists(results_dir):
#         os.makedirs(results_dir)
#     output_file = os.path.join(results_dir, f"{file_name}_search_results.html")
#     with open(output_file, 'w') as output:
#         output.write(f"<h1>Объект капитального строительства: {search_query}</h1><br>")
#         if not results:
#             output.write("<p>В этом документе совпадений не найдено.</p>")
#         else:
#             for i, result in enumerate(results, start=1):
#                 page_number, match_score, comment = result
#                 output.write(f"<li>{i}. Найдено совпадение на странице {page_number} - процент сходства {match_score}% - <b>{comment}</b> - <a href={pdf_document}>{pdf_document}</a></li>")

# import os
# import PyPDF2
# from celery import Celery
# from fuzzywuzzy import fuzz

# app = Celery('tasks', broker='redis://localhost:6379/0')

# @app.task
# def process_pdf_task(pdf_document, search_query, file_name):
#     results = []
#     with open(pdf_document, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         for page_number, page in enumerate(reader.pages, start=1):
#             text = page.extract_text()
#             text = text.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
#             match_score = fuzz.partial_ratio(search_query.lower(), text.lower())
#             if match_score >= 81:
#                 results.append((page_number, match_score, 'Допустимое совпадение'))
#             elif 81 > match_score >= 65:
#                 results.append((page_number, match_score, 'Внимание, необходимо проверить!'))
#     results_dir = "results"
#     if not os.path.exists(results_dir):
#         os.makedirs(results_dir)
#     output_file = os.path.join(results_dir, f"{file_name}_search_results.html")
#     with open(output_file, 'w', encoding='utf-8') as output:
#         output.write(f"""<!DOCTYPE html>
# <html>
# <head>
#   <meta charset="UTF-8">
# </head>
# <body>
# <h1>Объект капитального строительства: {search_query}</h1><br>""")
#         if not results:
#             output.write("<p>В этом документе совпадений не найдено.</p>")
#         else:
#             for i, result in enumerate(results, start=1):
#                 page_number, match_score, comment = result
#                 output.write(f"<li>{i}. Найдено совпадение на странице {page_number} - процент сходства {match_score}% - <b>{comment}</b> - <a href={pdf_document}>Подробнее...</a></li>")