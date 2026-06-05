import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# ============================================================
# Project 4A - Wokwi Simulated Hardware Test Bench
# Reads Wokwi Serial Monitor CSV data, cleans it, analyzes it,
# creates a voltage plot, summary text file, and PDF report.
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

REAL_WOKWI_FILE = ROOT / "data" / "wokwi_serial_log.csv"
SAMPLE_FILE = ROOT / "data" / "sample_wokwi_serial_log.csv"

PLOTS_DIR = ROOT / "plots"
REPORTS_DIR = ROOT / "reports"

PLOTS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)


def choose_data_file() -> Path:
    """
    Use real Wokwi data if it exists.
    Fall back to sample data only if real Wokwi data is missing.
    """
    if REAL_WOKWI_FILE.exists():
        return REAL_WOKWI_FILE

    if SAMPLE_FILE.exists():
        print("WARNING: data/wokwi_serial_log.csv was not found.")
        print("Using sample_wokwi_serial_log.csv instead.")
        return SAMPLE_FILE

    print("ERROR: No CSV data file found.")
    print(f"Expected: {REAL_WOKWI_FILE}")
    print(f"Or sample: {SAMPLE_FILE}")
    sys.exit(1)


def load_and_clean_data(data_file: Path) -> pd.DataFrame:
    """
    Loads Wokwi CSV data and cleans common Serial Monitor problems:
    - duplicate header rows
    - blank rows
    - bad numeric rows
    - extra spaces
    """

    df = pd.read_csv(data_file, dtype=str)

    required_columns = {"time_ms", "adc_value", "voltage", "status"}
    actual_columns = set(df.columns)

    if not required_columns.issubset(actual_columns):
        print("ERROR: CSV file does not have the correct header.")
        print("The first line must be:")
        print("time_ms,adc_value,voltage,status")
        print(f"Current columns found: {list(df.columns)}")
        sys.exit(1)

    # Remove duplicate header rows caused by restarting Wokwi simulation
    df = df[df["time_ms"].str.strip() != "time_ms"].copy()

    # Clean text
    df["status"] = df["status"].astype(str).str.strip().str.upper()

    # Convert numeric columns
    df["time_ms"] = pd.to_numeric(df["time_ms"], errors="coerce")
    df["adc_value"] = pd.to_numeric(df["adc_value"], errors="coerce")
    df["voltage"] = pd.to_numeric(df["voltage"], errors="coerce")

    # Drop bad rows
    df = df.dropna(subset=["time_ms", "adc_value", "voltage", "status"])

    # Keep only valid status values
    df = df[df["status"].isin(["NORMAL", "WARN", "FAIL"])].copy()

    # Sort by time
    df = df.sort_values("time_ms").reset_index(drop=True)

    if df.empty:
        print("ERROR: CSV file loaded, but no valid data rows were found.")
        print("Check your Wokwi Serial Monitor output.")
        sys.exit(1)

    return df


def determine_final_result(status_counts: dict) -> str:
    """
    Final result uses highest severity found in the whole run.
    """
    if status_counts.get("FAIL", 0) > 0:
        return "FAIL"
    if status_counts.get("WARN", 0) > 0:
        return "WARN"
    return "NORMAL"


def create_voltage_plot(df: pd.DataFrame) -> Path:
    """
    Creates voltage plot with WARN and FAIL thresholds.
    """

    plot_path = PLOTS_DIR / "wokwi_voltage_plot.png"

    plt.figure(figsize=(10, 6))
    plt.plot(df["time_ms"], df["voltage"], marker="o", label="Measured voltage")
    plt.axhline(y=3.0, linestyle="--", label="WARN threshold")
    plt.axhline(y=4.0, linestyle="--", label="FAIL threshold")
    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (V)")
    plt.title("Project 4A Wokwi ADC Voltage Test")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(plot_path, dpi=200)
    plt.close()

    return plot_path


def create_summary_text(
    data_file: Path,
    total_samples: int,
    min_adc: int,
    max_adc: int,
    min_voltage: float,
    max_voltage: float,
    avg_voltage: float,
    status_counts: dict,
    final_result: str,
) -> Path:
    """
    Creates text summary report.
    """

    summary_path = REPORTS_DIR / "project4a_summary.txt"

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("Project 4A Wokwi Simulated Hardware Test Bench\n")
        f.write("---------------------------------------------\n")
        f.write(f"Data file used: {data_file.name}\n")
        f.write(f"Total samples: {total_samples}\n")
        f.write(f"Min ADC: {min_adc}\n")
        f.write(f"Max ADC: {max_adc}\n")
        f.write(f"Min voltage: {min_voltage:.3f} V\n")
        f.write(f"Max voltage: {max_voltage:.3f} V\n")
        f.write(f"Average voltage: {avg_voltage:.3f} V\n")
        f.write(f"Status counts: {status_counts}\n")
        f.write(f"Final result: {final_result}\n")

    return summary_path


