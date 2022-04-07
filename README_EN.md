# ros2bag_convert

[Chinese](README.md) | [English](README_EN.md)

**Convert ROS2 Bag files to CSV, JSON, etc. **

## I. Installation

Command line installation.

```
sudo pip install ros2bag_convert
```

Download and install.

```
git clone git@github.com:fishros/ros2bag_convert.git
cd ros2_convert
python3 setup.py bdist_wheel
sudo pip install dist/ros2bag_convert-0.1.0-py3-none-any.whl
```

## II. Use

Currently only support converting data to csv format, the result will be output to `xxx.db3` sibling directory.

```
ros2bag-convert xxxx.db3
```

### Test command

#### Manually publish Pose data

```
ros2 topic pub test geometry_msgs/msg/Pose '{position:{x: 0.0,y: 0.0,z: 0.0}, orientation: {x: 0.0,y: 0.0,z: 0.0,w: 1.0}}'
```

#### record

```
ros2 bag record test
```

#### convert

```
ros2bag-convert xxxx.db3
```

## Author.
- [小鱼-公众号鱼香ROS](https://www.fishros.com)

![img](http://tools.fishros.com/README/imgs/image-20210726192026520.png)


## Version Record

- 20210830-V0.1.0
  - Completed basic conversion function
  - Known bug: Data is not exported by hierarchical expansion
