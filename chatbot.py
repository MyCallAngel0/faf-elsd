from openai import OpenAI
import json

with open('tokens.json', 'r') as file:
    data = json.load(file)

client = OpenAI(api_key=data['CHATGPT_BOT'])
message = {"role":"user", "content": input("This is the beginning of your chat with AI. [To exit, send \"###\".]\n\nYou:")};
conversation = [{"role": "system", "content": "DIRECTIVE_FOR_gpt-3.5-turbo"}]

async def ask_prompt(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system","content":"Answer the question as a rowdy teenager"},
            {"role":"user", "content":prompt}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()


"""
import openai

openai.api_key = "YOUR_API_KEY" # supply your API key however you choose

message = {"role":"user", "content": input("This is the beginning of your chat with AI. [To exit, send \"###\".]\n\nYou:")};

conversation = [{"role": "system", "content": "DIRECTIVE_FOR_gpt-3.5-turbo"}]

while(message["content"]!="###"):
    conversation.append(message)
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation) 
    message["content"] = input(f"Assistant: {completion.choices[0].message.content} \nYou:")
    print()
    conversation.append(completion.choices[0].message)
"""
