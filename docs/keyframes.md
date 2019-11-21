# Generating Keyframes

## VFRAME Scene Summarization

- under development

## FFMPEG with "Scene Detection"

Use FFMPEG to convert video to keyframes with scene detection

- Pros: easy to implement, fast
- Cons: inaccurate, uses sum of absolute frames 
- Read more: <https://www.luckydinosaur.com/u/ffmpeg-scene-change-detector>
- Output frames every 2 seconds: `ffmpeg -i my_video.mp4 -r 1/2 still_frames/%05d.jpg` 


## FFMPEG with Intervals

Use FFMPEG to convert video to keyframes at timed intervals

- Pros: simple command
- Cons: redundant frames
- Output frames every 2 seconds: `ffmpeg -i my_video.mp4 -r 1/2 still_frames/%05d.jpg` 
- Convert a batch of videos: 


## Helpful Commands

Convert directory of videos:

```
for f in videos/*.mp4; do
    fn=$(basename "$f" | cut -d. -f1);
    echo "Procedssing: $fn";
    ffmpeg -i videos/$f -r 1/5 "still_frames/$fn"_%05d.jpg;
done
```
