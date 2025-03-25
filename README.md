
# 📩 AI-Powered Cold Email Generator  

🚀 **Automatically generate personalized cold emails for job opportunities using AI!**  
This tool extracts job details from any **company job posting URL**, matches them with **stored portfolios in ChromaDB**, and generates a **professional cold email** using **Groq's Llama 3.1 model**.  

---

## 🎯 Features  
✅ **Dynamic Job Extraction** – Scrapes job descriptions from any job posting URL  
✅ **AI-Powered Job Parsing** – Uses LLM to extract skills, experience, and role in structured JSON  
✅ **Portfolio Matching** – Finds the best-matching portfolio stored in **ChromaDB**  
✅ **Cold Email Generation** – Creates **highly professional** and **personalized** cold emails  
✅ **Interactive Streamlit UI** – Simple interface to input job links and generate emails  
✅ **Fully Automated** – Just enter a job link and get a cold email in seconds!  

---


### **DEMO VIDEO**

https://github.com/user-attachments/assets/48134bde-ccb3-4a69-9aa7-a13aabc28152



### **ScreenShot**


![Screenshot from 2025-03-25 21-57-25](https://github.com/user-attachments/assets/349cced0-2a40-4a26-98c6-c99390798f12)




## 🛠 Tech Stack  
- **Streamlit** – Web UI  
- **Selenium** – Scrape job postings dynamically  
- **ChromaDB** – Store & match company portfolios  
- **LangChain (Groq Llama 3.1)** – AI-powered job parsing & email generation  

---

## 📌 Installation & Setup  

### **1️⃣ Clone This Repository**  
```bash
git clone https://github.com/your-username/ai-cold-email-generator.git
cd ai-cold-email-generator
```

### **2️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **3️⃣ Set Up Groq API Key**  
🔹 Replace `"your_groq_api_key"` in `cold_email_app.py` with your actual **Groq API key**.  
OR set it as an environment variable:  
```bash
export GROQ_API_KEY="your_actual_groq_api_key"  # Linux/Mac
set GROQ_API_KEY="your_actual_groq_api_key"    # Windows (Command Prompt)
```

---

## ▶️ How to Run  

```bash
streamlit run cold_email_app.py
```

📌 Open your browser and go to `http://localhost:8501`  

---





## 📸 Demo Usage  
1️⃣ **Enter any job posting URL**  
2️⃣ **Click "Generate Cold Email"**  
3️⃣ **AI will extract job details, match with portfolios & generate a cold email**  
4️⃣ **Copy & send your email to the company!**  

---

## 🚀 Future Enhancements  
🔹 **More AI Models** – Support GPT-4, Claude, etc.  
🔹 **Job Application Automation** – Apply directly via LinkedIn!  
🔹 **Better Portfolio Matching** – Improve ChromaDB matching with advanced vector embeddings  

---

## 👨‍💻 Contributors  
- **Ujjwalks9 (https://github.com/Ujjwalks9)**  

---

## 📜 License  
MIT License  
```
