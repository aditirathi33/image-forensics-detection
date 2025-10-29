# exif_tools.py
import exifread, json

def extract_exif(path):
    with open(path, 'rb') as f:
        tags = exifread.process_file(f, details=False)
    # Convert to simple dict of strings
    return {str(k): str(v) for k, v in tags.items()}
