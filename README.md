Actuonix Actuator Feedback Demo
This demo shows how to use an Actuonix actuator with the Linear Actuator Control (LAC) board to send position commands and receive position feedback. The demo was developed using the L16-100-150-12-P actuator (see Actuonix L16-100-150-12-P), although many of the 5-pin P-series actuators should work as well.

Requirements
Actuator & LAC Board:
Actuonix actuator (recommended model: L16-100-150-12-P) and the corresponding LAC board.
Microcontroller:
Raspberry Pi Pico running MicroPython.
Power Supply & Wiring:
Refer to the BOM and wiring folder for the physical setup.
Software:
Thonny IDE (or another MicroPython-compatible environment).
Setup Instructions
Wiring:
Follow the BOM and wiring folder for detailed setup instructions.
Reference Terminals:
Although it's recommended to wire the LAC board’s P+ and P– terminals to the Pico’s 3.3 V and GND respectively, you may notice little difference in readings if these connections are omitted.
Software Installation:
Upload the scripts from the scripts folder to your Raspberry Pi Pico.
Ensure your Pico has the latest MicroPython firmware installed. For guidance, see the Getting Started with the Pico project.
Running the Demo
The demo script, actuonix_feedback_demo_async.py, cycles the actuator through positions at 0%, 25%, 50%, 75%, and 100% of the stroke length while streaming live position data to the serial monitor.

Configuring Stroke Length:
In the script (line 5), update the variable ACTUATOR_STROKE_LENGTH to reflect the actual stroke length of your actuator (e.g., change to 50 mm if using an L16-50-150-12-P actuator).

Demo Video:
Placeholder for video demo

Additional Resources
Linear Actuator Control Board – Intro and Setup
How to Use a Linear Actuator Control Board With Arduino
AC Training Lab GitHub Issue
