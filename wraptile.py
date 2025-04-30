import sys
import os
import subprocess

# Try to use PyQt5, but fall back to PySide6 if PyQt5 is not available
try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                                QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton, 
                                QTabWidget, QGroupBox, QFileDialog, QMessageBox, QTextEdit,
                                QButtonGroup, QScrollArea, QFormLayout)
    from PyQt5.QtCore import Qt, QProcess, QThread, pyqtSignal
    from PyQt5.QtGui import QFont, QIcon
    USING_PYQT5 = True
except ImportError:
    try:
        from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                                    QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton, 
                                    QTabWidget, QGroupBox, QFileDialog, QMessageBox, QTextEdit,
                                    QButtonGroup, QScrollArea, QFormLayout)
        from PySide6.QtCore import Qt, QProcess, QThread, Signal as pyqtSignal
        from PySide6.QtGui import QFont, QIcon
        USING_PYQT5 = False
    except ImportError:
        print("Error: Either PyQt5 or PySide6 is required to run this application.")
        sys.exit(1)

class PyInstallerWorker(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)
    
    def __init__(self, command):
        super().__init__()
        self.command = command
        
    def run(self):
        try:
            process = QProcess()
            process.setProcessChannelMode(QProcess.MergedChannels)
            process.readyReadStandardOutput.connect(
                lambda: self.output_signal.emit(str(process.readAllStandardOutput().data().decode('utf-8', errors='replace')))
            )
            
            process.start(self.command[0], self.command[1:])
            process.waitForFinished(-1)  # Wait until process finishes
            
            exitCode = process.exitCode()
            self.finished_signal.emit(exitCode)
            
        except Exception as e:
            self.output_signal.emit(f"Error: {str(e)}")
            self.finished_signal.emit(1)

