import pandas as pd
from datasets import load_dataset, Dataset
import os
import json
import pyarrow.parquet as pq

def split_train_test(dataset, train_ratio=1):
    if train_ratio == 1:
        # Return the entire training set
        return {"train": dataset["train"]}
    else:
        test_size = 1 - train_ratio
        return dataset["train"].train_test_split(test_size=test_size, shuffle=True, seed=42) #dataset.train_test_split(test_size=test_size, shuffle=True, seed=seed)

def create_dataset(input_file, output_dir, train_ratio=1):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    # Detect file format
    file_ext = os.path.splitext(input_file)[1].lower() 
    format_map = {'.csv': 'csv', '.json': 'json', '.parquet': 'parquet'}

    # Load dataset
    try:
        dataset = load_dataset(format_map[file_ext], data_files=input_file)
    except Exception as e:
        raise RuntimeError(f"Error loading dataset: {str(e)}")
    #spliting dataset
    splits = split_train_test(dataset, train_ratio=train_ratio)
    # print('split[train]:\n', splits['train'])

    print("splits_info: \n", splits['train'].info)
    file_size = []
    print('**************SAVING PARQUET FILES (TRAIN/TEST)**********************')
    for split_name, split_dataset in splits.items():
        print(f"\n{split_name.capitalize()} Split Info:\n")
        print(f"\n - Number of rows: {split_dataset.num_rows}")
        print(f"\n - Features: {split_dataset.features}")
        print(f"\n - Dataset size: {split_dataset.dataset_size}")
        print(f"\n - Download size: {split_dataset.download_size}")
        output_path = os.path.join(output_dir, f"{split_name}.parquet")
        size = split_dataset.to_parquet(output_path) #converting file to parquet -- it returns the value of the number of bytes written during the process of saving the dataset
        file_size.append(size) #appending the size of each parquet files written
        print(f"Saved {split_name} set with {len(split_dataset)} records to {output_path}")
    return splits, splits['train'].info, file_size
    