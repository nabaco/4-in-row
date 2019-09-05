"""
This file contains a function to download and extract a dataset.
"""
import urllib.request
import zipfile
import os.path

__all__ = ['import_dataset']

DATASETS = {
    'house prices uk': {
        'url': r'https://pkgstore.datahub.io/core/house-prices-uk/data_csv/data/678865a5ff34fcce2145b857b8a9f248/data_csv.csv',
        'path': r'./house_prices_uk.data.csv'
    },
    'breast cancer':
        {'url': r'https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer/breast-cancer.data',
         'path': r'./breast-cancer.data'}
}


def import_dataset(name):
    if os.path.isfile(DATASETS[name]['path']):
        return None

    if name not in DATASETS:
        raise ValueError("This dataset is not supported yet.")
    url, local_path = DATASETS[name]['url'], DATASETS[name]['path']
    print(f"Downloading from {url} to {local_path}...")
    urllib.request.urlretrieve(url, local_path)
    print("Download complete.")
    is_zip = zipfile.is_zipfile(local_path)
    if is_zip:
        print("Extracting zip...")
        with zipfile.ZipFile(local_path) as archive:
            archive.extractall('.')
        print("Extracting complete.")
