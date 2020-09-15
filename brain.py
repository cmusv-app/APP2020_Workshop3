from Question import Question, QuestionDocument


def not_valid():
    print("Not a valid command.")


def db_to_question_list() -> [Question]:
    questions = QuestionDocument.objects
    result = []
    for question in questions:
        result.append(Question(question.question_text, question.replies))
    return result


def process_input(choice: str):
    questions_list = db_to_question_list()
    if choice == 'p':
        question_text = input("What is your question?\n>>")
        new_question = Question(question_text, [])
        question_document = QuestionDocument(question_text=new_question.question_text, replies=new_question.replies)
        question_document.save()
        print(f"'{question_text}' has been posted.")
    elif choice == 'l':
        print(f"Listing all questions... {questions_list} found \n")
        if len(questions_list) > 0:
            for index, q in enumerate(questions_list):
                print(f"[{index + 1}] {q}")
    elif choice.split(':')[0] == 'v':
        try:
            the_question_number = int(choice.split(':')[1])
            if 0 < the_question_number <= len(questions_list):
                the_index = the_question_number - 1
                print(questions_list[the_index])
                questions_list[the_index].print_replies()
                reply = input("Enter your reply... type 'stop' to stop answering\n>>")
                if reply != 'stop':
                    questions_list[the_index].replies.append(reply)
            else:
                print("Not a valid question number.\n")
        except TypeError:
            not_valid()
        except ValueError:
            not_valid()
    elif choice == 'h':
        print("=================== AskTerminal Help ===================\n"
              "Type 'v:' followed by the question number to reply to that question."
              " E.g. v:16 would allow you to reply to Question 16.\n")
    else:
        not_valid()
