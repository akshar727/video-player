unzip -q /opt/video-player-main/frames_raw.zip -d /opt/video-player-main/
rm /opt/video-player-main/frames_raw.zip
(cd /opt/video-player-main/Driver && sudo sh /opt/video-player-main/Driver/install_wm8960_drive.sh)
sudo systemctl daemon-reload
sudo systemctl enable autoplay.service
sudo reboot