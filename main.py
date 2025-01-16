from generate_report import load_data, clean_data, generate_report
from visualization import generate_chart

if __name__ == "__main__":
    # File paths
    input_file = "people_data.xml"
    report_file = "report.json"
    chart_file = "age_by_city.png"

    # Step 1: Load data from XML
    print("Loading data...")
    df = load_data(input_file)

    # Step 2: Clean the data
    print("Cleaning data...")
    df = clean_data(df)

    # Step 3: Generate report
    print(f"Generating report and saving to {report_file}...")
    generate_report(df, report_file)

    # Step 4: Generate chart
    print(f"Generating chart and saving to {chart_file}...")
    generate_chart(df, chart_file)

    print("Process completed successfully!")
