# Test Plan - Project 4A Wokwi Simulated Hardware Test Bench

## Objective
Verify that a simulated Arduino ADC circuit can read analog input, convert ADC counts to voltage, classify the result, and provide data for Python analysis.

## Test Input
Potentiometer connected to Arduino Uno analog pin A0.

## Pass / Warn / Fail Logic
- NORMAL: voltage < 3.0 V
- WARN: 3.0 V <= voltage < 4.0 V
- FAIL: voltage >= 4.0 V

## Evidence Required
- Wokwi circuit screenshot
- Serial monitor screenshot
- CSV log
- Python terminal summary
- Voltage plot
- PDF report
- README documentation

## Upgrade Path
Replace potentiometer with:
1. NTC thermistor
2. LM35 or TMP36 temperature sensor
3. Real Arduino hardware
4. Tiva-C TM4C123GXL hardware
