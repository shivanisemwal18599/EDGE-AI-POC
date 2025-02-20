license: apache-2.0
language:
- en
dataset_info:
  features:
  - name: name
    dtype: Value(dtype='string', id=None)
  - name: gender
    dtype: Value(dtype='string', id=None)
  splits:
  - name: train
    num_bytes: 130
    num_examples: 7
  - name: test
    num_bytes: 40
    num_examples: 2
  download_size: 2135
  dataset_size: 170
configs:
- config_name: default
  data_files:
  - split: train
    path: DATASET\data
  - split: test
    path: DATASET\data
