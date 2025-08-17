from concurrent.futures import ThreadPoolExecutor

from examples.claude.chain import chain
from examples.shared_client import get_canvas_client
from llm_canvas.types import Message


def parallel(prompt: str, inputs: list[dict], n_workers: int = 3) -> list[str]:
    """Process multiple inputs concurrently with the same prompt."""
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = [executor.submit(chain, prompt, [x["input"]], x["branch"]) for x in inputs]
        return [f.result() for f in futures]


if __name__ == "__main__":
    canvas_client = get_canvas_client()
    canvas = canvas_client.create_canvas("Parallelization")
    main_branch = canvas.checkout("main")

    prompt = """
    Analyze how market changes will impact this stakeholder group.
    Provide specific impacts and recommended actions.
    Format with clear sections and priorities.
    """

    main_branch.commit_message(message=Message(content=prompt, role="user"))

    customer_branch = canvas.checkout("customers", create_if_not_exists=True)
    employee_branch = canvas.checkout("employees", create_if_not_exists=True)
    investor_branch = canvas.checkout("investors", create_if_not_exists=True)
    supplier_branch = canvas.checkout("suppliers", create_if_not_exists=True)

    stakeholders = [
        {
            "input": """Customers:
        - Price sensitive
        - Want better tech
        - Environmental concerns""",
            "branch": customer_branch,
        },
        {
            "input": """Employees:
        - Job security worries
        - Need new skills
        - Want clear direction""",
            "branch": employee_branch,
        },
        {
            "input": """Investors:
        - Expect growth
        - Want cost control
        - Risk concerns""",
            "branch": investor_branch,
        },
        {
            "input": """Suppliers:
        - Capacity constraints
        - Price pressures
        - Tech transitions""",
            "branch": supplier_branch,
        },
    ]

    parallel(
        """Analyze how market changes will impact this stakeholder group.
        Provide specific impacts and recommended actions.
        Format with clear sections and priorities.""",
        stakeholders,
    )