class Wraptile(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wraptile - PyInstaller GUI")
        self.setMinimumSize(850, 650)
        
        # Create the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        # Create tabs
        self.tabs = QTabWidget()
        self.main_tab = QWidget()
        self.advanced_tab = QWidget()
        self.log_tab = QWidget()
        
        self.tabs.addTab(self.main_tab, "Main Settings")
        self.tabs.addTab(self.advanced_tab, "Advanced Settings")
        self.tabs.addTab(self.log_tab, "Output Log")
        
        self.main_layout.addWidget(self.tabs)
        
        # Create the UI elements for each tab
        self.create_main_tab()
        self.create_advanced_tab()
        self.create_log_tab()
        
        # Create compile button
        self.compile_button = QPushButton("Compile")
        self.compile_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.compile_button.setMinimumHeight(40)
        self.compile_button.clicked.connect(self.compile_script)
        self.main_layout.addWidget(self.compile_button)
        
        # Apply stylesheet
        self.apply_stylesheet()
    
    def apply_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                background: #e1e1e1;
                border: 1px solid #c4c4c4;
                padding: 6px 12px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5c94f0;
            }
            QPushButton:pressed {
                background-color: #3a76d8;
            }
            QLineEdit {
                border: 1px solid #cccccc;
                padding: 5px;
                border-radius: 3px;
            }
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
        """)
        
    def create_main_tab(self):
        layout = QVBoxLayout()
        self.main_tab.setLayout(layout)
        
        # Script Selection Group
        script_group = QGroupBox("Script Selection")
        script_layout = QFormLayout()
        script_group.setLayout(script_layout)
        
        script_widget = QWidget()
        script_hbox = QHBoxLayout(script_widget)
        script_hbox.setContentsMargins(0, 0, 0, 0)
        
        self.script_path = QLineEdit()
        script_browse = QPushButton("Browse...")
        script_browse.clicked.connect(self.browse_script)
        
        script_hbox.addWidget(self.script_path)
        script_hbox.addWidget(script_browse)
        
        script_layout.addRow("Python Script:", script_widget)
        layout.addWidget(script_group)
        
        # Output Settings Group
        output_group = QGroupBox("Output Settings")
        output_layout = QFormLayout()
        output_group.setLayout(output_layout)
        
        # Output directory
        output_dir_widget = QWidget()
        output_dir_hbox = QHBoxLayout(output_dir_widget)
        output_dir_hbox.setContentsMargins(0, 0, 0, 0)
        
        self.output_path = QLineEdit()
        output_browse = QPushButton("Browse...")
        output_browse.clicked.connect(self.browse_output)
        
        output_dir_hbox.addWidget(self.output_path)
        output_dir_hbox.addWidget(output_browse)
        
        output_layout.addRow("Output Directory:", output_dir_widget)
        
        # Executable name
        self.exe_name = QLineEdit()
        output_layout.addRow("Executable Name:", self.exe_name)
        
        layout.addWidget(output_group)
        
        # Icon Settings Group
        icon_group = QGroupBox("Icon Settings")
        icon_layout = QFormLayout()
        icon_group.setLayout(icon_layout)
        
        icon_widget = QWidget()
        icon_hbox = QHBoxLayout(icon_widget)
        icon_hbox.setContentsMargins(0, 0, 0, 0)
        
        self.icon_path = QLineEdit()
        icon_browse = QPushButton("Browse...")
        icon_browse.clicked.connect(self.browse_icon)
        
        icon_hbox.addWidget(self.icon_path)
        icon_hbox.addWidget(icon_browse)
        
        icon_layout.addRow("Icon File (.ico):", icon_widget)
        layout.addWidget(icon_group)
        
        # Console Settings Group
        console_group = QGroupBox("Console Settings")
        console_layout = QHBoxLayout()
        console_group.setLayout(console_layout)
        
        self.console_btn_group = QButtonGroup()
        self.console_show = QRadioButton("Show Console Window")
        self.console_hide = QRadioButton("Hide Console Window")
        self.console_show.setChecked(True)
        
        self.console_btn_group.addButton(self.console_show)
        self.console_btn_group.addButton(self.console_hide)
        
        console_layout.addWidget(self.console_show)
        console_layout.addWidget(self.console_hide)
        console_layout.addStretch()
        
        layout.addWidget(console_group)
        
        # Distribution Format Group
        format_group = QGroupBox("Distribution Format")
        format_layout = QVBoxLayout()
        format_group.setLayout(format_layout)
        
        self.onefile_option = QCheckBox("Create a single executable file (--onefile)")
        self.onefile_option.setChecked(True)
        
        format_layout.addWidget(self.onefile_option)
        layout.addWidget(format_group)
        
        # Add stretch to push everything to the top
        layout.addStretch()
    
    def create_advanced_tab(self):
        # Create a scroll area for the advanced tab
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        advanced_widget = QWidget()
        layout = QVBoxLayout()
        advanced_widget.setLayout(layout)
        scroll_area.setWidget(advanced_widget)
        
        advanced_tab_layout = QVBoxLayout()
        advanced_tab_layout.addWidget(scroll_area)
        self.advanced_tab.setLayout(advanced_tab_layout)
        
        # Advanced Options Group
        options_group = QGroupBox("Advanced PyInstaller Options")
        options_layout = QVBoxLayout()
        options_group.setLayout(options_layout)
        
        self.clean_option = QCheckBox("Clean before build (--clean)")
        self.clean_option.setChecked(True)
        options_layout.addWidget(self.clean_option)
        
        self.upx_option = QCheckBox("Use UPX compression (if installed)")
        options_layout.addWidget(self.upx_option)
        
        self.strip_option = QCheckBox("Strip symbols from executable (--strip)")
        options_layout.addWidget(self.strip_option)
        
        self.noupx_option = QCheckBox("Disable UPX (--noupx)")
        options_layout.addWidget(self.noupx_option)
        
        self.uac_admin_option = QCheckBox("Request UAC elevation (--uac-admin)")
        options_layout.addWidget(self.uac_admin_option)
        
        layout.addWidget(options_group)
        
        # Data Files Group
        data_group = QGroupBox("Additional Data Files")
        data_layout = QVBoxLayout()
        data_group.setLayout(data_layout)
        
        data_layout.addWidget(QLabel("Add data files using format: src;dest"))
        self.data_files = QTextEdit()
        self.data_files.setMinimumHeight(100)
        data_layout.addWidget(self.data_files)
        data_layout.addWidget(QLabel("Example: images/*.png;images/"))
        
        layout.addWidget(data_group)
        
        # Additional Arguments Group
        args_group = QGroupBox("Additional PyInstaller Arguments")
        args_layout = QVBoxLayout()
        args_group.setLayout(args_layout)
        
        args_layout.addWidget(QLabel("Additional command line arguments:"))
        self.extra_args = QLineEdit()
        args_layout.addWidget(self.extra_args)
        
        layout.addWidget(args_group)
        
        # Add stretch to push everything to the top
        layout.addStretch()
    
    def create_log_tab(self):
        layout = QVBoxLayout()
        self.log_tab.setLayout(layout)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Consolas", 9))
        layout.addWidget(self.log_output)
    
    def browse_script(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Python Script", "", "Python files (*.py);;All files (*.*)"
        )
        if file_path:
            self.script_path.setText(file_path)
            # Auto-fill executable name from script name
            script_name = os.path.splitext(os.path.basename(file_path))[0]
            self.exe_name.setText(script_name)
    
    def browse_output(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_path.setText(dir_path)
    
    def browse_icon(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Icon File", "", "Icon files (*.ico);;All files (*.*)"
        )
        if file_path:
            self.icon_path.setText(file_path)
    
    def log_message(self, message):
        self.log_output.append(message)
        # Force processing of events to update UI
        QApplication.processEvents()
    
    def compile_script(self):
        script_path = self.script_path.text().strip()
        if not script_path:
            QMessageBox.critical(self, "Error", "Please select a Python script file.")
            return
        
        if not os.path.isfile(script_path):
            QMessageBox.critical(self, "Error", f"Script file not found: {script_path}")
            return
        
        # Clear log
        self.log_output.clear()
        
        # Switch to log tab
        self.tabs.setCurrentIndex(2)
        
        # Build the command
        cmd = ["pyinstaller"]
        
        # Main options
        if self.onefile_option.isChecked():
            cmd.append("--onefile")
        
        if self.console_hide.isChecked():
            cmd.append("--windowed")
        
        # Icon
        icon_path = self.icon_path.text().strip()
        if icon_path:
            cmd.extend(["--icon", icon_path])
        
        # Output directory
        output_path = self.output_path.text().strip()
        if output_path:
            cmd.extend(["--distpath", output_path])
        
        # Executable name
        exe_name = self.exe_name.text().strip()
        if exe_name:
            cmd.extend(["--name", exe_name])
        
        # Advanced options
        if self.clean_option.isChecked():
            cmd.append("--clean")
        
        if self.upx_option.isChecked():
            cmd.append("--upx-dir")
        
        if self.strip_option.isChecked():
            cmd.append("--strip")
        
        if self.noupx_option.isChecked():
            cmd.append("--noupx")
        
        if self.uac_admin_option.isChecked():
            cmd.append("--uac-admin")
        
        # Add data files
        data_files_text = self.data_files.toPlainText().strip()
        if data_files_text:
            for line in data_files_text.split("\n"):
                if line.strip():
                    cmd.extend(["--add-data", line])
        
        # Additional arguments
        extra_args = self.extra_args.text().strip()
        if extra_args:
            cmd.extend(extra_args.split())
        
        # Add script path
        cmd.append(script_path)
        
        # Add exclusion for the Qt binding not in use by this app
        # This helps prevent the "multiple Qt bindings" error
        if USING_PYQT5:
            cmd.extend(["--exclude", "PyQt6", "--exclude", "PySide6"])
        else:
            cmd.extend(["--exclude", "PyQt5", "--exclude", "PySide2"])
            
        # Log the command
        self.log_message("Running command: " + " ".join(cmd))
        self.log_message("\nBuilding executable, please wait...\n")
        
        # Disable compile button
        self.compile_button.setEnabled(False)
        
        # Create and start worker thread
        self.worker = PyInstallerWorker(cmd)
        self.worker.output_signal.connect(self.log_message)
        self.worker.finished_signal.connect(self.build_finished)
        self.worker.start()
    
    def build_finished(self, return_code):
        # Re-enable compile button
        self.compile_button.setEnabled(True)
        
        if return_code == 0:
            self.log_message("\nBuild completed successfully!")
            
            # Get output path
            output_path = self.output_path.text().strip()
            exe_name = self.exe_name.text().strip()
            
            if output_path:
                final_path = os.path.join(output_path, exe_name + ".exe" if exe_name else "")
                self.log_message(f"Executable saved to: {final_path}")
            else:
                self.log_message("Executable saved to the 'dist' directory in the project folder.")
            
            QMessageBox.information(self, "Success", "Executable built successfully!")
        else:
            self.log_message("\nBuild failed with error code: " + str(return_code))
            QMessageBox.critical(self, "Error", "Build failed. Check the log for details.")

def check_pyinstaller():
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a consistent look
    app.setApplicationName("Wraptile")
    
    # Check if PyInstaller is installed
    if not check_pyinstaller():
        reply = QMessageBox.question(
            None, 
            "PyInstaller Not Found",
            "PyInstaller is not installed. Would you like to install it now?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                QMessageBox.information(
                    None,
                    "Installing PyInstaller",
                    "Installing PyInstaller. This may take a moment..."
                )
                
                process = QProcess()
                process.start(sys.executable, ["-m", "pip", "install", "pyinstaller"])
                process.waitForFinished(-1)
                
                if process.exitCode() == 0:
                    QMessageBox.information(None, "Success", "PyInstaller installed successfully!")
                else:
                    error = process.readAllStandardError().data().decode()
                    QMessageBox.critical(
                        None,
                        "Error",
                        f"Failed to install PyInstaller:\n{error}"
                    )
                    return
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to install PyInstaller: {str(e)}")
                return
        else:
            return
    
    window = Wraptile()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()