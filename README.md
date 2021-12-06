# download-youtube-chapters

This tool is a fork of the great [youtube-dl-split-chapters](https://github.com/bjsi/youtube-dl-split-chapters) script.

The main goal is to provide an easy poetry package with an easy interface for downloading chapters of a youtube video.

Example for downloading mp3 subchapters as files:

```bash
poetry run download-youtube-chapters -x -f "bestaudio/best" --keep-fragments --audio-format mp3 https://www.youtube.com/watch?v=imtPF2b2Q4M
```

Note: You can use the same options and arguments as the normal `youtube-dl`. Works with audio and video from youtube.

Requirements: python, youtube-dl and ffmpeg
