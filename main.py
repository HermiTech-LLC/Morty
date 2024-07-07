import os
import subprocess

def compile_verilog():
    try:
        subprocess.run(['iverilog', '-o', 'uart_comm', 'uart_comm.v'], check=True)
        subprocess.run(['vvp', 'uart_comm'], check=True)
        print("Verilog module compiled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Verilog compilation: {e}")

def run_ros_pinn():
    try:
        subprocess.run(['rosrun', 'rospinn', 'rospinn.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during ROS PINN execution: {e}")

if __name__ == "__main__":
    compile_verilog()
    run_ros_pinn()
