# ros2bag_convert

[中文](README.md) | [English](README_EN.md)

**将ROS2的Bag文件转换为CSV、JSON等。**

## 一、安装

命令行安装：

```
sudo pip install ros2bag_convert
```

下载安装：

```
git clone git@github.com:fishros/ros2bag_convert.git
cd ros2_convert
python3 setup.py bdist_wheel
sudo pip install dist/ros2bag_convert-0.1.0-py3-none-any.whl
```

## 二、使用

目前仅支持将数据转换为csv格式，结果将输出到`xxx.db3`同级目录。

```
ros2bag-convert xxxx.db3
```

### 测试指令

#### 手动发布Pose数据

```
ros2 topic pub test geometry_msgs/msg/Pose  '{position:{x: 0.0,y: 0.0,z: 0.0}, orientation: {x: 0.0,y: 0.0,z: 0.0,w: 1.0}}'
```

#### 记录

```
ros2 bag record test
```

#### 转换

```
ros2bag-convert xxxx.db3
```

## 作者

- [小鱼-公众号鱼香ROS](https://www.fishros.com)

![img](http://tools.fishros.com/README/imgs/image-20210726192026520.png)

## 版本记录

- 20210830-V0.1.0
  - 完成基础转换功能
  - 已知bug：数据未按层级展开输出