# SpeechCapture
An easy to use library for recording and saving speech audio

<details open>
<summary>Contents</summary>
1. [About the Project](#about-the-project) <br>
2. [Features](#features) <br>
3. [Installation](#installation) <br>
4. [Usage](#usage) <br>
</details>

## About the Project
SpeechCapture is a library made to simplify the complex process of recording and saving your voice automatically from Python code.

## Features
 - Automatic stop on silence
 - Customizable silence threshold
	- Dynamically adjust threshold based on surrounding noise
 - Pausing and resuming recording
 - Saving recording at any time as .WAV
 - Recording in background threads
 - Simultaneous recordings
 - Stopping at any time

## Installation
To install, simply run in your terminal:
```
$ pip install speechcapture
```
Once you have installed the package, do not forget to import:
```py
import speechcapture
```
You can now start using SpeechCapture (example usage below)

 ## Usage
 ```py
import speechcapture as sc

file_path = 'output.wav'

r = sc.Recorder(file_path)

r.adjust_for_ambient_noise(adjustment_time=3)

r.max_seconds_of_silence = 5

r.record()
 ```

## License
This library is distributed under the MIT License