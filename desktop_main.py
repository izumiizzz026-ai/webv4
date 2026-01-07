"""
QR Attendance System - Desktop Application
PyQt6-based native desktop window with embedded Flask server

Supports two modes:
- OFFLINE: Runs local Flask server with SQLite database
- ONLINE: Connects to remote cloud server (shared database)
"""

import os
import sys
import json
import threading
import time
from pathlib import Path

import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt, QTimer
from PyQt6.QtGui import QIcon

# Add app directory to path
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

from app import app as flask_app, db
from db_manager import init_db_manager


def resource_path(relative_path: str) -> Path:
    """Resolve resource path for bundled or dev runs."""
    base_path = getattr(sys, '_MEIPASS', Path(__file__).parent)
    return Path(base_path) / relative_path

class QRAttendanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load configuration
        self.config_file = Path(os.path.dirname(os.path.abspath(__file__))) / 'desktop_config.json'
        self.config = self.load_config()
        self.mode = self.config.get('mode', 'offline')
        self.server_url = self.get_server_url()
        self.server_thread = None
        self.server_running = False

        # Apply app icon early so window and taskbar pick it up
        icon_file = resource_path('LYFJRSHS_logo.ico')
        if not icon_file.exists():
            icon_file = resource_path('LYFJRSHS_logo.jpg')
        app_icon = QIcon(str(icon_file))
        self.setWindowIcon(app_icon)
        
        # Set window properties FIRST
        mode_label = "ONLINE" if self.mode == "online" else "OFFLINE"
        self.setWindowTitle(f'QR Attendance System [{mode_label}] - Starting...')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create web view (empty for now)
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        
        # Start based on mode
        if self.mode == 'online':
            # Online mode: just connect to remote server
            print(f"✓ Online mode - Connecting to: {self.server_url}")
            QTimer.singleShot(500, self.load_page)
        else:
            # Offline mode: start local Flask server first
            self.start_flask_server()
            QTimer.singleShot(2000, self.load_page)  # Wait 2 seconds for server to start
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠ Warning: Could not load config file: {e}")
        return {'mode': 'offline', 'server_url': 'http://localhost:5000'}
    
    def get_server_url(self):
        """Get the appropriate server URL based on mode"""
        if self.mode == 'online':
            return self.config.get('cloud_url', 'https://your-app.railway.app')
        return self.config.get('server_url', 'http://localhost:5000')
    
    def start_flask_server(self):
        """Start Flask server in background thread"""
        try:
            # Extract port from server URL
            port = 5000
            if ':' in self.server_url:
                try:
                    port = int(self.server_url.split(':')[-1].rstrip('/'))
                except:
                    port = 5000
            
            # Create database if needed and initialize db_manager
            with flask_app.app_context():
                db.create_all()
                # Initialize the multi-database manager
                init_db_manager(flask_app)
            
            # Start server in daemon thread
            self.server_thread = threading.Thread(
                target=lambda: flask_app.run(
                    host='localhost',
                    port=port,
                    debug=False,
                    use_reloader=False
                ),
                daemon=True
            )
            self.server_thread.start()
            self.server_running = True
            print(f"✓ Flask server started on {self.server_url}")
            
        except Exception as e:
            print(f"✗ Error starting Flask server: {e}")
            self.server_running = False
    
    def load_page(self):
        """Load the Flask app in the browser view"""
        mode_label = "ONLINE" if self.mode == "online" else "OFFLINE"
        self.setWindowTitle(f'QR Attendance System [{mode_label}]')
        self.browser.setUrl(QUrl(self.server_url))
        self.browser.loadFinished.connect(self.on_load_finished)
        print(f"✓ Loading page: {self.server_url}")
    
    def on_load_finished(self, success):
        """Handle page load completion"""
        if not success:
            if self.mode == 'online':
                error_msg = (
                    f'Could not connect to cloud server at:\n{self.server_url}\n\n'
                    'Please check:\n'
                    '1. Internet connection is active\n'
                    '2. Cloud server is running\n'
                    '3. URL in desktop_config.json is correct\n\n'
                    'To use offline mode, set "mode": "offline" in desktop_config.json'
                )
            else:
                error_msg = (
                    f'Could not connect to local server at:\n{self.server_url}\n\n'
                    'Please check:\n'
                    '1. Server started correctly\n'
                    '2. Port 5000 is available'
                )
            QMessageBox.warning(self, 'Connection Error', error_msg)
            print(f"✗ Failed to load: {self.server_url}")
        else:
            print(f"✓ Successfully loaded: {self.server_url}")
    
    def closeEvent(self, event):
        """Handle window close event"""
        print("✓ Closing application...")
        event.accept()

def main():
    """Entry point for the application"""
    print("=" * 60)
    print("QR ATTENDANCE SYSTEM - DESKTOP APPLICATION")
    print("=" * 60)
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName('QR Attendance System')
    icon_file = resource_path('LYFJRSHS_logo.ico')
    if not icon_file.exists():
        icon_file = resource_path('LYFJRSHS_logo.jpg')
    app.setWindowIcon(QIcon(str(icon_file)))
    
    # Create and show main window
    window = QRAttendanceApp()
    window.show()
    
    print("✓ Application window opened")
    print("=" * 60)
    
    # Run application event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
