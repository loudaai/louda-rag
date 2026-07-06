# LOUDA.md

Project rules for building Louda AI products with OpenCode, Claude Code, Cursor, or any AI coding assistant.

Use this file as the source of truth for design, architecture, behavior, and deployment. Before making changes, read this file and follow it unless the user explicitly says otherwise.

---

## 1. Product Identity

The product is **Louda AI**.

Louda AI should feel like a focused, premium, personal AI product — not a generic chatbot demo.

The main goal is to help users explore Louda's knowledge, projects, notes, and documents through a clean RAG experience.

Tone:

- Friendly
- Confident
- Minimal
- Personal
- Useful
- Not robotic

The app should feel like a mix of:

- Perplexity AI
- Linear
- Notion AI
- ChatGPT
- A clean technical zine
- A monochrome personal operating system

---

## 2. Core Assistant Behavior

The assistant is called **Louda AI**.

It represents Louda's uploaded knowledge, documents, notes, projects, and personal context.

### Answering Rules

Always answer based only on retrieved documents or approved context.

Do not hallucinate.

Do not invent facts about Louda.

When the answer exists in the documents, answer naturally:

> Based on what Louda shared, ...

> According to Louda's profile, ...

> From Louda's notes, ...

When the answer does not exist in the documents, say one of these:

> Louda hasn't shared that with me yet.

> I don't have that information yet because Louda hasn't taught me that.

> That's outside the knowledge Louda has provided so far.

> I can only answer based on what Louda has shared with me.

Avoid saying only:

> I don't know.

### Personality

Louda AI should sound like a thoughtful assistant built from Louda's knowledge, not like it literally is Louda.

Good:

> I'm Louda AI, built from Louda's documents, projects, and notes.

Avoid:

> I am Louda.

### Response Style

- Be concise first.
- Use clear language.
- Prefer short paragraphs.
- Use bullets only when they improve readability.
- Mention sources when possible.
- Never over-explain disclaimers.
- Do not repeat the same fallback phrase every time.

---

## 3. RAG Product Requirements

The app should support:

- PDF upload
- TXT and Markdown upload when possible
- Document ingestion
- Chunking
- Embedding generation
- ChromaDB vector storage
- Retrieval
- Groq-powered answer generation
- Source citations
- Chat history
- Clean error handling
- Friendly empty states

### Required Stack For Current MVP

- Python
- Streamlit
- Groq API
- LangChain or lightweight custom RAG code
- ChromaDB
- sentence-transformers embeddings
- GitHub
- Streamlit Community Cloud deployment

### Environment Variables

Use `.env` locally:

```env
GROQ_API_KEY=your_key_here
```

Use Streamlit Secrets in production:

```toml
GROQ_API_KEY = "your_key_here"
```

Never commit `.env`.

---

## 4. Project Structure

Prefer this structure:

```text
louda-rag/
├── app.py
├── requirements.txt
├── README.md
├── LOUDA.md
├── .env.example
├── .gitignore
├── docs/
├── chroma_db/
├── assets/
└── src/
    ├── config.py
    ├── rag.py
    ├── document_loader.py
    ├── vector_store.py
    ├── prompts.py
    ├── ui.py
    └── utils.py
```

Keep files small and understandable.

Do not create unnecessary abstractions.

Functionality must work before visual polish.

---

## 5. Development Workflow

Build in this order:

1. Make document loading work.
2. Make chunking work.
3. Make vector storage work.
4. Make retrieval work.
5. Make Groq response generation work.
6. Add source citations.
7. Add chat history.
8. Add polished UI.
9. Add deployment files.
10. Push to GitHub.

Do not polish the UI while the RAG pipeline is broken.

When debugging ingestion, always print:

- File name
- Number of raw documents/pages loaded
- Total extracted characters
- First 300 characters of extracted text
- Number of chunks created
- Whether documents were successfully added to ChromaDB

---

## 6. GitHub Rules

Repository:

```text
https://github.com/loudaai/louda-rag.git
```

Before pushing:

- Confirm `.env` is ignored.
- Confirm API keys are not committed.
- Confirm `requirements.txt` is updated.
- Confirm the app runs locally.
- Confirm README has setup steps.

Suggested commands:

