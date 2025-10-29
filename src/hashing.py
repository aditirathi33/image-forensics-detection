# hashing.py
import hashlib, pathlib

def file_hashes(path):
    data = pathlib.Path(path).read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    sha256 = hashlib.sha256(data).hexdigest()
    return {"md5": md5, "sha256": sha256}
