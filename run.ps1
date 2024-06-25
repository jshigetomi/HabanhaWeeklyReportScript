# PowerShell script to activate a Python virtual environment, install Selenium and Chrome driver if needed, and run a Python script

# Check if Python is already installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    # Install Python using WinGet
    Write-Host "Python is not installed. Installing Python..." -ForegroundColor Yellow
    winget install -e --id Python.Python.3.12 --scope machine
}

# Get the current directory
$current_directory = Get-Location

# Define the path to the "Scripts" folder
$scripts_folder = Join-Path -Path $current_directory -ChildPath "Scripts"

if (Test-Path -Path $scripts_folder) {
    Write-Host "Path to 'Scripts' folder: $scripts_folder" -ForegroundColor Green
} else {
    Write-Host "No 'Scripts' folder found in the current directory." -ForegroundColor Yellow
    Write-Host "Creating venv..." -ForegroundColor Yellow
    python -m venv ./
}

# Define the path to the "Scripts" folder
$scripts_folder = Join-Path -Path $current_directory -ChildPath "Scripts"
$activate_file = Join-Path -Path $scripts_folder -ChildPath "Activate.ps1"

# Activate the virtual environment
& $activate_file

# Check if Selenium is installed
$current_directory = Get-Location
$selenium_path = Join-Path -Path $current_directory -ChildPath "Lib\site-packages\selenium"
Write-Host "Path to Selenium: $selenium_path" -ForegroundColor Green
if (Test-Path -Path $selenium_path) {
    Write-Host "Selenium is already installed." -ForegroundColor Green
} else {
    # Install Selenium
    Write-Host "Selenium is not installed. Installing Selenium..." -ForegroundColor Yellow
    pip install selenium
}

# Check if Chrome driver is installed
$current_directory = Get-Location
$chrome_driver_path = Join-Path -Path $current_directory -ChildPath "driver"
if (Test-Path -Path $chrome_driver_path) {
    Write-Host "Chrome driver is already installed." -ForegroundColor Green
} else {
    Write-Host "Chrome driver is not installed. Installing Chrome driver..." -ForegroundColor Yellow
    New-Item -Name "driver" -ItemType Directory
    # Download and install Chrome driver
    Invoke-WebRequest -Uri "https://chromedriver.storage.googleapis.com/LATEST_RELEASE" -OutFile "chromedriver_version.txt"
    $chrome_driver_version = Get-Content "chromedriver_version.txt"
    Invoke-WebRequest -Uri "https://chromedriver.storage.googleapis.com/$chrome_driver_version/chromedriver_win32.zip" -OutFile "chromedriver.zip"
    $current_directory = Get-Location
    $chrome_driver_path = Join-Path -Path $current_directory -ChildPath "driver"
    Expand-Archive -Path "chromedriver.zip" -DestinationPath $chrome_driver_path
    Remove-Item "chromedriver.zip"
    Write-Host "Installing Chrome for testing..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://storage.googleapis.com/chrome-for-testing-public/114.0.5735.26/win64/chrome-win64.zip" -OutFile "chrome.zip"
    Expand-Archive -Path "chrome.zip" -DestinationPath $chrome_driver_path
    Remove-Item "chrome.zip"
}

# Run your Python script
python ./main.py
