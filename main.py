from moviepy.editor import *

def fadeClip(clip, points, duration):
    subclipLength = clip.duration / len(points)
    subclips = []

    total = sum(points)

    for i in range(len(points)):
        subclips.append(clip.subclip(i*subclipLength, (i+1)*subclipLength))

    for i in range(len(subclips)):
        subclips[i] = subclips[i].fx(vfx.speedx, final_duration=duration*(points[i]/total))

    return concatenate_videoclips(subclips)

bpm = 128
hitsPerSecond = bpm / 60
keepAudio = False
hitSounds = True
useSong = False

fade = [3,2,2,1,2,2,3]

clip = VideoFileClip("2021-12-22 14-26-37_Trim.mp4")

hitSound = AudioFileClip("hit.ogg")

hitClips = []
hitTimes = []

beatTimes = [0]

prevHit = 0

with open("hits.txt", "r") as file:
    for _line in file:

        line = _line.split("	")[0]

        hitTimes.append(prevHit)
        hitClips.append(clip.subclip(prevHit, float(line)))
        prevHit = float(line)

with open("Label Track.txt", "r") as file:
    for _line in file:

        line = _line.split("	")[0]

        beatTimes.append(float(line))

if (len(hitTimes) > len(beatTimes)):
    print("!! More Hits Than Beats !! Trimming Hits !!")
    print(hitTimes)
    del hitTimes[(len(beatTimes)):]
    del hitClips[(len(beatTimes)):]
    print(len(hitTimes))
    print(len(beatTimes))


# applying speed effect
for i in range(len(hitClips)):
    if useSong:
        #hitClips[i] = hitClips[i].fx(vfx.speedx, final_duration=(beatTimes[i+1] - beatTimes[i]))
        hitClips[i] = fadeClip(hitClips[i], fade, (beatTimes[i+1] - beatTimes[i]))
        print("should be", (beatTimes[i+1] - beatTimes[i]))
        print("is", hitClips[i].duration)
    else:
        hitClips[i] = fadeClip(hitClips[i], fade, 1 / hitsPerSecond)
        print("should be", 1 / hitsPerSecond)
        print("is", hitClips[i].duration)

# exporting final clip
final = concatenate_videoclips(hitClips)

modifier = []

if keepAudio:
    modifier.append(final.audio)

# Adding hit sounds
if hitSounds:
    for i in range(len(hitTimes)):
        if i != 0:
            if useSong:
                modifier.append(hitSound
                                .set_start(beatTimes[i])
                                .set_duration(hitSound.duration))
                print(i * (1 / hitsPerSecond))
            else:
                modifier.append(hitSound
                                .set_start(i * (1 / hitsPerSecond))
                                .set_duration(hitSound.duration))
                print(i * (1 / hitsPerSecond))

final = final.set_audio(CompositeAudioClip(modifier))
final.write_videofile("export.mp4")