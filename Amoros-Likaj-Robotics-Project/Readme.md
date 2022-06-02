## Steps to reproduce the project

### Setup Steps:
since we are using Galactic ROS2
_Installing:_
> `sudo apt install ros-galactic-slam-toolbox`
> `sudo apt install ros-galactic-nav2-bringup`
> `sudo apt install ros-galactic-navigation2`

_Configuration:_
(Is recommendable to make a backup of the files that are gonna be modified)
 `cp /opt/ros/galactic/share/slam_toolbox/config/mapper_params_online_async.yaml /opt/ros/galactic/share/slam_toolbox/config/mapper_params_online_async.yaml.bkp` 

 `cp /opt/ros/galactic/share/nav2_bringup/params/nav2_params.yaml /opt/ros/galactic/share/nav2_bringup/params/nav2_params.yaml.bkp`

After making a copy we update the files with our configurations 
 `cp ./mapper_params_online_async.yaml /opt/ros/galactic/share/slam_toolbox/config/mapper_params_online_async.yaml`
 
 `cp ./nav2_params.yaml /opt/ros/galactic/share/nav2_bringup/params/nav2_params.yaml` 

Add the respective scenes to coppelia.
> rob_project_WIP.ttt
> rob_project_full_v1.ttt
> rob_project_mini_v1.ttt


### Running of the project. 
1 Terminal:

>`~/apps/CoppeliaSim_Edu_V4_3_0_Ubuntu20_04/coppeliaSim.sh`

2 Terminal:

> `ros2 launch robomaster_ros ep.launch name:=robo1 tof_0:=True tof_1:=True tof_2:=True tof_3:=True`

3 Terminal:

> `ros2 launch nav2_bringup navigation_launch.py`

4 Terminal:

> `ros2 launch slam_toolbox online_async_launch.py`

5 Terminal:

> `ros2 run rm_nav rm2goal`

6 Terminal:

> `ros2 launch nav2_bringup rviz_launch.py`

7 terminal:

> `ros2 run tf2_ros static_transform_publisher 0.0 0 0.00 0 0 0 robo1/base_link robo1/base_scan`

(opt) Terminal:
==save the map==
> `ros2 run nav2_map_server map_saver_cli -f ~/map`





### Bonus
Just in case of bad saving of the scene, the script of the Sensor2d in coppelia is:

```
function sysCall_init() 
    model=sim.getObject('.')
    laserHandle=sim.getObject("./sensor")
    jointHandle=sim.getObject("./joint")
    red={1,0,0}
    points=sim.addDrawingObject(sim.drawing_spherepoints,0.01,0,-1,100000,nil,nil,nil,red)
    horizontalScanningAngle=90*math.pi/180
    scanningDensity=1
    laserScanPub=simROS2.createPublisher('/laser_scanner', 'sensor_msgs/msg/LaserScan')
end

function sysCall_sensing() 
    sim.addDrawingObjectItem(points,nil)
    
    pts=math.floor(horizontalScanningAngle*180*scanningDensity/math.pi)+1
    print(2*((1/40)/( pts ))*180)
    p=-horizontalScanningAngle/2
    stepSize=math.pi/(scanningDensity*180)
    local distance_arr={}
    for i=1,pts,1 do
        sim.setJointPosition(jointHandle,p)
        p=p+stepSize
        result,dist,pt=sim.handleProximitySensor(laserHandle)
        if result>0 then
            table.insert(distance_arr, dist)
            m=sim.getObjectMatrix(laserHandle,-1)
            pt=sim.multiplyVector(m,pt)
            sim.addDrawingObjectItem(points,pt)
        else
            table.insert(distance_arr, -1)
        end
    end
    
    timestamp=simROS2.getTime()
    msg={
        header={
            stamp=timestamp,
            frame_id='robo1/base_scan',
        },
        angle_min=-horizontalScanningAngle/2,
        angle_max=horizontalScanningAngle/2,
        angle_increment=stepSize,
        time_increment=(1/40)/( pts ), -- 40 is the laser frequency
        scan_time=2*((1/40)/( pts ))*180,
        range_min=0,
        range_max=100.0, --19.450,
        ranges=distance_arr,
        intensities={}
    }
    simROS2.publish(laserScanPub, msg)
end
 
function angleHMoved(ui,id,v)
    horizontalScanningAngle=math.pi*(10+1.7*v)/180
    simUI.setLabelText(ui,1,'Scanning angle ('..math.floor(horizontalScanningAngle*180/math.pi+0.5)..')')
end


```