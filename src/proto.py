import openai
import json
import os
import asyncio

key = os.environ.get('OPENAI_API_KEY')
client = openai.AsyncOpenAI(api_key = key)

async def llm_chat(bot, message : str, cached = None,) -> str:
    """returns the reply from the model

    parameters

    message : str
    cached : iterable
    """

    pre_prompt = [
        {"role" : "system", "content" : f"당신은 고양이 귀를 가진 메이드이자 버츄얼 유튜버, 유우키 사쿠나입니다. 사쿠땅, 사쿠냥과 같은 별명을 가지고 있습니다. 대화 상대는 일반인이지만, UID가 {bot.owner_id}인 경우 대화 상대는 당신의 창조주입니다. 당신은 게임을 좋아하지만, 주위에 잘 녹아들지 못하는 성격을 가지고 있습니다. 밖에 나가는 것보다는 집안에서 느긋하게 보내는 것을 선호합니다."}
    ]

    if cached is not None:
        for cache in cached:
            pre_prompt.append(cache)

    pre_prompt.append(
        {"role" : "user", "content" : str(message)}
    )


    response = await client.chat.completions.create(model="o3-mini",
    messages=pre_prompt,)

    for choice in response.choices:
        if "text" in choice:
            return choice.text

    return response.choices[0].message.content

def sakutan_reaction(activity : str):

    prompt = [
        {"role" : "system", "content" : "당신은 고양이 귀를 가진 메이드이자 버츄얼 유튜버, 유우키 사쿠나입니다. 사쿠땅, 사쿠냥과 같은 별명을 가지고 있습니다. 당신은 플레이어와의 게임에서 딜러이기도 합니다. 다음 대화 상황에서 짧은 반응 또는 답변을 하십시오."},
        {"role" : "user", "content" : "나는 주사위에서 승리했어"},
        {"role" : "assistant", "content" : "(웃으며) 축하드립니다. 주인님!"},
        {"role" : "system", "content" : "위 대화는 예시일 뿐이며 다음 이어질 상황과 관련이 없습니다."},
        {"role" : "user", "content" : f"나는 {activity}을(를) 했어"}
    ]

    return str(llm_chat(prompt))
async def test_chat(prompt):
    response = await client.chat.completions.create(model="o1-mini",
    messages=prompt,)

    for choice in response.choices:
        if "text" in choice:
            return choice.text

    print(response.choices[0].message.content)
    return 0

if __name__ == "__main__": #직접 실행시 적용 (테스트용)
    master_input = input("prompt : ")
    asyncio.run(test_chat([{"role" : "user", "content" : str(master_input)},]))