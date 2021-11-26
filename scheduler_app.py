from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QWidget
from functools import partial
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

        self.slots = {}

        self.init_UI()

    def init_UI(self):

        days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        days_label = QLabel()
        days_label.setText("Days")
        self.days_layout.addWidget(days_label)

        start_hours_label = QLabel()
        start_hours_label.setText("Start hours")
        self.start_hours_layout.addWidget(start_hours_label)

        start_minutes_label = QLabel()
        start_minutes_label.setText("Start minutes")
        self.start_minutes_layout.addWidget(start_minutes_label)

        end_hours_label = QLabel()
        end_hours_label.setText("End hours")
        self.end_hours_layout.addWidget(end_hours_label)

        end_minutes_label = QLabel()
        end_minutes_label.setText("End minutes")
        self.end_minutes_layout.addWidget(end_minutes_label)

        adds_label = QLabel()
        adds_label.setText("Registration buttons")
        self.adds_layout.addWidget(adds_label)

        registered_slots_label = QLabel()
        registered_slots_label.setText("Registered slots")
        self.registered_slots_layout.addWidget(registered_slots_label)

        for i in range(0, len(days_list)):

            self.slots[days_list[i].lower()] = []

            day_label = QLabel()
            day_label.setFixedSize(80, 30)
            day_label.setText(days_list[i])
            self.day_labels.append(day_label)
            self.days_layout.addWidget(day_label)

            start_hour_field = QLineEdit()
            start_hour_field.setFixedSize(50, 30)
            self.start_hour_fields.append(start_hour_field)
            self.start_hours_layout.addWidget(start_hour_field)

            start_minute_field = QLineEdit()
            start_minute_field.setFixedSize(50, 30)
            self.start_minute_fields.append(start_minute_field)
            self.start_minutes_layout.addWidget(start_minute_field)

            end_hour_field = QLineEdit()
            end_hour_field.setFixedSize(50, 30)
            self.end_hour_fields.append(end_hour_field)
            self.end_hours_layout.addWidget(end_hour_field)

            end_minute_field = QLineEdit()
            end_minute_field.setFixedSize(50, 30)
            self.end_minute_fields.append(end_minute_field)
            self.end_minutes_layout.addWidget(end_minute_field)

            registered_slot_label = QLabel()
            self.registered_slot_labels.append(registered_slot_label)
            self.registered_slots_layout.addWidget(registered_slot_label)

            add_button = QPushButton()
            add_button.setFixedSize(80, 30)

            add_button.clicked.connect(partial(self.registrationClicked
                                               , start_hour_field
                                               , start_minute_field
                                               , end_hour_field
                                               , end_minute_field
                                               , registered_slot_label
                                               , self.slots[days_list[i].lower()]))


            self.add_buttons.append(add_button)
            self.adds_layout.addWidget(add_button)


        self.app_layout.addLayout(self.days_layout)
        self.app_layout.addLayout(self.start_hours_layout)
        self.app_layout.addLayout(self.start_minutes_layout)
        self.app_layout.addLayout(self.end_hours_layout)
        self.app_layout.addLayout(self.end_minutes_layout)
        self.app_layout.addLayout(self.adds_layout)
        self.app_layout.addLayout(self.registered_slots_layout)

        self.setLayout(self.app_layout)

    def registrationClicked(self, start_hour_field, start_minute_field, end_hour_field, end_minute_field, registered_slot_labels, day_slots):
        day_slots.append(start_hour_field.text() + ':' + start_minute_field.text() + ' - ' \
                            + end_hour_field.text() + ':' + end_minute_field.text())
        registered_slot_labels.setText(str(day_slots))


def run_app():
    app = QApplication(sys.argv)
    window = SchedulerWindow()
    window.show()
    sys.exit(app.exec_())

run_app()

