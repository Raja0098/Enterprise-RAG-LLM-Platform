from core.query import RAGQuery   

class RAGPipeline:
    def __init__(self):
        self.rag = RAGQuery()

    def ask(self, question, session_id="default"):
        return self.rag.ask(question)