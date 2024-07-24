# rosnode.py

import rospy
import numpy as np
import serial
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Wrench
from std_msgs.msg import Float64MultiArray
from sklearn.preprocessing import StandardScaler
from collections import deque

# ROS Node Initialization
def initialize_ros_node():
    rospy.init_node('bipedal_humanoid_pinn')
    control_pub = rospy.Publisher('/control_signals', Float64MultiArray, queue_size=10)
    return control_pub

control_pub = initialize_ros_node()

# Data storage and normalization
data_storage = {
    "joint_angles": deque(maxlen=100),
    "velocities": deque(maxlen=100),
    "torques": deque(maxlen=100),
    "foot_forces": deque(maxlen=100),
    "hand_joint_angles": deque(maxlen=100),
    "object_forces": deque(maxlen=100)
}

scaler = StandardScaler()

def update_and_normalize(data, new_data):
    data.append(new_data)
    if len(data) == 100:
        return scaler.fit_transform(np.array(data))
    return None

# ROS Callback Functions
def joint_state_callback(msg):
    try:
        joint_angles = np.array(msg.position, dtype=np.float32).reshape(1, -1)
        velocities = np.array(msg.velocity, dtype=np.float32).reshape(1, -1)
        torques = np.array(msg.effort, dtype=np.float32).reshape(1, -1)

        norm_joint_angles = update_and_normalize(data_storage["joint_angles"], joint_angles)
        norm_velocities = update_and_normalize(data_storage["velocities"], velocities)
        norm_torques = update_and_normalize(data_storage["torques"], torques)

        if norm_joint_angles is not None and norm_velocities is not None and norm_torques is not None:
            data_storage["joint_angles_normalized"] = norm_joint_angles
            data_storage["velocities_normalized"] = norm_velocities
            data_storage["torques_normalized"] = norm_torques
    except Exception as e:
        rospy.logerr(f"Error in joint_state_callback: {e}")

def foot_force_callback(msg):
    try:
        foot_forces = np.array([msg.force.x, msg.force.y, msg.force.z], dtype=np.float32).reshape(1, -1)
        norm_foot_forces = update_and_normalize(data_storage["foot_forces"], foot_forces)
        if norm_foot_forces is not None:
            data_storage["foot_forces_normalized"] = norm_foot_forces
    except Exception as e:
        rospy.logerr(f"Error in foot_force_callback: {e}")

def hand_joint_state_callback(msg):
    try:
        hand_joint_angles = np.array(msg.position, dtype=np.float32).reshape(1, -1)
        norm_hand_joint_angles = update_and_normalize(data_storage["hand_joint_angles"], hand_joint_angles)
        if norm_hand_joint_angles is not None:
            data_storage["hand_joint_angles_normalized"] = norm_hand_joint_angles
    except Exception as e:
        rospy.logerr(f"Error in hand_joint_state_callback: {e}")

def object_force_callback(msg):
    try:
        object_forces = np.array([msg.force.x, msg.force.y, msg.force.z], dtype=np.float32).reshape(1, -1)
        norm_object_forces = update_and_normalize(data_storage["object_forces"], object_forces)
        if norm_object_forces is not None:
            data_storage["object_forces_normalized"] = norm_object_forces
    except Exception as e:
        rospy.logerr(f"Error in object_force_callback: {e}")

# Subscribe to ROS topics
def subscribe_to_ros_topics():
    rospy.Subscriber('/joint_states', JointState, joint_state_callback)
    rospy.Subscriber('/foot_force', Wrench, foot_force_callback)
    rospy.Subscriber('/hand_joint_states', JointState, hand_joint_state_callback)
    rospy.Subscriber('/object_force', Wrench, object_force_callback)

subscribe_to_ros_topics()

# Initialize serial communication with FPGA
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Send and receive data to/from FPGA
def communicate_with_fpga(sensor_data):
    # Send sensor data
    ser.write(sensor_data.tobytes())
    
    # Read control signal
    control_signal = ser.read(size=240)  # Adjusted size for 60 float32 values
    control_signal = np.frombuffer(control_signal, dtype=np.float32)
    
    return control_signal

if __name__ == "__main__":
    rospy.spin()
