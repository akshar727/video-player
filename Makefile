install:
	python3 -m venv .venv
	source .venv/bin/activate
	mkdir frames
	pip install Pillow numpy
	ffmpeg -i input.mp4 -vf "scale=240:280" frames/frame_%04d.png

run:
	./venv/bin/python test.py