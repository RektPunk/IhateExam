# IhateExam
Studying past exams shouldn't feel like a punishment.

---

## Installation

### 1. Using Poetry
If you're a fan of clean environments:

```bash
poetry install --no-root --no-dev
```

### 2. Using Conda
If you prefer the Conda ecosystem:

```bash
conda create -n IhateExam python=3.12
conda activate IhateExam
pip install -r requirements.txt
```

## How to use
### 1. `.env` Setting

Create a `.env` file in the root directory with the following content:
```
OPENAI_API_KEY="your-api-key-here"
```

### 2. Folder Structure
Before running the script, organize your study materials like this:
```md
data/
├── math101/
│   ├── week1_notes.pdf
│   ├── lecture2.pptx
│   └── summary.md
├── cs102/
│   ├── exam_review.docx
│   └── final_scores.xlsx
└── ...
```
- Each subfolder under data/ should be named after a subject (e.g., math101, cs102)
- Supported file types: .pdf, .pptx, .docx, .xlsx, .md
- This structure helps the system categorize and vectorize your documents by subject.

### 3. Ingest Your Docs
Prepare your local vectorstore:
```bash
chmod +x ingest_docs.sh
./ingest_docs.sh
```

### 4. Run the App
Once everything is set up:

```bash
streamlit run app.py
```
