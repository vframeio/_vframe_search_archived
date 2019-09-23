# Feature Selection

VFRAME Search uses CNN image features for content-based image similarity search. These vectors are typically extracted from the last unconnected layer of the CNN architecture. 

## Example CLI scripts

Extract features to pickle file:

- options: `python cli_image.py features --help`
- example: `python cli_proc.py features -i ../data_store_local/keyframes/ -o ../data_store_local/out.pkl -m caffe_googlenet_places365`


## Extract

```
from app.models import types
from app.image import cvdnn

# create cvmodel
my_model_enum = types.ModelZoo.CAFFE_BVLC_GOOGLENET_IMAGENET
dnn_factory = cvdnn.DNNFactory()
cvmodel = dnn_factory.from_enum(my_model)

# load image
fp_image = 'path/to/image.jpg'
im = cv.imread(fp_image)

# extract features
fv = cvmodel.features(im)
```
