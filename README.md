This contains an example of converting sequences of images to videos.
Folder contains four example sequences.

Call

`python main_img2video.py --img_basedir ./data --output_basedir ./output --n_worker 2 --ffmpeg_path /usr/bin/ffmpeg`

to convert the sequences with 2 threads.

You'll need to install ffmpeg and provide the ffmpeg_path to the script if it's installed in non-standard location.
