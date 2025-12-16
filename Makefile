.PHONY: install run run_on_startup
install:
	mkdir -p frames
	ffmpeg -i input.mp4 -vf "transpose=1,scale=240:280" frames/frame_%04d.png

run:
	sudo python3 video_5.py

run_on_startup:
	sudo chmod +x /etc/rc.local
	echo '#!/bin/bash\n(\n  cd /home/tdesai/Desktop/video-player-main\n  sudo python /home/tdesai/Desktop/video-player-main/video_5.py &\n)\nexit 0' | sudo tee /etc/rc.local