def create_pdf_report(
    data_file: Path,
    plot_path: Path,
    total_samples: int,
    min_adc: int,
    max_adc: int,
    min_voltage: float,
    max_voltage: float,
    avg_voltage: float,
    status_counts: dict,
    final_result: str,
) -> Path:
    """
    Creates PDF engineering report.
    """

    pdf_path = REPORTS_DIR / "project4a_wokwi_test_report.pdf"

    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    width, height = letter

    y = height - 60

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Project 4A - Wokwi Simulated Hardware Test Bench")

    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(
        50,
        y,
        "Purpose: Simulate a microcontroller ADC test workflow using Wokwi and Python analysis.",
    )

    y -= 25
    c.drawString(50, y, f"Data file used: {data_file.name}")

    y -= 35
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Engineering Summary")

    y -= 20
    c.setFont("Helvetica", 10)

    lines = [
        f"Total samples: {total_samples}",
        f"ADC range: {min_adc} to {max_adc}",
        f"Voltage range: {min_voltage:.3f} V to {max_voltage:.3f} V",
        f"Average voltage: {avg_voltage:.3f} V",
        f"Status counts: {status_counts}",
        f"Final result: {final_result}",
    ]

    for line in lines:
        c.drawString(70, y, line)
        y -= 16

    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Pass / Warn / Fail Logic")

    y -= 20
    c.setFont("Helvetica", 10)

    logic_lines = [
        "NORMAL: voltage < 3.0 V",
        "WARN: 3.0 V <= voltage < 4.0 V",
        "FAIL: voltage >= 4.0 V",
    ]

    for line in logic_lines:
        c.drawString(70, y, line)
        y -= 16

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Conclusion")

    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(
        70,
        y,
        f"The simulated ADC workflow completed with final result: {final_result}.",
    )
    y -= 16
    c.drawString(
        70,
        y,
        "This proves the data path from analog-style input to ADC conversion, classification,",
    )
    y -= 16
    c.drawString(
        70,
        y,
        "CSV logging, plotting, and automated engineering reporting.",
    )

    # Add plot on second page
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 60, "Voltage Plot")

    if plot_path.exists():
        c.drawImage(
            str(plot_path),
            50,
            170,
            width=500,
            height=300,
            preserveAspectRatio=True,
            anchor="c",
        )

    c.save()

    return pdf_path


def main() -> None:
    data_file = choose_data_file()
    df = load_and_clean_data(data_file)

    total_samples = len(df)
    min_adc = int(df["adc_value"].min())
    max_adc = int(df["adc_value"].max())
    min_voltage = float(df["voltage"].min())
    max_voltage = float(df["voltage"].max())
    avg_voltage = float(df["voltage"].mean())

    status_counts = df["status"].value_counts().to_dict()
    final_result = determine_final_result(status_counts)

    print("Project 4A Wokwi Simulated Hardware Test Bench")
    print("---------------------------------------------")
    print(f"Data file used: {data_file}")
    print(f"Total samples: {total_samples}")
    print(f"Min ADC: {min_adc}")
    print(f"Max ADC: {max_adc}")
    print(f"Min voltage: {min_voltage:.3f} V")
    print(f"Max voltage: {max_voltage:.3f} V")
    print(f"Average voltage: {avg_voltage:.3f} V")
    print(f"Status counts: {status_counts}")
    print(f"Final result: {final_result}")

    plot_path = create_voltage_plot(df)

    summary_path = create_summary_text(
        data_file=data_file,
        total_samples=total_samples,
        min_adc=min_adc,
        max_adc=max_adc,
        min_voltage=min_voltage,
        max_voltage=max_voltage,
        avg_voltage=avg_voltage,
        status_counts=status_counts,
        final_result=final_result,
    )

    pdf_path = create_pdf_report(
        data_file=data_file,
        plot_path=plot_path,
        total_samples=total_samples,
        min_adc=min_adc,
        max_adc=max_adc,
        min_voltage=min_voltage,
        max_voltage=max_voltage,
        avg_voltage=avg_voltage,
        status_counts=status_counts,
        final_result=final_result,
    )

    print(f"Saved plot to: {plot_path}")
    print(f"Saved summary to: {summary_path}")
    print(f"Saved PDF report to: {pdf_path}")


if __name__ == "__main__":
    main()