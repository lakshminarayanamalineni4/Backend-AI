from pathlib import Path

from pypdf import PdfReader

from app.ai.rag.schemas import DocumentMetadata


KNOWLEDGE_BASE_DIR = Path("app/ai/knowledge_base/demo")


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
}


def determine_source_type(file_path: Path) -> str:
    """
    Determine the high-level source type based on the document path.
    """

    relative_path = file_path.relative_to(KNOWLEDGE_BASE_DIR)

    top_level_directory = relative_path.parts[0]

    if top_level_directory == "enterprise":
        return "enterprise"

    if top_level_directory == "public_docs":
        return "public_docs"

    if top_level_directory == "demo":
        return "demo"

    return "unknown"


def determine_document_type(file_path: Path) -> str:
    """
    Determine document type based on file extension.
    """

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return "pdf"

    if extension == ".md":
        return "markdown"

    if extension == ".txt":
        return "text"

    return "unknown"


def extract_text_from_file(file_path: Path) -> list[dict]:
    """
    Extract text from a supported document.

    Returns a list of pages/sections because PDFs can contain
    multiple pages while TXT and Markdown files are treated
    as a single text unit.
    """

    extension = file_path.suffix.lower()

    if extension in {".txt", ".md"}:
        text = file_path.read_text(encoding="utf-8")

        return [
            {
                "text": text,
                "page_number": None,
            }
        ]

    if extension == ".pdf":
        reader = PdfReader(str(file_path))

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            pages.append(
                {
                    "text": text,
                    "page_number": page_number,
                }
            )

        return pages

    raise ValueError(
        f"Unsupported file type: {file_path.suffix}"
    )


def create_document_metadata(
    file_path: Path,
) -> DocumentMetadata:
    """
    Create metadata for a source document.
    """

    relative_path = file_path.relative_to(KNOWLEDGE_BASE_DIR)

    source_type = determine_source_type(file_path)

    document_type = determine_document_type(file_path)

    document_id = str(
        relative_path.with_suffix("")
    ).replace("\\", "-").replace("/", "-")

    document_name = file_path.stem.replace(
        "_",
        " ",
    ).replace(
        "-",
        " ",
    ).title()

    return DocumentMetadata(
        document_id=document_id,
        document_name=document_name,
        source_type=source_type,
        source_path=str(relative_path),
        document_type=document_type,
        access_level=(
            "public"
            if source_type == "public_docs"
            else "internal"
        ),
    )


def load_documents() -> list[dict]:
    """
    Discover and load all supported documents
    from the knowledge base.
    """

    documents = []
    for file_path in KNOWLEDGE_BASE_DIR.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        metadata = create_document_metadata(
            file_path
        )

        pages = extract_text_from_file(
            file_path
        )

        documents.append(
            {
                "metadata": metadata,
                "pages": pages,
            }
        )

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print(
        f"Total Documents: {len(documents)}"
    )

    for document in documents:

        metadata = document["metadata"]

        print("\n" + "=" * 60)

        print(
            f"Document: {metadata.document_name}"
        )

        print(
            f"Type: {metadata.document_type}"
        )

        print(
            f"Source: {metadata.source_type}"
        )

        print(
            f"Path: {metadata.source_path}"
        )

        print(
            f"Access: {metadata.access_level}"
        )

        print(
            f"Pages/Units: "
            f"{len(document['pages'])}"
        )
        
# python -m app.ai.rag.loaders.document_loader