class Summary:
    def __init__(self, title, body, url, generator):
        self.title = title
        self.body = body
        self.url = url
        self.generator = generator
        self.summarized_body = self.generator.generate(self.body)
    
    def print_summarized_text(self):
        print(self.summarized_body)