#!/usr/bin/python
from gi.repository import Gtk, GObject
from mpd import MPDClient
import cgi

# http://helloraspberrypi.blogspot.de/2013/12/install-and-program-with-gtk-30-in.html
# https://oli4444.wordpress.com/2015/11/22/from-power-on-to-gtk-gui-usable-as-fast-as-possible/
# sudo aptitude install python-gi gir1.2-gtk-3.0 libgtk-3-dev python-mpd

class MyWindow(Gtk.Window):

    mpdHost = "192.168.23.111"
    mpdPort = 6600
    mpdPassword = ""

    def __init__(self):
        Gtk.Window.__init__(self, title="MPD Touch")
        self.set_border_width(3)

        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.LEFT)
        self.add(self.notebook)

        # Icon List
        # https://specifications.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html

        self.nowPlayingPage = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.nowPlayingPage.set_border_width(10)

        #track display
        self.nowPlayingTrackDisplay = Gtk.Box(spacing=6)

        # cover art
        self.nowPlayingCoverArt = Gtk.Image.new_from_icon_name(
                "weather-few-clouds",
                Gtk.IconSize.DIALOG
            )
        self.nowPlayingTrackDisplay.add(self.nowPlayingCoverArt)

        # track info
        self.nowPlayingTrackText = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.nowPlayingTrackTitle = Gtk.Label()
        self.nowPlayingTrackTitle.set_markup("<b>Title</b>")
        self.nowPlayingTrackTitle.set_justify(Gtk.Justification.CENTER)
        self.nowPlayingTrackTitle.set_line_wrap(True)
        self.nowPlayingTrackText.add(self.nowPlayingTrackTitle)

        self.nowPlayingTrackArtist = Gtk.Label("Artist")
        self.nowPlayingTrackArtist.set_justify(Gtk.Justification.CENTER)
        self.nowPlayingTrackArtist.set_line_wrap(True)
        self.nowPlayingTrackText.add(self.nowPlayingTrackArtist)

        self.nowPlayingTrackAlbum = Gtk.Label("Album")
        self.nowPlayingTrackAlbum.set_justify(Gtk.Justification.CENTER)
        self.nowPlayingTrackAlbum.set_line_wrap(True)
        self.nowPlayingTrackText.add(self.nowPlayingTrackAlbum)

        self.nowPlayingTrackDisplay.add(self.nowPlayingTrackText)

        # current time and progress
        self.nowPlayingPage.add(self.nowPlayingTrackDisplay)

        self.nowPlayingProgress = Gtk.Box(spacing=6)
        self.nowPlayingProgress.set_border_width(10)

        self.timeLabel = Gtk.Label("0:00")
        self.nowPlayingProgress.pack_start(self.timeLabel, True, True, 0)

        self.progressbar = Gtk.ProgressBar()
        self.nowPlayingProgress.pack_start(self.progressbar, True, True, 0)

        self.nowPlayingPage.add(self.nowPlayingProgress)

        # volume buttons
        self.nowPlayingVolume = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.volumeButtonUp = Gtk.Button()
        self.volumeButtonUp.add(
            Gtk.Image.new_from_icon_name(
                "audio-volume-high",
                Gtk.IconSize.BUTTON
            )
        )
        self.volumeButtonUp.connect("clicked", self.on_volumeButtonUp_clicked)
        self.nowPlayingVolume.pack_start(self.volumeButtonUp, True, True, 0)

        self.volumeButtonDown = Gtk.Button()
        self.volumeButtonDown.add(
            Gtk.Image.new_from_icon_name(
                "audio-volume-low",
                Gtk.IconSize.BUTTON
            )
        )
        self.volumeButtonDown.connect("clicked", self.on_volumeButtonDown_clicked)
        self.nowPlayingVolume.pack_start(self.volumeButtonDown, True, True, 0)

        self.volumeButtonMute = Gtk.Button()
        self.volumeButtonMute.add(
            Gtk.Image.new_from_icon_name(
                "audio-volume-muted",
                Gtk.IconSize.BUTTON
            )
        )
        self.volumeButtonMute.connect("clicked", self.on_volumeButtonMute_clicked)
        self.nowPlayingVolume.pack_start(self.volumeButtonMute, True, True, 0)

        self.nowPlayingTrackDisplay.add(self.nowPlayingVolume)

        # control buttons
        self.nowPlayingControls = Gtk.Box(spacing=6)
        self.controlButtonPrevious = Gtk.Button()
        self.controlButtonPrevious.add(
            Gtk.Image.new_from_icon_name(
                "media-skip-backward",
                Gtk.IconSize.BUTTON
            )
        )
        self.controlButtonPrevious.connect("clicked", self.on_controlButtonPrevious_clicked)
        self.nowPlayingControls.pack_start(self.controlButtonPrevious, True, True, 0)

        self.controlButtonPlayPause = Gtk.Button()
        self.controlButtonPlayPause.add(
            Gtk.Image.new_from_icon_name(
                "media-playback-start",
                Gtk.IconSize.BUTTON
            )
        )
        self.controlButtonPlayPause.connect("clicked", self.on_controlButtonPlayPause_clicked)
        self.nowPlayingControls.pack_start(self.controlButtonPlayPause, True, True, 0)

        self.controlButtonStop = Gtk.Button()
        self.controlButtonStop.add(
            Gtk.Image.new_from_icon_name(
                "media-playback-stop",
                Gtk.IconSize.BUTTON
            )
        )
        self.controlButtonStop.connect("clicked", self.on_controlButtonStop_clicked)
        self.nowPlayingControls.pack_start(self.controlButtonStop, True, True, 0)

        self.controlButtonNext = Gtk.Button()
        self.controlButtonNext.add(
            Gtk.Image.new_from_icon_name(
                "media-skip-forward",
                Gtk.IconSize.BUTTON
            )
        )
        self.controlButtonNext.connect("clicked", self.on_controlButtonNext_clicked)
        self.nowPlayingControls.pack_start(self.controlButtonNext, True, True, 0)

        self.controlButtonRepeat = Gtk.ToggleButton()
        self.controlButtonRepeat.add(
            Gtk.Image.new_from_icon_name(
                "media-playlist-repeat",
                Gtk.IconSize.BUTTON
            )
        )
        #self.controlButtonRepeat.connect("clicked", self.on_controlButtonRepeat_clicked)
        self.nowPlayingControls.pack_start(self.controlButtonRepeat, True, True, 0)

        self.controlButtonShuffle = Gtk.ToggleButton()
        self.controlButtonShuffle.add(
            Gtk.Image.new_from_icon_name(
                "media-playlist-shuffle",
                Gtk.IconSize.BUTTON
            )
        )
        #self.controlButtonShuffle.connect("clicked", self.on_controlButtonShuffle_clicked)
        self.nowPlayingControls.pack_start(self.controlButtonShuffle, True, True, 0)

        self.nowPlayingPage.add(self.nowPlayingControls)
        self.notebook.append_page(
            self.nowPlayingPage, 
            Gtk.Image.new_from_icon_name(
                "media-playback-start",
                Gtk.IconSize.BUTTON
            )
        )

        self.libraryPage = Gtk.Box()
        self.libraryPage.set_border_width(10)
        self.libraryPage.add(Gtk.Label('Not implemented yet.'))
        self.notebook.append_page(
            self.libraryPage,
            Gtk.Image.new_from_icon_name(
                "user-bookmarks",
                Gtk.IconSize.MENU
            )
        )

        self.playlistPage = Gtk.Box()
        self.playlistPage.set_border_width(10)
        self.playlistPage.add(Gtk.Label('Not implemented yet.'))
        self.notebook.append_page(
            self.playlistPage,
            Gtk.Image.new_from_icon_name(
                "user-bookmarks",
                Gtk.IconSize.MENU
            )
        )

        self.settingsPage = Gtk.Box()
        self.settingsPage.set_border_width(10)

        self.settingsScrollWindow = Gtk.ScrolledWindow()
        self.settingsScrollWindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.settingsListBox = Gtk.ListBox()
        self.settingsListBox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.settingsScrollWindow.add(self.settingsListBox)

        self.settingsPage.add(self.settingsScrollWindow)
        self.notebook.append_page(
            self.settingsPage,
            Gtk.Image.new_from_icon_name(
                "preferences-system",
                Gtk.IconSize.MENU
            )
        )

        self.client = MPDClient()
        self.client.timeout = 10               
        self.client.idletimeout = None         
        self.client.connect(self.mpdHost, self.mpdPort) 

        self.updateMpd()

        self.connect("delete-event", self.mainQuit)

        # update window regularly
        self.update = GObject.timeout_add(1000, self.updateMpd)

    def on_controlButtonPlayPause_clicked(self, b):
        self.client.play()
        self.updateMpd()

    def on_controlButtonStop_clicked(self, b):
        self.client.stop()
        self.updateMpd()

    def on_controlButtonPrevious_clicked(self, b):
        self.client.previous()
        self.updateMpd()

    def on_controlButtonNext_clicked(self, b):
        self.client.next()
        self.updateMpd()

    def on_volumeButtonUp_clicked(self, b):
        #self.client.
        status = self.client.status()
        vol = int(status["volume"]) + 1
        if vol > 100:
            vol = 100
        self.client.setvol(vol)

    def on_volumeButtonDown_clicked(self, b):
        #self.client.
        status = self.client.status()
        vol = int(status["volume"]) - 1
        if vol < 0:
            vol = 0
        self.client.setvol(vol)

    def on_volumeButtonMute_clicked(self, b):
        #self.client.
        print("x")

    def format_time(self, input):
        nums = input.split(':')
        seconds = int(nums[0])
        result = []
        hours = seconds / 3600
        seconds = seconds % 3600
        minutes = seconds / 60
        seconds = seconds % 60
        return "%(hours)02d:%(minutes)02d:%(seconds)02d" % {"hours":hours,"minutes":minutes,"seconds":seconds}

    def mainQuit(self, b, c):
        self.client.close()
        self.client.disconnect()
        Gtk.main_quit(self, b, c)

    def updateMpd(self):
        status = self.client.status()
        # {'songid': '1', 'playlistlength': '1', 'playlist': '132', 'repeat': '0', 'consume': '0', 
        # 'mixrampdb': '0.000000', 'random': '1', 'state': 'play', 'elapsed': '99.186', 'volume': '75', 
        # 'single': '0', 'time': '99:0', 'song': '0', 'audio': '44100:24:2', 'bitrate': '128'}

        if status['state'] == "play":
            self.controlButtonPlayPause.set_image(
                Gtk.Image.new_from_icon_name(
                    "media-playback-pause",
                    Gtk.IconSize.BUTTON
                )
            )
        else:
            self.controlButtonPlayPause.set_image(
                Gtk.Image.new_from_icon_name(
                    "media-playback-start",
                    Gtk.IconSize.BUTTON
                )
            )
        self.controlButtonRepeat.set_active(status['repeat'] == '1')
        self.controlButtonShuffle.set_active(status['random'] == '1')

        currentSong = self.client.currentsong()
        # {'id': '1', 'pos': '0', 'name': 'hr3', 
        # 'file': 'http://hr-mp3-m-h3.akacast.akamaistream.net/7/785/142133/v1/gnl.akacast.akamaistream.net/hr-mp3-m-h3', 
        # 'title': 'Bloodhound Gang - The bad touch'}
        try:
            self.timeLabel.set_markup(self.format_time(status["time"]))
        except KeyError:
            self.timeLabel.set_markup("00:00")
            pass
        self.nowPlayingTrackTitle.set_markup("<b>" + cgi.escape(currentSong["title"]) + "</b>")
        self.nowPlayingTrackArtist.set_markup(cgi.escape(currentSong["name"]))
        return True


win = MyWindow()
win.show_all()
Gtk.main()