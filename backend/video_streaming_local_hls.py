import ffmpeg_streaming
from ffmpeg_streaming import Formats
from pathlib import Path

VIDEO_PATH = "C:/Users/ZZY/Desktop/0_cityeyelab/data/analysis_video/건기연_C지점_주간/2023-02-16 13_02_00.000.mp4"
HLS_ROOT = "hls"
HLS_NAME = "playlist"

hls_path = str(Path(HLS_ROOT) / HLS_NAME)
if not Path(VIDEO_PATH).exists():
    raise FileNotFoundError(VIDEO_PATH)

# 비디오 파일의 경로 지정
video = ffmpeg_streaming.input(VIDEO_PATH)

# HLS 포맷으로 스트리밍 설정
hls = video.hls(Formats.h264())

# 스트리밍 옵션 설정
hls.auto_generate_representations()

# 스트리밍 시작
hls.output(hls_path)