# 🤖 BIGPT WhatsApp Chatbot

An AI-driven WhatsApp chatbot built with **Django**, integrated with **Twilio** and **OpenAI GPT**, designed to serve as a virtual hotel receptionist for Hotel-related business. This bot handles customer greetings, hotel-related inquiries, and requests in a smart, polite, and contextual manner.

<p align="center">
  <img width="586" height="956" alt="image" src="https://github.com/user-attachments/assets/0b4d552d-a992-44b4-88af-de4e4b0e7aeb" />
</p>


includes a **CMS pages** to manage AI-related data in real time. Key features:

- 📤 Upload contextual knowledge (pdf, text, excel)
- 🏨 Manage Company Profile and service descriptions
- 📓 Define prefix/suffix for AI prompt tuning
- 🧾 Monitor and review user conversation logs
- 🧠 Customize how the bot understands and responds

The CMS empowers non-developers (e.g., admins, marketing) to modify chatbot behavior **without editing the code**.

---

## 🚀 Features

- 📱 WhatsApp integration via **Twilio API**
- 🧠 Contextual responses powered by **OpenAI GPT-4**
- 🗃️ Stores full conversation history to database
- 💬 Recognizes greetings, polite expressions, and off-topic requests
- 📚 Customizable with company profile and business logic
- 🛡️ Django-based architecture

---

## 🧰 Tech Stack

- **Backend:** Django + Django REST Framework  
- **AI:** OpenAI Chat Completions API (GPT-4)  
- **Messaging:** Twilio WhatsApp API  
- **Database:** Custom DB connection (`chatbotdb`)  

---
