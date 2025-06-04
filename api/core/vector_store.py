"""
Vector store for document embedding and retrieval
"""
import os
import json
import hashlib
import numpy as np
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import markdown


class DocumentVectorStore:
    """Simple vector store for document chunks with embeddings"""
    
    def __init__(self, storage_dir: str = "data/vectors", document_dir: str = "doc"):
        """
        Initialize the vector store
        
        Args:
            storage_dir: Directory to store vector data
            document_dir: Directory containing documents for filename-based access
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Set document directory for filename-based access
        current_dir = Path(__file__).parent.parent.parent
        self.document_dir = current_dir / document_dir
        
        self.embeddings: Dict[str, np.ndarray] = {}
        self.documents: Dict[str, Dict] = {}
        self.file_metadata: Dict[str, Dict] = {}
        
        # Load existing data
        self._load_data()
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """
        Get embedding for text using OpenAI's embedding model
        
        Args:
            text: Text to embed
            
        Returns:
            numpy array of embedding
        """
        try:
            client = OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE", "https://api.deepseek.com")
            )
            
            response = client.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            
            return np.array(response.data[0].embedding)
            
        except Exception as e:
            print(f"Error getting embedding: {e}")
            # Fallback to random embedding for development
            return np.random.rand(1536)
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split text into chunks with overlap
        
        Args:
            text: Text to chunk
            chunk_size: Maximum size of each chunk
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to end at a sentence boundary
            if end < len(text):
                # Look for sentence endings within the last 100 characters
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + chunk_size - 100:
                    end = sentence_end + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def _get_file_hash(self, file_path: str) -> str:
        """Get hash of file content for change detection"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return hashlib.md5(content.encode()).hexdigest()
        except Exception:
            return ""
    
    def _resolve_file_path(self, file_path: str = None, file_name: str = None) -> str:
        """
        Resolve file path from either file_path or file_name
        
        Args:
            file_path: Complete file path (takes priority)
            file_name: Just the filename (searches in document_dir)
            
        Returns:
            Resolved absolute file path
            
        Raises:
            ValueError: If neither file_path nor file_name provided, or file not found
        """
        if file_path:
            # Use provided file path
            resolved_path = str(Path(file_path).resolve())
            if not Path(resolved_path).exists():
                raise ValueError(f"文件不存在: {file_path}")
            return resolved_path
        
        elif file_name:
            # Search for file in document directory
            potential_path = self.document_dir / file_name
            if potential_path.exists():
                return str(potential_path.resolve())
            
            # Also search in common subdirectories
            for subdir in ['', 'docs', 'documents']:
                if subdir:
                    search_path = self.document_dir / subdir / file_name
                else:
                    search_path = potential_path
                
                if search_path.exists():
                    return str(search_path.resolve())
            
            raise ValueError(f"文件名未找到: {file_name} (在目录 {self.document_dir} 中)")
        
        else:
            raise ValueError("必须提供 file_path 或 file_name 参数")
    
    def add_document(self, file_path: str = None, file_name: str = None, force_reprocess: bool = False) -> bool:
        """
        Add a document to the vector store
        
        Args:
            file_path: Complete path to the document file (optional, for backward compatibility)
            file_name: Just the filename (optional, will search in document_dir)
            force_reprocess: Force reprocessing even if file hasn't changed
            
        Returns:
            True if document was processed, False if skipped
            
        Raises:
            ValueError: If neither file_path nor file_name provided
        """
        # Resolve the actual file path
        resolved_path = self._resolve_file_path(file_path, file_name)
        
        # Check if file has changed
        current_hash = self._get_file_hash(resolved_path)
        if not force_reprocess and resolved_path in self.file_metadata:
            if self.file_metadata[resolved_path].get('hash') == current_hash:
                print(f"File {resolved_path} unchanged, skipping...")
                return False

        try:
            # Read file content
            with open(resolved_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Convert markdown to text if needed
            if resolved_path.endswith('.md'):
                content = markdown.markdown(content)
                # Simple HTML tag removal
                import re
                content = re.sub(r'<[^>]+>', '', content)
            
            # Chunk the document
            chunks = self._chunk_text(content)
            
            # Remove old embeddings for this file
            old_chunk_ids = [cid for cid in self.documents 
                           if self.documents[cid]['file_path'] == resolved_path]
            for cid in old_chunk_ids:
                del self.documents[cid]
                if cid in self.embeddings:
                    del self.embeddings[cid]
            
            # Process each chunk
            for i, chunk in enumerate(chunks):
                chunk_id = f"{resolved_path}#{i}"
                
                # Get embedding
                embedding = self._get_embedding(chunk)
                
                # Store chunk data
                self.documents[chunk_id] = {
                    'file_path': resolved_path,
                    'chunk_index': i,
                    'content': chunk,
                    'length': len(chunk)
                }
                self.embeddings[chunk_id] = embedding
            
            # Update file metadata
            self.file_metadata[resolved_path] = {
                'hash': current_hash,
                'chunk_count': len(chunks),
                'processed_at': str(Path(resolved_path).stat().st_mtime)
            }
            
            # Save data
            self._save_data()
            
            print(f"Processed {resolved_path}: {len(chunks)} chunks")
            return True
            
        except Exception as e:
            print(f"Error processing {resolved_path}: {e}")
            return False
    
    def search(self, query: str, file_path: Optional[str] = None, file_name: Optional[str] = None, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant document chunks
        
        Args:
            query: Search query
            file_path: Optional file path to limit search scope (for backward compatibility)
            file_name: Optional file name to limit search scope (preferred)
            top_k: Number of top results to return
            
        Returns:
            List of relevant chunks with similarity scores
        """
        if not self.embeddings:
            return []
        
        # Get query embedding
        query_embedding = self._get_embedding(query)
        
        # Filter by file if specified
        target_file_path = None
        if file_name or file_path:
            try:
                target_file_path = self._resolve_file_path(file_path, file_name)
            except ValueError:
                # If file not found, return empty results
                return []
            
            candidate_ids = [cid for cid in self.documents 
                           if self.documents[cid]['file_path'] == target_file_path]
        else:
            candidate_ids = list(self.documents.keys())
        
        if not candidate_ids:
            return []
        
        # Calculate similarities
        similarities = []
        for chunk_id in candidate_ids:
            if chunk_id in self.embeddings:
                chunk_embedding = self.embeddings[chunk_id]
                similarity = cosine_similarity(
                    [query_embedding], [chunk_embedding]
                )[0][0]
                similarities.append((chunk_id, similarity))
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for chunk_id, similarity in similarities[:top_k]:
            chunk_data = self.documents[chunk_id].copy()
            chunk_data['similarity'] = float(similarity)
            chunk_data['chunk_id'] = chunk_id
            results.append(chunk_data)
        
        return results
    
    def list_files(self) -> List[Dict]:
        """
        List all files in the vector store
        
        Returns:
            List of file information
        """
        files = []
        for file_path, metadata in self.file_metadata.items():
            files.append({
                'file_path': file_path,
                'file_name': Path(file_path).name,
                'chunk_count': metadata.get('chunk_count', 0),
                'processed_at': metadata.get('processed_at', ''),
                'exists': Path(file_path).exists()
            })
        return files
    
    def remove_document(self, file_path: str) -> bool:
        """
        Remove a document from the vector store
        
        Args:
            file_path: Path to the document file to remove
            
        Returns:
            True if document was removed, False if not found
        """
        file_path = str(Path(file_path).resolve())
        
        if file_path not in self.file_metadata:
            return False
        
        try:
            # Remove all chunks for this file
            chunk_ids_to_remove = [cid for cid in self.documents 
                                 if self.documents[cid]['file_path'] == file_path]
            
            for chunk_id in chunk_ids_to_remove:
                del self.documents[chunk_id]
                if chunk_id in self.embeddings:
                    del self.embeddings[chunk_id]
            
            # Remove file metadata
            del self.file_metadata[file_path]
            
            # Save updated data
            self._save_data()
            
            print(f"Removed {file_path}: {len(chunk_ids_to_remove)} chunks deleted")
            return True
            
        except Exception as e:
            print(f"Error removing {file_path}: {e}")
            return False
    
    def get_document_stats(self) -> Dict:
        """
        Get statistics about the vector store
        
        Returns:
            Dictionary with vector store statistics
        """
        total_chunks = len(self.documents)
        total_files = len(self.file_metadata)
        
        # Calculate file size distribution
        file_stats = []
        for file_path, metadata in self.file_metadata.items():
            file_stats.append({
                'file_path': file_path,
                'chunk_count': metadata.get('chunk_count', 0),
                'exists': Path(file_path).exists()
            })
        
        return {
            'total_files': total_files,
            'total_chunks': total_chunks,
            'avg_chunks_per_file': total_chunks / total_files if total_files > 0 else 0,
            'files': file_stats,
            'storage_size_mb': self._get_storage_size()
        }
    
    def _get_storage_size(self) -> float:
        """Get total storage size in MB"""
        total_size = 0
        for file_path in [
            self.storage_dir / "embeddings.npz",
            self.storage_dir / "documents.json", 
            self.storage_dir / "file_metadata.json"
        ]:
            if file_path.exists():
                total_size += file_path.stat().st_size
        return round(total_size / (1024 * 1024), 2)
    
    def rerank_results(self, results: List[Dict], query: str) -> List[Dict]:
        """
        Rerank search results using additional scoring factors
        
        Args:
            results: Initial search results
            query: Original query
            
        Returns:
            Reranked results
        """
        # Add keyword matching score
        query_words = set(query.lower().split())
        
        for result in results:
            content_words = set(result['content'].lower().split())
            keyword_overlap = len(query_words.intersection(content_words))
            keyword_score = keyword_overlap / len(query_words) if query_words else 0
            
            # Combine semantic similarity with keyword matching
            combined_score = 0.7 * result['similarity'] + 0.3 * keyword_score
            result['combined_score'] = combined_score
            result['keyword_score'] = keyword_score
        
        # Sort by combined score
        results.sort(key=lambda x: x.get('combined_score', x['similarity']), reverse=True)
        return results
    
    def _save_data(self):
        """Save vector store data to disk"""
        try:
            # Save embeddings
            embeddings_file = self.storage_dir / "embeddings.npz"
            if self.embeddings:
                embedding_arrays = {k: v for k, v in self.embeddings.items()}
                np.savez_compressed(embeddings_file, **embedding_arrays)
            
            # Save documents metadata
            docs_file = self.storage_dir / "documents.json"
            with open(docs_file, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
            
            # Save file metadata
            metadata_file = self.storage_dir / "file_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.file_metadata, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error saving vector store data: {e}")
    
    def _load_data(self):
        """Load vector store data from disk"""
        try:
            # Load embeddings
            embeddings_file = self.storage_dir / "embeddings.npz"
            if embeddings_file.exists():
                data = np.load(embeddings_file)
                self.embeddings = {key: data[key] for key in data.files}
            
            # Load documents metadata
            docs_file = self.storage_dir / "documents.json"
            if docs_file.exists():
                with open(docs_file, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
            
            # Load file metadata
            metadata_file = self.storage_dir / "file_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    self.file_metadata = json.load(f)
                    
        except Exception as e:
            print(f"Error loading vector store data: {e}")


# Global vector store instance
vector_store = DocumentVectorStore()
