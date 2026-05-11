# AI Meeting Agent

A web app where someone uploads a meeting recording or pastes a transcript and gets back:
Meeting summary — 3 to 5 sentence overview of what was discussed
Key decisions — bullet list of decisions made in the meeting
Action items — specific tasks with the person responsible and deadline if mentioned
Follow-up email — a ready-to-send email summarising the meeting for attendees

**Live App:** [Click here to view the app](https://meeting-intelligence-fkmkrhnh6czlu5ae43ym9y.streamlit.app/)

---

## How It Works

1. User uploads an audio file or pastes a transcript
2. If audio — OpenAI Whisper API transcribes it to text
3. Transcript is sent to GPT with a structured prompt requesting JSON output
4. GPT extracts summary, decisions, action items, and drafts a follow-up email
5. Results displayed in organised sections with a download option

---

## Input Modes

**Audio Upload** — supports MP3, MP4, WAV, M4A formats. Whisper transcribes 
the audio before analysis. A 30 minute meeting transcribes in roughly 3 to 5 minutes.

**Paste Transcript** — paste any meeting transcript directly for instant analysis.

---

## Technical Stack

- **Transcription:** OpenAI Whisper API
- **Analysis:** GPT-3.5-turbo via OpenAI API
- **Structured Outputs:** JSON prompt engineering for reliable data extraction
- **Frontend:** Streamlit

---

## How to Run Locally

```bash
git clone https://github.com/RiSHLEO/meeting-intelligence
cd meeting-intelligence
pip install -r requirements.txt
```

Create a `.env` file: OPENAI_API_KEY=your-key-here

Then run:
```bash
cd app
streamlit run app.py
```

---

## What I Would Improve With More Time

- Speaker diarisation — identifying who said what in the transcript
- Calendar integration — automatically creating events for action item deadlines
- Email integration — sending the follow-up email directly from the app
- Support for very long meetings by chunking transcripts that exceed the context window
- Meeting history — searchable database of past meeting analyses