import openai
import json
import requests

def initVar():
    global EL_key
    global OAI_key
    global EL_voice
    global video_id
    global tts_type
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
        model = data["OAI_data"][0]["model"]
        prompt = data["OAI_data"][0]["prompt"]
        temperature = data["OAI_data"][0]["temperature"]
        max_tokens = data["OAI_data"][0]["max_tokens"]
        top_p = data["OAI_data"][0]["top_p"]
        frequency_penalty = data["OAI_data"][0]["frequency_penalty"]
        presence_penalty = data["OAI_data"][0]["presence_penalty"]

    class EL:
        key = data["keys"][0]["EL_key"]
        voice = data["EL_data"][0]["voice"]

def llm(message):

    openai.api_key = OAI.key
    response = openai.Completion.create(
      model= OAI.model,
      prompt= OAI.prompt + "\n\nMaster: " + message + "\nARiSA:",
      temperature = OAI.temperature,
      max_tokens = OAI.max_tokens,
      top_p = OAI.top_p,
      frequency_penalty = OAI.frequency_penalty,
      presence_penalty = OAI.presence_penalty
    )

    json_object = json.loads(str(response))
    return(json_object['choices'][0]['text'])

def EL_TTS(message):

    url = f'https://api.elevenlabs.io/v1/text-to-speech/{EL.voice}'
    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': EL.key,
        'Content-Type': 'application/json'
    }
    data = {
        'text': message,
        'voice_settings': {
            'stability': 0.75,
            'similarity_boost': 0.75
        }
    }

    response = requests.post(url, headers=headers, json=data, stream=True)
    audio_content = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
    play(audio_content)

master_input = input(prompt : )
res = llm(master_input)
EL_TTS(res)
print(res)