"""sys is responsible for command line arguments and exiting the app gracefully.
The other modules are as follows:
QApplication: main application handler.

QWidget: base class for all UI components (windows).

QLabel: for text display.

QLineEdit: for text input.

QPushButton: for clickable buttons.

QVBoxLayout / QHBoxLayout: vertical and horizontal layout containers.

QMessageBox: popup dialog for warnings/errors/info.

QComboBox: dropdown selection boxes.

"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from currency_utils import convert_currency # imports custom logic of functions from currency_utils
from config import API_KEY
from PyQt6.QtGui import QCursor
from valid_currencies import valid_currencies_dict
# used to fetch from tuple of currencies to populate
# the dropdown menu in the GUI.


"""we have set a Fixed Size of 300 by 200 pixels
The size is fixed, and not resizeable at this time. """
class CurrencyConverterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Currency Converter")
        self.setFixedSize(300, 200)

        # Amount Input
        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount (positive number)")

        """Validator is used to ensure that the legal range of values entered by a user
        are between (but greater than 0.0) and 1 x 10^ 15. The 2 is used to denote 
        2 decimal places. These are intended as data input sanitation methods.
        """
        validator = QDoubleValidator(0.0, 1e15, 2)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.amount_input.setValidator(validator)

        # Currency Selection
        """Label "From Currency:.
Dropdown combo box for selecting the currency to convert from.
Populates combo box with the valid currency codes imported earlier.
Sets the default selected currency to the second item (index 1) 
to avoid it being the same as "from" by default.

"""
        self.from_label = QLabel("From Currency:")
        self.from_combo = QComboBox()
        self.from_combo.addItems(VALID_CURRENCIES)

        self.to_label = QLabel("To Currency:")
        self.to_combo = QComboBox()
        self.to_combo.addItems(VALID_CURRENCIES)
        self.to_combo.setCurrentIndex(1)

        # Convert Button
        self.convert_button = QPushButton("Convert")
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(self.convert_currency)

        # Result Label
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)

        h_layout_from = QHBoxLayout()
        h_layout_from.addWidget(self.from_label)
        h_layout_from.addWidget(self.from_combo)
        layout.addLayout(h_layout_from)

        h_layout_to = QHBoxLayout()
        h_layout_to.addWidget(self.to_label)
        h_layout_to.addWidget(self.to_combo)
        layout.addLayout(h_layout_to)

        layout.addWidget(self.convert_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

        # Signal Connections
        self.amount_input.textChanged.connect(self.validate_input)
        self.from_combo.currentIndexChanged.connect(self.validate_input)
        self.to_combo.currentIndexChanged.connect(self.validate_input)

    def validate_input(self):
        amount_text = self.amount_input.text().strip()
        is_valid = False

        try:
            amount = float(amount_text)
            if amount > 0 and self.from_combo.currentText() != self.to_combo.currentText():
                is_valid = True
        except ValueError:
            pass

        # Feedback: Red background if invalid
        self.amount_input.setStyleSheet("" if is_valid else "background-color: #fdd;")
        self.convert_button.setEnabled(is_valid)

    def convert_currency(self):
        self.setCursor(QCursor(Qt.CursorShape.WaitCursor))  # Show loading cursor
        self.convert_button.setEnabled(False)
        amount_text = self.amount_input.text().strip()

        try:
            amount = float(amount_text)
            if not amount_text:
                self.show_error("Missing Input", "Please enter an amount.")
                return
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))
            self.convert_button.setEnabled(True)
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))  # Restore normal cursor
            return

        from_curr = self.from_combo.currentText()
        to_curr = self.to_combo.currentText()

        if from_curr == to_curr:
            QMessageBox.information(
                self, "Notice", "From and To currencies are the same."
            )
            self.result_label.setText(f"{amount:.2f} {from_curr} = {amount:.2f} {to_curr}")
            self.convert_button.setEnabled(True)
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))  # Restore normal cursor
            return

        try:
            converted = convert_currency(API_KEY, amount, from_curr, to_curr)
            if converted is not None:
                self.result_label.setText(
                    f"💱 {amount:.2f} {from_curr} = {converted:.2f} {to_curr}"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Conversion Failed",
                    "Conversion failed. Check API or currency codes.",
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{e}")
        finally:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))  # Restore normal cursor
            self.convert_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyConverterGUI()
    window.show()
    sys.exit(app.exec())