"""Claude Routing Canvas Example

This example demonstrates how to visualize LLM routing decisions using canvas.
It shows how support tickets are analyzed, categorized, and routed to specialized
prompts, with each step tracked in the canvas for analysis and debugging.

The canvas creates separate branches for each ticket, allowing you to see:
- Original ticket content
- Routing analysis and decision process
- Specialized prompt selection
- Final response generation

Original notebook: https://github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/basic_workflows.ipynb
"""

from examples.claude.chain import chain
from examples.claude.utils import extract_xml, llm_call
from examples.shared_client import get_canvas_client
from llm_canvas.canvas import Branch
from llm_canvas.types import Message


def route(
    input: str,
    routes: dict[str, str],
    route_branches: dict[str, Branch],
    route_analysis_branch: Branch,
) -> str:
    """Route input to specialized prompt using content classification."""

    # Log the input ticket to canvas
    route_analysis_branch.commit_message(
        message=Message(content=f"Support Ticket:\n{input}", role="user")
    )

    selector_prompt = f"""
    Analyze the input and select the most appropriate support team from these options: {list(routes.keys())}
    First explain your reasoning, then provide your selection in this XML format:

    <reasoning>
    Brief explanation of why this ticket should be routed to a specific team.
    Consider key terms, user intent, and urgency level.
    </reasoning>

    <selection>
    The chosen team name
    </selection>

    Input: {input}""".strip()

    route_response = llm_call(selector_prompt)
    route_key = extract_xml(route_response, "selection").strip().lower()

    # Log the routing decision to canvas
    routing_decision = f"Selected Route: {route_key}"
    route_analysis_branch.commit_message(
        message=Message(content=routing_decision, role="assistant")
    )

    # Validate route key exists
    if route_key not in routes:
        raise ValueError(
            f"Unknown route key: {route_key}. Available routes: {list(routes.keys())}"
        )

    # Process input with selected specialized prompt
    selected_prompt = routes[route_key]

    # Get the appropriate branch for the route
    branch = route_branches[route_key]
    return chain(selected_prompt, [input], branch)


support_routes = {
    "billing": """You are a billing support specialist. Follow these guidelines:
    1. Always start with "Billing Support Response:"
    2. First acknowledge the specific billing issue
    3. Explain any charges or discrepancies clearly
    4. List concrete next steps with timeline
    5. End with payment options if relevant
    
    Keep responses professional but friendly.
    
    Input: """,
    "technical": """You are a technical support engineer. Follow these guidelines:
    1. Always start with "Technical Support Response:"
    2. List exact steps to resolve the issue
    3. Include system requirements if relevant
    4. Provide workarounds for common problems
    5. End with escalation path if needed
    
    Use clear, numbered steps and technical details.
    
    Input: """,
    "account": """You are an account security specialist. Follow these guidelines:
    1. Always start with "Account Support Response:"
    2. Prioritize account security and verification
    3. Provide clear steps for account recovery/changes
    4. Include security tips and warnings
    5. Set clear expectations for resolution time
    
    Maintain a serious, security-focused tone.
    
    Input: """,
    "product": """You are a product specialist. Follow these guidelines:
    1. Always start with "Product Support Response:"
    2. Focus on feature education and best practices
    3. Include specific examples of usage
    4. Link to relevant documentation sections
    5. Suggest related features that might help
    
    Be educational and encouraging in tone.
    
    Input: """,
}

