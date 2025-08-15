"""Vacation Planning with Branched Conversations Example

This example demonstrates how to use the Canvas API to create
branched conversations using the shared CanvasClient instance.
"""

from __future__ import annotations

import time

from examples.shared_client import get_canvas_client
from llm_canvas.canvas import Message


def create_vacation_planning() -> None:
    """Create a vacation planning conversation with branches."""
    # Get the shared client
    client = get_canvas_client()

    # Create a new canvas via the client
    canvas = client.create_canvas(
        title="Vacation Planning", description="A branched conversation exploring Japan vs Italy vacation options"
    )

    print("🏖️ Creating Vacation Planning with Branches example...")

    # Get main branch
    main_branch = canvas.checkout(name="main", create_if_not_exists=True)

    # Step 1: User's initial question
    print("1️⃣ User asks about vacation destination")
    user_question: Message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "I'm planning a vacation. Should I go to Japan or Italy?",
            }
        ],
    }
    main_branch.commit_message(user_question)

    # Step 2: Assistant's response suggesting exploration
    print("2️⃣ Assistant suggests exploring both options")
    time.sleep(0.2)
    assistant_response: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Both Japan and Italy are incredible destinations! The choice depends on what kind of experience you're looking for. Let me help you explore both options to make the best decision for your preferences.""",  # noqa: E501
            }
        ],
    }
    branch_point = main_branch.commit_message(assistant_response)

    # Create Japan branch
    print("\n🏮 Creating Japan exploration branch")
    japan_branch = canvas.checkout(
        "japan-exploration",
        description="Exploring Japan as vacation destination",
        create_if_not_exists=True,
        commit_message=branch_point,
    )

    # Japan branch conversation
    print("3a️⃣ User asks about Japan")
    japan_question: Message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Tell me more about Japan. I'm interested in culture and technology.",
            }
        ],
    }
    japan_branch.commit_message(japan_question, meta={"branch": "japan"})

    print("4a️⃣ Assistant responds about Japan")
    time.sleep(0.2)
    japan_response: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Japan is perfect for culture and technology enthusiasts! Here's what makes it special:

🏮 **Cultural Highlights:**
- Ancient temples and shrines (Kyoto has over 2,000!)
- Traditional tea ceremonies and gardens
- Authentic geisha districts
- Rich samurai history and castles
- Traditional ryokan (inn) experiences

🤖 **Technology & Innovation:**
- Tokyo's high-tech districts like Akihabara and Shibuya
- Bullet trains (shinkansen) - engineering marvels
- Robot restaurants and cafes
- Cutting-edge gaming arcades
- Advanced automation in daily life

**Best Time:** Spring (cherry blossoms) or Fall (autumn colors)
**Duration:** 10-14 days to see both traditional and modern sides""",
            }
        ],
    }
    japan_branch.commit_message(japan_response, meta={"branch": "japan"})

    # Continue Japan conversation
    print("5a️⃣ User asks about Japanese food")
    japan_food_question: Message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What about the food scene? I'm quite adventurous with food.",
            }
        ],
    }
    japan_branch.commit_message(japan_food_question, meta={"branch": "japan"})

    print("6a️⃣ Assistant describes Japanese cuisine")
    time.sleep(0.2)
    japan_food_response: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Japan's food scene is absolutely incredible for adventurous eaters! 🍣

**Unique Experiences:**
- Tsukiji Fish Market (dawn tuna auctions)
- Authentic sushi omakase experiences
- Ramen crawls through different regional styles
- Kaiseki (traditional multi-course) dining
- Street food in Osaka (takoyaki, okonomiyaki)

**Adventurous Options:**
- Fugu (carefully prepared pufferfish)
- Natto (fermented soybeans)
- Raw horse sashimi (basashi)
- Sea urchin and unusual seafood
- Insects and exotic game meats

**Food Culture:**
- No tipping culture
- Vending machine restaurants
- Conveyor belt sushi
- Department store food courts (depachika)

Japan offers both comfort and challenge for food lovers!""",
            }
        ],
    }
    japan_branch.commit_message(japan_food_response, meta={"branch": "japan"})

    # Create Italy branch
    print("\n🇮🇹 Creating Italy exploration branch")
    italy_branch = canvas.checkout(
        "italy-exploration",
        description="Exploring Italy as vacation destination",
        create_if_not_exists=True,
        commit_message=branch_point,
    )

    # Italy branch conversation
    print("3b️⃣ User asks about Italy")
    italy_question: Message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What about Italy? I love art, history, and great food.",
            }
        ],
    }
    italy_branch.commit_message(italy_question, meta={"branch": "italy"})

    print("4b️⃣ Assistant responds about Italy")
    time.sleep(0.2)
    italy_response: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Italy is a dream destination for art, history, and food lovers! Here's why it's magical:

🎨 **Art & History:**
- Vatican Museums and Sistine Chapel
- Uffizi Gallery in Florence (Renaissance masterpieces)
- Colosseum and Roman Forum
- Pompeii's preserved ancient city
- Michelangelo's David and countless sculptures
- Medieval hill towns like San Gimignano

🍝 **Culinary Paradise:**
- Regional specialties (each city has unique dishes)
- Fresh pasta made daily
- World-class wines (Chianti, Barolo, Prosecco)
- Authentic gelato and espresso culture
- Pizza in its birthplace (Naples)

**Romance & Atmosphere:**
- Gondola rides in Venice
- Tuscan countryside vineyards
- Amalfi Coast's dramatic coastline
- Charming piazzas perfect for people-watching""",
            }
        ],
    }
    italy_branch.commit_message(italy_response, meta={"branch": "italy"})

    # Continue Italy conversation
    print("5b️⃣ User asks about Italy itinerary")
    italy_itinerary_question: Message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "How long should I plan for Italy, and what's the best route?",
            }
        ],
    }
    italy_branch.commit_message(italy_itinerary_question, meta={"branch": "italy"})

    print("6b️⃣ Assistant provides Italy itinerary")
    time.sleep(0.2)
    italy_itinerary_response: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """For Italy, I'd recommend 10-14 days minimum to really savor the experience! 🇮🇹

**Classic Route (North to South):**

**Days 1-3: Rome** 🏛️
- Vatican, Colosseum, Trevi Fountain
- Trastevere neighborhood for authentic dining

**Days 4-6: Florence** 🎨
- Uffizi Gallery, Duomo, Ponte Vecchio
- Day trip to Siena or Pisa

**Days 7-9: Venice** 🛶
- St. Mark's Square, Doge's Palace
- Murano and Burano islands

**Days 10-12: Amalfi Coast** 🌊
- Positano, Amalfi, Ravello
- Limoncello tastings and coastal views

**Optional Extensions:**
- Tuscany wine country (Chianti region)
- Cinque Terre hiking
- Milan for fashion and business

**Transportation:** High-speed trains connect major cities beautifully. The journey becomes part of the experience with stunning countryside views!""",  # noqa: E501
            }
        ],
    }
    italy_branch.commit_message(italy_itinerary_response, meta={"branch": "italy"})

    print("✅ Vacation Planning example completed! Canvas available at server.")


if __name__ == "__main__":
    create_vacation_planning()
