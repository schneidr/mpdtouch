# README #

MPDTouch is an MPD client, intended for touch screens, written in Python and using GTK+3.

The client is intended to run on a Raspberry Pi.

## Status ##

### Working ###

* basic UI
* communication with MPD
* display of play status
* basic control (play, stop, prev, next)
* status updates

### TODO ###

* advanced control (pause, repeat, shuffle)
* configurable settings

## Dependencies ##

The following packages are needed on Raspbian:

    sudo aptitude install python-gi gir1.2-gtk-3.0 libgtk-3-dev python-mpd