from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen

from logixcraft.core.config import APP_NAME, APP_VERSION, ASSETS_ROOT


class SplashScreen(QSplashScreen):
    def __init__(self) -> None:
        super().__init__(self._build_pixmap())
        self.setObjectName("splashScreen")
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

    def show_status(self, message: str) -> None:
        self.showMessage(
            message,
            Qt.AlignLeft | Qt.AlignBottom,
            QColor("#d7dde5"),
        )
        QApplication.processEvents()

    @staticmethod
    def _build_pixmap() -> QPixmap:
        width = 560
        height = 320
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor("#171b21"))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QColor("#202733"))
        painter.setPen(QColor("#364252"))
        painter.drawRoundedRect(0, 0, width - 1, height - 1, 18, 18)

        logo = QPixmap(str(ASSETS_ROOT / "icons" / "app" / "logo_symbol.png"))
        if not logo.isNull():
            logo = logo.scaled(92, 92, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap((width - logo.width()) // 2, 58, logo)

        painter.setPen(QColor("#f3f6fa"))
        title_font = QFont("Roboto", 26)
        title_font.setWeight(QFont.Bold)
        painter.setFont(title_font)
        painter.drawText(0, 170, width, 42, Qt.AlignCenter, APP_NAME)

        painter.setPen(QColor("#aeb8c5"))
        subtitle_font = QFont("Roboto", 10)
        painter.setFont(subtitle_font)
        painter.drawText(
            0,
            208,
            width,
            28,
            Qt.AlignCenter,
            "Industrial automation engineering workspace",
        )

        painter.setPen(QColor("#7f8b99"))
        version_font = QFont("Roboto", 9)
        painter.setFont(version_font)
        painter.drawText(18, height - 38, width - 36, 18, Qt.AlignRight, f"v{APP_VERSION}")

        painter.end()
        return pixmap
