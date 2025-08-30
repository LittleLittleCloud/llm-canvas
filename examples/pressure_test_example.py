"""Pressure Test Example

This example creates a high-volume canvas to test the performance of the Canvas API.
It simulates a customer service scenario with 100 branches, each representing
different customer conversation threads, totaling over 1000 messages.
"""

from __future__ import annotations

import json
import random
import time

from examples.shared_client import get_canvas_client
from llm_canvas.canvas import Canvas, Message

# Mock data for generating realistic conversations
CUSTOMER_NAMES = [
    "Alice Johnson",
    "Bob Smith",
    "Carol Williams",
    "David Brown",
    "Emma Davis",
    "Frank Wilson",
    "Grace Miller",
    "Henry Garcia",
    "Ivy Martinez",
    "Jack Anderson",
    "Kate Thompson",
    "Liam Jackson",
    "Maya White",
    "Noah Harris",
    "Olivia Clark",
    "Peter Lewis",
    "Quinn Lee",
    "Rachel Walker",
    "Sam Hall",
    "Tina Allen",
    "Uma Young",
    "Victor King",
    "Wendy Scott",
    "Xavier Green",
    "Yara Adams",
    "Zach Baker",
    "Alex Chen",
    "Bella Rodriguez",
    "Charlie Murphy",
    "Diana Cooper",
    "Ethan Reed",
    "Fiona Bailey",
    "George Ward",
    "Hannah Torres",
    "Ian Peterson",
    "Julia Gray",
    "Kevin Ramirez",
    "Luna James",
    "Max Watson",
    "Nina Brooks",
    "Owen Kelly",
    "Piper Sanders",
    "Quincy Price",
    "Ruby Bennett",
    "Seth Wood",
    "Tara Barnes",
    "Ulysses Ross",
    "Vera Henderson",
    "Wade Coleman",
    "Xena Jenkins",
]

CUSTOMER_ISSUES = [
    "billing inquiry",
    "account access problem",
    "service outage",
    "feature request",
    "technical support",
    "refund request",
    "upgrade inquiry",
    "password reset",
    "data migration",
    "integration help",
    "performance issue",
    "security concern",
    "mobile app bug",
    "api documentation",
    "subscription change",
    "delivery delay",
    "product defect",
    "warranty claim",
    "installation help",
    "configuration issue",
]

PRODUCTS = [
    "Pro Dashboard",
    "Analytics Suite",
    "Mobile App",
    "API Service",
    "Enterprise Edition",
    "Cloud Storage",
    "Security Module",
    "Backup Service",
    "Monitoring Tools",
    "Integration Hub",
]

DEPARTMENTS = [
    "Technical Support",
    "Billing",
    "Sales",
    "Account Management",
    "Product Team",
    "Security Team",
    "DevOps",
    "Customer Success",
    "Quality Assurance",
    "Engineering",
]


