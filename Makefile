install:
	python3 -m venv .venv
	mkdir -p frames
	.venv/bin/pip install Pillow numpy
	ffmpeg -i input.mp4 -vf "scale=240:280" frames/frame_%04d.png

run:
	.venv/bin/python video_5.py