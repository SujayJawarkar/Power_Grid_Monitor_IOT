import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import time
import sys

"""
This Python script connects to the Arduino's serial port,
reads the sensor data, and plots it in real-time using matplotlib.
It displays three subplots for Voltage, Current, and Temperature.
"""

# =========================================================================
# 1. SETUP & CONFIGURATION
# =========================================================================

# Configure serial port settings
# IMPORTANT: Change 'COM3' to the correct port for your Arduino.
# On Linux, it might be something like '/dev/ttyACM0' or '/dev/ttyUSB0'.
# On macOS, it might be something like '/dev/cu.usbmodem14101'.
# You can find the port in the Arduino IDE's "Tools" menu.
arduino_port = 'COM3'
baud_rate = 9600
ser = None

# Set up data storage for the plots
# deque (double-ended queue) is used to efficiently store a fixed number of data points
max_data_points = 100 # Adjust this value to change the visible time window on the plots
voltage_data = deque([0.0] * max_data_points)
current_data = deque([0.0] * max_data_points)
temperature_data = deque([0.0] * max_data_points)
time_data = deque([0.0] * max_data_points)
start_time = time.time()

# =========================================================================
# 2. PLOT INITIALIZATION
# =========================================================================

# Set up the figure and subplots
plt.style.use('fivethirtyeight')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
fig.suptitle('Power Grid Monitoring Dashboard', fontsize=16)

# Create the line objects for each plot
line1, = ax1.plot(time_data, voltage_data, 'b-', label='Voltage (V)')
line2, = ax2.plot(time_data, current_data, 'g-', label='Current (A)')
line3, = ax3.plot(time_data, temperature_data, 'r-', label='Temperature (°C)')

# Set labels and titles for the plots
ax1.set_title('Voltage')
ax1.set_ylabel('Voltage (V)')
ax1.set_xlabel('Time (s)')
ax1.legend()

ax2.set_title('Current')
ax2.set_ylabel('Current (A)')
ax2.set_xlabel('Time (s)')
ax2.legend()

ax3.set_title('Temperature')
ax3.set_ylabel('Temperature (°C)')
ax3.set_xlabel('Time (s)')
ax3.legend()

# Enable interactive plotting
plt.ion()
plt.show()

# =========================================================================
# 3. DATA PARSING AND UPDATING FUNCTION
# =========================================================================

def parse_data_from_serial(data_string):
    """
    Parses a string from the serial port into a dictionary of float values.
    Example input: "Voltage:225.4,Current:4.1,Temperature:28.9"
    Returns: {'Voltage': 225.4, 'Current': 4.1, 'Temperature': 28.9}
    """
    data_dict = {}
    try:
        parts = data_string.split(',')
        for part in parts:
            if ':' in part:
                key, value = part.split(':')
                data_dict[key.strip()] = float(value.strip())
    except (ValueError, IndexError) as e:
        print(f"Error parsing data: {data_string} -> {e}")
        return None
    return data_dict

def update_plots():
    """
    Updates the plots with the new data from the deques.
    """
    line1.set_data(list(time_data), list(voltage_data))
    line2.set_data(list(time_data), list(current_data))
    line3.set_data(list(time_data), list(temperature_data))

    # Rescale the plots to fit the new data
    for ax, data in zip([ax1, ax2, ax3], [voltage_data, current_data, temperature_data]):
        ax.relim()
        ax.autoscale_view()
        # Set a reasonable y-axis limit, avoiding zero-range issues
        min_val = min(data) - 1 if data else -1
        max_val = max(data) + 1 if data else 1
        if min_val == max_val: # Avoid a static y-axis
            min_val -= 1
            max_val += 1
        ax.set_ylim(min_val, max_val)

    # Re-draw the plot
    fig.canvas.draw()
    fig.canvas.flush_events()


# =========================================================================
# 4. MAIN LOOP
# =========================================================================

if __name__ == "__main__":
    try:
        # Attempt to open the serial port
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Connected to Arduino on port {arduino_port}")
        time.sleep(2)  # Give the Arduino time to reset

        while True:
            # Check if there is data in the serial buffer
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                print(f"Received: {line}")

                data = parse_data_from_serial(line)
                if data:
                    # Add new data and remove the oldest data point
                    voltage_data.append(data.get('Voltage', 0.0))
                    voltage_data.popleft()

                    current_data.append(data.get('Current', 0.0))
                    current_data.popleft()

                    temperature_data.append(data.get('Temperature', 0.0))
                    temperature_data.popleft()

                    # Update the time data
                    time_data.append(time.time() - start_time)
                    time_data.popleft()

                    # Update the plots
                    update_plots()

            # Small pause to reduce CPU usage
            time.sleep(0.1)

    except serial.SerialException as e:
        print(f"Error: Could not open serial port {arduino_port}. Please check your connection and port name.")
        print(e)
        sys.exit(1)
    except KeyboardInterrupt:
        print("Dashboard stopped by user.")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("Serial port closed.")
        plt.close('all')
        print("All plots closed.")
