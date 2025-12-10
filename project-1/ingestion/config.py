"""
Configuration for S3 Vector Storage
"""

# S3 Bucket Names
SEMANTIC_BUCKET = 'nl2sql-semantic-memory'
PROCEDURAL_BUCKET = 'nl2sql-procedural-memory'
EPISODIC_BUCKET = 'nl2sql-episodic-memory'

# AWS Configuration
AWS_REGION = 'us-east-1'

# Data Path
DATA_PATH = './data/knowledge_base'

# Embedding Model
EMBEDDING_MODEL = 'text-embedding-3-small'

# Retrieval Settings
SEMANTIC_TOP_K = 8
PROCEDURAL_TOP_K = 3
EPISODIC_TOP_K = 5