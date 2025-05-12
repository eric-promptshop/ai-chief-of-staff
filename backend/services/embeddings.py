"""
Embeddings service module for generating vector embeddings from text.
"""
import logging
import time
from typing import Any, Dict, List, Optional, Union
import openai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class EmbeddingsService:
    """Service for generating text embeddings using OpenAI."""
    
    def __init__(self):
        """Initialize the embeddings service."""
        self._client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self._model = "text-embedding-3-small"  # Default model, can be configured
        self._max_tokens = 8000  # text-embedding-3-small max tokens
        self._dimension = 1536  # Default embedding dimension
        logger.info(f"Embeddings service initialized with model: {self._model}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((openai.APIError, openai.APIConnectionError))
    )
    async def get_embeddings(
        self, 
        texts: List[str],
        model: Optional[str] = None
    ) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            model: OpenAI embedding model to use (optional)
        
        Returns:
            List of embedding vectors
        """
        try:
            # Use batch processing for efficiency
            model_name = model or self._model
            embeddings = []
            
            # Process in batches to avoid rate limits
            batch_size = 100  # Adjust based on usage
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                
                # Check for empty or whitespace-only strings
                valid_batch = [text for text in batch if text and text.strip()]
                
                if not valid_batch:
                    # Handle empty batch
                    embeddings.extend([[0.0] * self._dimension] * len(batch))
                    continue
                
                response = self._client.embeddings.create(
                    model=model_name,
                    input=valid_batch,
                    encoding_format="float"
                )
                
                # Verify response format
                if not hasattr(response, "data"):
                    raise ValueError(f"Unexpected response format: {response}")
                
                # Extract embeddings from response
                batch_embeddings = [item.embedding for item in response.data]
                
                # Re-align with original batch if there were empty strings
                aligned_embeddings = []
                valid_idx = 0
                for text in batch:
                    if text and text.strip():
                        aligned_embeddings.append(batch_embeddings[valid_idx])
                        valid_idx += 1
                    else:
                        # Use zero vector for empty strings
                        aligned_embeddings.append([0.0] * self._dimension)
                
                embeddings.extend(aligned_embeddings)
                
                # Respect rate limits
                if i + batch_size < len(texts):
                    time.sleep(0.5)
            
            logger.info(f"Generated {len(embeddings)} embeddings successfully")
            return embeddings
        
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    async def get_embedding(self, text: str, model: Optional[str] = None) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text string to embed
            model: OpenAI embedding model to use (optional)
        
        Returns:
            Embedding vector
        """
        # Handle empty or None input
        if not text or not text.strip():
            return [0.0] * self._dimension
        
        results = await self.get_embeddings([text], model)
        return results[0]
    
    async def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts.
        
        Args:
            text1: First text string
            text2: Second text string
        
        Returns:
            Cosine similarity score (0-1)
        """
        try:
            import numpy as np
            
            embeddings = await self.get_embeddings([text1, text2])
            vec1 = np.array(embeddings[0])
            vec2 = np.array(embeddings[1])
            
            # Compute cosine similarity
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            # Handle zero vectors
            if norm1 == 0 or norm2 == 0:
                return 0.0
                
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
        
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            raise
    
    async def batch_similarity(self, query: str, candidates: List[str]) -> List[float]:
        """
        Calculate similarity scores between a query and multiple candidates.
        
        Args:
            query: Query text to compare
            candidates: List of text strings to compare against
        
        Returns:
            List of similarity scores
        """
        try:
            import numpy as np
            
            # Get embeddings for query and all candidates
            all_texts = [query] + candidates
            embeddings = await self.get_embeddings(all_texts)
            
            # Separate query embedding from candidate embeddings
            query_embed = np.array(embeddings[0])
            candidate_embeds = [np.array(embed) for embed in embeddings[1:]]
            
            # Calculate similarity for each candidate
            similarities = []
            query_norm = np.linalg.norm(query_embed)
            
            for embed in candidate_embeds:
                candidate_norm = np.linalg.norm(embed)
                
                # Handle zero vectors
                if query_norm == 0 or candidate_norm == 0:
                    similarities.append(0.0)
                    continue
                
                dot_product = np.dot(query_embed, embed)
                similarity = dot_product / (query_norm * candidate_norm)
                similarities.append(float(similarity))
            
            return similarities
        
        except Exception as e:
            logger.error(f"Error calculating batch similarity: {str(e)}")
            raise

# Create a singleton instance
embeddings_service = EmbeddingsService() 