# Vehicle Detection Implemented with YOLOv5 and Paddle (Train, Test, Validate, Export) Based on paddlepaddle2.4.2
* Vehicle Detection Implemented with YOLOv5 and Paddle, Including trainning and testing, validating end Export the model.
* This project provides many pre-trained models about yolov5 namely YOLOv5s, YOLOv5m, and so on.if the model not exits, it will download automaticlly.
* This project classifies vehicles into four categories:['car', 'bus', 'van', 'others']
* VisulDL service tool can be used to visualize and output various training data in real-time, for example: visualdl --log_dir vsl_dir --port 8080 
* and then you can open a web browser and enter localhost:8080 to view the training data and curves in real-time

# Dependencies
* All is in requirements.txt file.
# Pre-Start
* A conda env for this prj is recommended, type follow code to create one with the dependencies.
```shell
conda create --name put_your_env_name_here --file requirements_conda.txt
```
It is recommended but not necessary.
# Start
* This is a simple Markdown tutorial that has been successfully tested on Linux  system, to be more precise, on Ubuntu 20.04 system without considering conda or similar environments
* make sure you are under the dir "work"
## 1. Install dependencies
```angular2html
pip install -r requirements.txt 
```
to avoid a big change, the dependencies are as follows:
```angular2html
python==3.9.16
paddlepaddle-GPU==2.4.2(GPU is better namely paddlepaddle-GPU,you can choose any type of you want to install it like conda or pip)
visualdl==2.5.1
albumentations==1.3.0
```

## 2. Train Model
### 1. Data and Dataset Preparation
* Downloading the [VOCData and weights for four types of vehicle](https://pan.baidu.com/s/1g9iPMoem3XJkQC1gdUW23g?pwd=8mw3) due to the storage of github.
* After the unzip, move the VOCData.zip to path "/work/VOCData/" and delete other files like "yolovx.pdparams" since it have been out of date .
* Execute the following code snippets to extract and move the dataset to the location consistent with the one set in code.
```commandline
unzip -q ../data/VOCData.zip -d ./
```
* Change the folder name to match our code .
```commandline
mv VOCData/JPEGImages VOCData/images
```
* Execute the following code snippets to convert VOC format dataset to YOLOv5 standard format.
```angular2html
python /voc2yolo.py
```
**Note: The execution path of the code above all is the current directory(under the 'work/' folder)**

## 2. Start to train
### Before Train
* To make your project work successfully,you should install the [Arial.ttf](https://github.com/GuoQuanhao/YOLOv5-Paddle/releases/download/v1.0/Arial.ttf),and move it to you path ```~/.config/yolov5_dir```, specifilly in utils.general.py file's function namely **user_config_dir**
### 2.2 training the model
My local machine is nuvo-8108GC 2080 Super and the other informations like memory are as follows:
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.63.01    Driver Version: 470.63.01    CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  Off  | 00000000:06:00.0 Off |                  N/A |
| 30%   33C    P8     2W / 250W |     11MiB /  7982MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```
* as my machine's memory just occupy almost 7900M so I choose my batch-size equal to 32 is fit
the code snippets are :
```commandline
python train.py --img 640 --batch 16 --epochs 64 --data ./data/vehicle.yaml --cfg ./models/yolov5s.yaml --weights ./weights/yolov5s.pdparams
```

**Command Line Parameter Explanation：**
* **epochs：** Numbers of iterations, which needs to be specified and is set to a default value of 300. For this prj's vehicle detection pre-trained model, a setting of 30 iterations can achieve good detection results；
* **batch:** The amount of data processed at once depends on your machine which running this prj, Processing 128 data points at a time will occupy approximately 23.9GB of graphics memory.
* **img:** The image size for train and test datasets, the default value is 640X640 pixels
* **data:** The dataset configuration file has been modified and saved as file ./data/vehicle.yaml, If you are training your own dataset, corresponding modifications are required.


> * if you execute this onlie like paddle the GPU Tesla V100 16G: the batch set recomment：
> * ![image.png](https://s1.ax1x.com/2022/05/02/OiT3RS.png)
> * 32G memory pls double
> * 16G memory pls reduce by half

## Visulize - (not necessary)
* Type the follow code snippets and open the browser input ```local:8080```you can see the training situation in real time, including various parameters ,loss curves and so on
```commandline
visualdl --logdir runs/train --port 8080
```

## 3. Validate the Model
* After your training, a not bad model will be generated in "/runs/train/exp/weights/best.pdparams", Of course it just fit for paddlepaddle.
Type the following command line code 
```commandline
python val.py --img 640 --data ./data/vehicle.yaml --cfg ./model/yolov5s.yaml --weights ./runs/train/exp/weights/best.pdparams
```
* The results pics in "run/val/exp/", they have been draw the prediction bounding box and tie the label above every bounding box.
## 4. Model Inference
Type the following command line code 
```commandline
python detect.py --data ./data/vehicle.yaml --cfg ./models/yolov5s.yaml --weights ./runs/train/exp/weights/best.pdparams --source ./data/images/
```
* and you can get the output in "./runs/detect/expx", expx,the last "x" will output you console, maybe 1,  2 and so on

## 5. Model Export(paddle inference,onnx, engine, paddle lite, openvino)
Type the following code to convert it to paddle inference .
```shell
python export.py --weights yolov5n.pdparams --include paddleinfer 
```
Type the following code to convert it to onnx .
```shell
python export.py --weights yolov5n.pdparams --include onnx
```
Type the following code to convert it to engine .
```shell
python export.py --weights yolov5n.pdparams --include engine
```
Type the following code to convert it to openvino .
```shell
python export.py --weights yolov5n.pdparams --include openvino
```
Type the following code to convert it to paddlelite .
```shell
python export.py --weights yolov5n.pdparams --include paddlelite
```
#### If the performance is acceptable, you can apply this model(./runs/train/exp/weights/best.pdparams) to your own project.