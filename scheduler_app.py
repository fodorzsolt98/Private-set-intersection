from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QWidget
import sys

class SchedulerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Privacy preserving scheduling app")
        self.day_labels = []
        self.start_hour_fields = []
        self.start_minute_fields = []
        self.end_hour_fields = []
        self.end_minute_fields = []
        self.add_buttons = []
        self.registered_slot_labels = []

        self.main_layout = QVBoxLayout()

        self.header_layout = QHBoxLayout()
        self.app_layout = QHBoxLayout()

        self.days_layout = QVBoxLayout()
        self.start_hours_layout = QVBoxLayout()
        self.start_minutes_layout = QVBoxLayout()
        self.end_hours_layout = QVBoxLayout()
        self.end_minutes_layout = QVBoxLayout()
        self.adds_layout = QVBoxLayout()
        self.registered_slots_layout = QVBoxLayout()

        self.init_UI()

        self.monday_slots = []
        self.tuesday_slots = []
        self.wednesday_slots = []
        self.thursday_slots = []
        self.friday_slots = []

    def init_UI(self):

        days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        for i in range(0, 5):

            if i == 0:
                days_label = QLabel()
                days_label.setText("Days")
                self.days_layout.addWidget(days_label)
            day_label = QLabel()
            day_label.setFixedSize(80, 30)
            day_label.setText(days_list[i])
            self.day_labels.append(day_label)
            self.days_layout.addWidget(day_label)


            if i == 0:
                start_hours_label = QLabel()
                start_hours_label.setText("Start hours")
                self.start_hours_layout.addWidget(start_hours_label)
            start_hour_field = QLineEdit()
            start_hour_field.setFixedSize(50, 30)
            self.start_hour_fields.append(start_hour_field)
            self.start_hours_layout.addWidget(start_hour_field)

            if i == 0:
                start_minutes_label = QLabel()
                start_minutes_label.setText("Start minutes")
                self.start_minutes_layout.addWidget(start_minutes_label)
            start_minute_field = QLineEdit()
            start_minute_field.setFixedSize(50, 30)
            self.start_minute_fields.append(start_minute_field)
            self.start_minutes_layout.addWidget(start_minute_field)

            if i == 0:
                end_hours_label = QLabel()
                end_hours_label.setText("End hours")
                self.end_hours_layout.addWidget(end_hours_label)
            end_hour_field = QLineEdit()
            end_hour_field.setFixedSize(50, 30)
            self.end_hour_fields.append(end_hour_field)
            self.end_hours_layout.addWidget(end_hour_field)

            if i == 0:
                end_minutes_label = QLabel()
                end_minutes_label.setText("End minutes")
                self.end_minutes_layout.addWidget(end_minutes_label)
            end_minute_field = QLineEdit()
            end_minute_field.setFixedSize(50, 30)
            self.end_minute_fields.append(end_minute_field)
            self.end_minutes_layout.addWidget(end_minute_field)

            if i == 0:
                adds_label = QLabel()
                adds_label.setText("Registration buttons")
                self.adds_layout.addWidget(adds_label)
            add_button = QPushButton()
            add_button.setFixedSize(80, 30)

            if i == 0:
                add_button.clicked.connect(self.monday_clicked)
            elif i == 1:
                add_button.clicked.connect(self.tuesday_clicked)
            elif i == 2:
                add_button.clicked.connect(self.wednesday_clicked)
            elif i == 3:
                add_button.clicked.connect(self.thursday_clicked)
            elif i == 4:
                add_button.clicked.connect(self.friday_clicked)
            self.add_buttons.append(add_button)
            self.adds_layout.addWidget(add_button)

            if i == 0:
                registered_slots_label = QLabel()
                registered_slots_label.setText("Registered slots")
                self.registered_slots_layout.addWidget(registered_slots_label)
            registered_slot_label = QLabel()
            self.registered_slot_labels.append(registered_slot_label)
            self.registered_slots_layout.addWidget(registered_slot_label)

        self.app_layout.addLayout(self.days_layout)
        self.app_layout.addLayout(self.start_hours_layout)
        self.app_layout.addLayout(self.start_minutes_layout)
        self.app_layout.addLayout(self.end_hours_layout)
        self.app_layout.addLayout(self.end_minutes_layout)
        self.app_layout.addLayout(self.adds_layout)
        self.app_layout.addLayout(self.registered_slots_layout)

        self.setLayout(self.app_layout)

    def monday_clicked(self):
        slot = self.start_hour_fields[0].text() + ":" + self.start_minute_fields[0].text() + "-" \
               + self.end_hour_fields[0].text() + ":" + self.end_minute_fields[0].text()
        self.monday_slots.append(slot)
        self.registered_slot_labels[0].setText(str(self.monday_slots))

    def tuesday_clicked(self):
        slot = self.start_hour_fields[1].text() + ":" + self.start_minute_fields[1].text() + "-" \
               + self.end_hour_fields[1].text() + ":" + self.end_minute_fields[1].text()
        self.tuesday_slots.append(slot)
        self.registered_slot_labels[1].setText(str(self.tuesday_slots))

    def wednesday_clicked(self):
        slot = self.start_hour_fields[2].text() + ":" + self.start_minute_fields[2].text() + "-" \
               + self.end_hour_fields[2].text() + ":" + self.end_minute_fields[2].text()
        self.wednesday_slots.append(slot)
        self.registered_slot_labels[2].setText(str(self.wednesday_slots))

    def thursday_clicked(self):
        slot = self.start_hour_fields[3].text() + ":" + self.start_minute_fields[3].text() + "-" \
               + self.end_hour_fields[3].text() + ":" + self.end_minute_fields[3].text()
        self.thursday_slots.append(slot)
        self.registered_slot_labels[3].setText(str(self.thursday_slots))

    def friday_clicked(self):
        slot = self.start_hour_fields[4].text() + ":" + self.start_minute_fields[4].text() + "-" \
               + self.end_hour_fields[4].text() + ":" + self.end_minute_fields[4].text()
        self.friday_slots.append(slot)
        self.registered_slot_labels[0].setText(str(self.friday_slots))

def run_app():
    app = QApplication(sys.argv)
    window = SchedulerWindow()
    window.show()
    sys.exit(app.exec_())

run_app()

