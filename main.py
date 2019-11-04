"""
A simple Discord Rich Presence client that connects to MPRIS and shows your current song.
"""

import sys
import time
import pypresence
import gi
gi.require_version('Playerctl', '2.0')

from gi.repository import Playerctl, GLib

manager = Playerctl.PlayerManager()

print("Starting RPC client...")
RPC = pypresence.Presence('440997014315204609')

def connect_rpc():
    while True:
        try:
            RPC.connect()
            print("RPC client connected")
            break
        except ConnectionRefusedError as e:
            print("Failed to connect to RPC! Trying again in 10 seconds...")
            time.sleep(10)

def setup_player(name):
    player = Playerctl.Player.new_from_name(name)
    player.connect('playback-status::playing', on_play, manager)
    player.connect('playback-status::paused', on_pause, manager)
    player.connect('metadata', on_metadata, manager)
    update(player)
    manager.manage_player(player)

def get_song(player):
    return "%s - %s" % (player.get_title(), player.get_artist())

def update(player):
    status = player.get_property('status')

    try:
        if status == "":
            RPC.clear()
        elif status == "Playing":
            song = get_song(player)
            RPC.update(state='Playing', details=song, large_image='music', large_text=song, small_image='play')
        elif status == "Paused":
            RPC.update(state='Paused', large_image='music', small_image='pause')
    except pypresence.exceptions.InvalidID:
        print("Lost connection to Discord RPC! Attempting reconnection...")
        connect_rpc()

def on_play(player, status, manager):
    update(player)

def on_pause(player, status, manager):
    update(player)

def on_metadata(player, metadata, manager):
    update(player)

def on_player_add(manager, name):
    setup_player(name)

def on_player_remove(manager, player):
    if len(manager.props.players) < 1:
        try:
            RPC.clear()
        except pypresence.exceptions.InvalidID:
            if e is "Client ID is Invalid":
                print("Lost connection to Discord RPC! Attempting reconnection...")
                connect_rpc()
            else:
                raise
    else:
        update(manager.props.players[0])

manager.connect('name-appeared', on_player_add)
manager.connect('player-vanished', on_player_remove)

for name in manager.props.player_names:
    setup_player(name)

# Start program, connect to Discord & hook into GLib's main loop
connect_rpc()
GLib.MainLoop().run()
