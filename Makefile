install:
	mkdir -p frames
	ffmpeg -i input.mp4 -vf "scale=240:280" frames/frame_%04d.png

run:
	sudo python3 video_5.py