"""Weather Tool Usage Example

This example demonstrates how to use the Canvas API to create
a conversation that includes tool usage using the shared CanvasClient instance.
"""

from __future__ import annotations

import json
import time

from examples.shared_client import get_canvas_client
from llm_canvas.types import Message


def simulate_weather_api(location: str, unit: str = "fahrenheit") -> dict:
    """Simulate a weather API call."""
    time.sleep(0.3)  # Simulate API call delay
    return {
        "location": location,
        "temperature": 68,
        "condition": "Partly cloudy",
        "humidity": 72,
        "wind_speed": 8,
        "wind_direction": "NW",
        "visibility": 10,
        "uv_index": 6,
        "unit": unit,
    }


def simulate_forecast_api(location: str, days: int = 1, unit: str = "fahrenheit") -> dict:
    """Simulate a weather forecast API call."""
    time.sleep(0.3)  # Simulate API call delay
    return {
        "location": location,
        "date": "2025-08-09",
        "high_temp": 72,
        "low_temp": 58,
        "condition": "Light rain",
        "precipitation_chance": 75,
        "precipitation_amount": 0.15,
        "humidity": 85,
        "wind_speed": 12,
        "wind_direction": "SW",
        "unit": unit,
        "days": days,
    }


def weather_inquiry() -> None:
    """Create a weather inquiry conversation with tool usage."""
    # Get the shared client
    client = get_canvas_client()

    # Create a new canvas via the client
    canvas = client.create_canvas(
        title="Weather Inquiry", description="A conversation demonstrating tool usage for weather queries"
    )

    # Get the main branch for committing messages
    main_branch = canvas.checkout()

    print("🌤️ Creating Weather Tool Usage example...")

    # Step 1: User asks about weather
    print("\n1️⃣ User asks about San Francisco weather")
    user_message: Message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What's the weather like in San Francisco today?",
            }
        ],
    }
    main_branch.commit_message(user_message)

    # Step 2: Assistant responds with tool use
    print("2️⃣ Assistant responds with tool use")
    time.sleep(0.2)
    assistant_tool_message: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "I'll check the current weather in San Francisco for you.",
            },
            {
                "type": "tool_use",
                "id": "weather_tool_001",
                "name": "get_weather",
                "input": {
                    "location": "San Francisco, CA",
                    "unit": "fahrenheit",
                },
            },
        ],
    }
    main_branch.commit_message(assistant_tool_message)

    # Step 3: Tool result (simulated)
    print("3️⃣ Tool execution and result")
    weather_data = simulate_weather_api("San Francisco, CA", "fahrenheit")
    tool_result_message: Message = {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": "weather_tool_001",
                "content": json.dumps(weather_data),
            }
        ],
    }
    main_branch.commit_message(tool_result_message)

    # Step 4: Assistant interprets the results
    print("4️⃣ Assistant interprets weather data")
    time.sleep(0.2)
    weather_response: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Based on the current weather data, here's what it's like in San Francisco today:

🌤️ **Partly Cloudy** - 68°F

**Details:**
- Humidity: 72%
- Wind: 8 mph from the Northwest
- Visibility: 10 miles
- UV Index: 6 (moderate)

It's a pleasant day with comfortable temperatures! The partly cloudy conditions mean you'll have some sun but also some cloud cover. Perfect weather for outdoor activities, though you might want to bring a light jacket if you'll be out in the evening as San Francisco can cool down quickly.""",  # noqa: E501
            }
        ],
    }
    main_branch.commit_message(weather_response)

    # Step 5: User asks follow-up question
    print("5️⃣ User asks about tomorrow's weather")
    followup_message: Message = {"content": [{"type": "text", "text": "What about tomorrow? Will it rain?"}], "role": "user"}
    main_branch.commit_message(followup_message)

    # Step 6: Assistant uses forecast tool
    print("6️⃣ Assistant uses forecast tool")
    time.sleep(0.2)
    forecast_tool_message: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "Let me check tomorrow's forecast for San Francisco.",
            },
            {
                "type": "tool_use",
                "id": "weather_tool_002",
                "name": "get_weather_forecast",
                "input": {
                    "location": "San Francisco, CA",
                    "days": 1,
                    "unit": "fahrenheit",
                },
            },
        ],
    }
    main_branch.commit_message(forecast_tool_message)

    # Step 7: Forecast tool result
    print("7️⃣ Forecast tool execution")
    forecast_data = simulate_forecast_api("San Francisco, CA", 1, "fahrenheit")
    forecast_result_message: Message = {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": "weather_tool_002",
                "content": json.dumps(forecast_data),
            }
        ],
    }
    main_branch.commit_message(forecast_result_message)

    # Step 8: Final assistant response
    print("8️⃣ Assistant provides forecast analysis")
    time.sleep(0.2)
    forecast_response: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Yes, it looks like tomorrow will bring some rain to San Francisco! Here's the forecast:

🌧️ **Light Rain Expected**

**Tomorrow's Weather:**
- High: 72°F, Low: 58°F
- Condition: Light rain
- Chance of precipitation: 75%
- Expected rainfall: 0.15 inches
- Humidity: 85%
- Wind: 12 mph from the Southwest

**Recommendations:**
- Definitely bring an umbrella or rain jacket
- The rain should be light, so it won't be too heavy
- Temperatures will be similar to today, just a bit more humid
- Great day for indoor activities or cozy coffee shop visits!

The Southwest wind pattern often brings moisture from the Pacific, which explains the increased chance of rain.""",
            }
        ],
    }
    main_branch.commit_message(forecast_response)

    print("✅ Weather Tool Usage example completed! Canvas available at server.")


if __name__ == "__main__":
    weather_inquiry()
