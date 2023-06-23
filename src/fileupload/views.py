import os
from django.shortcuts import render, HttpResponse

from .models import FilesUpload
from .pdf_processing import process_pdf


def home(request):
    """Функция загрузки pdf-файла."""
    if request.method == "POST":
        files = request.FILES.getlist("files")
        search_query = request.POST.get('search_query')
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        for file in files:
            document = FilesUpload.objects.create(file=file)
            document.save()
            file_path = document.file.path
            results, search_query = process_pdf(file_path, search_query)
            output_file = os.path.join(results_dir, f"{file.name}_search_results.txt")
            with open(output_file, 'w') as output:
                output.write(f"Объект капитального строительства: {search_query}\n")
                if not results:
                    output.write("В этом документе совпадений не найдено.\n")
                else:
                    for i, result in enumerate(results, start=1):
                        page_number, match_score, comment = result
                        output.write(f"{i}. Найдено совпадение на странице {page_number} - процент сходства {match_score}% - {comment}\n")
        return HttpResponse("Files uploaded")
    return render(request, "index.html")