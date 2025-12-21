"""Vector search functionality."""
import chromadb
from chromadb.config import Settings
import logging
from typing import List, Dict, Optional

from config import Config
from ingest.embed import get_embedding

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorSearch:
    """Vector search using Chroma."""
    
    def __init__(self, collection_name: Optional[str] = None):
        """
        Initialize vector search.
        
        Args:
            collection_name: Name of Chroma collection (defaults to Config value)
        """
        self.collection_name = collection_name or Config.CHROMA_COLLECTION_NAME
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_PERSIST_DIRECTORY,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_collection(name=self.collection_name)
    
    def search(
        self,
        query: str,
        top_k: Optional[int] = None,
        threshold: Optional[float] = None
    ) -> List[Dict]:
        """
        Search for similar FAQ entries.
        
        Args:
            query: Search query text
            top_k: Number of results to return (defaults to Config.TOP_K)
            threshold: Minimum similarity threshold (defaults to Config.SIMILARITY_THRESHOLD)
        
        Returns:
            List of search results with metadata
        """
        if top_k is None:
            top_k = Config.TOP_K
        if threshold is None:
            threshold = Config.SIMILARITY_THRESHOLD
        
        # Generate query embedding
        query_embedding = get_embedding(query)
        
        # Search in Chroma
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        formatted_results = []
        
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                # Convert distance to similarity score
                distance = results['distances'][0][i]
                similarity = 1 - distance  # Assuming cosine distance
                
                if similarity >= threshold:
                    result = {
                        'id': results['ids'][0][i],
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': distance,
                        'similarity': similarity
                    }
                    formatted_results.append(result)
        
        logger.info(f"Found {len(formatted_results)} results for query: {query[:50]}...")
        return formatted_results
    
    def get_all_documents(self) -> List[Dict]:
        """Get all documents from the collection (for debugging)."""
        results = self.collection.get()
        
        documents = []
        for i in range(len(results['ids'])):
            documents.append({
                'id': results['ids'][i],
                'text': results['documents'][i],
                'metadata': results['metadatas'][i]
            })
        
        return documents
