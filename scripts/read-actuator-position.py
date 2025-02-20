from machine import ADC, Pin
import time

# Initialize ADC on GP28
adc = ADC(Pin(28))

# The Pico's ADC is 16-bit (0-65535) with a 3.3V reference.
conversion_factor = 3.3 / 65535

while True:
    # Read the raw ADC value (0 to 65535)
    raw_value = adc.read_u16()
    
    # Convert the raw reading to the measured voltage at the ADC pin
    measured_voltage = raw_value * conversion_factor
    
    # Calculate the position percentage assuming 0V = 0% and 3.3V = 100%
    position_percent = (measured_voltage / 3.3) * 100
    
    print("Raw ADC: {:5d} | Voltage: {:.2f} V | Position: {:.1f}%"
          .format(raw_value, measured_voltage, position_percent))
    
    time.sleep(1)
