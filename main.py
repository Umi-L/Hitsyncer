# Import everything needed to edit video clips
from moviepy.editor import *

def fadeClip(clip, points, offset):
    subclipLength = clip.duration / len(points)
    subclips = []

    for i in range(len(points)):
        subclips.append(clip.subclip(i*subclipLength, (i+1)*subclipLength))

    for i in range(len(subclips)):
        subclips[i] = subclips[i].fx(vfx.speedx, points[i] * offset)

    return concatenate_videoclips(subclips)

hitsPerSecond = 2.13
keepAudio = False
hitSounds = True

fade = [1,1,1.5,0.5,1.5,1,1]

clip = VideoFileClip("input1.wmv")

hitSound = AudioFileClip("hit.mp3")
print("Hit duration:", hitSound.duration)

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
        multiplier = hitsPerSecond * (hitTimes[i+1] - hitTimes[i])
        #hitClips[i] = hitClips[i].fx(vfx.speedx, multiplier)
        hitClips[i] = fadeClip(hitClips[i], fade, multiplier)

# exporting final clip
final = concatenate_videoclips(hitClips)

modifier = []

if keepAudio:
    modifier.append(final.audio)

# Adding hit sounds
if hitSounds:
    for i in range(len(hitTimes)):
        if i != 0:
            modifier.append(hitSound
                            .set_start(i*(1/hitsPerSecond))
                            .set_duration(hitSound.duration))
            print(i*(1/hitsPerSecond))

final = final.set_audio(CompositeAudioClip(modifier))
final.write_videofile("export.mp4")

