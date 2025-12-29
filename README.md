

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone git@github.com:rochefym/20251124_Recommender_System-main.git
cd 20251124_Recommender_System-main
````

### 2. Set Up Virtual Environment

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Note:** Some packages like `faiss-gpu` or `nvidia` libraries are too large for GitHub and must be installed manually if required.

Example:

```bash
pip install faiss-gpu==<version>
```

---

### 4. Handling Large Files

Large ML files (e.g., `.faiss`) are not included in the repo. You can:

* Download them separately and place them in the correct folder:

```text
dietary_reference_intakes/index.faiss
```

---

### 5. Running the Server

If the project uses Django (based on `manage.py`):

```bash
cd recommender_system
python3 manage.py runserver 0.0.0.0:8000
```

---

### 6. Common Issues

1. **Python not found**: Use `python3` instead of `python` in all commands.
2. **Django not installed**: Make sure your virtual environment is active (`source venv/bin/activate`) and install with `pip install django`.
3. **Large files error on GitHub**: GitHub rejects files >100 MB. Keep them local or use Git LFS.

---

### 7. Recommendations

* Never commit `venv/` or system libraries. Use `requirements.txt`.
* Keep large ML models outside of GitHub, download them when needed.
* Use `.gitignore` to exclude temporary or system files:

```text
__pycache__/
*.pyc
*.pyo
*.pyd
venv/
.env
*.faiss
*.pt
*.pth
*.onnx
*.h5
dietary_reference_intakes/
logs/
.DS_Store
.vscode/
```

```

---
