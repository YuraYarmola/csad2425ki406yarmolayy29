# ------------------------- CONFIGURABLE VARIABLES -----------------------------------------
$board = "arduino:avr:nano:cpu=atmega328old"
$baudRate = 9600
$sketch = "D:\LPNU\SEMESTER7\APKS\csad2425ki406yarmolayy29\HWPart\TicTacToe\TicTacToe.ino"
$serialLog = "serial_output.log"
# ------------------------------------------------------------------------------------------


function Check-ArduinoCLI {
    if (-not (Get-Command arduino-cli -ErrorAction SilentlyContinue)) {
        Write-Output "arduino-cli не знайдено. Будь ласка, встановіть його."
        exit 1
    }
}

function Select-ArduinoPort {
    Write-Output "Доступні порти:"
    $ports = & arduino-cli board list | Select-Object -Skip 1 | ForEach-Object { $_.Split(" ")[0] }
    $ports | ForEach-Object { Write-Output "$([array]::IndexOf($ports, $_)) - $_" }

    $portNumber = Read-Host -Prompt "Виберіть номер порту для вашої плати Arduino Nano"
    $global:port = $ports[$portNumber]

    if (-not $global:port) {
        Write-Output "Невірний вибір порту."
        exit 1
    }
    Write-Output "Обраний порт: $global:port"
}

function Compile-Sketch {
    Write-Output "Компілляція скетчу..."
    & arduino-cli compile --fqbn $board $sketch
    if ($LASTEXITCODE -ne 0) {
        Write-Output "Помилка компіляції."
        exit 1
    }
    Write-Output "Компіляція успішна."
}

function Upload-Sketch {
    Write-Output "Завантаження скетчу на плату Arduino Nano через порт $global:port..."
    & arduino-cli upload -p $global:port --fqbn $board $sketch
    if ($LASTEXITCODE -ne 0) {
        Write-Output "Помилка завантаження."
        exit 1
    }
    Write-Output "Завантаження успішне."
}

function Run-Tests {
    Write-Output "Виконання тестів..."

    $serialPort = new-Object System.IO.Ports.SerialPort $global:port, $baudRate
    $serialPort.Open()
    Start-Sleep -Seconds 2  # Час на перезавантаження Arduino і початок виводу

    $serialPort.WriteLine('{"command":"RESET"}')
    Start-Sleep -Seconds 1
    $serialPort.WriteLine('{"command":"MOVE","row":0,"col":0}')
    Start-Sleep -Seconds 1
    $serialPort.WriteLine('{"command":"MOVE","row":1,"col":1}')

    $output = ""
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    while ($stopwatch.Elapsed.TotalSeconds -lt 5) {
        if ($serialPort.BytesToRead -gt 0) {
            $output += $serialPort.ReadExisting()
        }
    }
    $serialPort.Close()

    $output | Out-File -FilePath $serialLog

    if ($output -match "TicTacToe Game Started" -and $output -match '"type":"board"') {
        Write-Output "Тести пройдені успішно."
    } else {
        Write-Output "Тести не пройдені. Перевірте лог виводу серійного порту."
        exit 1
    }
}

Check-ArduinoCLI
Select-ArduinoPort
Compile-Sketch
Upload-Sketch
Run-Tests
