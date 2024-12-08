import sys
import serial
import serial.tools.list_ports
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QTextEdit,
                             QPushButton, QWidget, QLabel, QComboBox, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal, QObject


class SerialSignals(QObject):
    """Signals for thread-safe communication with GUI"""
    data_received = pyqtSignal(str)
    ports_updated = pyqtSignal(list)


class SerialMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Serial Port Monitor")
        self.setGeometry(100, 100, 400, 500)  # Slightly wider to accommodate buttons

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Ports Dropdown
        self.ports_combo = QComboBox()
        self.ports_combo.addItem("Select Device to Connect")
        self.ports_combo.setCurrentIndex(0)

        # Baud Rate Dropdown
        self.baud_combo = QComboBox()
        self.baud_combo.addItems([
            "9600", "115200", "57600", "38400",
            "19200", "14400", "4800", "2400"
        ])
        self.baud_combo.setCurrentText("9600")

        # Buttons Layout (Horizontal)
        buttons_layout = QHBoxLayout()

        # Refresh Ports Button
        self.refresh_ports_btn = QPushButton("Refresh Ports")
        self.refresh_ports_btn.clicked.connect(self.update_available_ports)

        # Connect Button
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.start_serial_connection)

        # Disconnect Button
        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_serial)

        # Auto Scroll Toggle Button
        self.autoscroll_btn = QPushButton("Auto Scroll: ON")
        self.autoscroll_btn.clicked.connect(self.toggle_autoscroll)
        self.is_autoscroll = True

        # Add buttons to horizontal layout
        buttons_layout.addWidget(self.refresh_ports_btn)
        buttons_layout.addWidget(self.connect_btn)
        buttons_layout.addWidget(self.disconnect_btn)
        buttons_layout.addWidget(self.autoscroll_btn)

        # Text area for serial data
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        # Clear Button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_text_area)

        # Add widgets to main layout
        main_layout.addWidget(self.ports_combo)
        main_layout.addWidget(self.baud_combo)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.text_area)
        main_layout.addWidget(self.clear_btn)

        # Serial connection variables
        self.serial_thread = None
        self.stop_event = threading.Event()
        self.signals = SerialSignals()
        self.signals.data_received.connect(self.update_text_area)

        # Initial port update
        self.update_available_ports()

    def toggle_autoscroll(self):
        """Toggle auto-scroll functionality"""
        self.is_autoscroll = not self.is_autoscroll
        if self.is_autoscroll:
            self.autoscroll_btn.setText("Auto Scroll: ON")
        else:
            self.autoscroll_btn.setText("Auto Scroll: OFF")

    def disconnect_serial(self):
        """Disconnect the serial connection"""
        if self.serial_thread and self.serial_thread.is_alive():
            self.stop_event.set()
            self.serial_thread.join()
            self.update_text_area("Disconnected from serial port")

    def update_available_ports(self):
        """Fetch and display available serial ports"""
        ports = serial.tools.list_ports.comports()
        port_list = []

        for port in ports:
            # Format: COM Port - Device Description
            port_description = f"{port.device} - {port.description}"
            port_list.append(port_description)

        # Clear existing items
        self.ports_combo.clear()
        self.ports_combo.addItem("Select Device to Connect")

        # Add new ports
        if port_list:
            self.ports_combo.addItems(port_list)
        else:
            self.ports_combo.addItem("No ports found")

    def start_serial_connection(self):
        # Stop any existing connection
        if self.serial_thread and self.serial_thread.is_alive():
            self.stop_event.set()
            self.serial_thread.join()

        # Reset stop event
        self.stop_event.clear()

        # Get selected port and baud rate
        selected_port = self.ports_combo.currentText()

        # Check if a valid port is selected
        if selected_port == "Select Device to Connect":
            self.update_text_area("Please select a valid port")
            return

        # Extract just the COM port (before the dash)
        port = selected_port.split(' - ')[0]
        baud = int(self.baud_combo.currentText())

        try:
            # Start new serial thread
            self.serial_thread = threading.Thread(
                target=self.read_serial,
                args=(port, baud)
            )
            self.serial_thread.start()
        except Exception as e:
            self.update_text_area(f"Error: {str(e)}")

    def read_serial(self, port, baud):
        try:
            with serial.Serial(port, baud, timeout=1) as ser:
                self.signals.data_received.emit(f"Connected to {port} at {baud} baud.")

                while not self.stop_event.is_set():
                    if ser.in_waiting > 0:
                        data = ser.readline().decode().strip()
                        self.signals.data_received.emit(data)
        except Exception as e:
            self.signals.data_received.emit(f"Error: {str(e)}")

    def update_text_area(self, text):
        """Update text area with new data"""
        self.text_area.append(text)

        # Auto-scroll only if enabled
        if self.is_autoscroll:
            self.text_area.verticalScrollBar().setValue(
                self.text_area.verticalScrollBar().maximum()
            )

    def clear_text_area(self):
        """Clear the text area"""
        self.text_area.clear()

    def closeEvent(self, event):
        """Handle application close"""
        if self.serial_thread and self.serial_thread.is_alive():
            self.stop_event.set()
            self.serial_thread.join()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = SerialMonitorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()