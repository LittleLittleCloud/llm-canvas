"""Mock canvas data for testing and development.

This module provides pre-built canvas examples that demonstrate various features
of the llm_canvas system, including simple conversations, tool usage, and branched
conversations.
"""

import json
import time
from typing import Any, Dict

# Current timestamp for consistent mock data
_current_time = time.time()


def _create_canvas_data(
    canvas_id: str, title: str, root_ids: list, nodes: Dict[str, Any]
) -> Dict[str, Any]:
    """Helper to create canvas data structure."""
    return {
        "canvas_id": canvas_id,
        "title": title,
        "created_at": _current_time,
        "root_ids": root_ids,
        "nodes": nodes,
    }


# Simple hello canvas
hello_canvas = _create_canvas_data(
    canvas_id="hello-canvas",
    title="Hello Canvas",
    root_ids=["n1"],
    nodes={
        "n1": {
            "id": "n1",
            "content": {
                "role": "user",
                "content": [{"type": "text", "text": "Hello model"}],
            },
            "parent_id": None,
            "child_ids": ["n2"],
            "meta": {"timestamp": _current_time},
        },
        "n2": {
            "id": "n2",
            "content": {
                "role": "assistant",
                "content": [{"type": "text", "text": "Model reply"}],
            },
            "parent_id": "n1",
            "child_ids": [],
            "meta": {"timestamp": _current_time},
        },
    },
)

# Weather inquiry canvas with tool usage
weather_canvas = _create_canvas_data(
    canvas_id="weather-canvas",
    title="Weather Inquiry",
    root_ids=["w1"],
    nodes={
        "w1": {
            "id": "w1",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's the weather like in San Francisco today?",
                    }
                ],
            },
            "parent_id": None,
            "child_ids": ["w2"],
            "meta": {"timestamp": _current_time},
        },
        "w2": {
            "id": "w2",
            "content": {
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
            },
            "parent_id": "w1",
            "child_ids": ["w3"],
            "meta": {"timestamp": _current_time},
        },
        "w3": {
            "id": "w3",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": "weather_tool_001",
                        "content": json.dumps(
                            {
                                "location": "San Francisco, CA",
                                "temperature": 68,
                                "condition": "Partly cloudy",
                                "humidity": 72,
                                "wind_speed": 8,
                                "wind_direction": "NW",
                                "visibility": 10,
                                "uv_index": 6,
                            }
                        ),
                    }
                ],
            },
            "parent_id": "w2",
            "child_ids": ["w4"],
            "meta": {"timestamp": _current_time},
        },
        "w4": {
            "id": "w4",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Based on the current weather data, here's what it's like in San Francisco today:\n\n🌤️ **Partly Cloudy** - 68°F\n\n**Details:**\n- Humidity: 72%\n- Wind: 8 mph from the Northwest\n- Visibility: 10 miles\n- UV Index: 6 (moderate)\n\nIt's a pleasant day with comfortable temperatures! The partly cloudy conditions mean you'll have some sun but also some cloud cover. Perfect weather for outdoor activities, though you might want to bring a light jacket if you'll be out in the evening as San Francisco can cool down quickly.",
                    }
                ],
            },
            "parent_id": "w3",
            "child_ids": ["w5"],
            "meta": {"timestamp": _current_time},
        },
        "w5": {
            "id": "w5",
            "content": {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What about tomorrow? Will it rain?"}
                ],
            },
            "parent_id": "w4",
            "child_ids": ["w6"],
            "meta": {"timestamp": _current_time},
        },
        "w6": {
            "id": "w6",
            "content": {
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
            },
            "parent_id": "w5",
            "child_ids": ["w7"],
            "meta": {"timestamp": _current_time},
        },
        "w7": {
            "id": "w7",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": "weather_tool_002",
                        "content": json.dumps(
                            {
                                "location": "San Francisco, CA",
                                "date": "2025-08-09",
                                "high_temp": 72,
                                "low_temp": 58,
                                "condition": "Light rain",
                                "precipitation_chance": 75,
                                "precipitation_amount": 0.15,
                                "humidity": 85,
                                "wind_speed": 12,
                                "wind_direction": "SW",
                            }
                        ),
                    }
                ],
            },
            "parent_id": "w6",
            "child_ids": ["w8"],
            "meta": {"timestamp": _current_time},
        },
        "w8": {
            "id": "w8",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Yes, it looks like tomorrow will bring some rain to San Francisco! Here's the forecast:\n\n🌧️ **Light Rain Expected**\n\n**Tomorrow's Weather:**\n- High: 72°F, Low: 58°F\n- Condition: Light rain\n- Chance of precipitation: 75%\n- Expected rainfall: 0.15 inches\n- Humidity: 85%\n- Wind: 12 mph from the Southwest\n\n**Recommendations:**\n- Definitely bring an umbrella or rain jacket\n- The rain should be light, so it won't be too heavy\n- Temperatures will be similar to today, just a bit more humid\n- Great day for indoor activities or cozy coffee shop visits!\n\nThe Southwest wind pattern often brings moisture from the Pacific, which explains the increased chance of rain.",
                    }
                ],
            },
            "parent_id": "w7",
            "child_ids": [],
            "meta": {"timestamp": _current_time},
        },
    },
)

