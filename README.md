# Math Expression Recognizer(Keras)
Handwritten Mathematical Expression Recognition System.
The Project is built using [Keras](https://keras.io/) library.

## Dataset
The [dataset](https://github.com/harshaldesai01/Math-Expression-Recognizer/tree/master/data) used in the project contains 2258 instances of labelled handwritten mathematical equations in InkML format.

The model has been trained on Image data which was obtained by conversion of this [InkML data](https://github.com/harshaldesai01/Math-Expression-Recognizer/tree/master/data) to 28,173 images of 75 classes of unique mathematical expression.

## Model

![Model Architecture](https://github.com/harshaldesai01/Math-Expression-Recognizer/blob/master/snaps/model_arch.png)


## Performance

The model achieves an accuracy of 94.29% on the validation data.

![Train Log](https://github.com/harshaldesai01/Math-Expression-Recognizer/blob/master/snaps/train_log.png)

The accuracy achieved is pretty decent considering the uneven distribution of images in various classes:
![Class Distribution](https://github.com/harshaldesai01/Math-Expression-Recognizer/blob/master/snaps/class_dist.jpg)

## Scripts

**inkml2img.py**: The code for extracting traces of different expressions from a given InkML format equation.\
**convert.py**: Converts InkML files to images.\
**run_model.py**: Contains code to build the Deep Learning architecture and train the converted images on the Deep Learning model.\
**training_monitor.py**: It monitors the training based on the validation loss to avoid overfitting.

## References
InkML to Image conversion credits: https://github.com/RobinXL/inkml2img
