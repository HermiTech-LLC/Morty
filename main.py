import os
import subprocess
import numpy as np
from tpu import BipedalHumanoidPINN, physics_informed_loss, RLAgent, train
from mother.Software.Firmware.rosnode import initialize_ros_node, subscribe_to_ros_topics, communicate_with_fpga

def compile_verilog():
    """
    Compiles the Verilog module using iverilog and executes the compiled output using vvp.
    
    This function runs the iverilog command to compile the uart_comm.v Verilog file and then
    runs the compiled output using the vvp command. It prints a success message if the
    compilation and execution are successful. Otherwise, it prints an error message.
    
    Raises:
        subprocess.CalledProcessError: If there is an error during the Verilog compilation
                                       or execution process.
    """
    try:
        subprocess.run(['iverilog', '-o', 'uart_comm', 'uart_comm.v'], check=True)
        subprocess.run(['vvp', 'uart_comm'], check=True)
        print("Verilog module compiled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Verilog compilation: {e}")

def run_ros_pinn():
    """
    Runs the ROS PINN node using rosrun.
    
    This function runs the rospinn.py script using the rosrun command. It prints a success
    message if the ROS node execution is successful. Otherwise, it prints an error message.
    
    Raises:
        subprocess.CalledProcessError: If there is an error during the ROS PINN execution process.
    """
    try:
        subprocess.run(['rosrun', 'rospinn', 'rospinn.py'], check=True, cwd='mother/Software/Firmware')
        print("ROS PINN node executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during ROS PINN execution: {e}")

def start_systemd_service(service_name):
    """
    Starts a specified systemd service using systemctl.
    
    Args:
        service_name (str): The name of the systemd service to start.
    
    This function runs the systemctl start command to start the specified systemd service.
    It prints a success message if the service is started successfully. Otherwise, it
    prints an error message.
    
    Raises:
        subprocess.CalledProcessError: If there is an error starting the systemd service.
    """
    try:
        subprocess.run(['systemctl', 'start', service_name], check=True)
        print(f"Systemd service {service_name} started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting systemd service {service_name}: {e}")

def run_micropython(script_path):
    """
    Executes a specified MicroPython script using the micropython command.
    
    Args:
        script_path (str): The path to the MicroPython script to execute.
    
    This function runs the specified MicroPython script using the micropython command.
    It prints a success message if the script is executed successfully. Otherwise, it
    prints an error message.
    
    Raises:
        subprocess.CalledProcessError: If there is an error executing the MicroPython script.
    """
    try:
        subprocess.run(['micropython', script_path], check=True)
        print(f"MicroPython script {script_path} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing MicroPython script {script_path}: {e}")

if __name__ == "__main__":
    # Compile Verilog
    compile_verilog()

    # Start systemd services
    systemd_services = ['service1', 'service2']  # Replace with actual service names
    for service in systemd_services:
        start_systemd_service(service)
    
    # Run ROS PINN script
    run_ros_pinn()

    # Run MicroPython script
    micropython_script_path = 'control_interface.py'  # Replace with actual script path
    run_micropython(micropython_script_path)

    # Initialize ROS node and subscribe to topics
    control_pub = initialize_ros_node()
    subscribe_to_ros_topics()

    # Initialize models and optimizers
    pinn_model = BipedalHumanoidPINN()
    rl_agent = RLAgent(input_dim=60, action_dim=60)
    optimizer_pinn = optimizers.Adam(learning_rate=0.001)
    optimizer_rl = optimizers.Adam(learning_rate=0.001)

    # Replace 'inputs' with actual input data
    inputs = np.random.rand(100, 60).astype(np.float32)  # Example input data
    train(pinn_model, rl_agent, optimizer_pinn, optimizer_rl, inputs, num_epochs=1000)

    # Initialize serial communication with FPGA
    ser = serial.Serial('/dev/ttyUSB0', 9600)

    # Example usage of communicate_with_fpga
    sensor_data = np.random.rand(60).astype(np.float32)  # Example sensor data
    control_signal = communicate_with_fpga(sensor_data)

    # Run ROS node main loop
    rospy.spin()