# Branched conversation canvas (vacation planning)
branched_canvas = _create_canvas_data(
    canvas_id="branched-canvas",
    title="Vacation Planning",
    root_ids=["b1"],
    nodes={
        "b1": {
            "id": "b1",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I'm planning a vacation. Should I go to Japan or Italy?",
                    }
                ],
            },
            "parent_id": None,
            "child_ids": ["b2"],
            "meta": {"timestamp": _current_time},
        },
        "b2": {
            "id": "b2",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Both Japan and Italy are incredible destinations! The choice depends on what kind of experience you're looking for. Let me help you explore both options to make the best decision for your preferences.",
                    }
                ],
            },
            "parent_id": "b1",
            "child_ids": ["b3a", "b3b"],
            "meta": {"timestamp": _current_time},
        },
        # Branch A: Japan path
        "b3a": {
            "id": "b3a",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Tell me more about Japan. I'm interested in culture and technology.",
                    }
                ],
            },
            "parent_id": "b2",
            "child_ids": ["b4a"],
            "meta": {"timestamp": _current_time, "branch": "japan"},
        },
        "b4a": {
            "id": "b4a",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Japan is perfect for culture and technology enthusiasts! Here's what makes it special:\n\n🏮 **Cultural Highlights:**\n- Ancient temples and shrines (Kyoto has over 2,000!)\n- Traditional tea ceremonies and gardens\n- Authentic geisha districts\n- Rich samurai history and castles\n- Traditional ryokan (inn) experiences\n\n🤖 **Technology & Innovation:**\n- Tokyo's high-tech districts like Akihabara and Shibuya\n- Bullet trains (shinkansen) - engineering marvels\n- Robot restaurants and cafes\n- Cutting-edge gaming arcades\n- Advanced automation in daily life\n\n**Best Time:** Spring (cherry blossoms) or Fall (autumn colors)\n**Duration:** 10-14 days to see both traditional and modern sides",
                    }
                ],
            },
            "parent_id": "b3a",
            "child_ids": ["b5a"],
            "meta": {"timestamp": _current_time, "branch": "japan"},
        },
        "b5a": {
            "id": "b5a",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What about the food scene? I'm quite adventurous with food.",
                    }
                ],
            },
            "parent_id": "b4a",
            "child_ids": ["b6a"],
            "meta": {"timestamp": _current_time, "branch": "japan"},
        },
        "b6a": {
            "id": "b6a",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Japan's food scene is absolutely incredible for adventurous eaters! 🍣\n\n**Unique Experiences:**\n- Tsukiji Fish Market (dawn tuna auctions)\n- Authentic sushi omakase experiences\n- Ramen crawls through different regional styles\n- Kaiseki (traditional multi-course) dining\n- Street food in Osaka (takoyaki, okonomiyaki)\n\n**Adventurous Options:**\n- Fugu (carefully prepared pufferfish)\n- Natto (fermented soybeans)\n- Raw horse sashimi (basashi)\n- Sea urchin and unusual seafood\n- Insects and exotic game meats\n\n**Food Culture:**\n- No tipping culture\n- Vending machine restaurants\n- Conveyor belt sushi\n- Department store food courts (depachika)\n\nJapan offers both comfort and challenge for food lovers!",
                    }
                ],
            },
            "parent_id": "b5a",
            "child_ids": [],
            "meta": {"timestamp": _current_time, "branch": "japan"},
        },
        # Branch B: Italy path
        "b3b": {
            "id": "b3b",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What about Italy? I love art, history, and great food.",
                    }
                ],
            },
            "parent_id": "b2",
            "child_ids": ["b4b"],
            "meta": {"timestamp": _current_time, "branch": "italy"},
        },
        "b4b": {
            "id": "b4b",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Italy is a dream destination for art, history, and food lovers! Here's why it's magical:\n\n🎨 **Art & History:**\n- Vatican Museums and Sistine Chapel\n- Uffizi Gallery in Florence (Renaissance masterpieces)\n- Colosseum and Roman Forum\n- Pompeii's preserved ancient city\n- Michelangelo's David and countless sculptures\n- Medieval hill towns like San Gimignano\n\n🍝 **Culinary Paradise:**\n- Regional specialties (each city has unique dishes)\n- Fresh pasta made daily\n- World-class wines (Chianti, Barolo, Prosecco)\n- Authentic gelato and espresso culture\n- Pizza in its birthplace (Naples)\n\n**Romance & Atmosphere:**\n- Gondola rides in Venice\n- Tuscan countryside vineyards\n- Amalfi Coast's dramatic coastline\n- Charming piazzas perfect for people-watching",
                    }
                ],
            },
            "parent_id": "b3b",
            "child_ids": ["b5b"],
            "meta": {"timestamp": _current_time, "branch": "italy"},
        },
        "b5b": {
            "id": "b5b",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "How long should I plan for Italy, and what's the best route?",
                    }
                ],
            },
            "parent_id": "b4b",
            "child_ids": ["b6b"],
            "meta": {"timestamp": _current_time, "branch": "italy"},
        },
        "b6b": {
            "id": "b6b",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "For Italy, I'd recommend 10-14 days minimum to really savor the experience! 🇮🇹\n\n**Classic Route (North to South):**\n\n**Days 1-3: Rome** 🏛️\n- Vatican, Colosseum, Trevi Fountain\n- Trastevere neighborhood for authentic dining\n\n**Days 4-6: Florence** 🎨\n- Uffizi Gallery, Duomo, Ponte Vecchio\n- Day trip to Siena or Pisa\n\n**Days 7-9: Venice** 🛶\n- St. Mark's Square, Doge's Palace\n- Murano and Burano islands\n\n**Days 10-12: Amalfi Coast** 🌊\n- Positano, Amalfi, Ravello\n- Limoncello tastings and coastal views\n\n**Optional Extensions:**\n- Tuscany wine country (Chianti region)\n- Cinque Terre hiking\n- Milan for fashion and business\n\n**Transportation:** High-speed trains connect major cities beautifully. The journey becomes part of the experience with stunning countryside views!",
                    }
                ],
            },
            "parent_id": "b5b",
            "child_ids": [],
            "meta": {"timestamp": _current_time, "branch": "italy"},
        },
    },
)

