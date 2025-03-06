import os
import zipfile
import requests
import shutil
import ctypes
from pathlib import Path

# URL for FFmpeg download
FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
DOWNLOAD_PATH = Path.home() / "Downloads" / "ffmpeg.zip"
INSTALL_PATH = Path("C:/ffmpeg")

# Function to check if running as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to download FFmpeg
def download_ffmpeg():
    print("Downloading FFmpeg...")
    response = requests.get(FFMPEG_URL, stream=True)
    with open(DOWNLOAD_PATH, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print("Download complete!")

# Function to extract FFmpeg
def extract_ffmpeg():
    print("Extracting FFmpeg...")
    with zipfile.ZipFile(DOWNLOAD_PATH, 'r') as zip_ref:
        extract_path = DOWNLOAD_PATH.parent
        zip_ref.extractall(extract_path)
        
    # Find the extracted FFmpeg folder (handling double nested issue)
    extracted_folder = next(extract_path.glob("ffmpeg-*"))
    while extracted_folder.is_dir() and len(list(extracted_folder.iterdir())) == 1:
        extracted_folder = next(extracted_folder.iterdir())
    
    ffmpeg_path = extracted_folder / "bin"
    
    # Ensure install directory exists
    if INSTALL_PATH.exists():
        shutil.rmtree(INSTALL_PATH)
    INSTALL_PATH.mkdir()
    
    # Move required files to C:\ffmpeg
    for folder in ["bin", "doc", "presets", "LICENSE.txt", "README.txt"]:
        source = extracted_folder / folder
        destination = INSTALL_PATH / folder
        if source.exists():
            shutil.move(str(source), str(destination))
    
    print("FFmpeg extracted and moved to C:\\ffmpeg")

# Function to update system PATH
def update_system_path():
    print("Updating system PATH variable...")
    ffmpeg_bin_path = str(INSTALL_PATH / "bin")
    current_path = os.environ.get("PATH", "")
    
    if ffmpeg_bin_path not in current_path:
        os.system(f'setx PATH "%PATH%;{ffmpeg_bin_path}" /M')
        print("System PATH updated. You may need to restart your terminal.")
    else:
        print("FFmpeg is already in the PATH.")

# Main function
def main():
    if not is_admin():
        print("Please run this script as administrator!")
        return
    
    download_ffmpeg()
    extract_ffmpeg()
    update_system_path()
    print("FFmpeg installation complete!")

if __name__ == "__main__":
    main()