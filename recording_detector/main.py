import sys
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QMessageBox, QMenuBar, QAction
from PyQt5.QtCore import QTimer

# List of recording applications to detect
RECORDING_APPS = ['obs64.exe', 'camtasia.exe', 'zoom.exe', 'teams.exe']

class RecordingDetectorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up main window
        self.setWindowTitle('Recording Detection App')
        self.setGeometry(100, 100, 400, 200)

        # Main layout
        self.layout = QVBoxLayout()

        # Add start/stop buttons
        self.start_button = QPushButton('Start Detection', self)
        self.start_button.clicked.connect(self.start_detection)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop Detection', self)
        self.stop_button.clicked.connect(self.stop_detection)
        self.layout.addWidget(self.stop_button)

        # Add status label
        self.status_label = QLabel('Status: Idle', self)
        self.layout.addWidget(self.status_label)

        # Set up timer for periodic detection
        self.timer = QTimer()
        self.timer.timeout.connect(self.detect_recording)

        # Set up the central widget and layout
        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Add a menu bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        # Add "About" action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        self.menu_bar.addAction(about_action)

        # Add "Exit" action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        self.menu_bar.addAction(exit_action)

        # Apply custom theme (QSS)
        self.apply_theme()

    def apply_theme(self):
        """Apply a custom QSS theme to the application."""
        theme = """
        QMainWindow {
            background-color: #2E3440;
            color: #D8DEE9;
        }
        QPushButton {
            background-color: #4C566A;
            color: #D8DEE9;
            font-size: 14px;
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #81A1C1;
        }
        QLabel {
            font-size: 16px;
            color: #D8DEE9;
        }
        QMenuBar {
            background-color: #3B4252;
            color: #D8DEE9;
        }
        QMenuBar::item:selected {
            background-color: #81A1C1;
        }
        QMenu {
            background-color: #4C566A;
            color: #D8DEE9;
        }
        QMessageBox {
            background-color: #2E3440;
            color: #D8DEE9;
        }
        """
        # Apply the stylesheet to the whole app
        self.setStyleSheet(theme)

    def start_detection(self):
        self.status_label.setText('Status: Detecting...')
        self.timer.start(5000)  # Check every 5 seconds

    def stop_detection(self):
        self.status_label.setText('Status: Idle')
        self.timer.stop()

    def detect_recording(self):
        detected_apps = self.check_recording()
        if detected_apps:
            self.status_label.setText(f'Recording Detected: {", ".join(detected_apps)}')
            self.show_notification(detected_apps)
        else:
            self.status_label.setText('Status: No Recording Detected')

    def check_recording(self):
        # Get the list of currently running processes
        running_processes = [proc.name() for proc in psutil.process_iter()]
        # Check if any recording app is running
        detected_apps = [app for app in RECORDING_APPS if app in running_processes]
        return detected_apps

    def show_notification(self, detected_apps):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Recording Detected")
        msg.setText(f"The following recording apps are detected: {', '.join(detected_apps)}")
        msg.exec_()

    def show_about(self):
        QMessageBox.about(self, "About", "Recording Detection App\nVersion 1.0\nDetects screen recording apps in real time.")

# Main loop
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RecordingDetectorApp()
    window.show()
    sys.exit(app.exec_())