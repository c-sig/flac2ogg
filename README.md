# flac2ogg
converts flac to ogg 192k~ made specifically for osu!

usage:
add ffmpeg to path first!!
you can either run main.py with python or download the executable in releases and run that instead

logic is basically
if bitrate is > 192000, decrement quality by some amount
if bitrate is < 192000, increment quality by some amount
increment/decrement amount changes over time until bitrate reaches 191500-192000 bps

built using pyinstaller
