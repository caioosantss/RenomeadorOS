ini
;==========================================================
; Renomeador de OS - Instalador
;==========================================================

#define MyAppName "Renomeador de OS"
#define MyAppVersion "2.0.0"
#define MyAppExeName "main.exe"

[Setup]
AppId={{8F3C2A61-4B7D-4E9A-9C21-6A1F0D5E2B44}}
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
; {src} = pasta onde este arquivo .iss está salvo — deve estar na mesma pasta que "dist"
Source: "{src}\dist\main\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs external

[Icons]
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Executar {#MyAppName}"; Flags: nowait postinstall skipifsilent