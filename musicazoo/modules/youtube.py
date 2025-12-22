import os
import socket
import tempfile
import threading
import queue as Queue

import yt_dlp
import musicazoo.lib.vlc as vlc
from shmooze.modules import JSONParentPoller

messages = Queue.Queue()

class YoutubeModule(JSONParentPoller):
    def __init__(self, headless=False):
        self.headless = headless
        self.update_lock = threading.Lock()
        self.thread_stopped = False
        self.downloaded_file = None
        super(YoutubeModule, self).__init__()

    def serialize(self):
        result = {t: getattr(self, t) for t in [
            "url", "title", "duration", "thumbnail", "description", "vid"
        ]}

        state = "initialized"
        if self.state_is_stopping:
            state = "stopping"
        elif self.state_has_started:
            if self.state_is_suspended:
                state = "suspended"
            elif self.state_is_paused:
                state = "paused"
            else:
                state = "playing"
        elif self.state_is_ready:
            state = "ready"

        result["status"] = state
        return result

    @property
    def state_is_playing(self):
        return self.state_has_started and not (self.state_is_suspended or self.state_is_paused)

    def cmd_init(self, url):
        # Initialize state flags
        self.state_is_ready = False
        self.state_has_started = False
        self.state_is_paused = False
        self.state_is_suspended = False
        self.state_is_stopping = False

        # Initialize video properties
        self.url = url
        self.title = None
        self.duration = None
        self.thumbnail = None
        self.description = None
        self.time = None
        self.vid = None

        messages.put("init")
        self.safe_update()

    def hide(self):
        self.vlc_mp.video_set_track(-1)

    def show(self):
        self.vlc_mp.video_set_track(0)

    def cmd_play(self):
        if self.state_has_started:
            if not self.state_is_paused:
                self.vlc_mp.play()
                self.show()
                self.state_is_paused = False
        else:
            messages.put("play")
        self.state_is_suspended = False
        self.safe_update()

    def cmd_suspend(self):
        if self.state_has_started:
            if self.vlc_mp.is_playing():
                self.vlc_mp.pause()
                self.hide()
        self.state_is_suspended = True
        self.safe_update()

    def cmd_resume(self):
        if self.state_has_started:
            self.vlc_mp.play()
            self.state_is_paused = False
            self.safe_update()

    def cmd_pause(self):
        if self.state_has_started:
            if self.vlc_mp.is_playing():
                self.vlc_mp.pause()
            self.state_is_paused = True
            self.safe_update()

    def cmd_rm(self):
        self.state_is_stopping = True
        messages.put("rm")

    def cmd_seek_abs(self, position):
        if self.state_has_started:
            self.vlc_mp.set_time(int(position * 1000))
            self.time = position
            self.safe_update()

    def cmd_seek_rel(self, delta):
        if self.state_has_started:
            cur_time = self.vlc_mp.get_time()
            if cur_time < 0:
                return
            self.vlc_mp.set_time(cur_time + int(delta * 1000))
            self.time = (cur_time / 1000) + delta
            self.safe_update()

    def stop(self):
        self.vlc_mp.stop()
        self.thread_stopped = True

        # Clean up downloaded file
        if self.downloaded_file and os.path.exists(self.downloaded_file):
            try:
                os.remove(self.downloaded_file)
            except Exception as e:
                print(f"Error removing downloaded file: {e}")

        with self.update_lock:
            self.rm()

    def play(self):
        def ev_end(ev):
            messages.put("rm")

        def ev_time(ev):
            self.time = ev.u.new_time / 1000.
            self.safe_update()

        def ev_length(ev):
            self.duration = ev.u.new_length / 1000.
            self.safe_update()

        # Create VLC instance
        if not self.headless:
            self.vlc_i = vlc.Instance(['--no-video-title-show'])
        else:
            self.vlc_i = vlc.Instance(['--novideo'])

        self.vlc_mp = self.vlc_i.media_player_new()
        # Set volume to maximum
        self.vlc_mp.audio_set_volume(100)
        self.vlc_ev = self.vlc_mp.event_manager()

        # Attach event handlers
        self.vlc_ev.event_attach(vlc.EventType.MediaPlayerEndReached, ev_end)
        self.vlc_ev.event_attach(vlc.EventType.MediaPlayerTimeChanged, ev_time)
        self.vlc_ev.event_attach(vlc.EventType.MediaPlayerLengthChanged, ev_length)

        # Play the downloaded file
        vlc_media = self.vlc_i.media_new_path(self.downloaded_file)
        self.vlc_mp.set_media(vlc_media)
        self.vlc_mp.play()

        self.state_has_started = True
        self.safe_update()

    def download_video(self):
        """Download the video using yt-dlp and extract metadata."""
        # Create temporary file for download
        temp_dir = tempfile.gettempdir()
        output_template = os.path.join(temp_dir, 'musicazoo_%(id)s.%(ext)s')

        # Configure yt-dlp options
        ydl_opts = {
            'format': 'best',  # Download best quality
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info and download
                info = ydl.extract_info(self.url, download=True)

                # Handle playlists - take first entry
                if 'entries' in info:
                    vinfo = info['entries'][0]
                else:
                    vinfo = info

                # Extract metadata
                self.title = vinfo.get('title', 'Unknown')
                self.duration = vinfo.get('duration', 0)
                self.thumbnail = vinfo.get('thumbnail')
                self.description = vinfo.get('description')
                self.vid = vinfo.get('id')

                # Get the downloaded file path
                self.downloaded_file = ydl.prepare_filename(vinfo)

                print(f"Downloaded: {self.downloaded_file}")

        except Exception as e:
            print(f"Error downloading video: {e}")
            raise

        self.state_is_ready = True
        self.safe_update()
        return True

    def safe_update(self):
        """Thread-safe parameter update."""
        with self.update_lock:
            self.set_parameters(self.serialize())

    commands = {
        'init': cmd_init,
        'play': cmd_play,
        'suspend': cmd_suspend,
        'rm': cmd_rm,
        'do_pause': cmd_pause,
        'do_resume': cmd_resume,
        'do_seek_rel': cmd_seek_rel,
        'do_seek_abs': cmd_seek_abs,
    }


# Main execution
import sys

headless = '--headless' in sys.argv
mod = YoutubeModule(headless=headless)

def serve_forever():
    """Handle incoming commands from the queue."""
    while not mod.thread_stopped:
        try:
            mod.handle_one_command()
        except socket.error:
            break

# Start command handler thread
t = threading.Thread(target=serve_forever)
t.daemon = True
t.start()

# Main message loop
while True:
    msg = messages.get(block=True)
    messages.task_done()
    if msg == "init":
        mod.download_video()
    elif msg == "play":
        mod.play()
    elif msg == "rm":
        mod.stop()
        break

mod.close()
