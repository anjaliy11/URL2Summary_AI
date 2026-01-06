import validators
import streamlit as st
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader


from langchain_community.document_loaders import YoutubeLoader as YTDLPYoutubeLoader

from youtube_transcript_api import YouTubeTranscriptApi
from langchain.schema import Document

os.environ["STREAMLIT_WATCHER_IGNORE_MODULES"] = "torch"

load_dotenv() 
groq_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader("Summarize URL")

# Sidebar: Groq Key
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

# URL input
generic_url = st.text_input("URL", label_visibility="collapsed")


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=groq_api_key
)

# Prompt
prompt_template = """
Provide a summary of the following content in 300 words:
Content: {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])


# Normalize YouTube link
def clean_youtube_url(url):
    if "&" in url:
        return url.split("&")[0]  # removes playlist/time params
    return url

def try_langchain_loader(url):
    """Try normal YoutubeLoader"""
    try:
        loader = YoutubeLoader.from_youtube_url(
            url,
            add_video_info=True,
            language=["en", "hi"]
        )
        return loader.load()
    except:
        return None

def try_ytdlp_loader(url):
    """Try yt-dlp based loader"""
    try:
        loader = YTDLPYoutubeLoader.from_youtube_url(
            url,
            add_video_info=False
        )
        return loader.load()
    except:
        return None

def try_transcript_api(url):
    """Try YouTubeTranscriptApi directly"""
    try:
        video_id = url.split("v=")[-1].split("&")[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "hi"])
        text = " ".join([x["text"] for x in transcript])
        return [Document(page_content=text)]
    except:
        return None


def safe_youtube_loader(url):


    docs = try_langchain_loader(url)
    if docs:
        return docs

    docs = try_ytdlp_loader(url)
    if docs:
        return docs

    docs = try_transcript_api(url)
    if docs:
        return docs

    return []  # no transcript a

# Button click
if st.button("Summarize the Content from YT or Website"):
    # Validate inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")

    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It can be a YouTube link or website URL.")

    else:
        try:
            with st.spinner("Loading & Summarizing..."):

                # Load data from YouTube or website
                if "youtube.com" in generic_url:
                    yt_url = clean_youtube_url(generic_url)
                    loader = YoutubeLoader.from_youtube_url(
                        yt_url,
                        add_video_info=True,
                        language=["en", "hi"],  # fallback language

                    )
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": (
                                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/116.0.0.0 Safari/537.36"
                            )
                        }
                    )

                docs = loader.load()
                
                
                if len(docs) == 0:
                    st.error("No transcript or readable content found for this URL.")
                    st.stop()

    # Safety: Some transcripts are long → split for better summarization
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200)
                chunked_docs = text_splitter.split_documents(docs)


                # Summarization Chain
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(chunked_docs)

                st.success(output_summary)

        except Exception as e:
            st.exception(f"Exception: {e}")
