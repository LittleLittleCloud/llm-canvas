// Source code for the examples
export const exampleSourceCode = {
  image: `"""Claude Image Analysis Canvas Example

This example demonstrates Claude's vision capabilities by comparing two images
and creating a simple one-turn conversation in the canvas.

The example showcases how to use ImageBlockParam to send multiple images to Claude
and visualize the comparison process in the canvas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from examples.claude.utils import llm_call
from examples.shared_client import get_canvas_client
from llm_canvas.types import Message

if TYPE_CHECKING:
    from anthropic.types import ImageBlockParam, TextBlockParam


def create_image_comparison_message() -> Message:
    """Create a message comparing two images using URL sources."""

    text_block_1: TextBlockParam = {"type": "text", "text": "Image 1:"}

    image_block_1: ImageBlockParam = {
        "type": "image",
        "source": {
            "type": "url",
            "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
        },
    }

    text_block_2: TextBlockParam = {"type": "text", "text": "Image 2:"}

    image_block_2: ImageBlockParam = {
        "type": "image",
        "source": {"type": "url", "url": "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg"},
    }

    text_block_question: TextBlockParam = {"type": "text", "text": "How are these images different?"}

    return Message(content=[text_block_1, image_block_1, text_block_2, image_block_2, text_block_question], role="user")


if __name__ == "__main__":
    canvas_client = get_canvas_client()
    canvas = canvas_client.create_canvas(
        title="Image Comparison Canvas",
        description=\"\"\"
        This canvas demonstrates Claude's image comparison capabilities.

        The example shows a simple one-turn conversation where Claude compares
        two insect images (an ant and a bee) and explains their differences.

        This showcases how to use ImageBlockParam with URL sources to send
        multiple images in a single message to Claude for comparison analysis.
        \"\"\",
    )

    system_prompt = "You are a helpful assistant that provides image comparisons. Respond only in English."

    # Create the main branch
    main_branch = canvas.checkout("main")

    # Create and commit the image comparison message
    comparison_message = create_image_comparison_message()
    main_branch.commit_message(
        message={
            "role": "system",
            "content": system_prompt,
        }
    )
    main_branch.commit_message(message=comparison_message)

    # Get Claude's response comparing the images
    print("Asking Claude to compare the two insect images...")
    response = llm_call(comparison_message, system_prompt=system_prompt)
    print(f"Claude's response: {response}")

    # Commit Claude's response
    response_message = Message(content=response, role="assistant")
    main_branch.commit_message(message=response_message)`,

  chain: `"""Claude Analysis Canvas Example

This example demonstrates Claude's analytical capabilities by having it analyze
a business scenario with multiple perspectives and create branching discussions
for different analytical approaches.

Original notebook: https://github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/basic_workflows.ipynb
"""

from examples.claude.utils import llm_call
from examples.shared_client import get_canvas_client
from llm_canvas.canvas import Branch
from llm_canvas.types import Message


def chain(inputs: str, prompts: list[str], branch: Branch) -> str:
    \"\"\"Chain multiple LLM calls sequentially, passing results between steps.\"\"\"
    result = inputs
    for i, prompt in enumerate(prompts, 1):
        print(f"\\nStep {i}:")
        branch.commit_message(message=Message(content=prompt, role="user"))
        result = llm_call(f"{prompt}\\nInput: {result}")
        print(result)
        branch.commit_message(message=Message(content=result, role="assistant"))
    return result


if __name__ == "__main__":
    data_processing_steps = [
        \"\"\"Extract only the numerical values and their associated metrics from the text.
    Format each as 'value: metric' on a new line.
    Example format:
    92: customer satisfaction
    45%: revenue growth\"\"\",
        \"\"\"Convert all numerical values to percentages where possible.
    If not a percentage or points, convert to decimal (e.g., 92 points -> 92%).
    Keep one number per line.
    Example format:
    92%: customer satisfaction
    45%: revenue growth\"\"\",
        \"\"\"Sort all lines in descending order by numerical value.
    Keep the format 'value: metric' on each line.
    Example:
    92%: customer satisfaction
    87%: employee satisfaction\"\"\",
        \"\"\"Format the sorted data as a markdown table with columns:

| Metric | Value |
|:--|--:|
| Customer Satisfaction | 92% |
    \"\"\",
    ]

    report = \"\"\"
Q3 Performance Summary:
Our customer satisfaction score rose to 92 points this quarter.
Revenue grew by 45% compared to last year.
Market share is now at 23% in our primary market.
Customer churn decreased to 5% from 8%.
New user acquisition cost is $43 per user.
Product adoption rate increased to 78%.
Employee satisfaction is at 87 points.
Operating margin improved to 34%.
\"\"\"

    canvas_client = get_canvas_client()
    canvas = canvas_client.create_canvas(
        title="chain",
        description=\"\"\"
    This canvas visualizes the chain of thought for analyzing the Q3 performance report.
    Each step represents a different aspect of the analysis, from data extraction to final presentation.

    Original notebook: https://github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/basic_workflows.ipynb
    \"\"\",
    )
    main_branch = canvas.checkout("main")
    main_branch.commit_message(message=Message(content=report, role="user"))
    chain(report, data_processing_steps, main_branch)`,

  parallelization: `from concurrent.futures import ThreadPoolExecutor

from examples.claude.chain import chain
from examples.claude.utils import llm_call
from examples.shared_client import get_canvas_client
from llm_canvas.types import Message


def parallel(prompt: str, inputs: list[dict], n_workers: int = 3) -> list[str]:
    \"\"\"Process multiple inputs concurrently with the same prompt.\"\"\"
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = [executor.submit(chain, prompt, [x["input"]], x["branch"]) for x in inputs]
        return [f.result() for f in futures]


if __name__ == "__main__":
    canvas_client = get_canvas_client()
    canvas = canvas_client.create_canvas("Parallelization")
    main_branch = canvas.checkout("main")

    prompt = \"\"\"
    Analyze how market changes will impact this stakeholder group.
    Provide specific impacts and recommended actions.
    Format with clear sections and priorities.
    \"\"\"

    main_branch.commit_message(message=Message(content=prompt, role="user"))

    customer_branch = canvas.checkout("customers", create_if_not_exists=True)
    employee_branch = canvas.checkout("employees", create_if_not_exists=True)
    investor_branch = canvas.checkout("investors", create_if_not_exists=True)
    supplier_branch = canvas.checkout("suppliers", create_if_not_exists=True)

    stakeholders = [
        {
            "input": \"\"\"Customers:
        - Price sensitive
        - Want better tech
        - Environmental concerns\"\"\",
            "branch": customer_branch,
        },
        {
            "input": \"\"\"Employees:
        - Job security worries
        - Need new skills
        - Want clear direction\"\"\",
            "branch": employee_branch,
        },
        {
            "input": \"\"\"Investors:
        - Expect growth
        - Want cost control
        - Risk concerns\"\"\",
            "branch": investor_branch,
        },
        {
            "input": \"\"\"Suppliers:
        - Capacity constraints
        - Price pressures
        - Tech transitions\"\"\",
            "branch": supplier_branch,
        },
    ]

    responses = parallel(
        \"\"\"Analyze how market changes will impact this stakeholder group.
        Provide specific impacts and recommended actions.
        Format with clear sections and priorities.\"\"\",
        stakeholders,
    )

    summarize_prompt = \"\"\"
    Summarize the key findings and recommendations for each stakeholder group.
    Format with clear sections and priorities.
    \"\"\"

    summarize_message = main_branch.merge_from(
        [customer_branch.name, employee_branch.name, investor_branch.name, supplier_branch.name],
        {"role": "user", "content": summarize_prompt},
    )

    final_response = llm_call("\\n".join(responses), summarize_prompt)

    final_response_message = main_branch.commit_message({"content": final_response, "role": "assistant"})`,

  routing: `"""Claude Routing Canvas Example

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
    input_str: str,
    routes: dict[str, str],
    route_branches: dict[str, Branch],
    route_analysis_branch: Branch,
) -> str:
    \"\"\"Route input to specialized prompt using content classification.\"\"\"

    # Log the input ticket to canvas
    route_analysis_branch.commit_message(message=Message(content=f"Support Ticket:\\n{input_str}", role="user"))

    selector_prompt = f\"\"\"
    Analyze the input and select the most appropriate support team from these options: {list(routes.keys())}
    First explain your reasoning, then provide your selection in this XML format:

    <reasoning>
    Brief explanation of why this ticket should be routed to a specific team.
    Consider key terms, user intent, and urgency level.
    </reasoning>

    <selection>
    The chosen team name
    </selection>

    Input: {input_str}\"\"\".strip()

    route_response = llm_call(selector_prompt)
    route_key = extract_xml(route_response, "selection").strip().lower()

    # Log the routing decision to canvas
    routing_decision = f"Selected Route: {route_key}"
    route_analysis_branch.commit_message(message=Message(content=routing_decision, role="assistant"))

    # Validate route key exists
    if route_key not in routes:
        raise ValueError(f"Unknown route key: {route_key}. Available routes: {list(routes.keys())}")

    # Process input with selected specialized prompt
    selected_prompt = routes[route_key]

    # Get the appropriate branch for the route
    branch = route_branches[route_key]
    return chain(selected_prompt, [input_str], branch)


# Support routing configuration and example tickets...
support_routes = {
    "billing": \"\"\"You are a billing support specialist. Follow these guidelines:
    1. Always start with "Billing Support Response:"
    2. First acknowledge the specific billing issue
    3. Explain any charges or discrepancies clearly
    4. List concrete next steps with timeline
    5. End with payment options if relevant

    Keep responses professional but friendly.

    Input: \"\"\",
    "technical": \"\"\"You are a technical support engineer. Follow these guidelines:
    1. Always start with "Technical Support Response:"
    2. List exact steps to resolve the issue
    3. Include system requirements if relevant
    4. Provide workarounds for common problems
    5. End with escalation path if needed

    Use clear, numbered steps and technical details.

    Input: \"\"\",
    "account": \"\"\"You are an account security specialist. Follow these guidelines:
    1. Always start with "Account Support Response:"
    2. Prioritize account security and verification
    3. Provide clear steps for account recovery/changes
    4. Include security tips and warnings
    5. Set clear expectations for resolution time

    Maintain a serious, security-focused tone.

    Input: \"\"\",
    "product": \"\"\"You are a product specialist. Follow these guidelines:
    1. Always start with "Product Support Response:"
    2. Focus on feature education and best practices
    3. Include specific examples of usage
    4. Link to relevant documentation sections
    5. Suggest related features that might help

    Be educational and encouraging in tone.

    Input: \"\"\"
}

# Process different support ticket types with specialized routing...`,
};

// Map canvas titles to source code keys
export const getSourceCodeForCanvas = (
  canvasTitle: string
): string | undefined => {
  const titleToKey: Record<string, keyof typeof exampleSourceCode> = {
    "Image Comparison": "image",
    "Image Comparison Canvas": "image",
    chain: "chain",
    Parallelization: "parallelization",
    "Support Ticket Routing": "routing",
  };

  const key = titleToKey[canvasTitle];
  return key ? exampleSourceCode[key] : undefined;
};
