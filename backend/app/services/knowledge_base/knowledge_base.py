import chromadb
from chromadb.utils import embedding_functions

class Knowledge_Base():
    def __init__(self, db_path="backend/app/knowledge_base/vector_db/"):
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    def get_collection(self, collection_name="knowledge_base"):
        collection = self.client.get_collection(collection_name)
        return collection # ChromaDB collection object.
    
    def create_collection(self, collection_name="knowledge_base"):
        collection = self.client.get_or_create_collection(
             name=collection_name, 
             embedding_function=self.embedding_func)
        return collection # ChromaDB collection object.

    def add_to_collection(self, collection, document):
        '''documnets format (List[dict]), e.g. [{"chunk":"foo","topic":"bar", "keywords": ["kw1,"kw2"]}
        '''
        if not isinstance(document, List[dict]):
                raise ValueError("Documents must be a list of dictionaries.")

        doc_chunks = [doc_chunk["chunk"] for doc_chunk in document] # document
        doc_topics = [doc_topic["topic"] for doc_topic in document] # ids
        doc_kws = [doc_kw["keywords"] for doc_kw in document] # metadata

        collection.add(
            documents=doc_chunks,
            ids=doc_topics,
            metadatas=doc_kws
        )

    def query(self, collection, query, n_results=5):
        results_raw = collection.query(query_texts=[query], n_results=n_results)
        results = [str(result) for result in results_raw["documents"][0]]
        return results
    
    #def clear_vector_db(self, clear: bool):
         # clear all docs in the current colelction when clear var is True(bool)


if __name__ == "__main__":
    # init knowledge base
    knowledge_base = Knowledge_Base()
    # create collection
    knowledge_base_collection = knowledge_base.create_collection()
    # get collection
    knowledge_base_collection = knowledge_base.get_collection()
    # query collection
    test_query = "I bought a TV last week and now it is not working. Since it is in warranty period, I would like to get it repaired or replace for a new one."
    context = knowledge_base.query(collection=knowledge_base_collection, query=test_query)
    print(context)
     
     