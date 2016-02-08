#!/usr/bin/python
from gi.repository import Gtk

# http://helloraspberrypi.blogspot.de/2013/12/install-and-program-with-gtk-30-in.html
# https://oli4444.wordpress.com/2015/11/22/from-power-on-to-gtk-gui-usable-as-fast-as-possible/
# sudo aptitude install python-gi gir1.2-gtk-3.0 libgtk-3-dev

class MyWindow(Gtk.Window):

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
        self.nowPlayingTrackText.add(self.nowPlayingTrackTitle)

        self.nowPlayingTrackArtist = Gtk.Label("Artist")
        self.nowPlayingTrackArtist.set_justify(Gtk.Justification.CENTER)
        self.nowPlayingTrackText.add(self.nowPlayingTrackArtist)

        self.nowPlayingTrackAlbum = Gtk.Label("Album")
        self.nowPlayingTrackAlbum.set_justify(Gtk.Justification.CENTER)
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

        # control buttons

        self.nowPlayingControls = Gtk.Box(spacing=6)
        self.controlButtonPrevious = Gtk.Button()
        self.controlButtonPrevious.add(
        	Gtk.Image.new_from_icon_name(
                "media-skip-backward",
                Gtk.IconSize.BUTTON
            )
        )
        #self.controlButtonPrevious.connect("clicked", self.on_controlButtonPrevious_clicked)
        self.nowPlayingControls.pack_start(self.controlButtonPrevious, True, True, 0)

        self.controlButtonPlayPause = Gtk.Button()
        self.controlButtonPlayPause.add(
        	Gtk.Image.new_from_icon_name(
                "media-playback-start",
                Gtk.IconSize.BUTTON
            )
        )
        #self.controlButtonPlayPause.connect("clicked", self.on_controlButtonPlayPause_clicked)
        self.nowPlayingControls.pack_start(self.controlButtonPlayPause, True, True, 0)

        self.controlButtonStop = Gtk.Button()
        self.controlButtonStop.add(
        	Gtk.Image.new_from_icon_name(
                "media-playback-stop",
                Gtk.IconSize.BUTTON
            )
        )
        #self.controlButtonStop.connect("clicked", self.on_controlButtonStop_clicked)
        self.nowPlayingControls.pack_start(self.controlButtonStop, True, True, 0)

        self.controlButtonNext = Gtk.Button()
        self.controlButtonNext.add(
        	Gtk.Image.new_from_icon_name(
                "media-skip-forward",
                Gtk.IconSize.BUTTON
            )
        )
        #self.controlButtonNext.connect("clicked", self.on_controlButtonNext_clicked)
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

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()