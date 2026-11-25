; LOI CATFARM PRO - Inno Setup 6
#define AppName "LOI CATFARM PRO"
#define AppVersion "FIX15"
#define AppExe "LOICatFarmPro.exe"

[Setup]
AppId={{A6D1B6C1-7F42-4D6A-9E42-1A2B3C4D5E6F}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=MGP
DefaultDirName={localappdata}\Programs\LOI CATFARM PRO
DefaultGroupName=LOI CATFARM PRO
OutputDir=Output
OutputBaseFilename=LOI_CATFARM_PRO_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\{#AppExe}
SetupLogging=yes

[Files]
Source: "dist\LOICatFarmPro\_internal\*"; DestDir: "{app}\_internal"; Flags: recursesubdirs createallsubdirs
Source: "dist\LOICatFarmPro\LOICatFarmPro.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "PREPARAR_VLC_PORTATIL.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\update_helper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\spotify_webview_host.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\LOI CATFARM PRO"; Filename: "{app}\{#AppExe}"; WorkingDir: "{app}"
Name: "{autodesktop}\LOI CATFARM PRO"; Filename: "{app}\{#AppExe}"; WorkingDir: "{app}"; Tasks: desktopicon
Name: "{autoprograms}\Preparar VLC portátil"; Filename: "{cmd}"; Parameters: "/c ""{app}\PREPARAR_VLC_PORTATIL.bat"""; WorkingDir: "{app}"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos:"

[Run]
Filename: "{app}\{#AppExe}"; Description: "Abrir LOI CATFARM PRO"; Flags: postinstall nowait skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\_internal\VLC_Portable"
