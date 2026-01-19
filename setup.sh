#!/bin/bash

RPI="${1:-akssh@raspberrypi.local}"

echo "Using remote Pi: $RPI"

echo "Making folders..."
mkdir -p frames
mkdir -p frames_raw

echo "Moving over autoplay service..."
ssh "$RPI" "sudo chmod 777 /etc/systemd/system/"
scp autoplay.service "$RPI:/etc/systemd/system/autoplay.service"
echo "Converting video..."
ffmpeg -i input.mp4 -map 0:v -vf "transpose=1,scale=240:280" frames/frame_%04d.png -map 0:a -c:a pcm_s16le vid.wav

python3 preconvert_frames.py

rm -rf frames

zip -rq frames_raw.zip frames_raw
rm -rf frames_raw
ssh "$RPI" "sudo mkdir -p /opt/video-player-main; sudo chmod 777 /opt/video-player-main;"

scp -r Driver video_player.py frames_raw.zip rpi_setup.sh vid.wav "$RPI:/opt/video-player-main/"

ssh "$RPI" "sudo sh /opt/video-player-main/rpi_setup.sh"

echo "Setup complete!"
