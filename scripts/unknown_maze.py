#! /usr/bin/env python3

# import ros stuff
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
import math

pub_ = None
regions_ = {
    'right': 0,
    'fright': 0,
    'front': 0,
    'fleft': 0,
    'left': 0,
}
state_ = 0
state_dict_ = {
    0: 'find the wall',
    1: 'turn left',
    2: 'follow the wall',
}

def clbk_laser(msg):
    global regions_
    regions_ = {
        'right':  min(min(msg.ranges[215:270]), 10),
        'fright': min(min(msg.ranges[280:315]), 10),
        'front':  min(min(msg.ranges[0:1]), 10),
        'fleft':  min(min(msg.ranges[10:45]), 10),
        'left':   min(min(msg.ranges[60:90]), 10),
    }

    take_action()

def change_state(state):
    global state_, state_dict_
    if state is not state_:
        print ('Wall follower - [%s] - %s' % (state, state_dict_[state]))
        state_ = state

def take_action():
    global regions_
    regions = regions_
    msg = Twist()
    linear_x = 0
    angular_z = 0
    
    state_description = ''
    
    d = 0.75
    
    if regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 1 - nothing'
        change_state(0)
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 2 - front'
        change_state(1)
    elif regions['front'] > d and regions['fleft'] > d and regions['fright'] < d:
        state_description = 'case 3 - fright'
        change_state(2)
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] > d:
        state_description = 'case 4 - fleft'
        change_state(0)
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] < d:
        state_description = 'case 5 - front and fright'
        change_state(1)
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] > d:
        state_description = 'case 6 - front and fleft'
        change_state(1)
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 7 - front and fleft and fright'
        change_state(1)
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 8 - fleft and fright'
        change_state(0)
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

def find_wall():
	msg = Twist()
	msg.linear.x = 0.14
	msg.angular.z = -0.3
	return msg
	
def turn_left():
	#Angular velocity ???x??? towards the left side
	msg = Twist()
	msg.angular.z = 0.3
	return msg
def follow_the_wall():#Linear velocity ???x??? in the forward direction
	global regions_
	msg = Twist()
	msg.linear.x = 0.4
	return msg
    
	#No obstacles detected 'case 1 - nothing'
	#Obstacle on the left side 'case 4 - fleft'
	#Obstacles on the left and right sides
	#if 'case 1 - nothing' or 'case 4 - fleft' or 'case 8 - fleft and fright':
if change_state(0):
    find_wall() 
	#Obstacles in front of the robot
	#Obstacles in front and left of the robot
	#Obstacles in front and right of the robot
	#Obstacles in front, left and right of the robot
	#if 'case 2 - front' or 'case 6 - front and fleft' or 'case 5 - front and fright' or 'case 7 - front and fleft and fright': 
if change_state(1):
	turn_left()

	#Linear velocity ???x??? in the forward direction
	#Obstacle detected only on the right side of the robot 'case 3 - fright':
if change_state(2):
	follow_the_wall()

def main():
    global pub_
    
    rospy.init_node('reading_laser')
    
    pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        msg = Twist()
        if state_ == 0:
            msg = find_wall()
        elif state_ == 1:
            msg = turn_left()
        elif state_ == 2:
            msg = follow_the_wall()
            pass
        else:
            rospy.logerr('Unknown state!')
            
        pub_.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    main()

