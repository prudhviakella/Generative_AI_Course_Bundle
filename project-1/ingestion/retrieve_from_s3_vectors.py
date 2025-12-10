"""
S3 Vector Retrieval using AWS S3 Vectors API
Query vectors from S3 vector indexes
"""

import boto3
from typing import List, Dict, Any
import logging

from langchain_openai import OpenAIEmbeddings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3VectorRetriever:
    """Retrieve vectors from S3 vector indexes"""

    def __init__(
        self,
        semantic_bucket: str,
        procedural_bucket: str,
        episodic_bucket: str,
        aws_region: str = 'us-east-1'
    ):
        self.semantic_bucket = semantic_bucket
        self.procedural_bucket = procedural_bucket
        self.episodic_bucket = episodic_bucket

        self.s3vectors = boto3.client('s3vectors', region_name=aws_region)
        self.embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

    def search_semantic(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search semantic memory using QueryVectors API"""
        query_embedding = self.embeddings.embed_query(query)

        try:
            response = self.s3vectors.query_vectors(
                vectorBucketName=self.semantic_bucket,
                indexName='semantic_index',
                queryVector={'float32': query_embedding},
                topK=top_k,
                returnDistance=True,
                returnMetadata=True
            )

            logger.info(f"Found {len(response.get('vectors', []))} semantic results")
            return response.get('vectors', [])
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def search_procedural(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search procedural memory using QueryVectors API"""
        query_embedding = self.embeddings.embed_query(query)

        try:
            response = self.s3vectors.query_vectors(
                vectorBucketName=self.procedural_bucket,
                indexName='procedural_index',
                queryVector={'float32': query_embedding},
                topK=top_k,
                returnDistance=True,
                returnMetadata=True
            )

            logger.info(f"Found {len(response.get('vectors', []))} procedural results")
            return response.get('vectors', [])
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def search_with_filter(self, query: str, table_name: str, top_k: int = 5) -> List[Dict]:
        """Search with metadata filter"""
        query_embedding = self.embeddings.embed_query(query)

        try:
            response = self.s3vectors.query_vectors(
                vectorBucketName=self.semantic_bucket,
                indexName='semantic_index',
                queryVector={'float32': query_embedding},
                topK=top_k,
                filter={'table_name': table_name},
                returnDistance=True,
                returnMetadata=True
            )

            return response.get('vectors', [])
        except Exception as e:
            logger.error(f"Filtered search failed: {e}")
            return []

    def search_both(self, query: str, semantic_k: int = 8, procedural_k: int = 3) -> Dict:
        """Search both memory types"""
        return {
            'semantic': self.search_semantic(query, semantic_k),
            'procedural': self.search_procedural(query, procedural_k)
        }


def main():
    """Test retrieval"""

    SEMANTIC_BUCKET = 'nl2sql-semantic-memory'
    PROCEDURAL_BUCKET = 'nl2sql-procedural-memory'
    EPISODIC_BUCKET = 'nl2sql-episodic-memory'

    retriever = S3VectorRetriever(
        semantic_bucket=SEMANTIC_BUCKET,
        procedural_bucket=PROCEDURAL_BUCKET,
        episodic_bucket=EPISODIC_BUCKET
    )

    query = "customers in California"
    print(f"Query: {query}\n")

    results = retriever.search_both(query)

    print(f"Semantic results: {len(results['semantic'])}")
    for vec in results['semantic'][:3]:
        metadata = vec.get('metadata', {})
        distance = vec.get('distance', 0)
        print(f"  Key: {vec.get('key')}, Distance: {distance:.4f}")
        print(f"  Table: {metadata.get('table_name')}, Entity: {metadata.get('entity_type')}\n")

    print(f"Procedural results: {len(results['procedural'])}")
    for vec in results['procedural']:
        metadata = vec.get('metadata', {})
        distance = vec.get('distance', 0)
        print(f"  Key: {vec.get('key')}, Distance: {distance:.4f}")
        print(f"  Table: {metadata.get('table_name')}\n")


if __name__ == "__main__":
    main()