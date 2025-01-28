# 📄 AI-Enhanced Customer Support Ticket Resolution and Proactive Issue Prevention System

Welcome to the **AI-Enhanced Customer Support System** project! This innovative solution leverages cutting-edge AI models and tools to streamline customer support operations, proactively address recurring issues, and enhance overall customer satisfaction.

## 🚀 Project Overview

### ⚙️ Project Statement:
This project aims to develop an advanced AI-powered customer support system that:
- Leverages historical ticket data analysis to predict recurring issues and provide preemptive solutions.
- Integrates LLMs (e.g., OpenAI GPT, Meta LLaMA) for natural language processing and sentiment analysis.
- Automates responses to common issues and escalates high-priority tickets based on sentiment and urgency.
- Connects seamlessly with Google Sheets, Slack, and Email for efficient communication and data handling.

### ⚡ Outcomes:
- **🔍 Predictive Issue Detection:** Automatically identifies recurring issues and suggests solutions.
- **⌛ Real-Time Escalation:** Uses sentiment analysis to prioritize high-stress situations for faster resolution.
- **📨 Automated Issue Resolution:** Resolves common issues across multiple communication platforms.
- **⬆️ Enhanced Efficiency:** Reduces ticket volume and improves first-contact resolution rates.

## 🔧 Features and Modules

### 1. Historical Analysis and Recurrence Detection Engine
- Analyzes historical ticket data to uncover patterns and predict future issues.
- Automatically generates solutions for commonly recurring problems.

### 2. Real-Time Sentiment Analysis and Escalation System
- Continuously monitors incoming tickets for urgency and customer sentiment.
- Escalates high-priority tickets to appropriate teams based on predefined criteria.

### 3. Automated Resolution and Multichannel Integration
- Automatically resolves common customer issues.
- Integrates with Google Sheets, Slack, and Email for seamless communication and data updates.

### 4. Proactive Issue Prevention
- Provides preemptive recommendations to customers to avoid common issues.
- Enhances customer satisfaction by addressing problems before escalation.

## 🛠️ Installation

Follow these steps to set up the project locally:

### 1. **🔄 Clone the Repository:**
```bash
# Clone the repository from GitHub
git clone https://github.com/Riya-Avasthi/Infosys-Springboard-Internship.git
```

### 2. **📥 Install Dependencies:**
Ensure you have Python 3.9 or later installed.
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. **🔑 Configure API Keys:**
- Sign up for OpenAI, Meta LLaMA, and other required APIs.
- Set up environment variables for the keys:
```bash
# Example (macOS/Linux):
echo "export OPENAI_API_KEY='your_openai_api_key'" >> ~/.zshrc
source ~/.zshrc
```

### 4. **🎮 Run the Application:**
```bash
# Start the application
python app.py
```

## 📀 Project Structure
```
CustomerSupportTicket/
├── requirements.txt          # Python dependencies
├── app/                    
│   ├── appp.py  # Main application script
│   ├── models/ # pyhton files of models
│       ├── I.py   # isue escalation model
        ├── R.py    # Response automation model
        ├── S.py  # Sentiment model
├── data/                   # Sample datasets and ticket data
├── rough/
    ├── 1. Analysis/
        ├──Response Prediction Dataset/  #Response Automation Dataset Analysis
        ├──Sentiment Prediction Dataset/  # Sentiment Dataset Analysis
    ├── 2. Sentiment Analysis/        # Sentiment Analysis
    ├── 3. Real Time escalation/ #Issue Escalation model
    ├── 4. Automated Responses/ #Response Automation Model
    ├── 5. Integrations/ #Zapier Integration                
└── README.md                 # Project documentation
```

## 🛠️ Key Dependencies
- **[Gemini](https://ai.google.dev/):** For natural language understanding and generation..
- **[Pandas](https://pandas.pydata.org/):** Data manipulation and analysis.
- **[FastApi](https://fastapi.tiangolo.com/):** Framework for API handling.
- **[Zapier](https://zapier.com/app/home):** Integration with Zapier for ticket notifications.
- **[Google API](https://developers.google.com/sheets/api):** Interaction with Google Sheets.

Install all dependencies listed in `requirements.txt` using:
```bash
pip install -r requirements.txt
```

## 🔍 How It Works

1. **Historical Data Analysis:**
   - Upload historical ticket data.
   - The system analyzes data to detect recurring issues and suggests proactive solutions.

2. **Real-Time Sentiment Analysis:**
   - Incoming tickets are processed for sentiment and urgency.
   - High-priority tickets are escalated automatically.

3. **Automated Resolution:**
   - Common issues are resolved automatically based on predefined rules.
   - Updates are sent to customers via Email or Slack.

## ✨ Future Enhancements
- Integration with more communication platforms (e.g., WhatsApp, Telegram).
- Advanced analytics dashboards for real-time insights.
- Multilingual support for global customer bases.

## 🌐 Contributing
Contributions are welcome! Follow these steps to contribute:

1. **Fork the Repository**
2. **Create a New Branch:**
```bash
git checkout -b feature/YourFeature
```
3. **Commit Your Changes:**
```bash
git commit -m "Add your message here"
```
4. **Push to the Branch:**
```bash
git push origin feature/YourFeature
```
5. **Open a Pull Request**

## 📘 License
This project is licensed under the [MIT License](LICENSE).

## 📧 Contact
For any inquiries or feedback, please reach out to **Riya Avasthi** at **riyaavasthi28@gmail.com**.

---

<div align="center">
  <img src="https://img.icons8.com/color/48/000000/ai.png" alt="AI Icon" /> 
  <img src="https://img.icons8.com/color/48/000000/customer-support.png" alt="Support Icon" />
</div>
