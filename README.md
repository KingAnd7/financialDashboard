# Financial Dashboard

A comprehensive personal finance tracking application that combines a robust **FastAPI** backend with an interactive **Streamlit** frontend. Manage your transactions, track assets, handle recurring payments, and visualize your financial health with interactive charts.

## 🚀 Features

*   **📊 Interactive Dashboard:**
    *   **Net Worth Trend:** Visualizes your cumulative cash flow over time.
    *   **Asset Breakdown:** Snapshot of your Cash, Debts, Investments, and Property values.
    *   **Monthly Analysis:** Income vs. Expenses breakdown with pie charts and daily trends.
*   **📝 Transaction Management:**
    *   Easily add Income and Expense entries with categories and notes.
    *   "Quick Add" interface for rapid data entry.
*   **🔄 Recurring Transactions:**
    *   Set up automated recurring income (e.g., Salary) or expenses (e.g., Rent, Subscriptions).
    *   Background scheduler automatically generates transactions on their due dates.
    *   Manage active recurring items (Edit/Delete/Pause).
*   **💰 Asset Tracking:**
    *   Log and update the value of your assets and liabilities.
    *   Calculates total Net Worth (Assets - Liabilities).
*   **📄 Data Viewer:**
    *   View raw history of all transactions and asset updates in tabular format.

## 🛠️ Tech Stack

*   **Frontend:** [Streamlit](https://streamlit.io/)
*   **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Database:** [SQLAlchemy](https://www.sqlalchemy.org/) (SQLite by default)
*   **Visualization:** [Plotly](https://plotly.com/)
*   **Data Processing:** [Pandas](https://pandas.pydata.org/)
*   **Scheduling:** [APScheduler](https://apscheduler.readthedocs.io/)

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/KingAnd7/financialDashboard.git
    cd financialDashboard
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃 Usage

This application requires running both the backend API and the frontend UI simultaneously.

### 1. Start the Backend (API)
Open a terminal and run:
```bash
uvicorn api:app --reload
```
*   The API will start at `http://localhost:8000`.
*   API Documentation (Swagger UI) is available at `http://localhost:8000/docs`.

### 2. Start the Frontend (UI)
Open a **new** terminal window (in the same directory) and run:
```bash
streamlit run main.py
```
*   The application will open in your default web browser (usually at `http://localhost:8501`).

## 📂 Project Structure

```
financialDashboard/
├── api.py              # FastAPI application & endpoints
├── main.py             # Streamlit frontend application
├── crud.py             # Database CRUD operations
├── database.py         # Database connection & session handling
├── models.py           # SQLAlchemy database models (implied)
├── schemas.py          # Pydantic models for data validation
├── requirements.txt    # Project dependencies
└── financial_data.db   # SQLite database (created after running)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
