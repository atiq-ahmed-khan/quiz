import streamlit as st
import time

# Initialize session state
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# Questions
questions = [
    {"question": "What does the 'yield' keyword do in Python?", "options": ["Returns a value", "Creates a generator", "Throws an error", "Initializes a loop"], "answer": "Creates a generator"},
    {"question": "What is the output of: type(lambda x: x)?", "options": ["function", "<class 'function'>", "lambda", "callable"], "answer": "<class 'function'>"},
    {"question": "Which of these is not a valid Python data type?", "options": ["Array", "String", "Integer", "List"], "answer": "Array"},
    {"question": "How do you create a virtual environment in Python 3?", "options": ["python -m venv env", "python create env", "virtualenv env", "env create"], "answer": "python -m venv env"},
    {"question": "Which built-in module can handle serialization in Python?", "options": ["pickle", "json", "os", "csv"], "answer": "pickle"},
    {"question": "What is the correct way to open a file for writing in Python?", "options": ["open('file.txt', 'r')", "open('file.txt', 'w')", "open('file.txt', 'a')", "open('file.txt')"], "answer": "open('file.txt', 'w')"},
    {"question": "Which keyword is used to handle exceptions?", "options": ["try", "catch", "except", "handle"], "answer": "try"},
    {"question": "What does the init() function do?", "options": ["Creates a class", "Initializes a class", "Initializes a variable", "Defines a function"], "answer": "Initializes a class"},
    {"question": "Which module in Python is used for regular expressions?", "options": ["re", "regex", "relib", "patterns"], "answer": "re"},
    {"question": "What is the result of 2 ** 3 ** 2?", "options": ["8", "64", "512", "128"], "answer": "512"},
    {"question": "Which of these is a mutable type?", "options": ["tuple", "list", "string", "int"], "answer": "list"},
    {"question": "Which statement is used to define a function in Python?", "options": ["def", "function", "func", "create"], "answer": "def"},
    {"question": "How do you import a module named 'math'?", "options": ["import math", "import math()", "from math import *", "import math as m"], "answer": "import math"},
    {"question": "What is the correct file extension for Python files?", "options": [".py", ".txt", ".exe", ".p"], "answer": ".py"},
    {"question": "Which operator is used for floor division?", "options": ["//", "/", "%", "div"], "answer": "//"},
    {"question": "What does len() function return?", "options": ["Number of elements", "Length of string", "Length of list", "Length of tuple"], "answer": "Number of elements"},
    {"question": "How do you declare a comment in Python?", "options": ["// comment", "# comment", "/* comment */", "-- comment"], "answer": "# comment"},
    {"question": "Which function is used to convert a string to an integer?", "options": ["int()", "str()", "float()", "convert()"], "answer": "int()"},
    {"question": "What is a correct syntax to create a class?", "options": ["class MyClass:", "class MyClass", "def MyClass:", "MyClass class:"], "answer": "class MyClass:"},
    {"question": "Which method is used to add an element to a list?", "options": ["add()", "insert()", "push()", "append()"], "answer": "append()"}
]

def main():
    st.title("🎓 Personal Python Quiz")
    st.markdown("#### Advanced Python MCQ Quiz (20 Questions, 20 Minutes)")

    # Ask for user name input if quiz not started
    if not st.session_state.quiz_started:
        # Capture user name input
        st.session_state.user_name = st.text_input("👤 Enter your name:")

        if st.session_state.user_name.strip() == "":
            st.warning("Please enter your name to start the quiz!")
            return

        if st.button("🚀 Start Quiz"):
            st.session_state.quiz_started = True
            st.session_state.start_time = time.time()

    elif st.session_state.quiz_started and not st.session_state.quiz_done:
        elapsed_time = int(time.time() - st.session_state.start_time)
        remaining_time = max(0, 1200 - elapsed_time)  # 20 minutes = 1200 seconds
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        st.info(f"⏱️ Time Left: {minutes:02d}:{seconds:02d}")

        if remaining_time <= 0:
            st.session_state.quiz_done = True

        if st.session_state.current_q < len(questions):
            q = questions[st.session_state.current_q]
            st.subheader(f"Q{st.session_state.current_q + 1}: {q['question']}")

            # Display previously selected answer (if exists)
            selected_answer = st.session_state.user_answers.get(st.session_state.current_q, None)
            answer = st.radio(
                "Select an option:", 
                q["options"], 
                index=None if selected_answer is None else q["options"].index(selected_answer), 
                key=f"q{st.session_state.current_q}"
            )

            if answer is not None:
                if st.button("Next"):
                    # Save user answer only when the user selects an answer
                    st.session_state.user_answers[st.session_state.current_q] = answer
                    if answer == q["answer"]:
                        st.session_state.score += 1
                    st.session_state.current_q += 1
                    if st.session_state.current_q >= len(questions):
                        st.session_state.quiz_done = True
            else:
                st.warning("Please select an answer to continue!")

        else:
            st.session_state.quiz_done = True

    if st.session_state.quiz_done:
        st.success("✅ Quiz Completed!")
        st.subheader("📊 Results")
        st.write(f"**Name:** {st.session_state.user_name}")
        st.write(f"**Score:** {st.session_state.score} / {len(questions)}")

        elapsed_time = int(time.time() - st.session_state.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        st.write(f"**Time Taken:** {minutes:02d}:{seconds:02d}")

        st.markdown("### ❌ Review Answers")
        for i, q in enumerate(questions):
            user_ans = st.session_state.user_answers.get(i, "Not answered")
            correct = q["answer"]
            if user_ans == correct:
                st.success(f"Q{i+1}: {q['question']} \n✅ Your answer: {user_ans}")
            else:
                st.error(f"Q{i+1}: {q['question']} \n❌ Your answer: {user_ans} \n✅ Correct answer: {correct}")

        st.markdown("---")
        st.subheader("🎉 Certificate of Completion")
        
        # Display the certificate information with the user's name
        st.markdown(f"""
        <div style='border:2px solid #ccc; padding:20px; border-radius:10px; text-align:center;'>
            <h2>Certificate of Completion</h2>
            <p>This is to certify that</p>
            <h3>{st.session_state.user_name}</h3>
            <p>has successfully completed the</p>
            <b>Advanced Python Quiz</b>
            <p>with a score of <b>{st.session_state.score} / {len(questions)}</b> in <b>{minutes:02d}:{seconds:02d}</b>.</p>
            <p><i>Keep learning and growing! 🚀</i></p>
            <p><strong>All Rights Reserved 2025 - Ubaid Ur Rehman</strong></p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
# Footer at the bottom of the page (after certificate)
st.markdown("""
    <hr style='margin-top: 50px;'>
    <div style='text-align: center; color: gray; font-size: 14px;'>
        © 2025 Ubaid Ur Rehman. All Rights Reserved.
    </div>
""", unsafe_allow_html=True)