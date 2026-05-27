import sys
import os
import pandas as pd

# Add project root to Python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from backend.app.services.analysis_pipeline import AnalysisPipeline
from backend.app.services.report_generator import ReportGenerator


def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Change filename here to test different scenarios
    csv_path = os.path.join(BASE_DIR, "sample_data", "failing_startup.csv")

    df = pd.read_csv(csv_path)

    # Initialize pipeline
    pipeline = AnalysisPipeline(
        df=df,
        founder_equity=55.0,
        simulation_runs=5000
    )

    # Run analysis
    results = pipeline.run_full_analysis()

    print("\n===== FULL ANALYSIS RESULTS =====\n")

    for section, data in results.items():
        print(f"\n--- {section.upper()} ---")
        for key, value in data.items():
            print(f"{key}: {value}")

    # Generate investor summary
    report = ReportGenerator(results)
    summary = report.generate_summary()

    print("\n===== INVESTOR SUMMARY =====\n")
    print(summary)


if __name__ == "__main__":
    main()