def generate_customer_message(customer_name: str, issue_type: str, product: str, sequence: int) -> str:
    """Generate a realistic customer message based on the issue type and sequence."""
    if sequence == 1:
        # Initial customer message
        templates = {
            "billing inquiry": f"Hi, I'm {customer_name} and I have a question about my {product} billing. I was charged twice this month and need clarification.",
            "account access problem": f"Hello, {customer_name} here. I can't access my {product} account. My login credentials aren't working.",
            "service outage": f"Hi, I'm {customer_name}. The {product} service seems to be down. Is there a known outage?",
            "feature request": f"Hello, {customer_name} here. I'd like to request a new feature for {product}. Can we discuss this?",
            "technical support": f"Hi, I'm {customer_name} and I'm having technical issues with {product}. It's not working as expected.",
            "refund request": f"Hello, {customer_name} here. I need to request a refund for my {product} subscription.",
            "upgrade inquiry": f"Hi, I'm {customer_name}. I want to upgrade my {product} plan. What options are available?",
            "password reset": f"Hello, {customer_name} here. I need help resetting my password for {product}.",
            "data migration": f"Hi, I'm {customer_name}. I need help migrating my data to {product}.",
            "integration help": f"Hello, {customer_name} here. I need assistance integrating {product} with our systems.",
        }
        return templates.get(issue_type, f"Hi, I'm {customer_name} and I need help with {product}.")

    if sequence == 2:
        # Follow-up customer responses
        responses = [
            f"Thanks for the quick response! Let me provide more details about the {issue_type}.",
            f"I appreciate your help. The issue with {product} started yesterday morning.",
            f"Could you clarify what you mean? I'm not seeing that option in my {product} dashboard.",
            f"I tried that solution but it didn't work. The {product} is still having the same problem.",
            f"That makes sense. When can I expect this {issue_type} to be resolved?",
            f"Perfect! That's exactly what I needed to know about {product}.",
            f"I have a few more questions about the {issue_type} if that's okay.",
            f"Actually, I just noticed something else related to this {product} issue.",
        ]
        return random.choice(responses)

    if sequence == 3:
        # Additional customer responses
        responses = [
            f"Great! That solution worked perfectly for {product}. Thank you so much!",
            "I'm still having some trouble. Could you walk me through it step by step?",
            f"Is there someone from the {random.choice(DEPARTMENTS)} team who can help with this?",
            f"How long will this {issue_type} typically take to resolve?",
            f"Can I get a reference number for this {product} support case?",
            "This is urgent for our business. Is there an expedited process?",
            f"I'd like to speak with a supervisor about this {issue_type}.",
            f"Could you send me documentation about this {product} feature?",
        ]
        return random.choice(responses)

    # Final customer responses
    responses = [
        "Perfect! Everything is working now. Thanks for your excellent support!",
        f"I understand. Please keep me updated on the {issue_type} progress.",
        f"That resolves my question about {product}. Have a great day!",
        f"Thanks for escalating this to {random.choice(DEPARTMENTS)}. I'll wait for their response.",
        f"Excellent service! I'll definitely recommend {product} to others.",
        f"I appreciate your patience in helping me resolve this {issue_type}.",
        f"All set! Thanks for the thorough explanation about {product}.",
        "This has been very helpful. I'll implement your suggestions right away.",
    ]
    return random.choice(responses)


def generate_agent_message(customer_name: str, issue_type: str, product: str, sequence: int) -> str:
    """Generate a realistic customer service agent response."""
    if sequence == 1:
        # Initial agent response
        templates = {
            "billing inquiry": f"Hello {customer_name}! I'm happy to help with your {product} billing question. Let me check your account for duplicate charges.",
            "account access problem": f"Hi {customer_name}! I can definitely help you regain access to your {product} account. Let me verify your identity first.",
            "service outage": f"Hello {customer_name}! Thank you for reporting this {product} issue. Let me check our system status immediately.",
            "feature request": f"Hi {customer_name}! I'd love to hear about your {product} feature request. Our product team reviews all suggestions.",
            "technical support": f"Hello {customer_name}! I'm here to help resolve your {product} technical issue. Can you describe what's happening?",
            "refund request": f"Hi {customer_name}! I can assist with your {product} refund request. Let me review your subscription details.",
            "upgrade inquiry": f"Hello {customer_name}! I'd be happy to discuss {product} upgrade options that would suit your needs.",
            "password reset": f"Hi {customer_name}! I can help you reset your {product} password. For security, I'll send instructions to your registered email.",
            "data migration": f"Hello {customer_name}! I can guide you through the {product} data migration process. It's actually quite straightforward.",
            "integration help": f"Hi {customer_name}! I can definitely help with {product} integration. Our API documentation will be very useful here.",
        }
        return templates.get(issue_type, f"Hello {customer_name}! I'm here to help with your {product} question.")

    if sequence == 2:
        # Follow-up agent responses
        responses = [
            f"I've reviewed your {product} account and found the issue. Here's what happened and how we'll fix it.",
            f"Based on your description, this appears to be a common {issue_type}. Here's the recommended solution.",
            f"I see the problem in your {product} configuration. Let me guide you through the fix.",
            f"This requires escalation to our {random.choice(DEPARTMENTS)} team. I'll create a priority ticket for you.",
            f"I've applied a temporary fix to your {product} account while we implement a permanent solution.",
            f"Your {issue_type} has been documented and assigned to our development team for resolution.",
            f"I can offer you several options for resolving this {product} issue. Which would you prefer?",
            f"I've sent detailed instructions to your email for fixing this {issue_type}.",
        ]
        return random.choice(responses)

    if sequence == 3:
        # Additional agent responses
        responses = [
            f"Excellent! I'm glad the {product} issue is resolved. Is there anything else I can help you with today?",
            f"Let me break this down step by step for your {product} setup.",
            f"I've connected you with our {random.choice(DEPARTMENTS)} specialist who will follow up within 2 hours.",
            f"Your case number is #{random.randint(100000, 999999)}. This {issue_type} should be resolved within 24 hours.",
            f"I understand the urgency. I've marked this {product} case as high priority.",
            f"I'm transferring this to my supervisor who specializes in {issue_type} cases.",
            f"I've sent comprehensive {product} documentation to your email address.",
            f"Our {random.choice(DEPARTMENTS)} team will contact you directly about this {issue_type}.",
        ]
        return random.choice(responses)

    # Final agent responses
    responses = [
        f"Wonderful! I'm so glad we could resolve your {product} issue quickly.",
        f"I'll monitor this {issue_type} and update you with any progress. Thank you for your patience!",
        f"It was my pleasure helping you with {product} today! Don't hesitate to contact us again.",
        f"The {random.choice(DEPARTMENTS)} team will be in touch soon. Have a great day!",
        f"Thank you for the kind words! We strive to provide excellent {product} support.",
        f"I'm happy I could help with your {issue_type}. Enjoy using {product}!",
        f"Perfect! Your {product} setup should work smoothly now. Thanks for choosing our service!",
        f"Great to hear! If you need any more help with {product}, we're always here for you.",
    ]
    return random.choice(responses)


