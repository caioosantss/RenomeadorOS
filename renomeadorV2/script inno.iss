;==========================================================
; Renomeador de OS - Instalador
;==========================================================

#define MyAppName "Renomeador de OS"
#define MyAppVersion "2.0.0"
#define MyAppExeName "main.exe"

[Setup]
AppId={{A4D84718-2F39-4C7E-90A7-RENOMEADOROS}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=
DefaultDirName={localappdata}\Programs\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

OutputDir=Installer
OutputBaseFilename=Setup_RenomeadorOS_v2.0.0

Compression=lzma2
SolidCompression=yes
WizardStyle=modern

PrivilegesRequired=lowest

UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "portuguesebrazil"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Atalhos:"; Flags: unchecked

[Files]
; {src} garante que ele busque a pasta dist no mesmo diretório do arquivo .iss
Source: "{src}\dist\main\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs external

[Icons]
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Executar {#MyAppName}"; Flags: nowait postinstall skipifsilent