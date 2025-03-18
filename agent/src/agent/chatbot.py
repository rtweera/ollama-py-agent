import ollama

# Choose a chat-capable model (ensured it is pulled)
model_name = 'llama3.2'

# Initialize conversation with a system prompt (optional) and a user message
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
]

# First response from the bot
response = ollama.chat(model=model_name, messages=messages)
print("Bot:", response.message.content)

# Continue the conversation:
while True:
    user_input = input("You: ")
    if not user_input:
        break  # exit loop on empty input
    messages.append({"role": "user", "content": user_input})
    response = ollama.chat(model=model_name, messages=messages)
    answer = response.message.content
    print("Bot:", answer)
    messages.append({"role": "assistant", "content": answer})