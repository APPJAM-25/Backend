class ChatStartDto:
    def __init__(self, data) -> None:
        self.a = data.get("a", {})
        self.b = data.get("b", {})

        self.a["age"] = self.a.get("age")
        self.a["gender"] = self.a.get("gender")
        self.a["mbti"] = self.a.get("mbti")

        self.b["age"] = self.b.get("age")
        self.b["gender"] = self.b.get("gender")
        self.b["mbti"] = self.b.get("mbti")
