import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QProgressBar, QMessageBox, QGraphicsDropShadowEffect
from PySide6.QtGui import QPalette, QColor, QIcon
from PySide6.QtCore import Qt, QThread, QObject, Signal
from crypto_utils import encrypt_file, decrypt_file


class Worker(QObject):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, mode: str, in_path: str, out_path: str, password: str):
        super().__init__()
        self.mode = mode
        self.in_path = in_path
        self.out_path = out_path
        self.password = password

    def run(self):
        try:
            if self.mode == "enc":
                encrypt_file(self.in_path, self.out_path, self.password)
            else:
                decrypt_file(self.in_path, self.out_path, self.password)
            self.finished.emit(self.out_path)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SecureCast")
        self.setAcceptDrops(True)
        layout = QVBoxLayout()
        self.file_edit = QLineEdit()
        self.browse = QPushButton("Choose File")
        row = QHBoxLayout()
        row.addWidget(self.file_edit)
        row.addWidget(self.browse)
        self.pw_edit = QLineEdit()
        self.pw_edit.setEchoMode(QLineEdit.Password)
        self.encrypt_btn = QPushButton("Encrypt")
        self.decrypt_btn = QPushButton("Decrypt")
        btns = QHBoxLayout()
        btns.addWidget(self.encrypt_btn)
        btns.addWidget(self.decrypt_btn)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()
        layout.addWidget(QLabel("File"))
        layout.addLayout(row)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.pw_edit)
        layout.addLayout(btns)
        layout.addWidget(self.progress)
        self.footer = QLabel("© Devsoldmecrack")
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setStyleSheet("color: #9aa3ad; font-size: 11px;")
        layout.addWidget(self.footer)
        self.setLayout(layout)
        self.browse.clicked.connect(self.choose_file)
        self.encrypt_btn.clicked.connect(self.handle_encrypt)
        self.decrypt_btn.clicked.connect(self.handle_decrypt)
        self.style_widgets()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            self.file_edit.setText(path)

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            self.file_edit.setText(path)

    def handle_encrypt(self):
        path = self.file_edit.text()
        pw = self.pw_edit.text()
        if not path:
            QMessageBox.warning(self, "Notice", "Please select a file first.")
            return
        if not os.path.isfile(path):
            QMessageBox.warning(self, "Notice", "The selected path is not a valid file.")
            return
        if not pw:
            QMessageBox.warning(self, "Notice", "Please enter a password.")
            return
        out = path + ".enc"
        self.start_worker("enc", path, out, pw)

    def handle_decrypt(self):
        path = self.file_edit.text()
        pw = self.pw_edit.text()
        if not path:
            QMessageBox.warning(self, "Notice", "Please select a file first.")
            return
        if not os.path.isfile(path):
            QMessageBox.warning(self, "Notice", "The selected path is not a valid file.")
            return
        if not pw:
            QMessageBox.warning(self, "Notice", "Please enter a password.")
            return
        base = path
        if base.lower().endswith(".enc"):
            base = base[:-4]
        out = base + ".dec"
        self.start_worker("dec", path, out, pw)

    def start_worker(self, mode: str, in_path: str, out_path: str, password: str):
        self.busy(True)
        thread = QThread()
        worker = Worker(mode, in_path, out_path, password)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(self.on_finished)
        worker.error.connect(self.on_error)
        
        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)
        thread.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        
        self._thread = thread
        self._worker = worker
        thread.start()

    def on_finished(self, out_path: str):
        self.busy(False)
        self.open_in_explorer(out_path)
        QMessageBox.information(self, "Done", f"Output file created:\n{out_path}")

    def on_error(self, msg: str):
        self.busy(False)
        QMessageBox.critical(self, "Error", msg)

    def busy(self, on: bool):
        self.progress.setVisible(on)
        self.encrypt_btn.setEnabled(not on)
        self.decrypt_btn.setEnabled(not on)
        self.file_edit.setEnabled(not on)

    def open_in_explorer(self, path: str):
        try:
            if sys.platform.startswith("win"):
                
                subprocess.run(["explorer", f"/select,{os.path.abspath(path)}"])  
            elif sys.platform == "darwin":
                subprocess.run(["open", "-R", path])  
            else:
                folder = os.path.dirname(os.path.abspath(path)) or "."
                subprocess.run(["xdg-open", folder])
        except Exception:
            
            pass

    def style_widgets(self):
        self.file_edit.setMinimumHeight(36)
        self.pw_edit.setMinimumHeight(36)
        self.encrypt_btn.setMinimumHeight(40)
        self.decrypt_btn.setMinimumHeight(40)

        for btn, base, border in [
            (self.browse, "#2b3a49", "#2f3a48"),
            (self.encrypt_btn, "#2b3a49", "#2f3a48"),
            (self.decrypt_btn, "#2b3a49", "#2f3a48"),
        ]:
            shadow = QGraphicsDropShadowEffect(blurRadius=18, xOffset=0, yOffset=4)
            shadow.setColor(QColor(0, 0, 0, 100))
            btn.setGraphicsEffect(shadow)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    color: #e6e6f0;
                    font-weight: 600;
                    border: 1px solid {border};
                    border-radius: 10px;
                    padding: 8px 18px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 #344455, stop:0.5 {base}, stop:1 #1f2a36);
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 #3b4d60, stop:0.5 #344657, stop:1 #243241);
                }}
                QPushButton:pressed {{
                    padding-top: 10px;
                    padding-bottom: 6px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 #1f2a36, stop:1 #17202a);
                    border-color: #1f2a36;
                }}
                """
            )


def apply_dark_theme(app: QApplication):
    p = QPalette()
    p.setColor(QPalette.Window, QColor(20, 26, 46))
    p.setColor(QPalette.WindowText, QColor(220, 220, 230))
    p.setColor(QPalette.Base, QColor(30, 34, 54))
    p.setColor(QPalette.AlternateBase, QColor(36, 40, 60))
    p.setColor(QPalette.ToolTipBase, QColor(220, 220, 230))
    p.setColor(QPalette.ToolTipText, QColor(220, 220, 230))
    p.setColor(QPalette.Text, QColor(220, 220, 230))
    p.setColor(QPalette.Button, QColor(36, 40, 60))
    p.setColor(QPalette.ButtonText, QColor(220, 220, 230))
    p.setColor(QPalette.Highlight, QColor(0, 122, 204))
    p.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(p)
    app.setStyleSheet(
        """
        QWidget{
            background:#141a2e;
            color:#dcdce6;
        }
        QLineEdit{
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                        stop:0 #232840, stop:1 #1e2236);
            border:1px solid #2f3a48;
            padding:8px 10px;
            border-radius:8px;
        }
        QLineEdit:hover{
            border-color:#3a4656;
        }
        QLineEdit:focus{
            border-color:#007acc;
            outline: none;
        }
        QProgressBar{
            background: #1e2236;
            border:1px solid #2f3a48;
            border-radius:8px;
            text-align:center;
            color:#dcdce6;
        }
        QProgressBar::chunk{
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                        stop:0 #0b82e6, stop:1 #0a69ba);
            border-radius:8px;
        }
        """
    )


def load_app_icon() -> QIcon:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ico_path = os.path.join(base_dir, "assets", "icon.ico")
    svg_path = os.path.join(base_dir, "assets", "icon.svg")
    if sys.platform.startswith("win") and os.path.exists(ico_path):
        return QIcon(ico_path)
    if os.path.exists(svg_path):
        return QIcon(svg_path)
    return QIcon()


def main():
    app = QApplication(sys.argv)
    
    if sys.platform.startswith("win"):
        try:
            import ctypes  
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("SecureCast.SecureCast")
        except Exception:
            pass
    apply_dark_theme(app)
    
    icon = load_app_icon()
    if not icon.isNull():
        app.setWindowIcon(icon)
    w = MainWindow()
    if not icon.isNull():
        w.setWindowIcon(icon)
    w.resize(520, 220)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
