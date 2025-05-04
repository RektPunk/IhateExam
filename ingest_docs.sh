#!/bin/bash

TARGET_DIR="data"
EXTENSIONS=("pdf" "xlsx" "pptx" "docx")
VECTOR_STORE_DIR="vectorstore"

echo "Processing directory: $TARGET_DIR"
for ext in "${EXTENSIONS[@]}"; do
    find "$TARGET_DIR" -type f -name "*.${ext}" | while read -r file; do
        base="${file%.*}"
        output="${base}.md"
        if [ ! -f "$output" ]; then
            echo "Converting: $file -> $output"
            markitdown "$file" > "$output"
        else
            echo "Skipping: $output already exists"
        fi
    done
done

python create_vectorstore.py --directory "$TARGET_DIR" --vectorstore-directory "$VECTOR_STORE_DIR"
echo "Conversion complete. Vectorstore created."
