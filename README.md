# Project 4A - Wokwi Simulated Hardware Test Bench

## Overview

Project 4A is a simulated embedded hardware validation project built with Wokwi, Arduino-style ADC logic, and Python analysis.

The project simulates an Arduino Uno reading an analog voltage from a potentiometer, converting the ADC value into voltage, classifying the result as NORMAL, WARN, or FAIL, exporting serial CSV-style data, and using Python to generate plots, summaries, and a PDF engineering report.

This project is the bridge between my virtual Project 3 sensor logger and a future real-hardware Project 4 using Arduino, Tiva-C, ESP32, or Raspberry Pi Pico.

## Live Wokwi Simulation

[Open Project 4A in Wokwi](https://wokwi.com/projects/466029466313485313)

## Engineering Goal

The goal of this project is to prove a complete test and validation workflow:

```text
Simulated analog input
→ Arduino ADC reading
→ Voltage conversion
→ NORMAL / WARN / FAIL classification
→ Serial CSV output
→ Python data analysis
→ Voltage plot
→ Text summary
→ Automated PDF report
```

## Why This Project Matters

This project demonstrates the same thinking used in hardware test and validation roles:

* Define pass/warn/fail limits
* Collect repeatable measurement data
* Convert raw readings into engineering units
* Classify test results
* Save evidence files
* Generate plots and reports
* Document the workflow clearly

It is not real hardware yet. It is a simulated hardware test bench. The next upgrade is to repeat the same workflow with a real microcontroller and physical sensor.

## Tools Used

| Area                  | Tools                         |
| --------------------- | ----------------------------- |
| Simulation            | Wokwi                         |
| Microcontroller Model | Arduino Uno                   |
| Input Device          | Potentiometer                 |
| Embedded Logic        | Arduino C/C++                 |
| Data Output           | Serial Monitor CSV            |
| Analysis              | Python                        |
| Python Libraries      | pandas, matplotlib, reportlab |
| Documentation         | Markdown, PDF report          |

## Project Files

```text
Project_4A_Wokwi_Simulated_Hardware_Test_Bench/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .gitattributes
│
├── wokwi/
│   ├── sketch.ino
│   └── diagram.json
│
├── python/
│   └── analyze_wokwi_log.py
│
├── data/
│   ├── sample_wokwi_serial_log.csv
│   └── wokwi_serial_log.csv
│
├── plots/
│   └── wokwi_voltage_plot.png
│
├── reports/
│   ├── project4a_summary.txt
│   └── project4a_wokwi_test_report.pdf
│
├── docs/
│   ├── test_plan.md
│   └── engineering_notes.md
│
└── evidence/
    ├── wokwi_voltage_plot_stress_test.png
    ├── project4a_summary_stress_test.txt
    ├── project4a_report_stress_test.pdf
    ├── wokwi_voltage_plot_final_run.png
    ├── project4a_summary_final_run.txt
    └── project4a_report_final_run.pdf
```

## Wokwi Circuit

The Wokwi circuit uses:

* Arduino Uno
* Potentiometer
* Potentiometer signal connected to analog pin A0
* Potentiometer VCC connected to 5V
* Potentiometer GND connected to GND

The potentiometer acts as a simulated analog voltage source. Turning the knob changes the voltage read by the Arduino ADC.

## ADC Conversion

The Arduino Uno ADC produces a value from 0 to 1023.

The voltage conversion formula is:

```text
voltage = adc_value * 5.0 / 1023.0
```

Examples:

| ADC Value | Approx. Voltage |
| --------: | --------------: |
|         0 |         0.000 V |
|       512 |         2.502 V |
|      1023 |         5.000 V |

## Pass / Warn / Fail Logic

| Status | Condition                |
| ------ | ------------------------ |
| NORMAL | voltage < 3.0 V          |
| WARN   | 3.0 V <= voltage < 4.0 V |
| FAIL   | voltage >= 4.0 V         |

The final result uses the highest severity detected during the full run.

If any FAIL value appears, the final result is FAIL.
If no FAIL appears but WARN appears, the final result is WARN.
If all values are normal, the final result is NORMAL.

## Final Wokwi Potentiometer Validation Run

The final Wokwi simulation produced 48 valid ADC samples from an Arduino Uno reading a potentiometer on analog pin A0.

| Metric          |             Result |
| --------------- | -----------------: |
| Total samples   |                 48 |
| ADC range       |          0 to 1023 |
| Voltage range   | 0.000 V to 5.000 V |
| Average voltage |            2.607 V |
| NORMAL readings |                 38 |
| WARN readings   |                  3 |
| FAIL readings   |                  7 |
| Final result    |               FAIL |

The final result was FAIL because the simulated analog input crossed the 4.0 V failure threshold.

## Evidence Generated

The Python analysis script generates:

* Voltage plot
* Text summary report
* PDF engineering report

Output files:

```text
plots/wokwi_voltage_plot.png
reports/project4a_summary.txt
reports/project4a_wokwi_test_report.pdf
```

Archived evidence files are saved in:

```text
evidence/
```

## How to Run the Python Analysis

From the project folder, activate the virtual environment:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies if needed:

```powershell
pip install -r requirements.txt
```

Run the analysis:

```powershell
python .\python\analyze_wokwi_log.py
```

Open the generated outputs:

```powershell
explorer .\plots
explorer .\reports
explorer .\evidence
```

## How to Use the Wokwi Files

1. Open Wokwi.
2. Create a new Arduino Uno project.
3. Copy the contents of `wokwi/sketch.ino` into Wokwi’s `sketch.ino`.
4. Copy the contents of `wokwi/diagram.json` into Wokwi’s `diagram.json`.
5. Run the simulation.
6. Move the potentiometer knob to generate different ADC values.
7. Copy the Serial Monitor output.
8. Save the output into:

```text
data/wokwi_serial_log.csv
```

9. Run the Python analysis script again.

## Serial Output Format

The Arduino code prints data in CSV format:

```text
time_ms,adc_value,voltage,status
999,413,2.019,NORMAL
9007,860,4.203,FAIL
18016,640,3.128,WARN
```

Column meanings:

| Column    | Meaning                            |
| --------- | ---------------------------------- |
| time_ms   | Time since simulation start        |
| adc_value | Arduino ADC reading from 0 to 1023 |
| voltage   | Converted voltage                  |
| status    | NORMAL, WARN, or FAIL              |

## What I Learned

This project helped me practice:

* Simulated embedded hardware testing
* Arduino ADC input reading
* Voltage conversion from ADC counts
* Threshold-based validation logic
* Serial data formatting
* CSV-based engineering data analysis
* Python plotting
* Automated PDF reporting
* Evidence-based technical documentation

## Limitations

This project uses simulated hardware. It does not replace real hardware testing.

Real hardware would introduce additional issues such as:

* Wiring mistakes
* Sensor tolerance
* ADC noise
* Power supply variation
* Measurement error
* Calibration requirements
* Multimeter comparison
* Physical debugging

## Next Upgrade

The next upgrade is Project 4B:

```text
Wokwi NTC Thermistor Temperature Test Bench
```

That version will replace the potentiometer with a simulated temperature sensor or thermistor-style circuit. This will connect directly to my earlier NTC thermistor voltage divider project and make the workflow closer to real embedded sensor validation.

Future real-hardware upgrade:

```text
Arduino / Tiva-C / ESP32
→ real sensor
→ ADC reading
→ serial logging
→ Python analysis
→ plots
→ PDF report
```

## Resume Bullet

Built a Wokwi-based simulated embedded hardware test bench using Arduino Uno ADC logic and Python analysis to collect potentiometer-based analog readings, convert ADC counts to voltage, evaluate NORMAL/WARN/FAIL thresholds, generate CSV data, create voltage plots, and produce automated PDF validation reports.

## Interview Explanation

For Project 4A, I built a simulated hardware test bench in Wokwi using an Arduino Uno and potentiometer. The Arduino reads analog voltage on A0, converts ADC counts into voltage, classifies each reading as NORMAL, WARN, or FAIL, and prints CSV-style serial data. I then process that data in Python to generate statistics, plots, and a PDF engineering report. This project proves the validation pipeline before moving to real hardware.
