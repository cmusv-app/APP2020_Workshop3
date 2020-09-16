from mongoengine import Document, StringField, ListField, IntField


class QuestionDocument(Document):
    question_text = StringField(max_length=200, required=True)
    replies = ListField(field=StringField)
    num_replies = IntField


class Question:
    question_text: str
    replies: list

    def __init__(self, q_text, q_replies):
        self.question_text = q_text
        self.replies = q_replies

    def get_num_replies(self):
        return len(self.replies)

    def print_replies(self):
        print("============ Replies ============")
        for reply in self.replies:
            print(f"<< {reply}")

    def __str__(self):
        result = self.question_text + " -- Replies: " + str(self.get_num_replies())
        return result
