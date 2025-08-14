"""Investment Decision Example

This example demonstrates how to use the Canvas API to create
a conversation with branching paths and tool usage using the shared
CanvasClient instance.
"""

from __future__ import annotations

import json
import time

from examples.shared_client import get_canvas_client
from llm_canvas.canvas import Message


def simulate_market_data_api(_symbols: list[str], _timeframe: str = "1M", _include_fundamentals: bool = True) -> dict:
    """Simulate a market data API call."""
    time.sleep(0.3)  # Simulate API call delay
    return {
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


def simulate_stock_analysis_api(
    _symbols: list[str], _analysis_type: str = "fundamental", _include_technicals: bool = True
) -> dict:
    """Simulate a stock analysis API call."""
    time.sleep(0.3)  # Simulate API call delay
    return {
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


def simulate_real_estate_data_api(_budget: int, _investment_types: list[str], _regions: list[str]) -> dict:
    """Simulate a real estate data API call."""
    time.sleep(0.3)  # Simulate API call delay
    return {
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


def simulate_reit_analysis_api(_reit_categories: list[str], _platform_types: list[str], _budget: int) -> dict:
    """Simulate a REIT and platforms analysis API call."""
    time.sleep(0.3)  # Simulate API call delay
    return {
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


def investment_decision() -> None:
    """Create an investment decision conversation with branching paths and tool usage."""
    # Get the shared client
    client = get_canvas_client()

    # Create a new canvas via the client
    canvas = client.create_canvas(
        title="Investment Decision",
        description="A conversation demonstrating branching paths and tool usage for investment decisions",
    )

    print("💰 Creating Investment Decision example...")

    # Get main branch
    main_branch = canvas.checkout(name="main", create_if_not_exists=True)

    # Step 1: User asks about investment options
    print("\n1️⃣ User asks about investment options")
    user_message: Message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "I'm planning to invest $10,000. Should I put it in stocks or real estate?",
            }
        ],
    }
    main_branch.commit_message(user_message)

    # Step 2: Assistant suggests exploring both paths
    print("2️⃣ Assistant suggests exploring both paths")
    time.sleep(0.2)
    assistant_intro_message: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": (
                    "Great question! Both stocks and real estate can be excellent investment options. "
                    "Let me help you explore both paths by analyzing current market conditions and "
                    "opportunities for each."
                ),
            }
        ],
    }
    assistant_intro_message_node = main_branch.commit_message(assistant_intro_message)

    print("\n📈 Exploring Stock Market Branch...")

    stock_branch = canvas.checkout(name="stock investment", description="Investment in stocks", create_if_not_exists=True)

    # Branch A: Stock Investment Path
    # Step 3a: User explores stock market
    print("3️⃣a User explores stock market option")
    stock_inquiry: Message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Let's explore the stock market option. What are the current market conditions?",
            }
        ],
    }
    stock_branch.commit_message(stock_inquiry)

    # Step 4a: Assistant uses market data tool
    print("4️⃣a Assistant uses market data tool")
    time.sleep(0.2)
    market_tool_message: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": (
                    "I'll check the current stock market conditions and analyze some potential "
                    "investment opportunities for you."
                ),
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
    }
    stock_branch.commit_message(market_tool_message)

    # Step 5a: Market data tool result
    print("5️⃣a Market data tool execution")
    market_data = simulate_market_data_api(["SPY", "QQQ", "VTI"], "1M", True)
    market_result_message: Message = {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": "market_analysis_001",
                "content": json.dumps(market_data),
            }
        ],
    }
    stock_branch.commit_message(market_result_message)

    # Step 6a: Assistant analyzes market data
    print("6️⃣a Assistant analyzes market conditions")
    time.sleep(0.2)
    market_analysis_response: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Excellent! The current market analysis shows promising conditions for stock investment:

📈 **Market Overview:**
- **Trend:** Bullish with cautious optimism
- **Volatility:** Moderate (good for entry)
- **Risk Sentiment:** Positive but measured

**Top ETF Options for $10,000:**

🏛️ **SPY (S&P 500)** - $445.30 (+1.2%)
- Broad market exposure
- P/E Ratio: 21.5 (reasonable valuation)
- Dividend Yield: 1.3%

💻 **QQQ (NASDAQ-100)** - $378.90 (+1.8%)
- Tech-heavy, higher growth potential
- P/E Ratio: 26.4 (premium for growth)
- Dividend Yield: 0.6%

🌍 **VTI (Total Stock Market)** - $248.70 (+1.1%)
- Complete US market diversification
- P/E Ratio: 22.1 (balanced)
- Dividend Yield: 1.4%