def simulate_tool_usage(issue_type: str, product: str, sequence: int) -> tuple[Message, Message]:
    """Simulate tool usage in customer service conversations."""
    tool_id = f"tool_{random.randint(1000, 9999)}"

    # Agent uses a tool
    tool_message: Message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": f"Let me check our {product} system for more information about this {issue_type}.",
            },
            {
                "type": "tool_use",
                "id": tool_id,
                "name": "check_system_status" if issue_type == "service outage" else "lookup_account_details",
                "input": {
                    "product": product,
                    "issue_type": issue_type,
                    "timestamp": time.time(),
                },
            },
        ],
    }

    # Tool result
    if issue_type == "service outage":
        tool_result = {
            "status": "operational" if random.random() > 0.3 else "degraded",
            "last_incident": "2025-08-28T10:30:00Z",
            "affected_regions": ["us-west-1"] if random.random() > 0.7 else [],
            "estimated_resolution": "within 30 minutes" if random.random() > 0.5 else "within 2 hours",
        }
    else:
        tool_result = {
            "account_status": "active",
            "subscription_tier": random.choice(["basic", "pro", "enterprise"]),
            "last_login": "2025-08-29T08:15:00Z",
            "support_tickets": random.randint(0, 5),
            "account_health": "good",
        }

    tool_result_message: Message = {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": json.dumps(tool_result),
            }
        ],
    }

    return tool_message, tool_result_message


def create_conversation_branch(canvas: Canvas, branch_info: dict, messages_per_branch: int) -> None:
    """Create a single conversation branch with multiple messages."""
    branch_name = branch_info["name"]
    customer_name = branch_info["customer"]
    issue_type = branch_info["issue"]
    product = branch_info["product"]

    print(f"📝 Creating branch: {branch_name} ({customer_name} - {issue_type})")

    try:
        # Create branch
        branch = canvas.checkout(
            name=branch_name,
            description=f"Customer: {customer_name}, Issue: {issue_type}, Product: {product}",
            create_if_not_exists=True,
        )

        # Add messages to this branch
        sequence = 1
        for i in range(messages_per_branch):
            try:
                if i % 4 == 0:  # Customer message
                    message_content = generate_customer_message(customer_name, issue_type, product, sequence)
                    message: Message = {"role": "user", "content": [{"type": "text", "text": message_content}]}
                    branch.commit_message(
                        message,
                        meta={
                            "customer": customer_name,
                            "issue_type": issue_type,
                            "product": product,
                            "sequence": sequence,
                            "timestamp": time.time(),
                        },
                    )

                elif i % 4 == 1:  # Agent response
                    message_content = generate_agent_message(customer_name, issue_type, product, sequence)
                    message: Message = {"role": "assistant", "content": [{"type": "text", "text": message_content}]}
                    branch.commit_message(
                        message,
                        meta={"agent_response": True, "issue_type": issue_type, "product": product, "sequence": sequence},
                    )

                elif i % 4 == 2 and random.random() > 0.5:  # Tool usage (50% chance)
                    tool_message, tool_result = simulate_tool_usage(issue_type, product, sequence)
                    branch.commit_message(tool_message, meta={"tool_usage": True})
                    branch.commit_message(tool_result, meta={"tool_result": True})
                    i += 1  # Account for the extra message

                else:  # Additional customer or agent message
                    if random.random() > 0.5:  # Customer
                        message_content = generate_customer_message(customer_name, issue_type, product, sequence + 1)
                        role = "user"
                    else:  # Agent
                        message_content = generate_agent_message(customer_name, issue_type, product, sequence + 1)
                        role = "assistant"

                    message: Message = {"role": role, "content": [{"type": "text", "text": message_content}]}
                    branch.commit_message(message, meta={"follow_up": True, "issue_type": issue_type, "product": product})

                # Small delay to simulate real conversation timing
                time.sleep(0.01)

                # Increment sequence every 2 messages
                if i % 2 == 1:
                    sequence += 1

            except Exception as e:
                print(f"⚠️  Error adding message {i} to branch {branch_name}: {e}")
                continue

    except Exception as e:
        print(f"❌ Error creating branch {branch_name}: {e}")
    finally:
        canvas.checkout(name="main")  # Return to main branch


