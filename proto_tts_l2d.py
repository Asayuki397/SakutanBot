import openai
import json
import requests
import cv2

# Live2D 모델 로드
model = Live2DModel("shizuku.model3.json")

# Live2D 모델 초기화
model.set_motion("idle_1")

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

initVar()
master_input = input(prompt : )
res = llm(master_input)

# 감정 분석 수행
blob = TextBlob(res)
polarity = blob.sentiment.polarity
subjectivity = blob.sentiment.subjectivity

# 감정 분석 결과에 따라 Live2D 모델 제어
if polarity > 0:
    # 긍정적인 감정일 경우
    model.set_expression("happy")
    model.set_motion("motion_3")
elif polarity < 0:
    # 부정적인 감정일 경우
    model.set_expression("sad")
    model.set_motion("motion_6")
else:
    # 중립적인 감정일 경우
    model.set_expression("normal")
    model.set_motion("idle_1")

EL_TTS(res)
print(res)