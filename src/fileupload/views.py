import os
from django.conf import settings
import time
from django.shortcuts import render, redirect
from .models import FilesUpload
from .tasks import process_pdf_task


def home(request):
    if request.method == "POST":
        results_dir = "results"
        
        # Удаление всех файлов в директории results перед загрузкой новых.
        for filename in os.listdir(results_dir):
            if filename.endswith(".css"):
                continue
            file_path = os.path.join(results_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        files = request.FILES.getlist("files")
        search_query = request.POST.get('search_query')
        for file in files:
            document = FilesUpload.objects.create(file=file)
            document.save()
            file_path = document.file.path
            process_pdf_task.delay(file_path, search_query, file.name)
        time.sleep(10)
        return redirect('results')
    return render(request, "index.html")


def results(request):
    media_files = os.listdir(settings.MEDIA_ROOT)
    results_files = os.listdir(settings.RESULTS_ROOT)
    context = {
        'media_files': media_files,
        'results_files': results_files,
    }
    return render(request, 'results.html', context)