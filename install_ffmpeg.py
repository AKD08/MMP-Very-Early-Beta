import os
import zipfile
import requests
import shutil
import ctypes
import subprocess
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

# Function to download FFmpeg safely
def download_ffmpeg():
    print("Downloading FFmpeg...")
    
    response = requests.get(FFMPEG_URL, stream=True)
    total_size = int(response.headers.get("content-length", 0))

    with open(DOWNLOAD_PATH, "wb") as file:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                downloaded += len(chunk)
                print(f"\rDownloading: {downloaded / total_size * 100:.2f}%", end="")
    
    print("\nDownload complete!")

# Function to extract FFmpeg safely
def extract_ffmpeg():
    print("Extracting FFmpeg...")
    
    with zipfile.ZipFile(DOWNLOAD_PATH, 'r') as zip_ref:
        extract_path = DOWNLOAD_PATH.parent
        zip_ref.extractall(extract_path)
    
    # Find extracted FFmpeg folder
    extracted_folder = next(extract_path.glob("ffmpeg-*"))
    while extracted_folder.is_dir() and len(list(extracted_folder.iterdir())) == 1:
        extracted_folder = next(extracted_folder.iterdir())
    
    ffmpeg_path = extracted_folder / "bin"
    
    # Ask before deleting old install
    if INSTALL_PATH.exists():
        user_input = input("FFmpeg is already installed. Do you want to overwrite it? (y/n): ").strip().lower()
        if user_input != 'y':
            print("Installation aborted.")
            return
        shutil.rmtree(INSTALL_PATH)
    
    INSTALL_PATH.mkdir()

    # Move necessary files
    for folder in ["bin", "doc", "presets", "LICENSE.txt", "README.txt"]:
        source = extracted_folder / folder
        destination = INSTALL_PATH / folder
        if source.exists():
            shutil.move(str(source), str(destination))
    
    print("FFmpeg extracted and moved to C:\\ffmpeg")

# Function to update system PATH safely
def update_system_path():
    print("Updating system PATH variable...")
    
    ffmpeg_bin_path = str(INSTALL_PATH / "bin")
    
    # Get current PATH safely
    current_path = os.environ.get("PATH", "")
    
    if ffmpeg_bin_path not in current_path:
        try:
            subprocess.run(["setx", "PATH", f"%PATH%;{ffmpeg_bin_path}", "/M"], check=True)
            print("System PATH updated. You may need to restart your terminal.")
        except subprocess.CalledProcessError:
            print("Failed to update PATH. Try running as admin or update manually.")
    else:
        print("FFmpeg is already in the PATH.")

# Main function
def main():
    if not is_admin():
        print("Warning: This script is not running as administrator. Some features may not work.")
        user_input = input("Do you want to continue? (y/n): ").strip().lower()
        if user_input != 'y':
            return

    download_ffmpeg()
    extract_ffmpeg()
    update_system_path()
    print("FFmpeg installation complete!")

if __name__ == "__main__":
    main()
