from django.shortcuts import render, HttpResponse
from .models import FilesUpload
from .pdf_processing import process_pdf


def home(request):
    """Функция загрузки pdf-файла."""
    if request.method == "POST":
        file2 = request.FILES["file"]
        document = FilesUpload.objects.create(file=file2)
        document.save()
        file_path = document.file.path
        process_pdf(file_path)
        return HttpResponse("Файл загружен")
    return render(request, "index.html")