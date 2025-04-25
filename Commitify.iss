[Setup]
AppName=Commitify
AppVersion=1.0
DefaultDirName={pf}\Commitify
DefaultGroupName=Commitify
OutputBaseFilename=CommitifyInstaller
ArchitecturesInstallIn64BitMode=x64
Compression=lzma
SolidCompression=yes

[Files]
Source: "CommitifyInstaller\Commitify.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{commondesktop}\Commitify"; Filename: "{app}\Commitify.exe"
Name: "{group}\Commitify"; Filename: "{app}\Commitify.exe"

[Registry]
; Add Commitify to the system PATH (for all users)
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Flags: preservestringtype

[Run]
; Optionally, you can force a reload of the PATH variable for running processes
Filename: "{cmd}"; Parameters: "/C setx /M PATH ""%PATH%;{app}"""; Flags: runhidden
