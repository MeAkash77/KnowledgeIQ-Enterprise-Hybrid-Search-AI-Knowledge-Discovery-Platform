#!/usr/bin/env python3
"""
Script to ingest sample documents for demonstration.
Processes all sample documents and makes them available for search.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.core.logger import app_logger
from backend.ingestion.loader import DocumentLoader
from backend.ingestion.chunker import DocumentChunker
from backend.embedding.index_manager import IndexManager


def ingest_sample_documents():
    """Ingest all sample documents from the samples directory."""
    try:
        app_logger.info("Starting sample document ingestion")

        # Correct path:
        # project_root/data/samples
        samples_dir = PROJECT_ROOT / "data" / "samples"

        app_logger.info(f"Looking for samples in: {samples_dir}")

        if not samples_dir.exists():
            app_logger.error(f"Samples directory not found: {samples_dir}")
            return False

        # Initialize components
        loader = DocumentLoader()
        chunker = DocumentChunker()
        index_manager = IndexManager()

        # Load all sample documents
        documents = loader.load_directory(
            str(samples_dir),
            recursive=False
        )

        if not documents:
            app_logger.warning("No sample documents found")
            return False

        app_logger.info(f"Found {len(documents)} sample documents")

        total_chunks = 0
        processed_docs = 0

        for doc in documents:
            try:
                chunks = chunker.chunk_document(doc)

                if not chunks:
                    app_logger.warning(
                        f"No chunks created for: "
                        f"{doc['metadata']['filename']}"
                    )
                    continue

                success = index_manager.add_documents(chunks)

                if success:
                    total_chunks += len(chunks)
                    processed_docs += 1

                    app_logger.info(
                        f"Processed: "
                        f"{doc['metadata']['filename']} "
                        f"-> {len(chunks)} chunks"
                    )
                else:
                    app_logger.error(
                        f"Failed to index: "
                        f"{doc['metadata']['filename']}"
                    )

            except Exception as e:
                app_logger.error(
                    f"Error processing "
                    f"{doc['metadata']['filename']}: {e}"
                )

        app_logger.info(
            f"Sample ingestion completed: "
            f"{processed_docs}/{len(documents)} documents, "
            f"{total_chunks} total chunks"
        )

        try:
            stats = index_manager.get_collection_stats()
            app_logger.info(f"Collection stats: {stats}")
        except Exception as e:
            app_logger.warning(
                f"Could not fetch collection stats: {e}"
            )

        return processed_docs > 0

    except Exception as e:
        app_logger.error(f"Sample ingestion failed: {e}")
        return False


def main():
    print("🔍 AI Knowledge Search Platform - Sample Document Ingestion")
    print("=" * 60)

    success = ingest_sample_documents()

    if success:
        print("\n✅ Sample documents ingested successfully!")
        print("📚 You can now search through the sample documents")
        print("🚀 Start the backend and Streamlit UI")
    else:
        print("\n❌ Sample document ingestion failed")
        print("🔧 Check the logs for detailed error information")
        sys.exit(1)


if __name__ == "__main__":
    main()