**Recommendation:** Consider a diversified approach with 60% VTI, 30% SPY, 10% QQQ for balanced growth and stability.""",
            }
        ],
    }
    stock_branch.commit_message(market_analysis_response)

    # Step 7a: User asks about individual stocks
    print("7️⃣a User asks about individual stocks")
    individual_stocks_inquiry: Message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What about individual stocks? Can you analyze some tech companies?",
            }
        ],
    }
    stock_branch.commit_message(individual_stocks_inquiry)

    # Step 8a: Assistant uses stock analysis tool
    print("8️⃣a Assistant uses stock analysis tool")
    time.sleep(0.2)
    stock_analysis_tool_message: Message = {
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
    }
    stock_branch.commit_message(stock_analysis_tool_message)

    # Step 9a: Stock analysis tool result
    print("9️⃣a Stock analysis tool execution")
    stock_data = simulate_stock_analysis_api(["AAPL", "MSFT", "GOOGL", "NVDA"], "fundamental", True)
    stock_result_message: Message = {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": "stock_analysis_002",
                "content": json.dumps(stock_data),
            }
        ],
    }
    stock_branch.commit_message(stock_result_message)

    # Step 10a: Final stock recommendations
    print("🔟a Assistant provides final stock recommendations")
    time.sleep(0.2)
    stock_final_response: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Here's the analysis of major tech stocks:

🍎 **Apple (AAPL)** - $189.50
- P/E: 28.5 | Growth: 8.2% | Risk: Medium
- **Recommendation: BUY** (Target: $205)
- Stable dividend, strong ecosystem

🪟 **Microsoft (MSFT)** - $378.85
- P/E: 32.1 | Growth: 12.5% | Risk: Low
- **Recommendation: STRONG BUY** (Target: $420)
- Cloud dominance, AI leadership

🔍 **Alphabet (GOOGL)** - $138.75
- P/E: 24.8 | Growth: 10.1% | Risk: Medium
- **Recommendation: BUY** (Target: $155)
- Search monopoly, reasonable valuation

🎮 **NVIDIA (NVDA)** - $875.20
- P/E: 65.4 | Growth: 45.2% | Risk: High
- **Recommendation: HOLD** (Target: $950)
- AI boom driver but expensive

**$10K Portfolio Suggestion:**
- $4,000 MSFT (40%)
- $3,000 AAPL (30%)
- $2,000 GOOGL (20%)
- $1,000 NVDA (10%)

This balances growth potential with risk management!""",
            }
        ],
    }
    stock_branch.commit_message(stock_final_response)

    print("\n🏠 Exploring Real Estate Branch...")

    # Branch B: Real Estate Investment Path
    # We need to branch from the assistant intro message for real estate
    # First, let's go back to that point and create the real estate branch
    real_estate_branch = canvas.checkout(
        name="real estate investment",
        description="Investment in real estate",
        create_if_not_exists=True,
        commit_message=assistant_intro_message_node,
    )

    # Step 3b: User explores real estate
    print("3️⃣b User explores real estate option")
    real_estate_inquiry: Message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What about real estate? Can you analyze the current market and opportunities?",
            }
        ],
    }
    real_estate_branch.commit_message(real_estate_inquiry)

    # Step 4b: Assistant uses real estate data tool
    print("4️⃣b Assistant uses real estate data tool")
    time.sleep(0.2)
    real_estate_tool_message: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": (
                    "Let me analyze the current real estate market conditions and find "
                    "investment opportunities suitable for your $10,000 budget."
                ),
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
    }
    real_estate_branch.commit_message(real_estate_tool_message)

    # Step 5b: Real estate data tool result
    print("5️⃣b Real estate data tool execution")
    real_estate_data = simulate_real_estate_data_api(
        10000, ["REIT", "crowdfunding", "fractional"], ["national", "high_growth_markets"]
    )
    real_estate_result_message: Message = {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": "real_estate_001",
                "content": json.dumps(real_estate_data),
            }
        ],
    }
    real_estate_branch.commit_message(real_estate_result_message)

    # Step 6b: Assistant analyzes real estate data
    print("6️⃣b Assistant analyzes real estate market")
    time.sleep(0.2)
    real_estate_analysis_response: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Here's the real estate investment landscape for your $10,000:

🏠 **Market Conditions:**
- Interest Rates: 6.8% (moderately high)
- Home Prices: Stabilizing after recent peaks
- Rental Demand: Strong across markets
- Outlook: Cautiously optimistic

**Investment Options:**

🏢 **REITs (Real Estate Investment Trusts)**
- Average Dividend Yield: 4.2%
- Price Appreciation: 2.1%
- Liquidity: High (trade like stocks)
- Min Investment: $100

🤝 **Real Estate Crowdfunding**
- Average Returns: 8.5%
- Investment Period: 2-5 years
- Liquidity: Low (money tied up)
- Min Investment: $1,000

🏘️ **Fractional Ownership**
- Average Returns: 6.2%
- Property Types: Residential & Commercial
- Liquidity: Medium
- Min Investment: $5,000

