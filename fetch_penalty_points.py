import pandas as pd
import json
import os
import requests
from bs4 import BeautifulSoup
import re

def fetch_penalty_points():
    """
    Fetches the F1 penalty points table from Liquipedia and processes it into JSON formats.
    """
    url = "https://liquipedia.net/formula1/Penalty_Points"
    
    # Fetch the table using pandas
    tables = pd.read_html(url)
    main_table = tables[0]  # The first table contains the penalty points
    
    # Process the data into a more structured format
    drivers_data = process_table_data(main_table)
    
    # Save the detailed data
    save_detailed_json(drivers_data)
    
    # Save chart-friendly data
    save_chart_json(drivers_data)
    
    print("Penalty points data successfully fetched and saved!")

def process_table_data(df):
    """Process the pandas DataFrame into a structured format."""
    # Group by driver
    grouped_data = []
    
    # Get unique drivers
    drivers = df['Driver'].unique()
    
    for driver in drivers:
        driver_rows = df[df['Driver'] == driver]
        
        # Get total points for this driver
        total_points = driver_rows['Total Points'].iloc[0]
        
        # Create driver entry
        driver_data = {
            "driver": driver.strip(),
            "totalPoints": int(total_points),
            "incidents": []
        }
        
        # Add each incident
        for _, row in driver_rows.iterrows():
            if pd.notna(row['Points']):  # Skip rows without points (usually the first row)
                incident = {
                    "points": int(row['Points']),
                    "expiryDate": row['Expiry Date'],
                    "grandPrix": row['Grand Prix'],
                    "reason": row['Reason']
                }
                driver_data["incidents"].append(incident)
        
        grouped_data.append(driver_data)
    
    return grouped_data

def save_detailed_json(data, filename="penalty_points.json"):
    """Save the detailed structured data as JSON."""
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Save to JSON file
    filepath = os.path.join("data", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    
    print(f"Detailed data saved to {filepath}")
    return filepath

def save_chart_json(data, filename="penalty_points_chart.json"):
    """Create a simplified version of the data that's friendly for charts."""
    chart_data = []
    
    for driver in data:
        chart_data.append({
            "name": driver["driver"],
            "points": driver["totalPoints"]
        })
    
    # Sort by points in descending order
    chart_data.sort(key=lambda x: x["points"], reverse=True)
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Save to JSON file
    filepath = os.path.join("data", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(chart_data, f, indent=2)
    
    print(f"Chart-friendly data saved to {filepath}")
    return filepath

if __name__ == "__main__":
    fetch_penalty_points()
