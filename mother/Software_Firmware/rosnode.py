import rospy
import numpy as np
import serial
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Wrench
from std_msgs.msg import Float64MultiArray
from sklearn.preprocessing import StandardScaler
from collections import deque
import casadi as ca

# ROS Node Initialization
def initialize_ros_node():
    rospy.init_node('bipedal_humanoid_pinn', anonymous=True)
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
    if len(data) == data.maxlen:
        normalized_data = scaler.fit_transform(np.array(data))
        return normalized_data
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
def initialize_serial(port='/dev/ttyUSB0', baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate)
        return ser
    except serial.SerialException as e:
        rospy.logerr(f"Failed to initialize serial communication: {e}")
        return None

ser = initialize_serial()

# Define the optimization problem using CasADi
def define_optimization_problem():
    n_controls = 60
    u = ca.MX.sym('u', n_controls)

    # Define the objective function (example: minimize the control effort)
    objective = ca.mtimes(u.T, u)

    # Define constraints (example: control signals must be within certain limits)
    lb_u = -np.ones(n_controls) * 1.0  # Lower bound for control signals
    ub_u = np.ones(n_controls) * 1.0  # Upper bound for control signals

    nlp = {'x': u, 'f': objective}
    opts = {'ipopt.print_level': 0, 'print_time': 0}
    solver = ca.nlpsol('solver', 'ipopt', nlp, opts)
    
    return solver, lb_u, ub_u

solver, lb_u, ub_u = define_optimization_problem()

# Send and receive data to/from FPGA
def communicate_with_fpga(sensor_data):
    try:
        # Send sensor data
        ser.write(sensor_data.tobytes())
        
        # Read control signal
        control_signal = ser.read(size=240)  # Adjusted size for 60 float32 values
        control_signal = np.frombuffer(control_signal, dtype=np.float32)
        
        # Optimize control signal
        sol = solver(x0=control_signal, lbg=lb_u, ubg=ub_u)
        optimized_control_signal = sol['x'].full().flatten()
        
        return optimized_control_signal
    except Exception as e:
        rospy.logerr(f"Error in communication with FPGA: {e}")
        return np.zeros(60, dtype=np.float32)  # Return a safe default control signal in case of error

if __name__ == "__main__":
    rospy.spin()