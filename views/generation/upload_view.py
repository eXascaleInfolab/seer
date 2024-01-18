import json
import os
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from views.generation.generation_view import GenerationView


def upload_datasets(request):
    if request.method == 'POST':
        folder = 'generation/data/'  # You can also use settings.YOUR_FOLDER

        title = request.POST.get('title')
        url = request.POST.get('url', "-")
        source = request.POST.get('source' , "")
        description = request.POST.get('description' , "")


        if title in os.listdir(folder):
            return HttpResponse("There already is a dataset with this name")
        else:
            folder = folder + title + '/'
            os.makedirs(folder)

        # Handle original dataset upload
        original_file = request.FILES.get('original_csv')
        if original_file:
            fs = FileSystemStorage(location=folder)
            fs.save(original_file.name, original_file)
            datapoints = len(open(folder + original_file.name).readlines()) - 1
            columns = len(open(folder + original_file.name).readline().split(','))

        # Handle synthetic dataset upload
        synthetic_file = request.FILES.get('synthetic_csv')
        if synthetic_file:
            fs = FileSystemStorage(location=folder)
            fs.save(synthetic_file.name, synthetic_file)

        with open('config/datasets.json', 'r') as file:
            datasets_info = json.load(file)

        datasets_info[title] = {
            "title": title,
            "description": description,
            "link": url,
            "source": source,
            "sensors": columns,
            "stations": columns,
            "datapoints": datapoints,
            "isCustom": True
        }

        with open('config/datasets.json', 'w') as file:
            json.dump(datasets_info, file, indent=4)

        # return generation view with dataset=title
        return GenerationView().get(request, title)

