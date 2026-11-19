from typing import Optional

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """
    Metadata describing the source document.
    """

    document_id: str = Field(
        ...,
        description="Unique identifier for the document.",
    )

    document_name: str = Field(
        ...,
        description="Human-readable document name.",
    )

    source_type: str = Field(
        ...,
        description="Origin of the document, e.g. enterprise, public_docs, demo.",
    )

    source_path: str = Field(
        ...,
        description="Path or URI of the original source document.",
    )

    document_type: str = Field(
        ...,
        description="Type of document, e.g. technical_guideline, policy, manual.",
    )

    department: Optional[str] = Field(
        default=None,
        description="Department associated with the document.",
    )

    category: Optional[str] = Field(
        default=None,
        description="High-level category of the document.",
    )

    access_level: str = Field(
        default="internal",
        description="Access classification used for authorization filtering.",
    )

    version: Optional[str] = Field(
        default=None,
        description="Document version.",
    )

    source_uri: Optional[str] = Field(
        default=None,
        description="Original external source URL if applicable.",
    )

    license: Optional[str] = Field(
        default=None,
        description="License or reuse information for externally sourced content.",
    )


class ChunkMetadata(BaseModel):
    """
    Metadata describing a chunk created from a source document.
    """

    document_id: str = Field(
        ...,
        description="Identifier of the source document.",
    )

    document_name: str = Field(
        ...,
        description="Human-readable name of the source document.",
    )

    source_type: str = Field(
        ...,
        description="Origin of the document.",
    )

    source_path: str = Field(
        ...,
        description="Path or URI of the original document.",
    )

    document_type: str = Field(
        ...,
        description="Type of source document.",
    )

    department: Optional[str] = Field(
        default=None,
        description="Department associated with the document.",
    )

    category: Optional[str] = Field(
        default=None,
        description="Document category.",
    )

    access_level: str = Field(
        default="internal",
        description="Access classification used for authorization filtering.",
    )

    version: Optional[str] = Field(
        default=None,
        description="Document version.",
    )

    source_uri: Optional[str] = Field(
        default=None,
        description="Original external source URL if applicable.",
    )

    license: Optional[str] = Field(
        default=None,
        description="License or reuse information.",
    )

    section: Optional[str] = Field(
        default=None,
        description="Section from which the chunk was extracted.",
    )

    chunk_id: str = Field(
        ...,
        description="Globally unique identifier for the chunk.",
    )

    chunk_index: int = Field(
        ...,
        ge=0,
        description="Zero-based position of the chunk within the document.",
    )

    page_number: Optional[int] = Field(
        default=None,
        ge=1,
        description="Page number for PDF-based documents.",
    )
    
    chunking_strategy: str = Field(
        default="fixed_character",
        description="Chunking strategy used to create the chunk.",
    )

    chunk_size: int = Field(
        ...,
        gt=0,
        description="Configured chunk size.",
    )

    chunk_overlap: int = Field(
        default=0,
        ge=0,
        description="Number of characters overlapping with the previous chunk.",
    )