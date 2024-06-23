import json
import requests

headers = {"Content-Type": "application/json"}


def text_generation(data, ip="localhost", port=None):
    resp = requests.put(f"http://{ip}:{port}/generate", data=json.dumps(data), headers=headers)
    return resp.json()


def get_generation(
    prompt, greedy, add_BOS, token_to_gen, min_tokens, temp, top_p, top_k, repetition, batch=False
):
    data = {
        "sentences": [prompt] if not batch else prompt,
        "tokens_to_generate": int(token_to_gen),
        "temperature": temp,
        "add_BOS": add_BOS,
        "top_k": top_k,
        "top_p": top_p,
        "greedy": greedy,
        "all_probs": False,
        "repetition_penalty": repetition,
        "min_tokens_to_generate": int(min_tokens),
        "end_strings": ["<|endoftext|>", "<extra_id_1>", "\x11", "<extra_id_1>User"],
    }
    sentences = text_generation(data, port=1424)["sentences"]
    return sentences[0] if not batch else sentences


PROMPT_TEMPLATE = """<extra_id_0>System

<extra_id_1>User
{prompt}
<extra_id_1>Assistant
"""

question = "Ge en sammanfattning av de 5 kändaste svenska författarna och deras verk."
question2 = "Vilka danska kungar har krigat mot Sverige? Berätta om deras krig och vad som hände."
question3 = """Ska det vara 'de' eller 'dem' i följande meningar:

1. Jag gav det till {de/dem}.
2. Jag gav {de/dem} det.
3. Vi spelade fotboll med {de/dem} bästa spelarna.
4. {De/Dem} såg jag på stan.

Motivera varför den ena eller andra formen ska användas.
"""
prompt = PROMPT_TEMPLATE.format(prompt=question)
prompt2 = PROMPT_TEMPLATE.format(prompt=question2)
prompt3 = PROMPT_TEMPLATE.format(prompt=question3)
prompts = [prompt, prompt2, prompt3]
print(prompts)

# "Batch = False" if you only send one prompt
response = get_generation(
    prompts,
    greedy=True,
    add_BOS=False,
    token_to_gen=1024,
    min_tokens=1,
    temp=1.0,
    top_p=1.0,
    top_k=0,
    repetition=1.0,
    batch=True,
)

if len(response) == 1:
    response = response[len(prompts[0]) :]
    if response.endswith("<extra_id_1>"):
        response = response[: -len("<extra_id_1>")]
    # print(prompts[0])
    print(response)

if len(response) > 2:
    for i, res in enumerate(response):
        res = res[len(prompts[i]) :]
        if res.endswith("<extra_id_1>"):
            res = res[: -len("<extra_id_1>")]
        # print(prompts[i])
        print(res)
