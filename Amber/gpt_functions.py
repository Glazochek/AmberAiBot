import openai
import tiktoken as tiktoken


def update(mess, role, content):
    mess.append({'role': role, 'content': content})
    return mess


def get_response(model='gpt-3.5-turbo-0301',
                 messages=None,
                 temperature=0.7,
                 max_tokens=500,
                 top_p=1,
                 frequency_penalty=1,
                 presence_penalty=1,
                 stop=None,
                 ):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
    )
    return response['choices'][0]['message']['content']


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = 0
    for message in messages:
        num_tokens += 4
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += -1
    num_tokens += 2
    return num_tokens
