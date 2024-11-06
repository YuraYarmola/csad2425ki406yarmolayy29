$ComPort = "COM3"
$IsGitHubActions = $env:GITHUB_ACTIONS -eq 'true'

function Is-ComPortConnected($portName) {
    try {
        $port = [System.IO.Ports.SerialPort]::GetPortNames() -contains $portName
        return $port
    } catch {
        return $false
    }
}
if ($env:GITHUB_ACTIONS -eq 'true') {
    $PythonPath = "$env:pythonLocation\python.exe"

} else {
    $PythonPath = "D:\LPNU\SEMESTER7\APKS\csad2425ki406yarmolayy29\TicTacToeSWPart\.venv\Scripts\python.exe"
}

Set-Location -Path (Join-Path -Path $PSScriptRoot -ChildPath "..\TicTacToeSWPart")
$SkipHwTests = $IsGitHubActions -or !(Is-ComPortConnected -portName $ComPort)
Write-Output "Running software tests..."
& $PythonPath -m unittest "sw_tests.py"
if (-not $SkipHwTests) {
    Write-Output "COM port $ComPort detected. Running hardware tests..."
    & $PythonPath -m unittest "hw_tests.py"
} else {
    Write-Output "Skipping hardware tests."
}
