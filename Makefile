.PHONY: install run setup
install:
	sudo chmod +x /etc/rc.local
	echo '#!/bin/bash\n(\n  cd /opt/video-player-main\n  source .venv/bin/activate\n  sudo .venv/bin/python video_5.py &\n)\nexit 0' | sudo tee /etc/rc.local
	mkdir -p frames
	ffmpeg -i input.mp4 -vf "transpose=2,scale=240:280" frames/frame_%04d.png

run:
	sudo /opt/video-player-main/.venv/bin/python video_5.py