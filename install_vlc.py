import hashlib 
import os 
import requests
import sys 
import tempfile 
import subprocess
from urllib.parse import urlparse


downloadlink = "https://get.videolan.org/vlc/3.0.21/win32/vlc-3.0.21-win32.exe"#htt
checksum =  " 4bd03202b6633f9611b3fc8757880a9b2b38c7c0c40ed6bcbefec71c0099d493"


def download_file(url,dest):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with (dest, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return dest 


def verify_checksum(file_path, checksum):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    file_checksum = sha256.hexdigest()
    return file_checksum == checksum



def install_vlc(installer_path):
    subprocess.run([installer_path, '/S'], check=True)

def delete_installer(installer_path):
    os.remove(installer_path)
def main():
    temp_dir = tempfile.gettemdir()
    filename = os.path.basename(urlparse(downloadlink).path)
    path = os.path.join(temp_dir, filename)
    download_file(downloadlink, path)

    print("Downloading!!!!")
    download_file(downloadlink, path)

    print("Veryfying checksum...")
    if verify_checksum(path, checksum):
        print("Verification passed.")
        print("Installing")
        install_vlc(path)
        print("VLC installed successfully.!")
    else:
        print("Verification failed.")
        sys.exit(1)



if __name__ == "__main__":
    main()

