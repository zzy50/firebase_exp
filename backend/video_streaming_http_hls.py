import ffmpeg
from pathlib import Path

VIDEO_PATH = "C:/Users/ZZY/Desktop/0_cityeyelab/data/analysis_video/건기연_C지점_주간/2023-02-16 13_02_00.000.mp4"
HLS_ROOT = "hls_http"
HLS_NAME = "playlist.m3u8"

hls_path = str(Path(HLS_ROOT) / HLS_NAME)
if not Path(VIDEO_PATH).exists():
    raise FileNotFoundError(VIDEO_PATH)


input_stream = ffmpeg.input(VIDEO_PATH)
output_stream = ffmpeg.output(input_stream, hls_path, format='hls', hls_flags='omit_endlist+append_list', hls_list_size=1, hls_time=10)
try:
    ffmpeg.run(output_stream)
except ffmpeg.Error as e:
    print('stdout:', e.stdout.decode('utf8'))
    print('stderr:', e.stderr.decode('utf8'))
    raise e
