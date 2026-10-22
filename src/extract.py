import shutil
import zipfile

from src import config


def extract_zip():
    zip_path = config.RAW_DIR / config.ZIP_NAME
    if not zip_path.exists():
        raise FileNotFoundError(f"Put your notes zip at {zip_path}")
    if config.EXTRACTED_DIR.exists():
        shutil.rmtree(config.EXTRACTED_DIR)
    config.EXTRACTED_DIR.mkdir(parents=True)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(config.EXTRACTED_DIR)
    return config.EXTRACTED_DIR