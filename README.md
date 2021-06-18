# youtube-dl split by chapters

Adds a chapter splitting postprocessor to `youtube-dl` to allow you to chop videos and audio into chapters.

Example:

`./main.py -x -f "bestaudio/best" <URL>`

The output will be a directory containing each chapter as a separate audio file.

Note: You can use the same options and arguments as the normal `youtube-dl`. Works with audio and video from youtube.
