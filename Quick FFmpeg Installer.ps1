# Check for administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Please run this script as Administrator."
    exit
}

# Define URLs and paths
$ffmpegZipUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$downloadPath = "$env:TEMP\ffmpeg.zip"
$installDir = "C:\ffmpeg"

Write-Host "Downloading ffmpeg from $ffmpegZipUrl..."
Invoke-WebRequest -Uri $ffmpegZipUrl -OutFile $downloadPath

# Create installation directory if it doesn't exist
if (-Not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir | Out-Null
}

Write-Host "Extracting ffmpeg..."
Expand-Archive -Path $downloadPath -DestinationPath $installDir -Force

# ffmpeg zip extracts to a folder like "ffmpeg-<version>-essentials_build"
# We'll grab the first directory inside our install directory
$extractedFolder = Get-ChildItem -Path $installDir -Directory | Select-Object -First 1
if (-not $extractedFolder) {
    Write-Host "Extraction failed or folder not found."
    exit
}

# The binaries are in the "bin" subfolder
$binFolder = Join-Path $extractedFolder.FullName "bin"
if (-not (Test-Path (Join-Path $binFolder "ffmpeg.exe"))) {
    Write-Host "ffmpeg.exe was not found in the expected location."
    exit
}

Write-Host "Adding $binFolder to the system PATH..."
# Get the current machine-level PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)

if (-not $currentPath.Split(";") -contains $binFolder) {
    $newPath = "$currentPath;$binFolder"
    [Environment]::SetEnvironmentVariable("Path", $newPath, [EnvironmentVariableTarget]::Machine)
    Write-Host "System PATH updated. You may need to restart your terminal or log off and on again for changes to take effect."
} else {
    Write-Host "The PATH already contains $binFolder."
}

Write-Host "ffmpeg installation completed successfully."
