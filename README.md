#  URL2Summary AI  
### AI-Powered YouTube & Website Content Summarizer (LangChain + Groq)

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green)
![Groq](https://img.shields.io/badge/Groq-LLM-orange)
![GenAI](https://img.shields.io/badge/Generative%20AI-Project-purple)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 📌 Project Overview

**URL2Summary AI** is a **Streamlit-based Generative AI application** that summarizes content from:
- **YouTube video URLs**
- **Website URLs**

The application uses **LangChain loaders**, **Groq LLM (LLaMA 3.1 – 8B Instant)**, and **recursive text chunking** to handle long transcripts and web pages efficiently.

---

## 🧠 How the Code Works (Actual Implementation)

### 1️⃣ User Input & Validation
```python
generic_url = st.text_input("URL")
```
- Validates URL using validators.url

- Accepts both YouTube and website URLs

- Groq API key is securely entered via Streamlit sidebar


---

### 2️⃣ LLM Initialization (Groq)
```python

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=groq_api_key
)
```

- Uses Groq’s ultra-fast inference

- LLaMA 3.1 model optimized for summarization tasks

---

 ### 3️⃣ Prompt Engineering
```python
prompt_template = """
Provide a summary of the following content in 300 words:
Content: {text}
"""

```
- Enforces controlled-length summarization

- Injected into LangChain load_summarize_chain

---

### 4️⃣ YouTube Content Loading (With Fallbacks)

The app intelligently attempts multiple loaders:

Primary: LangChain YouTubeLoader
```python
YoutubeLoader.from_youtube_url(
    url,
    add_video_info=True,
    language=["en", "hi"]
)
```
- Fallback 1: yt-dlp based loader
YTDLPYoutubeLoader.from_youtube_url(url)

- Fallback 2: YouTube Transcript API
YouTubeTranscriptApi.get_transcript(video_id)


 This ensures maximum success rate, even if transcripts are disabled.

---

### 5️⃣ Website Content Loading
```python
UnstructuredURLLoader(
    urls=[generic_url],
    ssl_verify=False,
    headers={"User-Agent": "..."}
)
```

- Extracts readable text from blogs, articles, and news websites

- Custom headers prevent request blocking

---

### 6️⃣ Long Text Handling (Critical Step)
```python
RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=200
)
```

- Prevents token overflow

- Improves summarization quality for long content

- Required for real-world YouTube transcripts

---

### 7️⃣ Summarization Chain
```python
chain = load_summarize_chain(
    llm,
    chain_type="stuff",
    prompt=prompt
)
```

- Uses LangChain’s Stuff Summarization Strategy

- All chunks passed to LLM with structured prompt

---

### 8️⃣ Streamlit Output
```python
st.success(output_summary)
```

- Displays final summary in UI

- Errors handled with st.exception()
---

##  Tech Stack (Mapped to Code)

- Component	Used In Code
- Streamlit	UI & state handling
- LangChain	Loaders, prompt, chains
- Groq LLM	Text summarization
- Recursive Splitter	Long transcript handling
- YouTube Transcript API	Transcript fallback
- dotenv	API key management

---


##  Installation & Execution
```bash
git clone https://github.com/anjaliy11/URL2Summary_AI.git
cd URL2Summary_AI
pip install -r requirements.txt
streamlit run app.py
```

---

### 🔑 Environment Variables
```bash
Create a .env file:
GROQ_API_KEY=your_groq_api_key
```
---


###  Key Engineering Highlights


- Multiple transcript fallback strategies

- Handles long-form content safely

- Clean prompt injection via LangChain

- Production-ready Streamlit UI

- Fast inference using Groq LLMs

- Supported Inputs

- Public YouTube videos

-  Blog articles & websites

-  Private / restricted videos

---



### 👩‍💻 Author
```md
Anjali Yadav
GitHub: https://github.com/anjaliy11
