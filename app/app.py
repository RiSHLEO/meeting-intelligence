import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Meeting Intelligence", page_icon="🎙️")
st.title("🎙️ Meeting Intelligence")
st.write("Upload a meeting recording or paste a transcript to get instant analysis.")

# ============ TRANSCRIBE AUDIO ============

def transcribe_audio(audio_file) -> str:
    try:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return transcript
    except Exception as e:
        return f"Transcription error: {str(e)}"


# ============ ANALYSE TRANSCRIPT ============

def analyse_meeting(transcript: str) -> dict:
    
    prompt = f"""You are an expert meeting analyst. Analyse the following meeting transcript and extract key information.

Return your response as valid JSON only — no other text, no markdown, no code blocks. Just the raw JSON.

The JSON must follow this exact structure:
{{
    "summary": "2-3 sentence overview of the meeting",
    "key_decisions": [
        "Decision 1",
        "Decision 2"
    ],
    "action_items": [
        {{
            "task": "specific task description",
            "owner": "person responsible or Unknown if not mentioned",
            "deadline": "deadline or Not specified if not mentioned"
        }}
    ],
    "follow_up_email": "complete ready-to-send email starting with Dear team..."
}}

Meeting transcript:
{transcript}"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {
            "role": "system", 
            "content": "You are a meeting analyst. Always respond with valid JSON only."
        },
        {"role": "user", "content": prompt}
    ],
        temperature=0
    )
    
    raw = response.choices[0].message.content.strip()
    
    # Remove markdown code blocks if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    return json.loads(raw)

# ============ DISPLAY RESULTS ============

def display_results(analysis: dict):
    
    st.subheader("📋 Meeting Summary")
    st.write(analysis["summary"])
    
    st.subheader("✅ Key Decisions")
    for decision in analysis["key_decisions"]:
        st.write(f"• {decision}")
    
    st.subheader("📌 Action Items")
    if analysis["action_items"]:
        import pandas as pd
        df = pd.DataFrame(analysis["action_items"])
        df.columns = ["Task", "Owner", "Deadline"]
        st.dataframe(df, use_container_width=True)
    
    st.subheader("📧 Follow-up Email")
    st.text_area("Copy this email", analysis["follow_up_email"], height=200)
    
    # Download button
    st.download_button(
        label="Download Analysis as JSON",
        data=json.dumps(analysis, indent=2),
        file_name="meeting_analysis.json",
        mime="application/json"
    )


# ============ MAIN APP ============

def main():
    
    tab1, tab2 = st.tabs(["📁 Upload Audio", "📝 Paste Transcript"])
    
    # Tab 1 — Audio upload
    with tab1:
        st.write("Upload an MP3, MP4, WAV, or M4A recording of your meeting.")
        audio_file = st.file_uploader(
            "Choose audio file", 
            type=["mp3", "mp4", "wav", "m4a", "webm"]
        )
        
        if audio_file is not None:
            st.audio(audio_file)
            
            if st.button("Transcribe and Analyse", key="audio_btn"):
                with st.spinner("Transcribing audio..."):
                    transcript = transcribe_audio(audio_file)
                
                if "error" in transcript.lower():
                    st.error(transcript)
                else:
                    st.success("Transcription complete")
                    with st.expander("View transcript"):
                        st.write(transcript)
                    
                    with st.spinner("Analysing meeting..."):
                        try:
                            analysis = analyse_meeting(transcript)
                            display_results(analysis)
                        except Exception as e:
                            st.error(f"Analysis error: {str(e)}")
    
    # Tab 2 — Paste transcript
    with tab2:
        st.write("Paste your meeting transcript directly.")
        transcript = st.text_area(
            "Paste transcript here",
            height=300,
            placeholder="Paste your meeting transcript here..."
        )
        
        if st.button("Analyse Transcript", key="transcript_btn"):
            if not transcript.strip():
                st.warning("Please paste a transcript first.")
            else:
                with st.spinner("Analysing meeting..."):
                    try:
                        analysis = analyse_meeting(transcript)
                        display_results(analysis)
                    except Exception as e:
                        st.error(f"Analysis error: {str(e)}")

if __name__ == "__main__":
    main()