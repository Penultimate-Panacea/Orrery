# coding=utf-8
from PyQt6.QtWidgets import QPushButton, QProgressBar, QVBoxLayout
from PyQt6.QtCore import QTimer, pyqtSignal, Qt, QEvent
from PyQt6.QtGui import QGuiApplication


class DelayProgressButton(QPushButton):
    activated = pyqtSignal()

    def __init__(self, text, parent=None, delay_ms=3000):
        super().__init__(text, parent)
        self.delay_ms = delay_ms
        self.current_time = 0
        self.update_interval = 50

        self._pressed = False

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, self.delay_ms)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: transparent;
                max-height: 75px;
            }
            QProgressBar::chunk {
                background-color: #ffffff;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.progress_bar)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_tick)

    def _cancel(self):
        self._pressed = False
        if self.timer.isActive():
            self.timer.stop()
        self.progress_bar.setValue(0)


    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() != Qt.MouseButton.LeftButton:
            return

        self._pressed = True
        self.current_time = 0
        self.progress_bar.setValue(0)



        self.timer.start(self.update_interval)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self._cancel()

    def focusOutEvent(self, event):
        self._cancel()
        super().focusOutEvent(event)

    def _on_tick(self):
        # If the button is released, cancel instead of emitting.
        if not self._pressed or not (QGuiApplication.mouseButtons() & Qt.MouseButton.LeftButton):
            self._cancel()
            return

        self.current_time += self.update_interval
        self.progress_bar.setValue(self.current_time)

        if self.current_time >= self.delay_ms:
            self.timer.stop()
            self.progress_bar.setValue(0)

            # Double-check right at the emission moment.
            if self._pressed and (QGuiApplication.mouseButtons() & Qt.MouseButton.LeftButton):
                self._pressed = False
                self.activated.emit()
            else:
                self._cancel()
