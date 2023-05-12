import sys
import threading
import vlc
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QSlider, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 중앙 위젯 생성
        centralWidget = QWidget()
        centralLayout = QVBoxLayout()
        centralWidget.setLayout(centralLayout)
        self.setCentralWidget(centralWidget)

        # 컨트롤 바 생성
        controlWidget = QWidget()
        controlLayout = QHBoxLayout()
        controlWidget.setLayout(controlLayout)
        centralLayout.addWidget(controlWidget)

        # 재생/일시정지 버튼 생성
        playButton = QPushButton("Play")
        playButton.clicked.connect(self.playButtonClicked)
        controlLayout.addWidget(playButton)

        # 슬라이더 생성
        self.positionSlider = QSlider()
        self.positionSlider.setRange(0, 100)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        controlLayout.addWidget(self.positionSlider)

        # 미디어 플레이어 생성
        self.mediaPlayer = vlc.MediaPlayer()

        # m3u8 미디어 재생 목록 파일 지정
        media = vlc.Media("C:/Users/ZZY/Desktop/0_cityeyelab/code/firebase_exp/backend/hls/playlist_1080p.m3u8")
        self.mediaPlayer.set_media(media)

        # 비디오 재생
        self.mediaPlayer.play()


    def playButtonClicked(self):
        # 미디어 플레이어 상태에 따라 재생/일시정지 전환
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
            self.sender().setText("Play")
        else:
            self.mediaPlayer.play()
            self.sender().setText("Pause")

    def setPosition(self, position):
        # 미디어 플레이어 위치 설정
        thread = threading.Thread(target=self.setPositionThread, args=(position,))
        thread.start()

    def setPositionThread(self, position):
        # 미디어 플레이어 위치 설정 (새로운 스레드에서 실행)
        self.mediaPlayer.set_position(position / 100.0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())