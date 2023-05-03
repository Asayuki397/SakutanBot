import openai
import json


def initVar():

    global OAI
    global EL
    try:
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
    except:
        print("Unable to open JSON file.")
        exit()

    class OAI:
        key = data["keys"][0]["OAI_key"]

    class EL:
        key = data["keys"][0]["EL_key"]
        voice = data["EL_data"][0]["voice"]

def llm(message, cached = None) -> str:
    """returns the reply from the model
    
    parameters

    message : str
    cached : iterable
    """

    pre_prompt = [
        {"role" : "system", "content" : "You are a dedicated maid named Arisa. This is a conversation between you and your master."},       
    ]

    if len(cached) > 0:
        for cache in cached:
            pre_prompt.append(cache)
    
    pre_prompt.append(
        {"role" : "user", "content" : str(message)}
    )

    openai.api_key = OAI.key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=pre_prompt,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=512,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    for choice in response.choices:
        if "text" in choice:
            return choice.text

    return response.choices[0].message.content
    


MAX_CACHE_SIZE = 6
if __name__ == "__main__":
    
    initVar()
    cache = []

    while True:

        while len(cache) > MAX_CACHE_SIZE:
            cache.pop(0)

        master_input = input("prompt : ")
        res = llm(master_input, cached = cache)
        print(res)

        new_cache = [
            {"role" : "user", "content" : str(master_input)},
            {"role" : "assistant", "content" : str(res)}
        ]

        for cache in new_cache:
            cache.append(cache)