import uasyncio as asyncio
from machine import Pin, PWM, ADC

# Set actuator stroke length in millimeters.
ACTUATOR_STROKE_LENGTH = 100  # mm

class Actuator:
    def __init__(self, pwm_pin_num=15, adc_pin_num=28, pwm_freq=50):
        # Initialize the PWM output (for controlling the actuator position)
        self.pwm = PWM(Pin(pwm_pin_num))
        self.pwm.freq(pwm_freq)  # 50 Hz -> 20ms period
        
        # Initialize the ADC input (for reading the position feedback)
        self.adc = ADC(Pin(adc_pin_num))
        # Conversion factor for Pico ADC (16-bit resolution with a 3.3V reference)
        self.conversion_factor = 3.3 / 65535.0
        
        # Full-scale voltage for position measurement (0-3.3V)
        self.full_range_voltage = 3.3

    def set_position(self, percentage):
        """
        Set the actuator position by sending a PWM signal.
        Mapping: 0% stroke  -> 1ms pulse width, 100% stroke -> 2ms pulse width.
        """
        # Clamp the percentage between 0 and 100.
        percentage = max(0, min(100, percentage))
        # Calculate pulse width in milliseconds.
        pulse_width_ms = 1 + (percentage / 100.0)
        # Convert pulse width to 16-bit duty cycle (20ms period).
        duty_cycle = int((pulse_width_ms / 20.0) * 65535)
        self.pwm.duty_u16(duty_cycle)
        print("Set actuator to {}% stroke (pulse width: {:.2f} ms)".format(percentage, pulse_width_ms))

    def read_position(self):
        """
        Read the actuator position.
        The wiring produces an inverted response (0V at full extension). Thus,
        we invert the measured voltage so that:
          0V measured => 3.3V inverted => 100% stroke
          3.3V measured => 0V inverted => 0% stroke
        Returns:
          relative_percentage: position as a percentage (0-100% of stroke)
          absolute_position_mm: actuator position in millimeters (based on ACTUATOR_STROKE_LENGTH)
          raw_value: the raw ADC reading
          measured_voltage: the ADC voltage before inversion
        """
        raw_value = self.adc.read_u16()
        measured_voltage = raw_value * self.conversion_factor
        inverted_voltage = self.full_range_voltage - measured_voltage
        relative_percentage = (inverted_voltage / self.full_range_voltage) * 100
        absolute_position_mm = (relative_percentage / 100.0) * ACTUATOR_STROKE_LENGTH
        return relative_percentage, absolute_position_mm, raw_value, measured_voltage

async def position_task(actuator):
    """Continuously read and print the actuator position every 0.5 seconds."""
    while True:
        rel, abs_mm, raw, meas = actuator.read_position()
        print("Raw ADC: {:5d} | Voltage: {:.2f} V | Relative: {:.1f}% | Absolute: {:.1f} mm"
              .format(raw, meas, rel, abs_mm))
        await asyncio.sleep(0.5)

async def control_task(actuator):
    """Periodically set the actuator to new positions every 10 seconds."""
    positions = [0, 25, 50, 75, 100, 75, 50, 25]
    while True:
        for pos in positions:
            actuator.set_position(pos)
            await asyncio.sleep(10)

async def main():
    actuator = Actuator()
    # Create asynchronous tasks for live position reading and position control.
    task1 = asyncio.create_task(position_task(actuator))
    task2 = asyncio.create_task(control_task(actuator))
    await asyncio.gather(task1, task2)

# Run the asynchronous main function.
asyncio.run(main())
