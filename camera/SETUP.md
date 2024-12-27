To use libcamera which is available at system-wide level
So create and invoke the virtual environment

```
python -m venv --system-site-packages myenv
```

Dependencies to install:
```
sudo apt install libcamera-dev python3-libcamera python3-libcamera python3-kms++ python3-pyqt5 python3-pyqt5.qtquick python3-opengl python3-libcamera python3-kms++ python3-pyqt5 python3-pyqt5.qtquick python3-opengl python3-picamera2 ffmpeg libavcodec-dev libavformat-dev libavdevice-dev libavutil-dev libswscale-dev libswresample-dev libavfilter-dev libjpeg-dev zlib1g-dev libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libavfilter-dev libswresample-dev python3-opencv libcap-dev build-essential python3-dev
```

Install Picamera2:
```
pip install picamera2
```
