This django application takes in a video file as input and outputs the emotion the characters are feeling throughout the clip.
Uses Google Vision API and Django and ffmpeg

In order to use this you must set up a google cloud project and enable the cloud vision api. You must also set up your environment for using default application credentials (do the first few steps of this: https://cloud.google.com/vision/docs/face-tutorial) and have the following python libraries installed.
PIL
PILDraw
Django
