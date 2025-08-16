"""Claude Analysis Canvas Example

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
    """Chain multiple LLM calls sequentially, passing results between steps."""
    result = inputs
    for i, prompt in enumerate(prompts, 1):
        print(f"\nStep {i}:")
        branch.commit_message(message=Message(content=prompt, role="user"))
        result = llm_call(f"{prompt}\nInput: {result}")
        print(result)
        branch.commit_message(message=Message(content=result, role="assistant"))
    return result


if __name__ == "__main__":
    data_processing_steps = [
        """Extract only the numerical values and their associated metrics from the text.
    Format each as 'value: metric' on a new line.
    Example format:
    92: customer satisfaction
    45%: revenue growth""",
        """Convert all numerical values to percentages where possible.
    If not a percentage or points, convert to decimal (e.g., 92 points -> 92%).
    Keep one number per line.
    Example format:
    92%: customer satisfaction
    45%: revenue growth""",
        """Sort all lines in descending order by numerical value.
    Keep the format 'value: metric' on each line.
    Example:
    92%: customer satisfaction
    87%: employee satisfaction""",
        """Format the sorted data as a markdown table with columns:

| Metric | Value |
|:--|--:|
| Customer Satisfaction | 92% |
    """,
    ]

    report = """
Q3 Performance Summary:
Our customer satisfaction score rose to 92 points this quarter.
Revenue grew by 45% compared to last year.
Market share is now at 23% in our primary market.
Customer churn decreased to 5% from 8%.
New user acquisition cost is $43 per user.
Product adoption rate increased to 78%.
Employee satisfaction is at 87 points.
Operating margin improved to 34%.
"""

    canvas_client = get_canvas_client()
    canvas = canvas_client.create_canvas(
        title="chain",
        description="""
    This canvas visualizes the chain of thought for analyzing the Q3 performance report.
    Each step represents a different aspect of the analysis, from data extraction to final presentation.

    Original notebook: https://github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/basic_workflows.ipynb
    """,
    )
    main_branch = canvas.checkout("main")
    main_branch.commit_message(message=Message(content=report, role="user"))
    chain(report, data_processing_steps, main_branch)
