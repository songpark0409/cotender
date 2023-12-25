from openai import OpenAI
import streamlit as st
import time
import elevenlabs

assistant_id = "asst_zlQiYutOyBhPH9tpIZG0Mtib"
thread_id = "thread_W1grA8BV3GqexQqqz2zO2IoD"

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password", value="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")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    user_input = st.selectbox('Do you want voice?',('yes','no'))
    st.write('You selected:', user_input)

st.title("🍷 Cotender")
st.caption("🚀 101가지의 칵테일 제조법을 알고있는 ai 'cotender'입니다.")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "무엇을 도와드릴까요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=prompt,
    )
    print(response)

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    print(run)

    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
            )
        if run.status == "completed":
            break
        else:
            time.sleep(5)
        print(run)

    thread_messages = client.beta.threads.messages.list(thread_id)
    print(thread_messages.data)

    msg = thread_messages.data[0].content[0].text.value

    #print(msg)

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

    from elevenlabs import generate, play, set_api_key

    elevenlabs.set_api_key("a28b5039b638aa1feabf22ac54827d30")

    audio = generate(
        text=msg,
        voice="Clyde",
        model="eleven_multilingual_v2"
    )

   # play(audio)

    import sys

    if user_input.lower() == 'yes':
        play(audio)
    elif user_input.lower() == 'no':
        sys.exit()
    else:
        print('Type y or n')

    #response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    #msg = response.choices[0].message.content
    #st.session_state.messages.append({"role": "assistant", "content": msg})
    #st.chat_message("assistant").write(msg)