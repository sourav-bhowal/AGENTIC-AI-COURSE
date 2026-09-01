import asyncio
import time

# This code demonstrates how to fetch weather and news data concurrently using asynchronous programming with asyncio, which can significantly reduce the total time taken compared to sequential execution.

async def fetch_weather():
    print("Fetching weather data...")
    await asyncio.sleep(4)  # Simulate delay
    return "Weather data: Sunny, 25°C"

async def fetch_news():
    print("Fetching news data...")
    await asyncio.sleep(2)  # Simulate delay
    return "News data: Breaking News!"

async def main():
    start_time = time.time()
    # Fetch both weather and news data concurrently
    weather, news = await asyncio.gather(fetch_weather(), fetch_news())

    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print(weather)
    print(news)


# Wrap the main function call in asyncio.run() to execute the asynchronous code
asyncio.run(main())