# TS-LSH: LSH-based Generation Technique for Long Time Series

TS-LSH is a scalable data generator that closely emulates the properties of real-world time series. One of the benefits of this tool is to facilitate data sharing for benchmarking tasks, particularly when datasets are non-public due to privacy issues.  Our method relies on Generative Adversarial Network (GAN) to create large volumes of time series data. The code can be used in two different ways:
- **Option 1**: You can use our pre-trained model to generate new time series from the list of provided datasets in `data/`
- **Option 2**: You can add your own dataset and generate new time series by retraining the model from scratch. 

The generated plots and data will be saved in the `generation/results` folder.

## Generation Examples

![image](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/13d8c2f9-fdbf-495f-aaf9-7f5ec0999470)



## Setup
- Install the necessary dependencies using the following script:

```bash
cd generation/
sh install.sh
```


## Arguments:

- You can customize the time series generation using the following parameters:

   - `--len_ts` (optional, integer): The length of time series; default: 10K datapoints.
   - `--nb_ts` (optional, integer): The number of time series; default: 3 time series.
   - `--seed` (optional, string): The name of the seed dataset file; default: _bafu_.

*Note: Additional parameters for the generation method, including the number of iterations for GAN training and LSH configuration, can be found in the `config.toml` file.*

## TS-LSH Usage

### Option 1: Generation using a pre-trained model 


- Default generation
```bash
   python run_pretrained.py
```
- Customized generation: Generate 10 time series with 20K datapoints each from the conductivity dataset 

```bash
   python run_pretrained.py --len_ts 20000 --nb_ts 10 --seed conductivity
```


### Option 2: Generation by retraining the model from scratch 

#### Dataset Creation

- Name your dataset as `original.txt`. The file should satisfy the following requirements:
   - contains one column that represents the time series to augment.
   - nrows >= 3000.
- Create a new folder under `data/` with the name of your dataset and add `original.txt` inside, i.e., `data/{dataset_name}/original.txt`
 

#### 1. Data Partitioning

- Partition your input data located in `data/` into segments of the same length

```bash
python ts_partition.py --seed {dataset_name}
```

#### 2. Model Training



- Train a GAN model on the original segments and add the generated segments into `results/` (takes ~ 2 days for 80K datapoints original dataset) 

```bash
cd gan/
python DCGAN.py --seed {dataset_name}
python encoder_dc.py --seed {dataset_name}
```
- Generate new segments using the trained ones 
```bash
python test_dc.py --seed {dataset_name}
```

#### 3. Data Generation

```bash
cd ..
python gen_ts.py  --seed {dataset_name}
```
- Example: Generate 10 time series with with 100K datapoints each:

```bash
python gen_ts.py --len_ts 100000 --nb_ts 10 --seed {dataset_name}
```
  
<!--
Apply LSH to generate long time series using ```gen_ts.py```. To use this script, the following arguments and examples are provided:

- `--len_ts` (optional, integer): The length of ts.
- `--nb_ts` (optional, integer): The number of ts.
- `--fori` (optional, string): A link to the original file.
- `--fsynth` (optional, string): A link to the synthetic segments.
- `--output_to` (optional, string): A link to the exported generated file.

1. Running the script with default values:

   ```bash
   python gen_ts.py
    ```
1. Generate 10 time series with 10K datapoints each:

```bash
   python gen_ts.py --len_ts 10000 --nb_ts 10
```
The generated plots and data are stored in the `generation/results` folder.
-->



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
