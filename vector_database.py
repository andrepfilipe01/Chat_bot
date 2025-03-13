import chromadb
from chromadb.config import Settings
import os
from sentence_transformers import SentenceTransformer

class VectorDatabase:
    def __init__(self, collection_name="documents", persist_directory="./chroma_db"):
        os.makedirs(persist_directory, exist_ok=True)

        # Load SentenceTransformer model
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        # chromdb iniciar cliente
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Using cosine similarity
        )

    def add_documents(self, documents, metadatas=None, ids=None):
        if ids is None:
            ids = [str(i) for i in range(len(documents))]

        # Generate embeddings
        embeddings = self.embedding_model.encode(documents).tolist()

        # Add to ChromaDB
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(documents)} documents to the collection.")

    def query(self, query_text, n_results=5, min_similarity=0.5):
        query_embedding = self.embedding_model.encode([query_text]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )

        # Filter based on similarity threshold
        filtered_results = {
            "documents": [],
            "distances": []
        }
        for doc, dist in zip(results["documents"][0], results["distances"][0]):
            if dist <= min_similarity:
                filtered_results["documents"].append(doc)
                filtered_results["distances"].append(dist)

        return filtered_results


    
    def get_collection_stats(self):
        count = self.collection.count()
        return {
            "count": count
        }
    
    def get_all_ids(self):
        results = self.collection.get()
        return results['ids'] if 'ids' in results else []

    
    def clear_collection(self):
        ids = self.get_all_ids()
        if ids:
            self.collection.delete(ids=ids)
            print(f"Deleted {len(ids)} documents from the collection.")
        else:
            print("No documents found to delete.")


