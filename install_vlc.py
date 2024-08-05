import os
import hashlib
import requests
import sys
import tempfile
import subprocess
from urllib.parse import urlparse


installer_url = "https://get.videolan.org/vlc/3.0.21/win64/vlc-3.0.21-win64.exe"
sha256_url = "https://get.videolan.org/vlc/3.0.21/win64/vlc-3.0.21-win64.exe.sha256"

def main():

    try:

        # Get the expected SHA-256 hash value of the VLC installer
        expected_sha256 = get_expected_sha256(sha256_url)

        # Download (but don't save) the VLC installer from the VLC website
        installer_data = download_installer(installer_url)

        # Verify the integrity of the downloaded VLC installer by comparing the
        # expected and computed SHA-256 hash values

        if installer_ok(installer_data, expected_sha256):

            # Save the downloaded VLC installer to disk
            installer_path = save_installer(installer_data)

            # Silently run the VLC installer
            run_installer(installer_path)

            # Delete the VLC installer from disk
            delete_installer(installer_path)

        else:

            print("The downloaded installer is corrupted or has been tampered with.")
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)



def get_expected_sha256(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    sha256_value = response.text.strip().split()[0]  # Assumes the SHA-256 value is the first word in the file
    return sha256_value

def download_installer(url):

    response = requests.get(url, stream=True)
    response.raise_for_status()
    return response.content

def installer_ok(installer_data, expected_sha256):

    sha256 = hashlib.sha256()
    sha256.update(installer_data)

    computed_sha256 = sha256.hexdigest() 
    return computed_sha256 == expected_sha256

def save_installer(installer_data):
    temp_dir = tempfile.gettempdir()
    filename = os.path.basename(urlparse(installer_url).path)
    path = os.path.join(temp_dir, filename)
    with open(path, 'wb') as f:
        f.write(installer_data)
    return path
def run_installer(installer_path):
    try:
        # Run the installer with the /S option for silent installation
        subprocess.run([installer_path, '/S'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during installation: {e}")
        sys.exit(1)

def delete_installer(installer_path):
    try:
        os.remove(installer_path)
    except OSError as e:
        print(f"Error occurred while deleting the installer: {e}")

if __name__ == "__main__":
    main()