```bash
git init
git remote add origin https://github.com/loudaai/louda-rag.git
git add .
git commit -m "Build Louda RAG chatbot"
git branch -M main
git push -u origin main
```

If the remote already exists, update it instead of adding a duplicate remote:

```bash
git remote set-url origin https://github.com/loudaai/louda-rag.git
```

---

## 7. Visual Direction

The visual identity should be minimal, premium, monochrome, and typography-led.

Use inspiration from Bryl Lim's minimal design language, but do not copy it directly. Adapt the ideas into Louda AI's product identity.

The design should feel:

- Quiet
- Sharp
- Editorial
- Technical
- Personal
- Premium
- Slightly futuristic

Avoid:

- Loud gradients
- Random accent colors
- Default-looking Streamlit UI
- Overcrowded cards
- Excessive shadows
- Too many animations
- Generic SaaS blue

---

## 8. Color System

Use a monochrome-first palette.

### Light Theme

```css
--background: #ffffff;
--foreground: #0a0a0a;
--surface: #fafafa;
--surface-strong: #f5f5f5;
--border: #e9e9e9;
--border-strong: #d4d4d4;
--muted: #737373;
--faint: #a3a3a3;
```

### Dark Theme

```css
--background: #0c0c0f;
--foreground: #f4f4f5;
--surface: #18181b;
--surface-strong: #1e1e22;
--border: #2a2a30;
--border-strong: #3a3a42;
--muted: #a0a0a8;
--faint: #8a8a92;
```

### Color Rules

- Use black, white, and gray as the default visual system.
- Avoid accent colors unless absolutely necessary for status states.
- Use inversion for emphasis: black chip on white, white chip on black.
- Use hairline borders instead of heavy fills.
- Use muted text for metadata, timestamps, labels, and captions.

---

## 9. Typography

Use typography to create hierarchy.

Preferred font roles:

- Body/UI: Geist, Inter, or system-ui
- Technical labels: Geist Mono, ui-monospace, monospace
- Editorial/long-form: Source Serif 4 or Georgia when needed
- Display: pixel/mono-inspired headings only when tasteful

### Type Rules

- Base UI text: 15px
- Small text: 13px
- Micro labels: 9–11px, uppercase, monospace, wide tracking
- Headings should be clean and compact.
- Avoid huge type unless used in a hero section.
- Use lowercase titles where it feels intentional.

Examples:

```text
LOUDA AI
ASK THE KNOWLEDGE BASE
SOURCES
DOCUMENTS
STATUS
```

Micro labels should feel like technical annotations.

---

## 10. Layout

The app should be search-first, like Perplexity.

### Main Screen

- Centered hero title
- Short subtitle
- Large rounded search input
- Minimal upload area
- Recent or suggested questions
- Clean answer area below

### Chat Screen

- User query at the top
- Answer card below
- Source cards underneath
- Follow-up input sticky near the bottom
- Sidebar for documents/settings

### Spacing

- Use generous whitespace.
- Keep content width narrow enough to read comfortably.
- Prefer 42rem–56rem max width for main content.
- Use section spacing instead of heavy boxes.
- Use borders and labels to separate sections.

---

## 11. Components

### Cards

Cards should use:

- 12–16px radius
- 1px border
- subtle surface fill
- soft shadow in light mode
- border emphasis in dark mode
- clean internal spacing

### Buttons

Primary buttons:

- Dark fill in light mode
- Light fill in dark mode
- Small radius
- Compact text
- No loud color

Secondary buttons:

- Border only
- Transparent background
- Monospace label when appropriate

### Inputs

Search input should feel premium:

- Large rounded container
- Minimal border
- Soft background
- Clear placeholder
- No default Streamlit visual clutter when possible

### Source Cards

Each source card should show:

- File name
- Page number if available
- Short quote or chunk preview
- Optional relevance indicator

Do not overwhelm users with raw metadata.

### Empty States

Empty states should be useful and calm:

> Upload Louda's notes, PDFs, or profile to begin.

> Ask a question about Louda's work, projects, or background.

---

## 12. Texture And Detail

Use subtle monochrome texture sparingly.

Allowed details:

- Halftone dot background accent
- Hairline dividers
- Tiny uppercase labels
- Soft card shadows
- Slight page entrance animation
- Small arrow glyphs
- Minimal status dots

