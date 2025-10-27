[Setup]
AppName=ALS
AppVersion={#MyAppVersion}
DefaultDirName={commonpf64}\ALS
DefaultGroupName=ALS
OutputDir=..\..
OutputBaseFilename={#MyAppName}-{#MyAppVersion}_Setup
SetupIconFile=..\..\src\resources\als_logo.ico
Compression=lzma
SolidCompression=yes
WizardImageFile=installer-wizard-artwork.bmp
UsePreviousAppDir=yes
UninstallDisplayIcon={app}\als.exe
Uninstallable=yes
LicenseFile=gpl-3.0.txt
LanguageDetectionMethod=uilanguage

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Files]
Source: "..\..\dist\als\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\ALS"; Filename: "{app}\als.exe"

[Run]
Filename: "{app}\als.exe"; Description: "{cm:LaunchProgram,ALS}"; Flags: nowait postinstall skipifsilent
