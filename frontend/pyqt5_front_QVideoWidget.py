import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QSlider, QVBoxLayout, QWidget, QStatusBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 비디오 위젯 생성
        self.videoWidget = QVideoWidget()
        self.setCentralWidget(self.videoWidget)

        # 미디어 플레이어 생성
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.error.connect(self.handleError)
        self.mediaPlayer.mediaStatusChanged.connect(self.handleMediaStatusChanged)

        # m3u8 재생 목록 파일 지정
        url = QUrl("C:/Users/ZZY/Desktop/0_cityeyelab/code/firebase_exp/backend/hls/playlist_1080p.m3u8")
        self.mediaPlayer.setMedia(QMediaContent(url))

        # 비디오 재생
        self.mediaPlayer.play()

        # 컨트롤 바 생성
        self.createControls()
        print(QMediaPlayer.supportedMimeTypes())

    def createControls(self):
        # 컨트롤 위젯 생성
        controlWidget = QWidget()
        controlLayout = QHBoxLayout()
        controlWidget.setLayout(controlLayout)

        # 재생/일시정지 버튼 생성
        playButton = QPushButton("Play")
        playButton.clicked.connect(self.playButtonClicked)
        controlLayout.addWidget(playButton)

        # 슬라이더 생성
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        controlLayout.addWidget(self.positionSlider)

        # 미디어 플레이어 시그널 연결
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)

        # 컨트롤 위젯을 상태 표시줄에 추가
        statusBar = QStatusBar()
        statusBar.addWidget(controlWidget)
        self.setStatusBar(statusBar)

    def playButtonClicked(self):
        # 미디어 플레이어 상태에 따라 재생/일시정지 전환
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def durationChanged(self, duration):
        # 슬라이더 범위 설정
        self.positionSlider.setRange(0, duration)
        print(f"Duration changed: {duration}")

    def positionChanged(self, position):
        # 슬라이더 위치 설정
        self.positionSlider.setValue(position)

    def setPosition(self, position):
        # 미디어 플레이어 위치 설정
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        print(f"Error: {self.mediaPlayer.errorString()}")

    def handleMediaStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            print("End of media")
        elif status == QMediaPlayer.InvalidMedia:
            print("Invalid media")
        elif status == QMediaPlayer.NoMedia:
            print("No media")
        elif status == QMediaPlayer.BufferedMedia:
            print(f"Duration: {self.mediaPlayer.duration()}")
        elif status == QMediaPlayer.LoadingMedia:
            print("Loading media")
        elif status == QMediaPlayer.StalledMedia:
            print("Stalled media")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
