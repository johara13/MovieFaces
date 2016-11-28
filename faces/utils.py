import subprocess

def grab_frame(videofile, timestamp):
    subprocess.call('ffmpeg -i %s -vf "select=gte(n\,100)" -vframes 1 out_img.png'% videofile)

def get_totalframes(videofile):
    return subprocess.check_output('ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 %s'% videofile)