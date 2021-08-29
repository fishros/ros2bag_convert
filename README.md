# ros2bag_convert


Convert ROS2 bag files to CSV, JSON, etc. 

将ROS2的Bag文件转换为CSV、JSON等。


### 测试

```
ros2 topic pub test geometry_msgs/msg/Pose  '{position:{x: 0.0,y: 0.0,z: 0.0}, orientation: {x: 0.0,y: 0.0,z: 0.0,w: 1.0}}'
```