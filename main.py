import streamlit as st
import json

# Команда запуска программы локально в терминале
# python -m streamlit run main.py

def run():
    st.set_page_config(
        page_title="TEST",
        page_icon="❓",
    )

if __name__ == "__main__":
    run()

# CSS стили для кнопок
st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
</style>
""", unsafe_allow_html=True)

# Переменные сессии
default_values = {'current_index': 0, 'current_question': 0, 'score': 0, 'selected_option': None, 'answer_submitted': False}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)

# Загрузка вопросов из JSON
with open('content/quiz_data.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)


# перезапуск теста с вопросами
def restart_quiz():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

# следующий вопрос
def next_question():
    st.session_state.current_index += 1
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

# Заголовок
st.title("TEST")

# Строка прогресса
progress_bar_value = (st.session_state.current_index + 1) / len(quiz_data)
st.metric(label="Õiged vastused", value=f"{st.session_state.score} / {len(quiz_data)}")
st.progress(progress_bar_value)

# Отображение вопроса 
question_item = quiz_data[st.session_state.current_index]
st.subheader(f"Küsimus {st.session_state.current_index + 1}")
st.title(f"{question_item['question']}")


st.markdown(""" ___""")

# результат правильности ответа
options = question_item['options']
correct_answer = question_item['answer']

if st.session_state.answer_submitted:
    for i, option in enumerate(options):
        label = option
        if option == correct_answer:
            st.success(f"{label} (Õige vastus)")
        elif option == st.session_state.selected_option:
            st.error(f"{label} (Vale vastus)")
        else:
            st.write(label)
else:
    for i, option in enumerate(options):
        # use container width not working
        if st.button(option, key=i):
            st.session_state.selected_option = option

st.markdown(""" ___""")

# обработка нажатияя кнопки подтверждения ответа
def submit_answer():

    # проверка был ли выбран ответ
    if st.session_state.selected_option is not None:
        # помечаем что ответ выбран в сессии
        st.session_state.answer_submitted = True
        # проверка правильности ответа
        if st.session_state.selected_option == quiz_data[st.session_state.current_index]['answer']:
            st.session_state.score += 1
    else:
        # Если не выбран никакой ответ выдаем ала
        st.warning("Palun valige vastus!")


# обработка кнопки далее
if st.session_state.answer_submitted:
    if st.session_state.current_index < len(quiz_data) - 1:
        st.button('Järgmine', on_click=next_question)
    else:
        st.write(f"Test on lõpetatud! Õiged vastused: {st.session_state.score} / {len(quiz_data)}")
        if st.button('Uuesti', on_click=restart_quiz):
            pass
else:
    if st.session_state.current_index < len(quiz_data):
        st.button('Salvesta ja edasi', on_click=submit_answer)

