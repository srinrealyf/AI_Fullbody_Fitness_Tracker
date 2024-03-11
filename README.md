# OpenCV Exercise Tracker

This project consists of two programs that use computer vision to track and count repetitions of two exercises: push-ups and sit-ups. The tracking is based on the detection of key landmarks using the MediaPipe Pose library.

## Requirements

Make sure you have the following dependencies installed:

- Python 3.x
- OpenCV
- Mediapipe

You can install the required Python packages using the following command:

```bash
pip install -r requirements.txt 
```

## Usage

### 1. Push-Ups Tracker
Run the push-ups tracker program using the following command:

```bash
python pushups_tracker.py
```
The program will use your webcam to detect your body movements and count push-ups.

### 2. Sit-Ups Tracker
Run the sit-ups tracker program using the following command:

```bash
python situps_tracker.py
```
The program will use your webcam to detect your body movements and count sit-ups.

## Streamlit App

To use the Streamlit app for easy exercise tracking, follow these steps:

### 1. Install Streamlit:

```bash
pip install streamlit
```
### 2. Run the Streamlit app:

```bash
streamlit run main.py
```
The app will prompt you to select an exercise (Push-Ups or Sit-Ups) and start tracking.

## Note

* Ensure that your webcam is connected and properly functioning.
* If you encounter issues, check the console or terminal for error messages.
* Adjust the exercise detection thresholds in the tracking scripts based on your preferences.

For MacOS users:

I have faced the following issue:
1. WARNING: AVCaptureDeviceTypeExternal is deprecated for Continuity Cameras. Please use AVCaptureDeviceTypeContinuityCamera and add NSCameraUseContinuityCameraDeviceType to your         Info.plist.

   This error is happening for MacOS Sonoma due to a version change, I simply changed the VideoCapture(0) to VideoCapture(1) and now it's working fine. While this is a temporary fix,     I'll post the permanent fix once I find it.

2. ValidatedGraphConfig Initialization Failed - The number of output streams should match the number of ranges specified in the CalculatorOptions.

   Downgrading mediapipe version from 0.10.11 to 0.10.9 fixed the issue for me.
   

   



