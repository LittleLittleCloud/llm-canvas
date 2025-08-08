from llm_canvas import Canvas
import time


def fake_llm(prompt: str) -> str:
    # placeholder for real LLM call
    # Simulate processing time
    time.sleep(0.5)
    return prompt[::-1]


def main():
    canvas = Canvas()
    canvas.run(port=5173, background=True)
    
    print("Adding first user message...")
    user_msg = canvas.add_message("Hello model", role="user")
    time.sleep(0.2)  # Brief pause before LLM response
    
    print("Generating assistant response...")
    response = fake_llm("Hello model")
    canvas.add_message(response, role="assistant", parent_node=user_msg)
    time.sleep(0.3)  # Pause between conversations
    
    # Add a few more messages to make it interesting
    print("Adding second user message...")
    user_msg2 = canvas.add_message("Can you help me with Python?", role="user", parent_node=user_msg)
    time.sleep(0.2)
    
    print("Generating second assistant response...")
    response2 = fake_llm("Can you help me with Python?")
    canvas.add_message(response2, role="assistant", parent_node=user_msg2)
    time.sleep(0.3)
    
    # Branch conversation
    print("Creating conversation branch...")
    user_msg3 = canvas.add_message("What about JavaScript?", role="user", parent_node=user_msg)
    time.sleep(0.2)
    
    print("Generating branched response...")
    response3 = fake_llm("What about JavaScript?")
    canvas.add_message(response3, role="assistant", parent_node=user_msg3)
    
    time.sleep(0.5)  # Final pause before saving
    canvas.save("example_canvas.json")
    print("Saved example_canvas.json")
    
    print("\nCanvas ready! view the conversation.")
    canvas.wait_for_server()  # Keep the server running

if __name__ == "__main__":
    main()
