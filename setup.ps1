# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker could not be found. Please install Docker."
    exit
}

# Check if Docker Compose is installed, if not, install it
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "Docker Compose could not be found. Installing Docker Compose..."
    Invoke-WebRequest -Uri "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-Windows-x86_64.exe" -OutFile "$Env:ProgramFiles\Docker\docker-compose.exe"
}

# Build and start the Docker containers
docker-compose up --build