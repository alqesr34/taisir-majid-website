# Script to run Flask server with SSH tunnel for external access

Write-Host "======================================"
Write-Host "Starting Flask Server + SSH Tunnel"
Write-Host "======================================"
Write-Host ""

# Kill any existing Python processes
Get-Process python* -ErrorAction SilentlyContinue | Stop-Process -Force

# Start Flask server
Write-Host "Starting Flask server on port 8000..."
$flaskProcess = Start-Process -FilePath "I:\web\.venv\Scripts\python.exe" `
    -ArgumentList "web.py" `
    -NoNewWindow `
    -PassThru

Write-Host "Flask server started (PID: $($flaskProcess.Id))"
Write-Host ""

# Wait for server to start
Start-Sleep -Seconds 3

Write-Host "======================================"
Write-Host "Creating SSH tunnel..."
Write-Host "Your external URL will be printed below:"
Write-Host "======================================"
Write-Host ""

# Create SSH tunnel using localhost.run
# This creates a secure tunnel to your local Flask server
ssh -R 80:localhost:8000 ssh.localhost.run

# Cleanup on exit
Write-Host ""
Write-Host "Stopping Flask server..."
Stop-Process -Id $flaskProcess.Id -Force -ErrorAction SilentlyContinue
Write-Host "Done!"
