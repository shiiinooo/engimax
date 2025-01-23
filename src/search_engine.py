import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
from exa_py import Exa
from datetime import datetime, timedelta

class SearchEngine:
    def __init__(self, csv_file="data/products.csv", exa_api_key=None):
        self.csv_file = csv_file
        self.df = None
        self.model = None
        self.index = None
        self.exa = Exa(exa_api_key) if exa_api_key else None
        self._initialize_engine()

    def _initialize_engine(self):
        # Load CSV Data
        self.df = pd.read_csv(self.csv_file)
        self.df['combined_text'] = self.df['name'] + " " + self.df['description']
        #print(self.df.head())
        
        # Generate Embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = self.model.encode(self.df['combined_text'].tolist(), convert_to_numpy=True)
        
        # Create FAISS Index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def search(self, query, top_k=5, use_fallback=True):
        # Search local database first
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)
        local_results = self.df.iloc[indices[0]].to_dict(orient="records")
        
        # Check if local results are relevant enough
        # Lower distance means better match (FAISS uses L2 distance)
        if local_results and min(distances[0]) < 1.5:  # Adjust this threshold as needed
            return local_results
        
        # If no relevant results found and Exa is configured, use it as fallback
        if use_fallback and self.exa:
            try:
                one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
                exa_results = self.exa.search_and_contents(
                    query,
                    use_autoprompt=True,
                    start_published_date=one_month_ago
                ).results

                external_results = []
                for result in exa_results:
                    external_results.append({
                        'name': result.title,
                        'price': 'External Result',
                        'description': result.text[:200] + "...",
                        'source': result.url,
                        'is_external': True
                    })
                return external_results
            except Exception as e:
                print(f"Exa search failed: {e}")
                return local_results
        
        return local_results
