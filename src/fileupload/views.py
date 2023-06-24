from django.shortcuts import render, HttpResponse
from .models import FilesUpload
from .tasks import process_pdf_task

def home(request):
    if request.method == "POST":
        files = request.FILES.getlist("files")
        search_query = request.POST.get('search_query')
        for file in files:
            document = FilesUpload.objects.create(file=file)
            document.save()
            file_path = document.file.path
            process_pdf_task.delay(file_path, search_query, file.name)
        return HttpResponse("Files uploaded")
    return render(request, "index.html")
