from dotenv import load_dotenv
load_dotenv()
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


from loader import load_text


text = load_text()

# Split text into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=900,
    chunk_overlap=150
)

docs = splitter.create_documents([text])

# Create embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# Build FAISS index
db = FAISS.from_documents(docs, embeddings)

db.save_local("db")

print("Vector index built ✅")
