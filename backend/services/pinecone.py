"""
Pinecone service module for vector database operations.
"""
import logging
import time
from typing import Any, Dict, List, Optional, Union
import numpy as np
from pinecone import Pinecone, ServerlessSpec
from config.settings import get_settings
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)
settings = get_settings()

class PineconeService:
    """Service for Pinecone vector database operations."""
    
    def __init__(self):
        """Initialize the Pinecone client."""
        self._pc = None
        self._index = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish connection to Pinecone."""
        try:
            # Create Pinecone client
            self._pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Check if index exists
            index_name = settings.PINECONE_INDEX_NAME
            all_indexes = self._pc.list_indexes()
            
            if index_name not in [idx.name for idx in all_indexes]:
                logger.info(f"Creating new Pinecone index: {index_name}")
                # Default to 1536 dimensions for OpenAI embeddings
                self._pc.create_index(
                    name=index_name,
                    dimension=1536,  # OpenAI embeddings dimension
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-west-2")
                )
                # Wait for index to be ready
                time.sleep(10)
            
            # Connect to the index
            self._index = self._pc.Index(index_name)
            logger.info(f"Connected to Pinecone index: {index_name}")
        
        except Exception as e:
            logger.error(f"Failed to connect to Pinecone: {str(e)}")
            raise
    
    @property
    def index(self):
        """Get the Pinecone index instance."""
        if not self._index:
            self._connect()
        return self._index
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def upsert_vectors(
        self, 
        vectors: List[Dict[str, Any]], 
        namespace: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Insert or update vectors in Pinecone.
        
        Args:
            vectors: List of vector records to insert/update.
                    Each record should have 'id', 'values', and 'metadata'.
            namespace: Optional namespace for the vectors.
        
        Returns:
            Response from Pinecone upsert operation.
        """
        try:
            # Process vectors in batches of 100 (recommended by Pinecone)
            batch_size = 100
            total_vectors = len(vectors)
            
            for i in range(0, total_vectors, batch_size):
                batch = vectors[i:i + batch_size]
                response = self.index.upsert(
                    vectors=batch,
                    namespace=namespace,
                    show_progress=False
                )
                logger.info(f"Upserted batch {i // batch_size + 1}/{(total_vectors // batch_size) + 1} to Pinecone")
            
            return {"status": "success", "count": total_vectors}
        
        except Exception as e:
            logger.error(f"Error upserting vectors to Pinecone: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def query_vectors(
        self, 
        query_vector: List[float], 
        top_k: int = 5, 
        namespace: Optional[str] = None,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Query vectors from Pinecone.
        
        Args:
            query_vector: The vector to query.
            top_k: Number of results to return.
            namespace: Optional namespace to query.
            filter: Optional metadata filters.
        
        Returns:
            List of matches.
        """
        try:
            # Ensure vector is normalized
            vector = self._normalize_vector(query_vector)
            
            response = self.index.query(
                vector=vector,
                top_k=top_k,
                namespace=namespace,
                filter=filter,
                include_metadata=True
            )
            
            return response["matches"]
        
        except Exception as e:
            logger.error(f"Error querying vectors from Pinecone: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def delete_vectors(
        self, 
        ids: Optional[List[str]] = None,
        filter: Optional[Dict[str, Any]] = None,
        namespace: Optional[str] = None,
        delete_all: bool = False
    ) -> Dict[str, Any]:
        """
        Delete vectors from Pinecone.
        
        Args:
            ids: List of vector IDs to delete.
            filter: Metadata filter for vectors to delete.
            namespace: Optional namespace.
            delete_all: Whether to delete all vectors in the namespace.
        
        Returns:
            Response from Pinecone delete operation.
        """
        try:
            if delete_all:
                # Delete all vectors in namespace
                self.index.delete(delete_all=True, namespace=namespace)
                return {"status": "success", "message": f"All vectors deleted from namespace {namespace or 'default'}"}
            
            elif ids:
                # Delete specific vectors by ID
                self.index.delete(ids=ids, namespace=namespace)
                return {"status": "success", "count": len(ids)}
            
            elif filter:
                # Delete vectors by filter
                self.index.delete(filter=filter, namespace=namespace)
                return {"status": "success", "message": "Vectors deleted by filter"}
            
            else:
                raise ValueError("Must provide either ids, filter, or delete_all=True")
        
        except Exception as e:
            logger.error(f"Error deleting vectors from Pinecone: {str(e)}")
            raise
    
    async def get_stats(self, namespace: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics about the index.
        
        Args:
            namespace: Optional namespace.
        
        Returns:
            Index statistics.
        """
        try:
            stats = self.index.describe_index_stats()
            if namespace:
                return {
                    "namespace": namespace,
                    "vector_count": stats.get("namespaces", {}).get(namespace, {}).get("vector_count", 0)
                }
            return stats
        except Exception as e:
            logger.error(f"Error getting Pinecone stats: {str(e)}")
            raise
    
    def _normalize_vector(self, vector: List[float]) -> List[float]:
        """
        Normalize a vector to unit length for cosine similarity.
        
        Args:
            vector: The vector to normalize.
        
        Returns:
            Normalized vector.
        """
        try:
            vector_np = np.array(vector, dtype=np.float32)
            norm = np.linalg.norm(vector_np)
            if norm > 0:
                return (vector_np / norm).tolist()
            return vector
        except Exception as e:
            logger.error(f"Error normalizing vector: {str(e)}")
            return vector

# Create a singleton instance
pinecone = PineconeService() 