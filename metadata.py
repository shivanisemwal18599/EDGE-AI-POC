from datasets import load_dataset, Value, Sequence, ClassLabel
import os
import yaml
import pyarrow as pa
from create_dataset import create_dataset
    
dataset_size = 0
download_size = 0

def generate_metadata_readme(file_path, output_file) -> None:
    dataset, info, size = create_dataset(file_path, output_file, 0.8)
    features = info.features
    dataset_size = info.dataset_size
    
    # Build metadata structure
    metadata = {
        "dataset_info": {
            "features": [],
            "splits": [],
            "download_size": 0,
            "dataset_size": 0
        },
        "configs": [{
            "config_name": "default",
            "data_files": []
        }]
    }
    # Get the first split to examine features
    first_split = list(dataset.keys())[0]

    split_dataset = dataset[first_split]
    print('------------------split_dataset: ', split_dataset)
    # Process features
    for feature_name, feature_type in split_dataset.features.items():
        print('------------------feature_type: ', feature_type)
        metadata["dataset_info"]["features"].append({
            "name": feature_name,
            "dtype": str(feature_type)
        })
    
    # Process splits
    i = 0
    for split_name, split_data in dataset.items():
        num_bytes = size[i] #getting size from the size list function parameter
        i = i+1

        #number of rows
        num_examples = split_data.num_rows #len(split_data)
        
        metadata["dataset_info"]["splits"].append({
            "name": split_name,
            "num_bytes": num_bytes,
            "num_examples": num_examples
        })
        metadata["configs"][0]["data_files"].append({
        "split": split_name,
        "path": output_file
        })
    # download size of the parquet files
    for filename in os.listdir(output_file):
        global download_size
        # Check if the file has a .parquet extension
        if filename.endswith(".parquet"):
            # Build the full file path
            file_path = os.path.join(output_file, filename)
            # Make sure it's a file and not a directory
            if os.path.isfile(file_path):
                # Add the size of the file to the download_size variable
                download_size += os.path.getsize(file_path)

    metadata["dataset_info"]["dataset_size"] = dataset_size
    metadata["dataset_info"]["download_size"] = download_size


    # Create YAML content
    yaml_content = yaml.dump(
        metadata,
        sort_keys=False,
        width=1000,
        indent=2,
        default_flow_style=False,
        allow_unicode=True
    )

    # Create full README content
    readme_content = f"""\
license: apache-2.0
language:
- en
{yaml_content}"""
    output_file = os.path.join(output_file, "README.md")
    # Write to file
    with open(output_file, "w") as f:
        f.write(readme_content)
    print('######### METADATA CREATED #########')
    
    # return readme_content

generate_metadata_readme('test_data.csv', 'DATASET\data') 