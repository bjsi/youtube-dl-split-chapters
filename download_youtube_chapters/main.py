#!/usr/bin/env python3

import os
import typing as T
from youtube_dl import YoutubeDL, options
from youtube_dl.postprocessor.common import PostProcessor
from download_youtube_chapters.opts import parse_opts
import subprocess
from youtube_dl.utils import sanitize_filename, sanitize_path


class ChapterProcessor(PostProcessor):

    _downloader = None
    file: "DownloadedFile"

    def __init__(self, downloader=None):
        super().__init__(downloader)

    @staticmethod
    def log(s: str):
        print("ChapterProcessor: " + s)

    def create_chapter(self, chapter) -> bool:
        start = chapter["start_time"]
        end = chapter["end_time"]
        diff = end - start
        args = [
            "ffmpeg",
            "-i", self.file.media_filepath,
            "-ss", str(start),
            "-t", str(diff),
            "-acodec", "copy",
            "-vcodec", "copy",
            self.file.output_chapter_file(chapter["title"])
            ]
        ret = subprocess.run(args)
        return ret.returncode == 0

    def split_into_chapters(self):
        if not self.file.chapters:
            self.log("No chapters available.")
            return False

        if not self.file.create_output_folder():
            self.log("Failed to create output folder.")
            return False

        for chapter in self.file.chapters:
            if not self.create_chapter(chapter):
                self.log("Failed to create chapter file: " + chapter["title"])
        return True

    def run(self, info):
        restricted = self._downloader.params.get("restrictfilenames", False)
        self.file = DownloadedFile(info, restricted)
        if self.split_into_chapters():
            return [info["filepath"]], info
        else:
            return [], info


class DownloadedFile:

    media_filepath: str
    fulltitle: str
    chapters: T.Optional[T.Dict]
    restricted = False

    def __init__(self, info: T.Dict, restricted: bool):
        self.chapters = info.get("chapters")
        self.media_filepath = info["filepath"]
        self.fulltitle = info["fulltitle"]
        self.restricted = restricted

    def output_chapter_file(self, chapter: str):
        basename = chapter + self.extension
        return os.path.join(self.output_folder, sanitize_filename(basename, self.restricted))

    @property
    def extension(self):
        return os.path.splitext(self.media_filepath)[1]

    @property
    def filename(self):
        return os.path.basename(self.media_filepath)

    @property
    def basedir(self):
        return os.path.dirname(self.media_filepath)

    @property
    def output_folder(self):
        return sanitize_path(os.path.join(self.basedir, sanitize_filename(self.fulltitle, self.restricted)))

    def create_output_folder(self):
        try:
            if not os.path.isdir(self.output_folder):
                print("Creating output folder: " + self.output_folder)
                os.mkdir(self.output_folder)
            return True
        except:
            return False


def parse_urls():
    return options.parseOpts()[2]


def download(opts: T.Dict, urls: T.List[str]):
    with YoutubeDL(opts) as ydl:
        ydl.add_post_processor(ChapterProcessor(ydl))
        ydl.download(urls)


def main():
    opts = parse_opts()
    urls = parse_urls()
    download(opts, urls)


if __name__ == "__main__":
    main()
