"""
S3 Vectors Ingestion using AWS S3 Vectors API
Ingest semantic memory chunks into S3 vector buckets and indexes
"""

import json
import boto3
from pathlib import Path
from typing import List, Dict
import logging

from langchain_openai import OpenAIEmbeddings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3VectorIngestion:
    """Ingest chunks into S3 vector buckets using AWS S3 Vectors API"""

    def __init__(
        self,
        semantic_bucket: str,
        procedural_bucket: str,
        episodic_bucket: str,
        data_path: str = './data/knowledge_base',
        aws_region: str = 'us-east-1',
        dimension: int = 1536
    ):
        self.semantic_bucket = semantic_bucket
        self.procedural_bucket = procedural_bucket
        self.episodic_bucket = episodic_bucket
        self.data_path = Path(data_path)
        self.aws_region = aws_region
        self.dimension = dimension

        # Initialize S3 Vectors client
        self.s3vectors = boto3.client('s3vectors', region_name=aws_region)

        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

        # Create buckets and indexes
        self._create_buckets()
        self._create_indexes()

    def _create_buckets(self):
        """Create S3 vector buckets if they don't exist"""
        s3 = boto3.client('s3', region_name=self.aws_region)

        for bucket in [self.semantic_bucket, self.procedural_bucket, self.episodic_bucket]:
            try:
                self.s3vectors.describe_vector_bucket(vectorBucketName=bucket)
                logger.info(f"Vector bucket exists: {bucket}")
            except:
                try:
                    self.s3vectors.create_vector_bucket(
                        vectorBucketName=bucket,
                        encryptionType='SSE-S3'
                    )
                    logger.info(f"Created vector bucket: {bucket}")
                except Exception as e:
                    logger.error(f"Failed to create vector bucket {bucket}: {e}")

    def _create_indexes(self):
        """Create vector indexes in buckets"""
        indexes = [
            (self.semantic_bucket, 'semantic_index'),
            (self.procedural_bucket, 'procedural_index'),
            (self.episodic_bucket, 'episodic_index')
        ]

        for bucket, index_name in indexes:
            try:
                self.s3vectors.describe_vector_index(
                    vectorBucketName=bucket,
                    indexName=index_name
                )
                logger.info(f"Index exists: {bucket}/{index_name}")
            except:
                try:
                    self.s3vectors.create_vector_index(
                        vectorBucketName=bucket,
                        indexName=index_name,
                        dimension=self.dimension,
                        distanceMetric='cosine'
                    )
                    logger.info(f"Created index: {bucket}/{index_name}")
                except Exception as e:
                    logger.error(f"Failed to create index {bucket}/{index_name}: {e}")

    def load_json_files(self) -> List[Path]:
        """Get all semantic JSON files"""
        return list(self.data_path.glob('semantic_*.json'))

    def parse_chunk(self, chunk: Dict, table_name: str) -> tuple:
        """Parse chunk and return text, metadata, memory type"""
        chunk_id = chunk.get('chunk_id', 'unknown')
        entity_type = chunk.get('entity_type', 'unknown')
        text = chunk.get('text', '')

        memory_type = 'procedural' if entity_type == 'query_example' else 'semantic'

        metadata = {
            'table_name': table_name,
            'entity_type': entity_type,
            'keywords': ','.join(chunk.get('keywords', []))
        }

        if 'column_name' in chunk:
            metadata['column_name'] = chunk['column_name']

        return chunk_id, text, metadata, memory_type

    def process_file(self, json_file: Path) -> tuple:
        """Process JSON file and return vectors for semantic and procedural"""
        with open(json_file, 'r') as f:
            data = json.load(f)

        table_name = data.get('table', 'unknown')
        chunks = data.get('chunks', [])

        semantic_vectors = []
        procedural_vectors = []

        for chunk in chunks:
            chunk_id, text, metadata, memory_type = self.parse_chunk(chunk, table_name)

            # Generate embedding
            embedding = self.embeddings.embed_query(text)

            vector = {
                'key': chunk_id,
                'data': {'float32': embedding},
                'metadata': metadata
            }

            if memory_type == 'semantic':
                semantic_vectors.append(vector)
            else:
                procedural_vectors.append(vector)

        logger.info(f"{table_name}: {len(semantic_vectors)} semantic, {len(procedural_vectors)} procedural")
        return semantic_vectors, procedural_vectors

    def upload_vectors(self, vectors: List[Dict], bucket: str, index_name: str):
        """Upload vectors using PutVectors API in batches"""
        if not vectors:
            return

        batch_size = 100
        total_uploaded = 0

        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]

            try:
                self.s3vectors.put_vectors(
                    vectorBucketName=bucket,
                    indexName=index_name,
                    vectors=batch
                )
                total_uploaded += len(batch)
                logger.info(f"Uploaded batch {i//batch_size + 1}: {len(batch)} vectors to {bucket}/{index_name}")
            except Exception as e:
                logger.error(f"Failed to upload batch: {e}")

        logger.info(f"Total uploaded to {bucket}/{index_name}: {total_uploaded} vectors")

    def ingest_all(self):
        """Main ingestion pipeline"""
        logger.info("Starting S3 Vectors ingestion...")

        json_files = self.load_json_files()
        logger.info(f"Found {len(json_files)} files")

        all_semantic_vectors = []
        all_procedural_vectors = []

        for json_file in json_files:
            semantic_vectors, procedural_vectors = self.process_file(json_file)
            all_semantic_vectors.extend(semantic_vectors)
            all_procedural_vectors.extend(procedural_vectors)

        # Upload to S3 vector indexes
        logger.info(f"Uploading {len(all_semantic_vectors)} semantic vectors...")
        self.upload_vectors(all_semantic_vectors, self.semantic_bucket, 'semantic_index')

        logger.info(f"Uploading {len(all_procedural_vectors)} procedural vectors...")
        self.upload_vectors(all_procedural_vectors, self.procedural_bucket, 'procedural_index')

        logger.info("Ingestion complete!")

        return {
            'semantic_count': len(all_semantic_vectors),
            'procedural_count': len(all_procedural_vectors),
            'semantic_bucket': self.semantic_bucket,
            'procedural_bucket': self.procedural_bucket
        }


def main():
    """Run ingestion"""
    
    # Configuration
    SEMANTIC_BUCKET = 'nl2sql-semantic-memory'
    PROCEDURAL_BUCKET = 'nl2sql-procedural-memory'
    EPISODIC_BUCKET = 'nl2sql-episodic-memory'
    DATA_PATH = './data/knowledge_base'
    
    ingestion = S3VectorIngestion(
        semantic_bucket=SEMANTIC_BUCKET,
        procedural_bucket=PROCEDURAL_BUCKET,
        episodic_bucket=EPISODIC_BUCKET,
        data_path=DATA_PATH
    )
    
    results = ingestion.ingest_all()
    
    print(f"\nResults:")
    print(f"  Semantic documents: {results['semantic_count']}")
    print(f"  Procedural documents: {results['procedural_count']}")
    print(f"  Semantic bucket: {results['semantic_bucket']}")
    print(f"  Procedural bucket: {results['procedural_bucket']}")


if __name__ == "__main__":
    main()
