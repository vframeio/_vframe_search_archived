# Simple search (deprecated)

Note: The simple search has been deprecated.  These instructions are out of date.  While the backend server still works, the frontend codebase has been superceded.

Getting started with image search.

## Setup

- start docker `docker-compose up`
- `cd cli`
- run test script `python cli_simple.py`
- this will show the avilable options for running the demo search engine

## Download Models

Before you can run the search engine you'll need to download a model to use for feature extraction. Install a pretrained GoogleNet Places365 model using the VFRAME CLI models script:

`python cli_models.py download --model caffe_googlenet_places365`

The models originate from:

- Download prototxt: <https://github.com/CSAILVision/places365/blob/master/deploy_googlenet_places365.prototxt>
- Download weights: <http://places2.csail.mit.edu/models_places365/googlenet_places365.caffemodel>

# Download Images

Before extract features you'll need a directory of images to process. You can use JPG or PNG images. If you have video you'll need to output keyframes.

- FFMPEG convert video to still frames at 2 FPS: `ffmpeg -i my_video.mp4 -r 1/2 still_frames/%05d.jpg` 
- convert a batch of videos: 

```
for f in videos/*.mp4;do 
    fn=$(basename "$f" | cut -d. -f1);
    echo "Processing: $fn";
    ffmpeg -i videos/$f -r 1/5 "still_frames/$fn"_%05d.jpg;
done
```

## Extract Features

Next, build the feature vector index:

`./cli.py process features -i ../data_store/still_frames/ -o ../data_store/still_frames.pkl`

## Run Flask Server

Finally, start the simple Flask sever:

- `./cli.py server simple -i ../keyframes.pkl`


## API

You can also receive JSON results from the command line

```
curl -X GET 127.0.0.1:3000/api/v1/search/info

curl -X POST \
  -F "query_img=@../static/data/keyframes/0a9d430ac04d94e8c148dec1d97076c6f931db35127e6e2e1953dca404f4c195_001.jpg" \
  127.0.0.1:3000/api/v1/search/image
```

## Next Steps

Try download another classification model and generating a different index. Results will vary depending on how the DNNs were trained. For example networks trained on ImageNet are biased towards objects appearing centered in the image. The Places365 DNN should work better at diffrentiating between more scene-based imagery.

Show all Model Zoo models: `./cli.py models download --help`
