import ollama

code_prompt = input("Enter your code prompt: ") or (code_prompt := "Make a hello world")
response = ollama.generate(model='llama3.2', prompt=code_prompt)
print(response['response'])