def create_pressure_test() -> None:
    """Create a pressure test canvas with 100 branches and 1000+ messages."""
    print("🚀 Starting Pressure Test Example...")
    print("This will create 100 customer service conversation branches with 1000+ total messages")

    # Get the shared client
    client = get_canvas_client()

    # Create a new canvas
    canvas = client.create_canvas(
        title="Customer Service Pressure Test",
        description="High-volume canvas with 100 customer service conversation branches for performance testing",
    )

    print(f"📋 Canvas ID: {canvas.canvas_id}")

    # Get main branch and add initial welcome message
    main_branch = canvas.checkout(name="main", create_if_not_exists=True)

    welcome_message: Message = {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "Welcome to Customer Service Portal - Pressure Test Simulation. This canvas contains 100 different customer conversation branches for performance testing.",
            }
        ],
    }
    main_branch.commit_message(welcome_message, meta={"system_message": True, "test_start": time.time()})

    # Configuration
    num_branches = 100
    messages_per_branch = 12  # This will create 1200+ messages total (including tool messages)

    # Generate branch information
    branch_configs = []
    for i in range(num_branches):
        customer = random.choice(CUSTOMER_NAMES)
        issue = random.choice(CUSTOMER_ISSUES)
        product = random.choice(PRODUCTS)

        branch_config = {
            "name": f"ticket-{i + 1:03d}-{customer.lower().replace(' ', '-')}",
            "customer": customer,
            "issue": issue,
            "product": product,
        }
        branch_configs.append(branch_config)

    # Create branches sequentially (parallel execution might overwhelm the server)
    print(f"🏗️  Creating {num_branches} branches with ~{messages_per_branch} messages each...")

    start_time = time.time()
    total_messages = 0

    # Process branches in batches for better performance
    batch_size = 10
    for batch_start in range(0, num_branches, batch_size):
        batch_end = min(batch_start + batch_size, num_branches)
        batch_configs = branch_configs[batch_start:batch_end]

        print(f"📦 Processing batch {batch_start // batch_size + 1}/{(num_branches + batch_size - 1) // batch_size}")

        for branch_config in batch_configs:
            create_conversation_branch(canvas, branch_config, messages_per_branch)
            total_messages += messages_per_branch

        # Small delay between batches to prevent overwhelming the server
        time.sleep(0.1)

    # Add summary message to main branch
    end_time = time.time()
    duration = end_time - start_time

    summary_message: Message = {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": f"""Pressure Test Completed! 
            
📊 **Statistics:**
- Branches Created: {num_branches}
- Total Messages: ~{total_messages}
- Duration: {duration:.2f} seconds
- Messages/Second: {total_messages / duration:.2f}

🎯 **Test Scenarios:**
- {len(set(config["issue"] for config in branch_configs))} different issue types
- {len(set(config["product"] for config in branch_configs))} different products
- {len(set(config["customer"] for config in branch_configs))} unique customers

✅ Canvas is ready for performance analysis!""",
            }
        ],
    }
    main_branch.commit_message(
        summary_message,
        meta={
            "test_summary": True,
            "branches_created": num_branches,
            "total_messages": total_messages,
            "duration_seconds": duration,
            "messages_per_second": total_messages / duration,
        },
    )

    print("✅ Pressure Test completed!")
    print(f"📊 Created {num_branches} branches with ~{total_messages} total messages in {duration:.2f} seconds")
    print(f"⚡ Performance: {total_messages / duration:.2f} messages/second")
    print("🌐 Canvas available at server for analysis")


if __name__ == "__main__":
    create_pressure_test()
