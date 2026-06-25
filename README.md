\# AI Internship \& Student Helpdesk Assistant



A local desktop chatbot built using \*\*Python, Tkinter, JSON and scikit-learn\*\*.  

It acts as an \*\*Internship \& Student Helpdesk Assistant\*\* and answers common questions related to internship domains, certificates, project submission, fees, support, company details and services.



\---



\## Features



\- Desktop chatbot GUI with colorful chat-bubble interface

\- Topic-based FAQ sidebar with expandable sections

\- Guided internship/helpdesk support flow

\- Retrieval-based chatbot using \*\*TF-IDF + cosine similarity\*\*

\- Internship domain and certificate queries

\- Project submission, fee and support FAQs

\- Local chat history saving

\- Export chat to `.txt`

\- Safe fallback replies instead of random wrong answers



\---



\## Tech Stack



\- \*\*Python\*\*

\- \*\*Tkinter\*\*

\- \*\*scikit-learn\*\*

\- \*\*JSON\*\*



\---



\## Project Structure



```bash

CodeAlpha\_Task4\_DesktopChatbot/

│

├── chatbot\_gui.py          # Desktop UI

├── chatbot\_engine.py       # NLP / response logic

├── intents.json            # Chatbot intents, patterns and responses

├── faq\_topics.py           # Topic-wise FAQ menu data

├── chat\_history.json       # Local chat history

├── requirements.txt        # Python dependencies

├── README.md               # Project documentation

├── .gitignore              # Git ignore rules

├── LICENSE                 # MIT license

├── screenshots/           # UI screenshots for demo / README

└── exported\_chats/        # Exported chat files

```



\---



\## How It Works



This chatbot follows a \*\*retrieval-based NLP approach\*\*.



\### Workflow

1\. User enters a question in the desktop chatbot.

2\. The chatbot cleans and normalizes the text.

3\. The question is converted into TF-IDF vectors.

4\. The bot compares the question with trained patterns from `intents.json`.

5\. The most similar intent is selected using cosine similarity.

6\. If confidence is strong, the bot returns the relevant response.

7\. If confidence is weak, it avoids bluffing and gives a safer fallback response.



\---



\## Supported FAQ Areas



\### Internship

\- What domains are available for internship?

\- Will I get internship certificate?

\- How do I submit project?

\- Is there any internship fee?

\- How many tasks do I need to complete?



\### Company \& Services

\- Tell me about your company

\- What services do you offer?



\### Support

\- How can I contact support?

\- What are your working hours?

\- I have an issue



\### General

\- Hi

\- Help

\- Thank you

\- Bye



\---



\## Installation



\### 1. Clone the repository

```bash

git clone https://github.com/your-username/CodeAlpha\_Task4\_DesktopChatbot.git

cd CodeAlpha\_Task4\_DesktopChatbot

```



\### 2. Install dependencies

```bash

pip install -r requirements.txt

```



\### 3. Run the chatbot

```bash

python chatbot\_gui.py

```



\---



\## Example Questions



\- What domains are available for internship?

\- Will I get internship certificate?

\- How do I submit project?

\- Tell me about your company

\- What services do you offer?

\- How can I contact support?



\---



\## Screenshots



Add screenshots inside the `screenshots/` folder and display them here.



\### Home Screen

!\[Home](screenshots/home.png)



\### Internship FAQ Expanded

!\[FAQ](screenshots/internship\_faq.png)



\### Chat Demo

!\[Chat](screenshots/chat\_demo.png)



\---



\## Why This Project Is Good for Internship Submission



\- It is a \*\*complete working chatbot application\*\*

\- It uses \*\*AI/NLP concepts\*\* in a beginner-friendly way

\- It has a \*\*real desktop GUI\*\*, not just terminal output

\- It supports \*\*topic-based helpdesk usage\*\*

\- It is easy to explain during \*\*demo, viva and GitHub review\*\*



\---



\## Future Improvements



\- Dark mode

\- Voice input

\- More advanced NLP / synonym handling

\- Admin panel to edit FAQs

\- Database-based chat storage

\- Multi-language support



\---



\## License



This project is licensed under the \*\*MIT License\*\*.

