import os
import platform
import sys
from pathlib import Path

import wx

import yt_dl

IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

if IS_WINDOWS:
    YOUTUBEDL_MAIN = "youtube_dl\\__main__.exe -v "
elif IS_LINUX:
    YOUTUBEDL_MAIN = "youtube_dl/__main__.py -v "
else:
    sys.exit("Error: Unknow Platform")

HOME = Path().home() / Path("Videos")

if not HOME.exists():
    os.makedirs(HOME)


def run_youtube_dl(args: str) -> None:
    """Run youtube-dl commands on platform"""
    # TODO: Change for subprocess module
    os.system(YOUTUBEDL_MAIN + args)
    # Logs (can use logging module)
    # print(YOUTUBEDL_MAIN + args)


class CalcFrame(yt_dl.MyFrame):
    def __init__(self, parent):
        yt_dl.MyFrame.__init__(self, parent)
        text_ctr: wx.TextCtrl = self.m_dirPicker1.GetTextCtrl()
        text_ctr.AppendText(str(HOME))
        self.m_checkBox2.Hide()

    @staticmethod
    def convert2seconds(raw_time: str) -> int:
        """Convert raw text in format 00:00 to seconds"""
        minutes, seconds = raw_time.split(":", maxsplit=1)
        return int(minutes) * 60 + int(seconds)

    def video_dl(self, event):
        link: str = self.link_box.GetValue()
        directory: str = self.m_dirPicker1.GetPath()
        args: str = self.m_custom_args.GetValue()

        # Audio/Quality/Video
        # TODO: Refactor by Video Quality
        if self.m_checkBox1.GetValue() == 1:
            cmd_args = (
                "-x --audio-format mp3 --audio-quality 2 "
                + link
                + ' -o "'
                + directory
                + '/%(title)s-%(id)s.%(ext)s" '
                + args
            )
        elif self.quality_selection_drop_down.GetSelection() == 5:
            cmd_args = (
                "-f bestvideo[width=640]+bestaudio "
                + link
                + ' -o "'
                + directory
                + '/%(title)s-%(id)s-360p.%(ext)s" '
                + args
            )
        elif self.quality_selection_drop_down.GetSelection() == 4:
            cmd_args = (
                "-f bestvideo[width=854]+bestaudio "
                + link
                + ' -o "'
                + directory
                + '/%(title)s-%(id)s-480p.%(ext)s" '
                + args
            )
        elif self.quality_selection_drop_down.GetSelection() == 3:
            cmd_args = (
                "-f bestvideo[width=1280]+bestaudio "
                + link
                + ' -o "'
                + directory
                + '/%(title)s-%(id)s-720p.%(ext)s" '
                + args
            )
        elif self.quality_selection_drop_down.GetSelection() == 2:
            cmd_args = (
                "-f bestvideo[width=1920]+bestaudio "
                + link
                + ' -o "'
                + directory
                + '/%(title)s-%(id)s-1080p.%(ext)s" '
                + args
            )
        elif self.quality_selection_drop_down.GetSelection() == 1:
            cmd_args = (
                "-f bestvideo[width=2560]+bestaudio "
                + link
                + ' -o "'
                + directory
                + '/%(title)s-%(id)s-1440p.%(ext)s" '
                + args
            )
        elif self.quality_selection_drop_down.GetSelection() == 0:
            cmd_args = (
                "-f bestvideo[width=3840]+bestaudio "
                + link
                + ' -o "'
                + directory
                + '/%(title)s-%(id)s-4k.%(ext)s" '
                + args
            )
        else:
            cmd_args = link + ' -o "' + directory + '/%(title)s-%(id)s.%(ext)s" ' + args

        run_youtube_dl(cmd_args)

    def clip_dl(self, event):
        link: str = self.link_box.GetValue()
        directory: str = self.m_dirPicker1.GetPath()
        args: str = self.m_custom_args.GetValue()
        startTimeRaw: str = self.clip_start_box.GetValue()
        endTimeRaw: str = self.clip_end_box.GetValue()

        # converts for starttime
        startTime = self.convert2seconds(startTimeRaw)
        # conversion for endtime
        endTime = self.convert2seconds(endTimeRaw)
        # run command to download clip
        cmd_args = (
            link
            + ' --external-downloader ffmpeg --external-downloader-args "-ss '
            + str(startTime)
            + " -to "
            + str(endTime)
            + '" -o "'
            + directory
            + '/%(title)s-%(id)s.%(ext)s" '
            + args
        )
        run_youtube_dl(cmd_args)

    def clip_mp3_dl(self, event):

        link = self.link_box.GetValue()
        directory = self.m_dirPicker1.GetPath()
        args = self.m_custom_args.GetValue()
        startTimeRaw = self.clip_start_box.GetValue()
        endTimeRaw = self.clip_end_box.GetValue()

        # converts for starttime
        startTime = self.convert2seconds(startTimeRaw)
        # conversion for endtime
        endTime = self.convert2seconds(endTimeRaw)

        # run command to download clip
        cmd_args = (
            "-f bestaudio "
            + link
            + ' --external-downloader ffmpeg --external-downloader-args "-ss '
            + str(startTime)
            + " -to "
            + str(endTime)
            + '" -o "'
            + directory
            + '/%(title)s-%(id)s.%(ext)s" '
            + args
        )
        run_youtube_dl(cmd_args)


app = wx.App(False)
frame = CalcFrame(None)
frame.Show(True)
# start the applications
app.MainLoop()
