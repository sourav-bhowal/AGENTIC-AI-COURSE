import time

# This code simulates fetching weather and news data sequentially, which can take a significant amount of time due to the simulated delays.

def fetch_weather():
    print("Fetching weather data...")
    time.sleep(4)  # Simulate a delay in fetching data
    return {"temperature": 22, "condition": "Sunny"}

def fetch_news():
    print("Fetching news data...")
    time.sleep(2)  # Simulate a delay in fetching data
    return {"headline": "Breaking News!", "details": "Some important news details."}

def main():
    start_time = time.time()

    weather_data = fetch_weather()
    news_data = fetch_news()

    end_time = time.time()
    print(f"Weather Data: {weather_data}")
    print(f"News Data: {news_data}")
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()

