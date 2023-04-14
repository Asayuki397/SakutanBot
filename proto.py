import openai
import json


def initVar():

    global EL_key
    global OAI_key
    global EL_voice
    global video_id
    global tts_type
    global OAI
    global EL
    global OAIKR

    try:
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
    except:
        print("Unable to open JSON file.")
        exit()

    class OAI:
        key = data["keys"][0]["OAI_key"]
        model = data["OAI_data"][0]["model"]
        prompt = data["OAI_data"][0]["prompt"]
        temperature = data["OAI_data"][0]["temperature"]
        max_tokens = data["OAI_data"][0]["max_tokens"]
        top_p = data["OAI_data"][0]["top_p"]
        frequency_penalty = data["OAI_data"][0]["frequency_penalty"]
        presence_penalty = data["OAI_data"][0]["presence_penalty"]

    class OAIKR:
        key = data["keys"][1]["OAI_key"]
        model = data["OAI_data"][1]["model"]
        prompt = data["OAI_data"][1]["prompt"]
        temperature = data["OAI_data"][1]["temperature"]
        max_tokens = data["OAI_data"][1]["max_tokens"]
        top_p = data["OAI_data"][1]["top_p"]
        frequency_penalty = data["OAI_data"][1]["frequency_penalty"]
        presence_penalty = data["OAI_data"][1]["presence_penalty"]

    class EL:
        key = data["keys"][0]["EL_key"]
        voice = data["EL_data"][0]["voice"]

initVar()

def llm(message, cached = None, lang = "en"):

    if lang == "en":
        if cached is not None:
            cache_prompt = "".join(cached) + "\nMaster: " + message + "\nARiSA:"
        else:
            cache_prompt = "\nMaster: " + message + "\nARiSA:"

        openai.api_key = OAI.key
        response = openai.Completion.create(
        model= OAI.model,
        prompt= OAI.prompt + cache_prompt,
        temperature = OAI.temperature,
        max_tokens = OAI.max_tokens,
        top_p = OAI.top_p,
        frequency_penalty = OAI.frequency_penalty,
        presence_penalty = OAI.presence_penalty
        )
        json_object = json.loads(str(response))

    elif lang == "kr":
        if cached is not None:
            cache_prompt = "".join(cached) + "\n주인님: " + message + "\n아리사:"
        else:
            cache_prompt = "\n주인님: " + message + "\n아리사:"

        openai.api_key = OAI.key
        response = openai.Completion.create(
        model= OAIKR.model,
        prompt= OAIKR.prompt + cache_prompt,
        temperature = OAIKR.temperature,
        max_tokens = OAIKR.max_tokens,
        top_p = OAIKR.top_p,
        frequency_penalty = OAIKR.frequency_penalty,
        presence_penalty = OAIKR.presence_penalty
        )
        json_object = json.loads(str(response))

    

    
    return(json_object['choices'][0]['text'])



if __name__ == "__main__":
    master_input = input("prompt : ")
    print(llm(master_input))