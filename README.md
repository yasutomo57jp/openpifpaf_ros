# OpenPifpaf ROS node

## installation

```shell
pip install opencv-python
pip install openpifpaf
```

## usage

```shell
ROS_NAMESPACE=camera rosrun openpifpaf_ros openpifpaf_ros_node.py
```

If you want to run it faster, use smaller inputs.
```shell
ROS_NAMESPACE=camera rosrun openpifpaf_ros openpifpaf_ros_node.py _scale:=0.5
```

## parameters

|topic name| default    |
|--------- |------------|
|in_topic  | image_color|
|out_topic | human_pose |
|scale     |         1.0|
