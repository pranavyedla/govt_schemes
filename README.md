# 🗳️ Government Welfare Schemes Chatbot

A conversational AI chatbot built with **Flask** and **Google's Gemini API** to provide quick and informative responses about Indian government welfare schemes. Users can ask questions related to various central and state schemes, and the bot intelligently fetches and formats the relevant details.

---

## 🧰 Features

- 🤖 Powered by **Google Gemini** (Generative AI)
- 📚 Covers 100+ Indian government schemes
- 📌 Short, point-based answers with scheme highlighting
- 🕵️ Conversational memory to retain context
- 🌐 Web interface using **Flask + Jinja2**
- ⚙️ Easy deployment with **Gunicorn**

---

## 🚀 Live Demo (Optional)

> _You can add a demo link here if hosted on Render, Railway, etc._

---

## 📂 Project Structure

```
├── app.ipynb                 # Main Flask application
├── requirements.txt       # Project dependencies
├── templates/
│   └── index.html         # Web UI template
├── .env                   # Environment file with API key
```

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/pranavyedla/govt_schemes.git
cd govt_schemes
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your API Key

Create a `.env` file and add your Gemini API key:

```env
api_key=your_gemini_api_key_here
```

---

## ▶️ Run the App Locally

Click on the run button on the code cell

---

## 🌐 Deploying on Production (Gunicorn)

```bash
gunicorn app:app
```

---

## 📦 Requirements

See `requirements.txt`, which includes:

- `Flask`
- `google.generativeai`
- `python-dotenv`
- `gunicorn`
- `requests`

---

## 📘 Example Query

**User Input:**

```
What is Pradhan Mantri Jan Dhan Yojana?
```

**Bot Output:**

```
1. Pradhan Mantri Jan Dhan Yojana (PMJDY) is a financial inclusion scheme.
2. It aims to provide affordable access to banking services to all households.
3. Offers benefits such as zero-balance savings account, debit card, and insurance.

Do you have any further queries?
```

---

## 💡 Future Enhancements

- Add speech-to-text and text-to-speech support
- Multilingual responses
- Integration with official government APIs

---

## 👨‍💻 Author

- **Pranav Yedla**  
  [GitHub](https://github.com/pranavyedla)
