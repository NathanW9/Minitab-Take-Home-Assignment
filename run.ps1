$port = if ($env:PORT) { $env:PORT } else { "3000" }

docker build -t minitab-service .
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

docker run --rm --name minitab-service-container -p "$($port):$($port)" -e "PORT=$port" minitab-service