# Test with different support tickets
tickets = [
    """Subject: Can't access my account
    Message: Hi, I've been trying to log in for the past hour but keep getting an 'invalid password' error. 
    I'm sure I'm using the right password. Can you help me regain access? This is urgent as I need to 
    submit a report by end of day.
    - John""",
    """Subject: Unexpected charge on my card
    Message: Hello, I just noticed a charge of $49.99 on my credit card from your company, but I thought
    I was on the $29.99 plan. Can you explain this charge and adjust it if it's a mistake?
    Thanks,
    Sarah""",
    """Subject: How to export data?
    Message: I need to export all my project data to Excel. I've looked through the docs but can't
    figure out how to do a bulk export. Is this possible? If so, could you walk me through the steps?
    Best regards,
    Mike""",
    """Subject: Feature request - bulk actions
    Message: I love using your product! I was wondering if you have any plans to add bulk action features
    like bulk delete or bulk edit? This would really help with managing large datasets.
    Also, are there any advanced features I might not know about that could help with my workflow?
    Thanks!
    Emma""",
]

if __name__ == "__main__":
    # Create canvas for tracking support ticket routing
    canvas_client = get_canvas_client()
    canvas = canvas_client.create_canvas(
        title="Support Ticket Routing",
        description="""
        This canvas visualizes the routing process for support tickets.
        Each branch represents a different support ticket and shows:
        1. The original ticket content
        2. The routing analysis and decision
        3. The specialized prompt used
        4. The final response
        
        This demonstrates how LLM routing can be tracked and analyzed across different ticket types.
        """,
    )

    print("Processing support tickets...\n")
    main_branch = canvas.checkout("main", create_if_not_exists=True)
    route_analysis_branch = canvas.checkout("route_analysis", create_if_not_exists=True)
    billing_support_branch = canvas.checkout(
        "billing_support", create_if_not_exists=True
    )
    account_security_branch = canvas.checkout(
        "account_security", create_if_not_exists=True
    )
    technical_support_branch = canvas.checkout(
        "technical_support", create_if_not_exists=True
    )
    product_support_branch = canvas.checkout(
        "product_support", create_if_not_exists=True
    )

    route_analysis_branch.commit_message(
        Message(
            content=f"""Analyze the input and select the most appropriate support team from these options: {list(support_routes.keys())}
    First explain your reasoning, then provide your selection in this XML format:

    <reasoning>
    Brief explanation of why this ticket should be routed to a specific team.
    Consider key terms, user intent, and urgency level.
    </reasoning>

    <selection>
    The chosen team name
    </selection>
    """,
            role="user",
        )
    )

    billing_support_branch.commit_message(
        message=Message(content=support_routes["billing"], role="user")
    )
    account_security_branch.commit_message(
        message=Message(content=support_routes["account"], role="user")
    )
    technical_support_branch.commit_message(
        message=Message(content=support_routes["technical"], role="user")
    )
    product_support_branch.commit_message(
        message=Message(content=support_routes["product"], role="user")
    )

    for i, ticket in enumerate(tickets, 1):
        # Create temporary branches for each route for this ticket
        canvas.checkout(route_analysis_branch.name)
        temp_route_analysis_branch = canvas.checkout(
            f"ticket-{i}-route_analysis", create_if_not_exists=True
        )

        canvas.checkout(billing_support_branch.name)
        temp_billing_support_branch = canvas.checkout(
            f"ticket-{i}-billing", create_if_not_exists=True
        )

        canvas.checkout(account_security_branch.name)
        temp_account_security_branch = canvas.checkout(
            f"ticket-{i}-account", create_if_not_exists=True
        )

        canvas.checkout(technical_support_branch.name)
        temp_technical_support_branch = canvas.checkout(
            f"ticket-{i}-technical", create_if_not_exists=True
        )

        canvas.checkout(product_support_branch.name)
        temp_product_support_branch = canvas.checkout(
            f"ticket-{i}-product", create_if_not_exists=True
        )

        # Create route_branches mapping for this ticket
        ticket_route_branches = {
            "account": temp_account_security_branch,
            "technical": temp_technical_support_branch,
            "billing": temp_billing_support_branch,
            "product": temp_product_support_branch,
        }

        route(
            ticket,
            support_routes,
            route_branches=ticket_route_branches,
            route_analysis_branch=temp_route_analysis_branch,
        )
