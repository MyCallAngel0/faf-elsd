from openai import OpenAI
import json

with open('tokens.json', 'r') as file:
    data = json.load(file)

client = OpenAI(api_key=data['CHATGPT_BOT'])
# message = {"role":"user", "content": input("This is the beginning of your chat with AI. [To exit, send \"###\".]\n\nYou:")};
# conversation = [{"role": "system", "content": "DIRECTIVE_FOR_gpt-3.5-turbo"}]

userdata = {}

async def ask_prompt(user:str, prompt: str) -> str:
    prompt = prompt[:255]

    if user not in userdata:
        userdata[user]=[{"role": "system","content":"Answer the questions"}]
    userdata[user] += [{"role": "user", "content":prompt}]
    print(userdata[user])
    

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=userdata[user],
        max_tokens=1000
    )
    
    userdata[user] += [{"role": "assistant", "content":response.choices[0].message.content.strip()}]
    userdata[user] = userdata[user][-50:]
    userdata[user][0]={"role": "system","content":"Answer the questions"}
    
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
