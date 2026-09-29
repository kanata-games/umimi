$ErrorActionPreference = 'Stop'
$files = Split-Path -Parent $MyInvocation.MyCommand.Path
$here = Split-Path -Parent $files
$url  = 'https://github.com/electron/electron/releases/download/v33.2.1/electron-v33.2.1-win32-x64.zip'
$hash = 'C325A6D905C67107E166267813EA2151AE7FD316C0A88DE0081DB0B9851A9946'
$zip  = Join-Path $env:TEMP 'umimi-electron-v33.2.1.zip'
$dest = Join-Path $here 'UmimiDesktop'

try {
  Write-Host ''
  Write-Host '  ウミミの水そうを じゅんびしています…'
  Write-Host '  （はじめの1回だけ、100MBほどダウンロードします。数分かかることがあります）'
  Write-Host ''
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  $ProgressPreference = 'SilentlyContinue'

  $need = $true
  if (Test-Path $zip) { if ((Get-FileHash $zip -Algorithm SHA256).Hash -eq $hash) { $need = $false } }
  if ($need) {
    Write-Host '  1/3 ダウンロード中…'
    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
  }
  if ((Get-FileHash $zip -Algorithm SHA256).Hash -ne $hash) {
    Remove-Item $zip -Force -ErrorAction SilentlyContinue
    throw 'ダウンロードしたファイルが正しくありませんでした。もう一度「はじめにダブルクリック」を実行してください。'
  }

  Write-Host '  2/3 展開中…'
  if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
  Expand-Archive -Path $zip -DestinationPath $dest -Force
  Rename-Item (Join-Path $dest 'electron.exe') 'UmimiDesktop.exe'
  Remove-Item (Join-Path $dest 'resources\default_app.asar') -ErrorAction SilentlyContinue
  Copy-Item (Join-Path $files 'app') (Join-Path $dest 'resources\app') -Recurse -Force
  Copy-Item (Join-Path $files 'umimi.ico') (Join-Path $dest 'umimi.ico') -Force
  Get-ChildItem (Join-Path $dest 'locales') | Where-Object { $_.Name -ne 'ja.pak' -and $_.Name -ne 'en-US.pak' } | Remove-Item -Force
  Remove-Item $zip -Force -ErrorAction SilentlyContinue

  Write-Host '  3/3 デスクトップにショートカットを作成中…'
  $ws  = New-Object -ComObject WScript.Shell
  $lnk = $ws.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'ウミミ デスクトップ.lnk'))
  $lnk.TargetPath = Join-Path $dest 'UmimiDesktop.exe'
  $lnk.WorkingDirectory = $dest
  $lnk.IconLocation = (Join-Path $dest 'umimi.ico') + ',0'
  $lnk.Description = 'ウミミ デスクトップ'
  $lnk.Save()

  Write-Host ''
  Write-Host '  できました！ 画面の下に ウミミが あらわれます。'
  Write-Host '  次からは デスクトップの「ウミミ デスクトップ」から ひらけます。'
  Start-Process (Join-Path $dest 'UmimiDesktop.exe') -WorkingDirectory $dest
}
catch {
  Write-Host ''
  Write-Host ('  うまくいきませんでした: ' + $_.Exception.Message)
  Write-Host '  インターネットにつながっているか確認して、もう一度「はじめにダブルクリック」を実行してください。'
}
