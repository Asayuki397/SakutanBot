import openai
from textblob import TextBlob
from google.cloud import texttospeech
from playsound import playsound
import requests
from io import BytesIO
from PIL import Image
from live2d import Live2DModel

# GPT-3 API 인증 정보 설정
openai.api_key = "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"

# Google Cloud 인증 정보 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YOUR_CREDENTIALS.json"

# Live2D 모델 로드
model = Live2DModel("shizuku.model3.json")

# Live2D 모델 초기화
model.set_motion("idle_1")

# 사용자 입력 받기
user_input = input("질문: ")

# GPT-3에 질문 보내기
response = openai.Completion.create(
    engine="davinci",
    prompt=user_input,
    temperature=0.7,
    max_tokens=50,
    n=1,
    stop=None,
)

# GPT-3 답변 출력
answer = response.choices[0].text.strip()
print("답변: " + answer)

# 감정 분석 수행
blob = TextBlob(answer)
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

# TTS로 답변 음성 생성
client = texttospeech.TextToSpeechClient()
synthesis_input = texttospeech.SynthesisInput(text=answer)
voice = texttospeech.VoiceSelectionParams(
    language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio

audio_content = response.audio_content
with open("answer.mp3", "wb") as out:
out.write(audio_content)
playsound("answer.mp3")

model.update_motions()
model.draw()

image_data = model.to_image()
image = Image.open(BytesIO(image_data))
image.show()