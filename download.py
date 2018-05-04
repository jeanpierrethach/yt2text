import os
import youtube_dl
import argparse

from utils import maybe_make_directory

MBPS = 8e-06

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', 
                        required=True,
                        type=str,
                        nargs='+',
                        help='Youtube video url.')
    parser.add_argument('--video_dir', type=str,
                        default='./audio_output',
                        help='Relative or absolute directory path to videos audio output.') 
    
    args = parser.parse_args()

    maybe_make_directory(args.video_dir)
    return args

class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def hook(d):
    if d['status'] == 'downloading':
        print("Downloading: at {0:.2f} Mbps".format(d['speed'] * MBPS), d['_percent_str'], "ETA:", d['_eta_str'])
    if d['status'] == 'finished':
        print("Finished downloading {}\n".format(os.path.basename(d['filename'])))

class Downloader(object):
    def _get_opts(self, dir):
        ydl_opts = {
            'format': "bestaudio/best", 
            'outtmpl': os.path.join(dir, "%(id)s.%(ext)s"),
            'logger': Logger(),
            'progress_hooks': [hook],
        }
        return ydl_opts

    def download(self, args):
        with youtube_dl.YoutubeDL(self._get_opts(args.video_dir)) as ydl:
            ydl.download(args.url)

if __name__ == '__main__':
    args = parse_args()
    d = Downloader()
    d.download(args)