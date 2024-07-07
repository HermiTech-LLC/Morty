import torch
import torch.nn as nn
import torch.optim as optim
import rospy
import numpy as np
import serial
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Wrench
from std_msgs.msg import Float64MultiArray
from sklearn.preprocessing import StandardScaler
from collections import deque
from torch.distributions import Normal

# Neural Network Architecture for PINN
class BipedalHumanoidPINN(nn.Module):
    def __init__(self):
        super(BipedalHumanoidPINN, self).__init__()
        self.fc1 = nn.Linear(60, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, 128)
        self.fc4 = nn.Linear(128, 60)
        self.dropout = nn.Dropout(0.3)

    def forward(self, inputs):
        x = torch.tanh(self.fc1(inputs))
        x = torch.tanh(self.fc2(x))
        x = self.dropout(x)
        x = torch.tanh(self.fc3(x))
        control_signals = self.fc4(x)
        return control_signals

# Physics-Informed Loss Function
def calculate_com_position(control_signals):
    return torch.mean(control_signals[:, :30], dim=1, keepdim=True)

def calculate_desired_com_position(batch_size):
    return torch.zeros(batch_size, 1)

def calculate_object_interaction(control_signals):
    object_position = control_signals[:, :30]
    object_force = control_signals[:, 30:60]
    return object_position, object_force

def calculate_desired_object_interaction(batch_size):
    desired_object_position = torch.zeros(batch_size, 30)
    desired_object_force = torch.zeros(batch_size, 30)
    return desired_object_position, desired_object_force

def physics_informed_loss(model, inputs, k_stability=0.01):
    control_signals = model(inputs)
    batch_size = inputs.size(0)

    com_position = calculate_com_position(control_signals)
    desired_com_position = calculate_desired_com_position(batch_size)
    stability_loss = torch.mean((com_position - desired_com_position) ** 2)

    object_position, object_force = calculate_object_interaction(control_signals)
    desired_object_position, desired_object_force = calculate_desired_object_interaction(batch_size)
    manipulation_loss = torch.mean((object_position - desired_object_position) ** 2) + torch.mean((object_force - desired_object_force) ** 2)

    total_loss = stability_loss + k_stability * manipulation_loss
    return total_loss
    # Reinforcement Learning Agent
class RLAgent(nn.Module):
    def __init__(self, input_dim, action_dim):
        super(RLAgent, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_dim)
        self.value_head = nn.Linear(128, 1)
        self.log_std = nn.Parameter(torch.zeros(action_dim))

    def forward(self, x):
        x = torch.tanh(self.fc1(x))
        x = torch.tanh(self.fc2(x))
        action_mean = self.fc3(x)
        value = self.value_head(x)
        return action_mean, value

    def select_action(self, state):
        action_mean, _ = self.forward(state)
        action_dist = Normal(action_mean, self.log_std.exp())
        action = action_dist.sample()
        return action, action_dist.log_prob(action).sum(dim=-1)

# Initialize models and optimizers
pinn_model = BipedalHumanoidPINN()
rl_agent = RLAgent(input_dim=60, action_dim=60)
optimizer_pinn = optim.Adam(pinn_model.parameters(), lr=0.001)
optimizer_rl = optim.Adam(rl_agent.parameters(), lr=0.001)

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
        joint_angles = torch.tensor(msg.position, dtype=torch.float32).unsqueeze(0)
        velocities = torch.tensor(msg.velocity, dtype=torch.float32).unsqueeze(0)
        torques = torch.tensor(msg.effort, dtype=torch.float32).unsqueeze(0)

        norm_joint_angles = update_and_normalize(data_storage["joint_angles"], joint_angles)
        norm_velocities = update_and_normalize(data_storage["velocities"], velocities)
        norm_torques = update_and_normalize(data_storage["torques"], torques)

        if norm_joint_angles is not None and norm_velocities is not None and norm_torques is not None:
            data_storage["joint_angles_normalized"] = torch.tensor(norm_joint_angles, dtype=torch.float32)
            data_storage["velocities_normalized"] = torch.tensor(norm_velocities, dtype=torch.float32)
            data_storage["torques_normalized"] = torch.tensor(norm_torques, dtype=torch.float32)
    except Exception as e:
        rospy.logerr(f"Error in joint_state_callback: {e}")

def foot_force_callback(msg):
    try:
        foot_forces = torch.tensor([msg.force.x, msg.force.y, msg.force.z], dtype=torch.float32).unsqueeze(0)
        norm_foot_forces = update_and_normalize(data_storage["foot_forces"], foot_forces)
        if norm_foot_forces is not None:
            data_storage["foot_forces_normalized"] = torch.tensor(norm_foot_forces, dtype=torch.float32)
    except Exception as e:
        rospy.logerr(f"Error in foot_force_callback: {e}")

def hand_joint_state_callback(msg):
    try:
        hand_joint_angles = torch.tensor(msg.position, dtype=torch.float32).unsqueeze(0)
        norm_hand_joint_angles = update_and_normalize(data_storage["hand_joint_angles"], hand_joint_angles)
        if norm_hand_joint_angles is not None:
            data_storage["hand_joint_angles_normalized"] = torch.tensor(norm_hand_joint_angles, dtype=torch.float32)
    except Exception as e:
        rospy.logerr(f"Error in hand_joint_state_callback: {e}")

def object_force_callback(msg):
    try:
        object_forces = torch.tensor([msg.force.x, msg.force.y, msg.force.z], dtype=torch.float32).unsqueeze(0)
        norm_object_forces = update_and_normalize(data_storage["object_forces"], object_forces)
        if norm_object_forces is not None:
            data_storage["object_forces_normalized"] = torch.tensor(norm_object_forces, dtype=torch.float32)
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

# Training Loop
def train(pinn_model, rl_agent, optimizer_pinn, optimizer_rl, num_epochs, print_every=100):
    rate = rospy.Rate(10)
    for epoch in range(num_epochs):
        if all("normalized" in key for key in data_storage.keys()):
            try:
                inputs = torch.cat([data_storage["joint_angles_normalized"],
                                    data_storage["velocities_normalized"],
                                    data_storage["torques_normalized"],
                                    data_storage["foot_forces_normalized"],
                                    data_storage["hand_joint_angles_normalized"],
                                    data_storage["object_forces_normalized"]], dim=1)

                # PINN optimization
                optimizer_pinn.zero_grad()
                pinn_loss = physics_informed_loss(pinn_model, inputs)
                pinn_loss.backward()
                optimizer_pinn.step()

                # Reinforcement Learning optimization
                optimizer_rl.zero_grad()
                actions, log_probs = rl_agent.select_action(inputs)
                value_loss = -log_probs.mean()  # Example loss for RL, usually more complex
                value_loss.backward()
                optimizer_rl.step()

                if epoch % print_every == 0:
                    rospy.loginfo(f'Epoch {epoch}, PINN Loss: {pinn_loss.item()}, RL Loss: {value_loss.item()}')

                    # Communicate with FPGA
                    control_signals = communicate_with_fpga(inputs.numpy())
                    control_signals_msg = Float64MultiArray(data=control_signals.tolist())
                    control_pub.publish(control_signals_msg)

            except Exception as e:
                rospy.logerr(f"Error in training loop: {e}")
        rate.sleep()

if __name__ == "__main__":
    try:
        train(pinn_model, rl_agent, optimizer_pinn, optimizer_rl, num_epochs=1000)
    except rospy.ROSInterruptException:
        pass
