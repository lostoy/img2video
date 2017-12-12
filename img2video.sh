#! /bin/bash
ffmpeg -framerate 30 -pattern_type glob -i "$1/*.png" -vf "fps=30,format=yuv420p" $2