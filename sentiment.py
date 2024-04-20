from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification


class Sentiment:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            "nlp04/korean_sentiment_analysis_dataset3"
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            "nlp04/korean_sentiment_analysis_dataset3"
        )

        self.classifier = pipeline(
            "text-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            device="cpu",
            top_k=None,
        )

    async def __call__(self, text: str):
        return self.classifier(text)


if __name__ == "__main__":
    sentiment = Sentiment()
    text = "이 영화는 정말 재미있었어!"
    result = sentiment(text)
    print(result)
