# Adding New Datasets

To add a new dataset to the Dockerized pretrained GAN setup, follow these steps:

1. **Create a Folder for the Dataset:**
   - Navigate to the `/generation/data` directory.
   - Create a new folder named after your dataset. For example: `mkdir /generation/data/new_dataset`.

2. **Add the Required Files:**
   - Inside the newly created folder, add the following files:

     - **`original.txt`**
       - This should be a headerless `.txt` file with comma-separated values (CSV format).

     - **`synthetic.txt`**
       - This file should be obtained by training a model using the [TSM-Bench repository](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/generation).

     - **`description.json`**
       - Create a JSON file named `description.json` with the following structure:

       ```json
       {
         "title": "Dataset Title",
         "description": "Dataset Description",
         "link": "Source Link",
         "source": "Source Name",
         "sensors": "Number of Sensors",
         "stations": "Number of Stations",
         "datapoints": "Total Values",
         "header": ["Header1", "Header2", ...]
       }
       ```

       - **Fields Explanation:**
         - `title`: The title of your dataset.
         - `description`: A description of your dataset.
         - `link`: The URL where the dataset can be sourced from.
         - `source`: The name of the source from which the dataset was obtained.
         - `sensors`: The number of sensors in the dataset.
         - `stations`: The number of stations in the dataset.
         - `datapoints`: The total number of values in the dataset.
         - `header`: An array listing the headers of the CSV file, if applicable.

  

<!--

Debugging the container 

## run pretrained using Docker:
 docker build -t gan  .
 # -v results:/app/results \

docker run -it --name gan_container \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/results:/app/results \
  --mount type=bind,source="$(pwd)"/run_pretrained.py,target=/app/run_pretrained.py \
  gan 

docker start gan_container

### inspect the container 
docker exec -it gan_container /bin/bash 

docker exec gan_container python3 run_pretrained.py --seed bafu

docker stop gan_container  
docker rm gan_container 

# run gan docker exec gan_container 

-->
