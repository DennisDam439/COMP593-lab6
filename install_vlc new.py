import os
import hashlib
import requests
import sys
import tempfile
import subprocess
from urllib.parse import urlparse


installer_url = "https://get.videolan.org/vlc/3.0.21/win64/vlc-3.0.21-win64.exe"
expected_sha256 = "https://get.videolan.org/vlc/3.0.21/win64/vlc-3.0.21-win64.exe.sha256"


def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    """Downloads the text file containing the expected SHA-256 value for the VLC installer file from the 
    videolan.org website and extracts the expected SHA-256 value from it.

    Returns:
        str: Expected SHA-256 hash value of VLC installer
    """
    # TODO: Step 1
    # Hint: See example code in lab instructions entitled "Extracting Text from a Response Message Body"
    # Hint: Use str class methods, str slicing, and/or regex to extract the expected SHA-256 value from the text 
    response = requests.get(expected_sha256)
    response.raise_for_status()  # Ensure we notice bad responses

    sha256_value = response.text.strip().split()[0] 
    return sha256_value


def download_installer(url):
    """Downloads, but does not save, the .exe VLC installer file for 64-bit Windows.

    Returns:
        bytes: VLC installer file binary data
    """
    # TODO: Step 2
    # Hint: See example code in lab instructions entitled "Downloading a Binary File"
    response = requests.get(url, stream=True)

    response.raise_for_status()
    return response.content


def installer_ok(installer_data, expected_sha256):
    """Verifies the integrity of the downloaded VLC installer file by calculating its SHA-256 hash value 
    and comparing it against the expected SHA-256 hash value. 

    Args:
        installer_data (bytes): VLC installer file binary data
        expected_sha256 (str): Expeced SHA-256 of the VLC installer

    Returns:
        bool: True if SHA-256 of VLC installer matches expected SHA-256. False if not.
    """    
    # TODO: Step 3
    # Hint: See example code in lab instructions entitled "Computing the Hash Value of a Response Message Body"
    
    sha256 = hashlib.sha256()
    sha256.update(installer_data)
    computed_sha256 = sha256.hexdigest() 
    return computed_sha256 == expected_sha256 


def save_installer(installer_data):
    """Saves the VLC installer to a local directory.

    Args:
        installer_data (bytes): VLC installer file binary data

    Returns:
        str: Full path of the saved VLC installer file
    """
    # TODO: Step 4
    # Hint: See example code in lab instructions entitled "Downloading a Binary File"
    temp_dir = tempfile.gettempdir()
    filename = os.path.basename(urlparse(installer_url).path)
    path = os.path.join(temp_dir, filename)
    with open(path, 'wb') as f:
        f.write(installer_data)
    return path

def run_installer(installer_path):
    """Silently runs the VLC installer.

    Args:
        installer_path (str): Full path of the VLC installer file
    """    
    # TODO: Step 5
    # Hint: See example code in lab instructions entitled "Running the VLC Installer"
    try:
      subprocess.run([installer_path, '/S'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during installation: {e}")
        sys.exit(1)
    return
    
def delete_installer(installer_path):
    # TODO: Step 6
    # Hint: See example code in lab instructions entitled "Running the VLC Installer"
    """Deletes the VLC installer file.

    Args:
        installer_path (str): Full path of the VLC installer file
    """
    try:
        os.remove(installer_path)
    except OSError as e:
        print(f"Error occurred while deleting the installer: {e}")
        return
    
if __name__ == '__main__':
    main()