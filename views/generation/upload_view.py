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
        source = request.POST.get('source', "")
        description = request.POST.get('description', "")

        if title in os.listdir(folder):
            return HttpResponse("There already is a dataset with this name")
        else:
            folder = folder + title + '/'
            os.makedirs(folder)

        # Handle original dataset upload
        original_file = request.FILES.get('original_csv')
        headers = []
        if original_file:
            fs = FileSystemStorage(location=folder)
            file_path = fs.save("original.txt", original_file)

            with fs.open(file_path, 'r') as file:
                lines = file.readlines()
                headers = lines[0].strip().split(',')
                datapoints = len(lines) - 1
                columns = len(headers)

            # Rewrite file without header
            with fs.open(file_path, 'w') as file:
                file.writelines(lines[1:])

        # Handle synthetic dataset upload
        synthetic_file = request.FILES.get('synthetic_csv')
        if synthetic_file:
            fs.save("synthetic.txt", synthetic_file)

        with open('config/datasets.json', 'r') as file:
            datasets_info = json.load(file)


        print("headers", headers)
        headers = [ header.strip() for header in headers ]
        headers = [ header.replace(" ", "_") for header in headers ]

        is_int_or_float = lambda x: x.replace('.', '', 1).isdigit()

        headers = [ header if not is_int_or_float(header) else  title+str(i+1)   for i, header in enumerate(headers)]

        datasets_info[title] = {
            "title": title,
            "description": description,
            "link": url,
            "source": source,
            "sensors": columns,
            "stations": columns,
            "datapoints": datapoints,
            "header": headers,
            "isCustom": True
        }

        with open('config/datasets.json', 'w') as file:
            json.dump(datasets_info, file, indent=4)

        # return generation view with dataset=title
        return GenerationView().get(request, title)
