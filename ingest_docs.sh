#!/bin/bash

TARGET_DIR="data"
EXTENSIONS=("pdf" "xlsx" "pptx" "docx")
VECTOR_STORE_DIR="vectorstore"

echo "Processing directory: $TARGET_DIR"
for ext in "${EXTENSIONS[@]}"; do
    find "$TARGET_DIR" -type f -name "*.${ext}" | while read -r file; do
        base="${file%.*}"
        output="${base}.md"
        echo "Converting: $file -> $output"
        markitdown "$file" > "$output"
    done
done

python create_vectorstore.py --directory "$TARGET_DIR" --vectorstore-directory "$VECTOR_STORE_DIR"
echo "Conversion complete. Vectorstore created."