**$10K Strategy:** Mix REITs (60% = $6K) for liquidity + Crowdfunding (40% = $4K) for higher returns""",
            }
        ],
    }
    real_estate_branch.commit_message(real_estate_analysis_response)

    # Step 7b: User asks for specific recommendations
    print("7️⃣b User asks for specific REIT recommendations")
    reit_inquiry: Message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Can you find specific REIT recommendations and crowdfunding platforms?",
            }
        ],
    }
    real_estate_branch.commit_message(reit_inquiry)

    # Step 8b: Assistant uses REIT analysis tool
    print("8️⃣b Assistant uses REIT analysis tool")
    time.sleep(0.2)
    reit_analysis_tool_message: Message = {
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
                    "reit_categories": ["residential", "commercial", "healthcare", "industrial"],
                    "platform_types": ["crowdfunding", "fractional_ownership"],
                    "budget": 10000,
                },
            },
        ],
    }
    real_estate_branch.commit_message(reit_analysis_tool_message)

    # Step 9b: REIT analysis tool result
    print("9️⃣b REIT analysis tool execution")
    reit_data = simulate_reit_analysis_api(
        ["residential", "commercial", "healthcare", "industrial"], ["crowdfunding", "fractional_ownership"], 10000
    )
    reit_result_message: Message = {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": "reit_analysis_002",
                "content": json.dumps(reit_data),
            }
        ],
    }
    real_estate_branch.commit_message(reit_result_message)

    # Step 10b: Final real estate recommendations
    print("🔟b Assistant provides final real estate recommendations")
    time.sleep(0.2)
    real_estate_final_response: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Here are specific recommendations for real estate investing:

🏗️ **Top REIT Options:**

📊 **VNQ (Vanguard Real Estate ETF)** - $92.50
- Dividend Yield: 3.8% | Expense Ratio: 0.12%
- Diversified across all real estate sectors

🏢 **SCHH (Schwab US REIT ETF)** - $19.85
- Dividend Yield: 4.1% | Expense Ratio: 0.07%
- Lowest fees, broad market exposure

🏛️ **IYR (iShares US Real Estate ETF)** - $101.30
- Dividend Yield: 3.9% | Expense Ratio: 0.42%
- Focus on large-cap REITs

🤝 **Crowdfunding Platforms:**

🏘️ **Fundrise** (Min: $1K)
- Returns: 8.7% | Fees: 1.0%
- Residential & commercial mix

🏢 **YieldStreet** (Min: $2.5K)
- Returns: 9.2% | Fees: 0.5-2.5%
- Alternative real estate focus

🏬 **RealtyMogul** (Min: $5K)
- Returns: 8.1% | Fees: 0.5-1.5%
- Commercial properties

**$10K Portfolio:**
- $3K SCHH (low fees, high yield)
- $3K VNQ (diversification)
- $4K Fundrise (higher returns)

This gives you liquidity + growth potential!""",
            }
        ],
    }
    real_estate_branch.commit_message(real_estate_final_response)

    # Switch back to main branch for comparison
    print("\n🔄 Switching back to main branch for comparison")
    main_branch = canvas.checkout()  # Returns to main

    # User asks to compare options
    print("🤔 User asks for comparison")
    time.sleep(0.2)
    comparison_request: Message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Can you summarize the key differences between the crypto and real estate investment "
                "strategies? Which might be better for a cautious investor?",
            }
        ],
    }
    main_branch.commit_message(comparison_request)

    # Final comparison and recommendation
    print("🎯 Assistant provides final comparison")
    time.sleep(0.2)
    final_comparison: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Let me compare the two investment strategies:

📊 **CRYPTO STRATEGY**
💰 Risk: High | Returns: 15-200%+
⚡ Liquidity: Very High
🎯 Best for: Risk-tolerant, tech-savvy investors
⏰ Time Horizon: 1-5 years
🛡️ Strategy: 70% established (BTC/ETH) + 30% growth

🏠 **REAL ESTATE STRATEGY**
💰 Risk: Medium | Returns: 6-9%
⚡ Liquidity: Medium
🎯 Best for: Income-focused, conservative investors
⏰ Time Horizon: 3-10 years
🛡️ Strategy: REITs + crowdfunding mix

**For a CAUTIOUS investor:**
🏆 **Real Estate wins** due to:
✅ Predictable income streams
✅ Lower volatility
✅ Tangible asset backing
✅ Inflation hedge

**Hybrid Approach:** 70% Real Estate + 30% Crypto
- Balances growth potential with stability
- $7K in REITs/crowdfunding
- $3K in BTC/ETH only

Would you like me to explore this balanced approach?""",
            }
        ],
    }
    main_branch.commit_message(final_comparison)

    print("\n✅ Investment Decision example completed! Canvas available at server.")


if __name__ == "__main__":
    investment_decision()