Do not use texture everywhere.

One tasteful accent per screen is enough.

---

## 13. Motion

Motion should be subtle.

Use:

- 150–250ms hover transitions
- Gentle fade-in
- Slight lift on cards
- Smooth loading indicator
- Reduced motion support when possible

Avoid:

- Bouncy animations
- Excessive transitions
- Distracting loaders
- Constant movement

---

## 14. Accessibility

Always preserve:

- Good contrast
- Keyboard navigation
- Readable text sizes
- Clear focus states
- Semantic labels
- Useful error messages
- Mobile responsiveness

Minimal design must still be usable.

---

## 15. Streamlit-Specific Rules

Streamlit can look premium if styled carefully.

Use custom CSS to reduce the default app look.

Allowed:

- `st.markdown(..., unsafe_allow_html=True)` for controlled CSS and layout polish
- `st.chat_input`
- `st.chat_message`
- `st.file_uploader`
- `st.session_state`
- Custom card HTML for source cards

Avoid:

- Broken avatar values in `st.chat_message`
- Raw debug output in production UI
- Too many default Streamlit widgets on the main screen
- Exposed API keys

### Avatar Rule

Do not use:

```python
avatar="U"
avatar="L"
avatar="✦"
```

Use no avatar argument or valid emoji:

```python
with st.chat_message("user", avatar="👤"):
    ...

with st.chat_message("assistant", avatar="🤖"):
    ...
```

Safest:

```python
with st.chat_message("assistant"):
    ...
```

---

## 16. Prompt Template For Louda AI

Use a system prompt like this:

```text
You are Louda AI, a personal RAG assistant built from Louda's uploaded documents, notes, and project files.

Answer only using the provided context.
Do not invent facts.
If the answer is not available in the context, say: "Louda hasn't shared that with me yet."

When answering, sound friendly, concise, and natural.
When possible, mention that the answer is based on Louda's profile, notes, project documentation, or uploaded documents.

Context:
{context}

Question:
{question}
```

---

## 17. Error Handling

Errors should be understandable.

Bad:

```text
Traceback: ModuleNotFoundError...
```

Good:

```text
The app could not find your Groq API key. Add GROQ_API_KEY to .env locally or Streamlit Secrets in production.
```

For ingestion:

```text
This file did not produce readable text. If it is a scanned PDF, convert it to selectable text or upload a TXT/Markdown version.
```

---

## 18. Deployment Rules

For Streamlit Community Cloud:

- Entry file: `app.py`
- Add `GROQ_API_KEY` in Secrets
- Keep `requirements.txt` complete
- Do not rely on local `.env` in production
- Keep large local databases out of Git unless intentionally bundling a small demo database

Preferred `.gitignore`:

```text
.env
.venv/
__pycache__/
*.pyc
.DS_Store
chroma_db/
.streamlit/secrets.toml
```

If the app needs demo documents, include safe sample files only.

---

## 19. Quality Checklist

Before marking work done, verify:

- App starts with `streamlit run app.py`
- Ingestion works
- ChromaDB stores documents
- Retrieval returns relevant chunks
- Groq answers correctly
- Unknown answers use the Louda fallback phrase
- Sources display cleanly
- `.env` is not committed
- `requirements.txt` is updated
- UI looks polished in light and dark mode if both exist
- Mobile layout is usable
- No broken Streamlit avatars
- No hardcoded API keys
- GitHub remote is correct

---

## 20. OpenCode Instruction

When using OpenCode, start with:

```text
Read LOUDA.md first and follow it throughout this project.
Build the app function-first, then polish the UI.
Do not commit secrets.
Push to https://github.com/loudaai/louda-rag.git when the app runs locally.
```

When asking for UI improvements:

```text
Read LOUDA.md and restyle the app using the Louda AI visual direction.
Make it feel like a Perplexity-inspired, monochrome, premium personal AI product.
Preserve all working RAG functionality.
```

---

## 21. Final Principle

The app should not feel like a tutorial.

It should feel like Louda's personal AI knowledge product:

- Useful
- Fast
- Polished
- Minimal
- Honest about what it knows
- Easy to share
- Easy to extend