# Branched tool canvas with investment decision
branched_tool_canvas = _create_canvas_data(
    canvas_id="branched-tool-canvas",
    title="Investment Decision",
    root_ids=["bt1"],
    nodes={
        "bt1": {
            "id": "bt1",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I'm planning to invest $10,000. Should I put it in stocks or real estate?",
                    }
                ],
            },
            "parent_id": None,
            "child_ids": ["bt2"],
            "meta": {"timestamp": _current_time},
        },
        "bt2": {
            "id": "bt2",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Great question! Both stocks and real estate can be excellent investment options. Let me help you explore both paths by analyzing current market conditions and opportunities for each.",
                    }
                ],
            },
            "parent_id": "bt1",
            "child_ids": ["bt3a", "bt3b"],
            "meta": {"timestamp": _current_time},
        },
        # Branch A: Stock Investment Path
        "bt3a": {
            "id": "bt3a",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Let's explore the stock market option. What are the current market conditions?",
                    }
                ],
            },
            "parent_id": "bt2",
            "child_ids": ["bt4a"],
            "meta": {"timestamp": _current_time, "branch": "stocks"},
        },
        "bt4a": {
            "id": "bt4a",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "I'll check the current stock market conditions and analyze some potential investment opportunities for you.",
                    },
                    {
                        "type": "tool_use",
                        "id": "market_analysis_001",
                        "name": "get_market_data",
                        "input": {
                            "symbols": ["SPY", "QQQ", "VTI"],
                            "timeframe": "1M",
                            "include_fundamentals": True,
                        },
                    },
                ],
            },
            "parent_id": "bt3a",
            "child_ids": ["bt5a"],
            "meta": {"timestamp": _current_time, "branch": "stocks"},
        },
        "bt5a": {
            "id": "bt5a",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": "market_analysis_001",
                        "content": json.dumps(
                            {
                                "market_summary": {
                                    "trend": "bullish",
                                    "volatility": "moderate",
                                    "risk_sentiment": "cautious optimism",
                                },
                                "symbols": {
                                    "SPY": {
                                        "price": 445.3,
                                        "change_percent": 1.2,
                                        "pe_ratio": 21.5,
                                        "dividend_yield": 1.3,
                                    },
                                    "QQQ": {
                                        "price": 378.9,
                                        "change_percent": 1.8,
                                        "pe_ratio": 26.4,
                                        "dividend_yield": 0.6,
                                    },
                                    "VTI": {
                                        "price": 248.7,
                                        "change_percent": 1.1,
                                        "pe_ratio": 22.1,
                                        "dividend_yield": 1.4,
                                    },
                                },
                            }
                        ),
                    }
                ],
            },
            "parent_id": "bt4a",
            "child_ids": ["bt6a"],
            "meta": {"timestamp": _current_time, "branch": "stocks"},
        },
        "bt6a": {
            "id": "bt6a",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Excellent! The current market analysis shows promising conditions for stock investment:\n\n📈 **Market Overview:**\n- **Trend:** Bullish with cautious optimism\n- **Volatility:** Moderate (good for entry)\n- **Risk Sentiment:** Positive but measured\n\n**Top ETF Options for $10,000:**\n\n🏛️ **SPY (S&P 500)** - $445.30 (+1.2%)\n- Broad market exposure\n- P/E Ratio: 21.5 (reasonable valuation)\n- Dividend Yield: 1.3%\n\n💻 **QQQ (NASDAQ-100)** - $378.90 (+1.8%)\n- Tech-heavy, higher growth potential\n- P/E Ratio: 26.4 (premium for growth)\n- Dividend Yield: 0.6%\n\n🌍 **VTI (Total Stock Market)** - $248.70 (+1.1%)\n- Complete US market diversification\n- P/E Ratio: 22.1 (balanced)\n- Dividend Yield: 1.4%\n\n**Recommendation:** Consider a diversified approach with 60% VTI, 30% SPY, 10% QQQ for balanced growth and stability.",
                    }
                ],
            },
            "parent_id": "bt5a",
            "child_ids": ["bt7a"],
            "meta": {"timestamp": _current_time, "branch": "stocks"},
        },
        "bt7a": {
            "id": "bt7a",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What about individual stocks? Can you analyze some tech companies?",
                    }
                ],
            },
            "parent_id": "bt6a",
            "child_ids": ["bt8a"],
            "meta": {"timestamp": _current_time, "branch": "stocks"},
        },
        "bt8a": {
            "id": "bt8a",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Let me analyze some major tech companies for potential individual stock investments.",
                    },
                    {
                        "type": "tool_use",
                        "id": "stock_analysis_002",
                        "name": "analyze_stocks",
                        "input": {
                            "symbols": ["AAPL", "MSFT", "GOOGL", "NVDA"],
                            "analysis_type": "fundamental",
                            "include_technicals": True,
                        },
                    },
                ],
            },
            "parent_id": "bt7a",
            "child_ids": ["bt9a"],
            "meta": {"timestamp": _current_time, "branch": "stocks"},
        },
        "bt9a": {
            "id": "bt9a",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": "stock_analysis_002",
                        "content": json.dumps(
                            {
                                "stocks": {
                                    "AAPL": {
                                        "price": 189.5,
                                        "pe_ratio": 28.5,
                                        "growth_rate": 8.2,
                                        "risk_score": "medium",
                                        "recommendation": "buy",
                                        "target_price": 205,
                                    },
                                    "MSFT": {
                                        "price": 378.85,
                                        "pe_ratio": 32.1,
                                        "growth_rate": 12.5,
                                        "risk_score": "low",
                                        "recommendation": "strong_buy",
                                        "target_price": 420,
                                    },
                                    "GOOGL": {
                                        "price": 138.75,
                                        "pe_ratio": 24.8,
                                        "growth_rate": 10.1,
                                        "risk_score": "medium",
                                        "recommendation": "buy",
                                        "target_price": 155,
                                    },
                                    "NVDA": {
                                        "price": 875.2,
                                        "pe_ratio": 65.4,
                                        "growth_rate": 45.2,
                                        "risk_score": "high",
                                        "recommendation": "hold",
                                        "target_price": 950,
                                    },
                                },
                            }
                        ),
                    }
                ],
            },
            "parent_id": "bt8a",
            "child_ids": ["bt10a"],
            "meta": {"timestamp": _current_time, "branch": "stocks"},
        },
        "bt10a": {
            "id": "bt10a",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Here's the analysis of major tech stocks:\n\n🍎 **Apple (AAPL)** - $189.50\n- P/E: 28.5 | Growth: 8.2% | Risk: Medium\n- **Recommendation: BUY** (Target: $205)\n- Stable dividend, strong ecosystem\n\n🪟 **Microsoft (MSFT)** - $378.85\n- P/E: 32.1 | Growth: 12.5% | Risk: Low\n- **Recommendation: STRONG BUY** (Target: $420)\n- Cloud dominance, AI leadership\n\n🔍 **Alphabet (GOOGL)** - $138.75\n- P/E: 24.8 | Growth: 10.1% | Risk: Medium\n- **Recommendation: BUY** (Target: $155)\n- Search monopoly, reasonable valuation\n\n🎮 **NVIDIA (NVDA)** - $875.20\n- P/E: 65.4 | Growth: 45.2% | Risk: High\n- **Recommendation: HOLD** (Target: $950)\n- AI boom driver but expensive\n\n**$10K Portfolio Suggestion:**\n- $4,000 MSFT (40%)\n- $3,000 AAPL (30%)\n- $2,000 GOOGL (20%)\n- $1,000 NVDA (10%)\n\nThis balances growth potential with risk management!",
                    }
                ],
            },
            "parent_id": "bt9a",
            "child_ids": [],
            "meta": {"timestamp": _current_time, "branch": "stocks"},
        },
        # Branch B: Real Estate Investment Path
        "bt3b": {
            "id": "bt3b",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What about real estate? Can you analyze the current market and opportunities?",
                    }
                ],
            },
            "parent_id": "bt2",
            "child_ids": ["bt4b"],
            "meta": {"timestamp": _current_time, "branch": "real_estate"},
        },
        "bt4b": {
            "id": "bt4b",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Let me analyze the current real estate market conditions and find investment opportunities suitable for your $10,000 budget.",
                    },
                    {
                        "type": "tool_use",
                        "id": "real_estate_001",
                        "name": "get_real_estate_data",
                        "input": {
                            "budget": 10000,
                            "investment_types": ["REIT", "crowdfunding", "fractional"],
                            "regions": ["national", "high_growth_markets"],
                        },
                    },
                ],
            },
            "parent_id": "bt3b",
            "child_ids": ["bt5b"],
            "meta": {"timestamp": _current_time, "branch": "real_estate"},
        },
        "bt5b": {
            "id": "bt5b",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": "real_estate_001",
                        "content": json.dumps(
                            {
                                "market_conditions": {
                                    "interest_rates": 6.8,
                                    "home_price_trend": "stabilizing",
                                    "rental_demand": "strong",
                                    "investment_outlook": "cautiously optimistic",
                                },
                                "investment_options": {
                                    "REITs": {
                                        "avg_dividend_yield": 4.2,
                                        "price_appreciation": 2.1,
                                        "liquidity": "high",
                                        "min_investment": 100,
                                    },
                                    "real_estate_crowdfunding": {
                                        "avg_returns": 8.5,
                                        "investment_period": "2-5 years",
                                        "liquidity": "low",
                                        "min_investment": 1000,
                                    },
                                    "fractional_ownership": {
                                        "avg_returns": 6.2,
                                        "property_types": ["residential", "commercial"],
                                        "liquidity": "medium",
                                        "min_investment": 5000,
                                    },
                                },
                            }
                        ),
                    }
                ],
            },
            "parent_id": "bt4b",
            "child_ids": ["bt6b"],
            "meta": {"timestamp": _current_time, "branch": "real_estate"},
        },
        "bt6b": {
            "id": "bt6b",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Here's the real estate investment landscape for your $10,000:\n\n🏠 **Market Conditions:**\n- Interest Rates: 6.8% (moderately high)\n- Home Prices: Stabilizing after recent peaks\n- Rental Demand: Strong across markets\n- Outlook: Cautiously optimistic\n\n**Investment Options:**\n\n🏢 **REITs (Real Estate Investment Trusts)**\n- Average Dividend Yield: 4.2%\n- Price Appreciation: 2.1%\n- Liquidity: High (trade like stocks)\n- Min Investment: $100\n\n🤝 **Real Estate Crowdfunding**\n- Average Returns: 8.5%\n- Investment Period: 2-5 years\n- Liquidity: Low (money tied up)\n- Min Investment: $1,000\n\n🏘️ **Fractional Ownership**\n- Average Returns: 6.2%\n- Property Types: Residential & Commercial\n- Liquidity: Medium\n- Min Investment: $5,000\n\n**$10K Strategy:** Mix REITs (60% = $6K) for liquidity + Crowdfunding (40% = $4K) for higher returns",
                    }
                ],
            },
            "parent_id": "bt5b",
            "child_ids": ["bt7b"],
            "meta": {"timestamp": _current_time, "branch": "real_estate"},
        },
        "bt7b": {
            "id": "bt7b",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Can you find specific REIT recommendations and crowdfunding platforms?",
                    }
                ],
            },
            "parent_id": "bt6b",
            "child_ids": ["bt8b"],
            "meta": {"timestamp": _current_time, "branch": "real_estate"},
        },
        "bt8b": {
            "id": "bt8b",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Let me find specific REIT recommendations and top crowdfunding platforms for real estate investment.",
                    },
                    {
                        "type": "tool_use",
                        "id": "reit_analysis_002",
                        "name": "analyze_reits_and_platforms",
                        "input": {
                            "reit_categories": [
                                "residential",
                                "commercial",
                                "healthcare",
                                "industrial",
                            ],
                            "platform_types": ["crowdfunding", "fractional_ownership"],
                            "budget": 10000,
                        },
                    },
                ],
            },
            "parent_id": "bt7b",
            "child_ids": ["bt9b"],
            "meta": {"timestamp": _current_time, "branch": "real_estate"},
        },
        "bt9b": {
            "id": "bt9b",
            "content": {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": "reit_analysis_002",
                        "content": json.dumps(
                            {
                                "top_reits": {
                                    "VNQ": {
                                        "name": "Vanguard Real Estate ETF",
                                        "price": 92.5,
                                        "dividend_yield": 3.8,
                                        "expense_ratio": 0.12,
                                        "focus": "diversified",
                                    },
                                    "SCHH": {
                                        "name": "Schwab US REIT ETF",
                                        "price": 19.85,
                                        "dividend_yield": 4.1,
                                        "expense_ratio": 0.07,
                                        "focus": "broad_market",
                                    },
                                    "IYR": {
                                        "name": "iShares US Real Estate ETF",
                                        "price": 101.3,
                                        "dividend_yield": 3.9,
                                        "expense_ratio": 0.42,
                                        "focus": "large_cap_reits",
                                    },
                                },
                                "crowdfunding_platforms": {
                                    "fundrise": {
                                        "min_investment": 1000,
                                        "avg_returns": "8.7%",
                                        "fees": "1.0%",
                                        "focus": "residential_commercial",
                                    },
                                    "yieldstreet": {
                                        "min_investment": 2500,
                                        "avg_returns": "9.2%",
                                        "fees": "0.5-2.5%",
                                        "focus": "alternative_real_estate",
                                    },
                                    "realty_mogul": {
                                        "min_investment": 5000,
                                        "avg_returns": "8.1%",
                                        "fees": "0.5-1.5%",
                                        "focus": "commercial_properties",
                                    },
                                },
                            }
                        ),
                    }
                ],
            },
            "parent_id": "bt8b",
            "child_ids": ["bt10b"],
            "meta": {"timestamp": _current_time, "branch": "real_estate"},
        },
        "bt10b": {
            "id": "bt10b",
            "content": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Here are specific recommendations for real estate investing:\n\n🏗️ **Top REIT Options:**\n\n📊 **VNQ (Vanguard Real Estate ETF)** - $92.50\n- Dividend Yield: 3.8% | Expense Ratio: 0.12%\n- Diversified across all real estate sectors\n\n🏢 **SCHH (Schwab US REIT ETF)** - $19.85\n- Dividend Yield: 4.1% | Expense Ratio: 0.07%\n- Lowest fees, broad market exposure\n\n🏛️ **IYR (iShares US Real Estate ETF)** - $101.30\n- Dividend Yield: 3.9% | Expense Ratio: 0.42%\n- Focus on large-cap REITs\n\n🤝 **Crowdfunding Platforms:**\n\n🏘️ **Fundrise** (Min: $1K)\n- Returns: 8.7% | Fees: 1.0%\n- Residential & commercial mix\n\n🏢 **YieldStreet** (Min: $2.5K)\n- Returns: 9.2% | Fees: 0.5-2.5%\n- Alternative real estate focus\n\n🏬 **RealtyMogul** (Min: $5K)\n- Returns: 8.1% | Fees: 0.5-1.5%\n- Commercial properties\n\n**$10K Portfolio:**\n- $3K SCHH (low fees, high yield)\n- $3K VNQ (diversification)\n- $4K Fundrise (higher returns)\n\nThis gives you liquidity + growth potential!",
                    }
                ],
            },
            "parent_id": "bt9b",
            "child_ids": [],
            "meta": {"timestamp": _current_time, "branch": "real_estate"},
        },
    },
)

# Export all mock canvases
MOCK_CANVASES = {
    "hello-canvas": hello_canvas,
    "weather-canvas": weather_canvas,
    "branched-canvas": branched_canvas,
    "branched-tool-canvas": branched_tool_canvas,
}


def get_mock_canvas(canvas_id: str) -> Dict[str, Any] | None:
    """Get a mock canvas by ID."""
    return MOCK_CANVASES.get(canvas_id)


def get_all_mock_canvases() -> Dict[str, Dict[str, Any]]:
    """Get all mock canvases."""
    return MOCK_CANVASES
