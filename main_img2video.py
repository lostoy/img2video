import os
import argparse
from multiprocessing.pool import Pool

def convert_job(args, ffmpeg_path):
    for i, (img_dir, output_path) in enumerate(args):
        if i % 10 == 0:
            print('converting {}/{}'.format(i, len(args)))
        try:
            os.makedirs(os.path.dirname(output_path))
        except:
            pass

        cmd = '{} -nostats -loglevel 0 -framerate 30 -pattern_type glob -i "{}/*.png" -vf "fps=30,format=yuv420p" {}'.format(
            ffmpeg_path, img_dir, output_path)
        os.system(cmd)
    print('job done!')
    return 0

def get_video_dir_list(input_basedir, output_basedir):
    try:
        os.makedirs(output_basedir)
    except:
        pass
    exist_files = filter(lambda x: '.mp4' in x, os.listdir(output_basedir))
    exist_files = map(lambda x: os.path.splitext(os.path.basename(x))[0], exist_files)
    all_dirs = os.listdir(input_basedir)

    not_done_dirnames = sorted(list(set(all_dirs) - set(exist_files)))
    not_done_dirs = map(lambda x: os.path.join(input_basedir, x), not_done_dirnames)
    output_paths = map(lambda x: os.path.join(output_basedir, '{}.mp4'.format(x)), not_done_dirnames)
    return not_done_dirs, output_paths

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ffmpeg_path', type=str, help='ffmpeg executable path', default='/usr/bin/ffmpeg')
    parser.add_argument('--img_basedir', type=str, help='parent folder of all image sequence folders')
    parser.add_argument('--output_basedir', type=str, help='parent output folder of all converted videos')
    parser.add_argument('--n_worker', type=int, help='number of workers', default=2)

    args = parser.parse_args()
    if not os.path.exists(args.ffmpeg_path):
        print('please install ffmpeg add provide its path!')
        parser.print_help()
        exit(-1)

    video_dirs, output_paths = get_video_dir_list(args.img_basedir, args.output_basedir)

    print('{} img sequences to be converted.'.format(len(video_dirs)))

    workers = Pool(args.n_worker)

    # chunk jobs
    chunks = [list(zip(video_dirs, output_paths))[i::args.n_worker] for i in range(args.n_worker)]
    for i in range(args.n_worker):
        workers.apply(convert_job, (chunks[i], args.ffmpeg_path))

    workers.close()
    workers.join()
