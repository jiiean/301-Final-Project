## How to Run the Code

### 1. Google Colab Notebook (in `code/`)

All data processing, analysis, and interactive Plotly graphs live in a Colab notebook.

1. Open the notebook in Colab (e.g. click **“Open in Colab”** on `code/YourNotebook.ipynb`).
2. When prompted, upload **all four** data files to the Colab session:

   * `annual_aqi_by_county_2021.csv`
   * `tableL6.csv`
   * `adult_asthma_by_state.csv`
   * `table4_shorter.xlsx`
3. Run **Runtime → Run all**.
4. Colab will install any needed packages, preprocess the data, fit regressions, and render the interactive graphs.
5. Explore the charts inline and review the printed model summaries.

### 2. Streamlit Dashboard (in `Dashboard/`)

A standalone web‑app built with Streamlit—no notebook required.

```bash
# Clone or download your repo and cd into the Dashboard folder
git clone https://github.com/jiiean/301-Final-Project.git
cd 301-Final-Project/Dashboard

# 1. (Optional) Create & activate a virtual environment
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Run the dashboard
streamlit run app.py
```

* After a few seconds, your browser will open at **[http://localhost:8501/](http://localhost:8501/)**.
* If it doesn’t open automatically, just paste that URL into your browser.
* Interact with the charts, read the built‑in interpretations, and view the conclusions.

---

## Dependencies & Environment

All required Python packages are listed in `Dashboard/requirements.txt`:

```
streamlit
pandas
numpy
plotly
statsmodels
openpyxl
```

Your Colab notebook will install its own dependencies automatically—no extra setup needed beyond uploading the data files.

---

## Example Usage

* **Notebook**: Drag & drop your files into Colab and run all cells.
* **Dashboard**:

  * Launch with `streamlit run app.py`
  * Tweak data or code, git commit & push, and redeploy (e.g. on Streamlit Cloud).

---

Feel free to adjust paths or environment names to suit your local setup.
