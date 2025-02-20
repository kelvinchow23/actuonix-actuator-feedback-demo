from machine import Pin, PWM
import time

# Initialize PWM on a chosen pin (e.g., GP15)
pwm_pin = Pin(15)
pwm = PWM(pwm_pin)
pwm.freq(50)  # 50 Hz for servo-like control (20ms period)

def set_actuator_position(percentage):
    # Ensure the percentage is between 0 and 100
    percentage = max(0, min(100, percentage))
    # Map percentage to a pulse width: 1ms (0%) to 2ms (100%)
    pulse_width_ms = 1 + (percentage / 100.0)
    # Calculate duty cycle relative to the 20ms period.
    # The Pico's PWM in MicroPython uses a 16-bit value (0-65535).
    duty_cycle = int((pulse_width_ms / 20.0) * 65535)
    pwm.duty_u16(duty_cycle)
    print("Set actuator to {}% stroke (pulse width: {:.2f}ms)".format(percentage, pulse_width_ms))

# Loop to move the actuator to the specified positions
while True:
    for pos in [0, 25, 50, 100]:
        set_actuator_position(pos)
        time.sleep(15)
