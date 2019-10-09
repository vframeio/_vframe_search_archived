# Images

Keyframes are taking from videos of YouTube playlists associated with Syrian conflict documentation. Accounts are unverified and will also include a few random playlists

- 1,000 keyframes: <http://vframe.ams3.digitaloceanspaces.com/v2/dev/keyframes/keyframes_1k.zip> (80MB)

# Generating your own keyframes

Before extracting features you'll need a directory of images to process. You can use JPG or PNG images. If you have video you'll need to output keyframes.

- FFMPEG convert video to still frames at 2 FPS: `ffmpeg -i my_video.mp4 -r 1/2 still_frames/%05d.jpg` 
- Convert a batch of videos: 

```
for f in videos/*.mp4; do
    fn=$(basename "$f" | cut -d. -f1);
    echo "Processing: $fn";
    ffmpeg -i videos/$f -r 1/5 "still_frames/$fn"_%05d.jpg;
done
```

If you are using your own set of images, ensure that they are named in
a similar format (uniqueid_frameno).
