from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
import re


def is_table_block(text: str) -> bool:
    """
    Detect if text block looks like a table
    """
    lines = text.split("\n")
    if len(lines) < 2:
        return False

    return any(len(re.split(r"\s{2,}", line)) > 2 for line in lines)


def split_tables_and_text(text: str):
    """
    Separate table blocks from normal text
    """
    blocks = text.split("\n\n")
    structured = []

    for b in blocks:
        if is_table_block(b):
            structured.append({"type": "table", "content": b})
        else:
            structured.append({"type": "text", "content": b})

    return structured


def smart_chunk(chunks, max_chars=1000, overlap=200):
    final_chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_chars,
        chunk_overlap=overlap,
        separators=[
            "\n\n",   
            "\n",
            "\t",   
            ". ",
            " "
        ]
    )

    for c in chunks:
        text = c.get("text", "")
        meta = c.get("metadata", {})

        if not text:
            continue

        page = meta.get("page")

        blocks = split_tables_and_text(text)

        for block in blocks:
            content = block["content"]
            block_type = block["type"]

            if block_type == "table":
                if len(content) > max_chars:
                    table_chunks = splitter.split_text(content)
                else:
                    table_chunks = [content]

                for t in table_chunks:
                    final_chunks.append({
                        "id": str(uuid.uuid4()),
                        "text": t,
                        "metadata": {
                                **meta,
                                "page": page,
                                "type": "table"
                    }
                })
                continue

            # 🔥 Step 3: split normal text semantically
            split_texts = splitter.split_text(content)

            for t in split_texts:
                final_chunks.append({
                    "id": str(uuid.uuid4()),
                    "text": t,
                    "metadata": {
                        **meta,
                        "page": page,
                        "type": "text"
                    }
                })

    return final_chunks