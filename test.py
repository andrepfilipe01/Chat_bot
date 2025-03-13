from vector_database import VectorDatabase

# Initialize the database
db = VectorDatabase(collection_name="test_collection")

db.clear_collection()

# Add some test documents
test_docs = [
    "The sky is blue",
    "The sky is red",
    "Grass is green",
    "the sun is yellow",
    "Clouds cover the sky",
    "The sky is purple",
    "O cão é um husky",
    "The sky is blue and the sun is yellow, but i dont know what color the grass is"
]

db.add_documents(documents=test_docs)

stats = db.get_collection_stats()
print(f"Collection contains {stats['count']} documents")


# Query
results = db.query("que raça é o cão?", n_results=3, min_similarity=0.6)

print("\nFiltered Query Results:")
for i, doc in enumerate(results['documents']):
    print(f"{i+1}. {doc} (distance: {results['distances'][i]})")