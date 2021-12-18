# Import everything needed to edit video clips
from moviepy.editor import *

hitsPerSecond = 2.13
keepAudio = False


# loading video dsa gfg intro video
clip = VideoFileClip("input1.wmv")
if not keepAudio: clip = clip.without_audio()

audioclip = AudioFileClip("hit.mp3")

hitClips = []
hitTimes = []

prevHit = 0

with open("hits", "r") as file:
    for line in file:
        hitTimes.append(prevHit)
        hitClips.append(clip.subclip(prevHit, float(line)))
        prevHit = float(line)

# applying speed effect
for i in range(len(hitClips)):
    #if not on the last item
    if (i != len(hitClips)-1):
        hitClips[i] = hitClips[i].fx(vfx.speedx, hitsPerSecond * (hitTimes[i+1] - hitTimes[i]))
        print(hitsPerSecond * (hitTimes[i+1] - hitTimes[i]))

# exporting final clip
final = concatenate_videoclips(hitClips)
final.write_videofile("export.mp4")