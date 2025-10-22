from gemini_call import gemini_data
import os

# Define the 5 topics with CSV-focused prompts
TOPICS = {
    "aqi": {
        "name": "Air Quality Index", 
        "file": "aqi.csv",
        "prompt": "Generate updated CSV data for global air quality index. Format: country_code,aqi,country_name. Include 50+ countries with realistic current AQI values. Only return the CSV data, no explanations."
    },
    "forest": {
        "name": "Forest/Deforestation",
        "file": "forest.csv",
        "prompt": "Generate updated CSV data for global deforestation rates. Format: country_code,deforestation_rate,country_name. Include 50+ countries with realistic current deforestation percentages. Only return the CSV data, no explanations."
    },
    "ocean_levels": {
        "name": "Ocean Levels", 
        "file": "ocean_levels.csv",
        "prompt": "Generate updated CSV data for ocean levels by region and year. Format: location,year,sea_level_mm. Include data for major regions from 2010-2024. Only return the CSV data, no explanations."
    },
    "severe_weather": {
        "name": "Severe Weather",
        "file": "severe_weather.csv", 
        "prompt": "Generate updated CSV data for severe weather events by continent. Format: location,year,# of Severe Weather Events. Include data for all continents from 2010-2024. Only return the CSV data, no explanations."
    },
    "temperature": {
        "name": "Global Temperature",
        "file": "temperature_data.csv",
        "prompt": "Generate updated CSV data for global temperature by country. Format: country_code,temperature_change,country_name. Include 50+ countries with realistic temperature change values. Only return the CSV data, no explanations."
    }
}

def update_all_climate_data():
    """Update all 5 CSV files with new Gemini-generated data"""    
    for topic_key, topic_info in TOPICS.items():
        try:            
            # Get new CSV data from Gemini
            csv_data = gemini_data(topic_info['prompt'])
            
            # Delete old CSV file if it exists
            csv_path = f"csv/{topic_info['file']}"
            if os.path.exists(csv_path):
                os.remove(csv_path)
                print(f"🗑️  Deleted old {topic_info['file']}")
            
            # Save new CSV data
            with open(csv_path, 'w') as f:
                f.write(csv_data)
            
            print(f"✅ Saved new {topic_info['file']}")
            
        except Exception as e:
            print(f"❌ Error updating {topic_info['name']}: {str(e)}")
    
if __name__ == "__main__":
    update_all_climate_data()