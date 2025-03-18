import ollama
from typing import Literal

""" Tool function: add two numbers """
def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers and return the result.
    """
    # Ensure the inputs are integers
    a = int(a) if isinstance(a, str) else a
    b = int(b) if isinstance(b, str) else b
    return a + b

""" Tool function: do mathematical operations (add, subtract, multiply, divide) """
def calculate(a: int, b: int, operation: Literal["+", "-", "*", "/"]) -> float:
    """
    Perform a mathematical operation on two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.
        operation (Literal["+", "-", "*", "/"]): The operation to perform.
    Returns:
        float: The result of the operation.
    Raises:
        ValueError: If the operation is not one of the supported operations.
    Note:
        If the operation is "divide" and the second number (b) is 0, the function will return 0 to avoid division by zero.

    """
    # Ensure the inputs are integers
    a = int(a) if isinstance(a, str) else a
    b = int(b) if isinstance(b, str) else b

    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        if b == 0:
            return 0
        return a / b
    else:
        raise ValueError(f"Invalid operation: {operation}. Supported operations: add, subtract, multiply, divide.")
    
""" System prompt to inform the model about the tool is usage """
system_message = {
    "role": "system", 
    "content": "You are a helpful assistant. Use the tools as needed. Always chat with normal texts, never use markdown or code blocks. "
}

for op in ["+", "-", "*", "/"]:
    # User asks a question that involves a calculation
    user_message = {
        "role": "user", 
        "content": f"What is 10 {op} 10?"
    }
    messages = [system_message, user_message]


    response = ollama.chat(
        model='llama3.2', 
        messages=messages,
        tools=[calculate]  # pass the actual function object as a tool
    )

    if response.message.tool_calls:
        for tool_call in response.message.tool_calls:
            func_name = tool_call.function.name   # e.g., "add_two_numbers"
            args = tool_call.function.arguments   # e.g., {"a": 10, "b": 10}
            # If the function name matches and we have it in our tools, execute it:
            if func_name == "calculate":
                result = calculate(**args)
                print("Function output:", result)
                messages.append({"role": "tool", "tool_result": f"{result}", "content": "tell me the result in a professional way."})
                follow_up = ollama.chat(model='llama3.2', messages=messages)
                print("Assistant (final):", follow_up.message.content)

""" (Continuing from previous code) """

# available_functions = {"add_two_numbers": add_two_numbers}

# """ Model's initial response after possibly invoking the tool """
# assistant_reply = response.message.content
# print("Assistant (initial):", assistant_reply)

# """ If a tool was called, handle it """
# for tool_call in (response.message.tool_calls or []):
#     func = available_functions.get(tool_call.function.name)
#     if func:
#         result = func(**tool_call.function.arguments)
#         # Provide the result back to the model in a follow-up message
#         messages.append({"role": "assistant", "content": f"The result is {result}."})
#         follow_up = ollama.chat(model='llama3.2', messages=messages)
#         print("Assistant (final):", follow_up.message.content)