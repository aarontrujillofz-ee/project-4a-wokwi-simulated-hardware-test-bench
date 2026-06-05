# Engineering Notes

## Why Start with a Potentiometer?
A potentiometer is the cleanest first ADC test input. It lets the user manually sweep voltage from low to high and verify ADC conversion before adding sensor math.

## ADC Formula
For Arduino Uno:

voltage = adc_value * 5.0 / 1023.0

## Validation Meaning
This project proves the test workflow:

input signal -> ADC reading -> voltage conversion -> status classification -> CSV data -> Python analysis -> plot/report evidence.

## Limitation
This is simulated hardware. It does not replace real hardware evidence because real systems include noise, wiring issues, measurement error, ADC tolerance, and calibration problems.
