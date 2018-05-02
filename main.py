"""
A simple Discord Rich Presence client that connects to MPRIS and shows your current song.
"""

import sys
import time
import pypresence
import gi
gi.require_version('Playerctl', '1.0')

from gi.repository import Playerctl, GLib

player = Playerctl.Player()
while player.get_property('status') == "":
    print("Waiting for player...")
    time.sleep(5)

print("Starting RPC client...")
RPC = pypresence.Presence('440997014315204609')
RPC.connect()
print("RPC client connected")

def getSong():
    return "%s - %s" % (player.get_title(), player.get_artist())

def update():
    print("Updating")
    status = player.get_property('status')

    if status == "":
        RPC.clear()
    elif status == "Playing":
        song = getSong()
        RPC.update(state='Playing', details=song, large_image='music', large_text=song, small_image='play')
    elif status == "Paused":
        RPC.update(state='Paused', large_image='music', small_image='pause')

def on_play(player):
    update()

def on_pause(player):
    update()

def on_metadata(player, e):
    update()

player.on('play', on_play)
player.on('pause', on_pause)
player.on('metadata', on_metadata)

update()

GLib.MainLoop().run()
