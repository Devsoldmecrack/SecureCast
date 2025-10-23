# SecureCast

Simple file encryption/decryption desktop app built with Python and PySide6.

## Features
- **Encrypt/Decrypt** any file with a password (Fernet + PBKDF2-HMAC-SHA256)
- **Modern dark UI** with soft 3D buttons
- **Drag & Drop** file input
- **Windows Explorer reveal** on finish

## Requirements
- Python 3.10+
- `pip install -r requirements.txt`

## Run (dev)
```powershell
python .\main.py
```

## Build (Single EXE)
Creates a single portable `SecureCast.exe` using PyInstaller.
```powershell
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed \
  --name SecureCast \
  --icon assets/icon.ico \
  --add-data "assets;assets" \
  .\main.py
# Result: .\dist\SecureCast.exe
```

## Build (Spec-based, one-folder)
```powershell
pyinstaller --noconfirm .\SecureCast.spec
# Result: .\dist\SecureCast\SecureCast.exe
```

## Folder structure
```
SecureCast/
├─ assets/
│  ├─ icon.svg
│  └─ icon.ico
├─ tools/
│  ├─ make_icon.py
│  └─ create_shortcut.ps1
├─ crypto_utils.py
├─ main.py
├─ requirements.txt
└─ SecureCast.spec
```

## License
Licensed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
