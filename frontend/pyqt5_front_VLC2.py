import sys
import threading
import vlc
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QSlider, QVBoxLayout, QWidget, QFrame


class Player(QFrame):
    def __init__(self, *args):
        super().__init__(*args)
        self.vlc_instance = vlc.Instance()
        self.vlc_player = self.vlc_instance.media_player_new()
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.vlc_player.set_xwindow(self.winId())
        elif sys.platform == "win32": # for Windows
            self.vlc_player.set_hwnd(self.winId())

        self.setMinimumSize(640, 930)

    def play(self, media):
        self.vlc_player.set_media(media)
        self.vlc_player.play()
        self.vlc_player.video_set_scale(0)  # 비디오 출력 비율 조정. 0일시 자동 조정

    # def resizeEvent(self, event):
    #     # VLC 미디어 플레이어의 비디오 출력 크기 조정
    #     # 이 메소드는 QFrame 인스턴스의 크기가 변경될 때마다 호출됨
    #     self.vlc_player.video_resize(event.size().width(), event.size().height())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 중앙 위젯 생성
        centralWidget = QWidget()
        centralLayout = QVBoxLayout()
        centralWidget.setLayout(centralLayout)
        self.setCentralWidget(centralWidget)

        # 미디어 플레이어 생성
        self.mediaPlayer = Player()
        
        # 미디어 플레이어 추가
        centralLayout.addWidget(self.mediaPlayer)
        centralLayout.setStretchFactor(self.mediaPlayer, 1)

        # 컨트롤 바 생성
        controlWidget = QWidget()
        controlLayout = QHBoxLayout()
        controlWidget.setLayout(controlLayout)
        centralLayout.addStretch(1)
        centralLayout.addWidget(controlWidget)

        # 감속 버튼 생성
        slowDownButton = QPushButton("Slow Down")
        slowDownButton.clicked.connect(self.slowDownButtonClicked)
        controlLayout.addWidget(slowDownButton)
        
        # 재생/일시정지 버튼 생성
        playButton = QPushButton("Play")
        playButton.setStyleSheet("color: white; background-color: blue")
        playButton.clicked.connect(self.playButtonClicked)
        controlLayout.addWidget(playButton)

        # 배속 버튼 생성
        speedUpButton = QPushButton("Speed Up")
        speedUpButton.clicked.connect(self.speedUpButtonClicked)
        controlLayout.addWidget(speedUpButton)

        # 현재 시간 레이블 생성
        self.currentTimeLabel = QLabel("0:00")
        controlLayout.addWidget(self.currentTimeLabel)

        # 슬라이더 생성
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 100)
        self.positionSlider.setValue(0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        controlLayout.addWidget(self.positionSlider)

        # 최대 시간 레이블 생성
        self.maxTimeLabel = QLabel("0:00")
        controlLayout.addWidget(self.maxTimeLabel)

        # 타이머 생성 및 시작
        # 타이머는 1초마다 updateUI 메소드를 호출합니다.
        timer = QTimer(self)
        timer.timeout.connect(self.updateUI)
        timer.start(1000)

        # m3u8 미디어 재생 목록 파일 지정
        media = vlc.Media("C:/Users/ZZY/Desktop/0_cityeyelab/code/firebase_exp/backend/hls/playlist.m3u8")
        
        # 비디오 재생
        self.mediaPlayer.play(media)

    def slowDownButtonClicked(self):
        # 미디어 플레이어의 재생 속도 감소
        rate = max(0.1, self.mediaPlayer.vlc_player.get_rate() / 2)
        self.mediaPlayer.vlc_player.set_rate(rate)

    def speedUpButtonClicked(self):
        # 미디어 플레이어의 재생 속도 증가
        rate = min(10.0, self.mediaPlayer.vlc_player.get_rate() * 2)
        self.mediaPlayer.vlc_player.set_rate(rate)

    def playButtonClicked(self):
        # 미디어 플레이어 상태에 따라 재생/일시정지 전환
        if self.mediaPlayer.vlc_player.is_playing():
            self.mediaPlayer.vlc_player.pause()
            self.sender().setText("Play")
        else:
            if self.mediaPlayer.vlc_player.get_time() == -1:
                self.mediaPlayer.vlc_player.stop()
            self.mediaPlayer.vlc_player.play()
            self.sender().setText("Pause")

    def setPosition(self, position):
        # 미디어 플레이어 위치 설정
        thread = threading.Thread(target=self.setPositionThread, args=(position,))
        thread.start()

    def setPositionThread(self, position):
        # 미디어 플레이어 위치 설정 (새로운 스레드에서 실행)
        # self.mediaPlayer.vlc_player.set_position(position / 100.0)
        mediaLength = self.mediaPlayer.vlc_player.get_length()
        print(mediaLength)
        if mediaLength > 0:
            self.mediaPlayer.vlc_player.set_time(int(position / 100.0 * mediaLength))        

    def updateUI(self):
        # 미디어 플레이어의 길이와 현재 재생 위치를 가져옵니다.
        mediaLength = self.mediaPlayer.vlc_player.get_length() / 1000
        mediaTime = self.mediaPlayer.vlc_player.get_time() / 1000

        # 최대 시간 레이블 업데이트
        self.maxTimeLabel.setText("{0}:{1:02d}".format(int(mediaLength / 60), int(mediaLength % 60)))

        # 현재 시간 레이블 업데이트
        self.currentTimeLabel.setText("{0}:{1:02d}".format(int(mediaTime / 60), int(mediaTime % 60)))

        # 슬라이더 업데이트
        # if mediaLength > 0:
        #     self.positionSlider.setValue(int(mediaTime / mediaLength * 100))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
