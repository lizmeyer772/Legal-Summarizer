import { useMemo, useState } from 'react';

export default function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState('');
  const [nextSteps, setNextSteps] = useState('');
  const [isSummarizing, setIsSummarizing] = useState(false);
  const [error, setError] = useState('');

  const canProcess = useMemo(() => Boolean(file), [file]);

  const handleFileSelect = (event) => {
    const selectedFile = event.target.files?.[0] ?? null;
    setFile(selectedFile);
    setSummary('');
    setNextSteps('');
    setError('');
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload a legal document before running analysis.');
      return;
    }

    setError('');
    setIsSummarizing(true);

    try {
      const llmResult = await summarizeDocument(file);
      setSummary(llmResult.summary);
      setNextSteps(llmResult.nextSteps);
    } catch (err) {
      setError(err.message || 'Something went wrong while processing the document.');
    } finally {
      setIsSummarizing(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <span className="eyebrow">Attorney Workflow Assistant</span>
        <h1>Legal Document Summarizer</h1>
        <p>Upload a document, generate an LLM summary, and review practical attorney follow-up guidance.</p>
      </header>

      <main className="app-layout">
        <section className="panel upload-panel">
          <h2>1. Upload Legal Document</h2>
          <p className="panel-intro">Upload a complaint or other legal document, then run the analysis.</p>

          <label className="file-input-label" htmlFor="legalDoc">
            Select file
          </label>
          <input id="legalDoc" type="file" accept=".pdf,.doc,.docx,.txt" onChange={handleFileSelect} />

          <p className="meta-text">{file ? `Selected: ${file.name}` : 'No file selected yet.'}</p>

          <button type="button" onClick={handleAnalyze} disabled={!canProcess}>
            Run Analysis
          </button>
        </section>

        <section className="panel output-panel">
          <h2>2. LLM Output</h2>
          <p className="panel-intro">Summary and practical follow-up guidance for attorney review.</p>

          <div className="output-grid">
            <div className="result-box">
              <h3>Summary</h3>
              {isSummarizing ? (
                <p>Generating summary...</p>
              ) : summary ? (
                <StructuredOutput text={summary} />
              ) : (
                <p className="placeholder">Placeholder: summary from LLM will be shown here.</p>
              )}
            </div>

            <div className="result-box">
              <h3>Attorney Next Steps / Questions</h3>
              {isSummarizing ? (
                <p>Generating next steps...</p>
              ) : nextSteps ? (
                <StructuredOutput text={nextSteps} />
              ) : (
                <p className="placeholder">Placeholder: next steps and follow-up questions will be shown here.</p>
              )}
            </div>
          </div>
        </section>
      </main>

      {error ? <p className="error-message">{error}</p> : null}
    </div>
  );
}

function StructuredOutput({ text }) {
  const sections = parseSections(text);

  if (sections.length === 0) {
    return <p className="llm-raw">{text}</p>;
  }

  return (
    <div className="llm-structured">
      {sections.map((section, index) => (
        <section key={`${section.title}-${index}`} className="llm-section">
          <h4>{section.title}</h4>

          {section.paragraphs.map((paragraph, paragraphIndex) => (
            <p key={`${section.title}-p-${paragraphIndex}`} className="llm-paragraph">
              {paragraph}
            </p>
          ))}

          {section.bullets.length > 0 ? (
            <ul>
              {section.bullets.map((bullet, bulletIndex) => (
                <li key={`${section.title}-b-${bulletIndex}`}>{bullet}</li>
              ))}
            </ul>
          ) : null}
        </section>
      ))}
    </div>
  );
}

function parseSections(text) {
  const lines = text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);

  const sections = [];
  let currentSection = null;

  for (const line of lines) {
    if (line.startsWith('## ')) {
      if (currentSection) {
        sections.push(currentSection);
      }

      currentSection = {
        title: line.replace(/^##\s+/, ''),
        paragraphs: [],
        bullets: []
      };
      continue;
    }

    if (!currentSection) {
      currentSection = {
        title: 'Summary',
        paragraphs: [],
        bullets: []
      };
    }

    if (/^[-*]\s+/.test(line)) {
      currentSection.bullets.push(line.replace(/^[-*]\s+/, ''));
    } else {
      currentSection.paragraphs.push(line);
    }
  }

  if (currentSection) {
    sections.push(currentSection);
  }

  return sections;
}

async function summarizeDocument(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('/api/v1/analysis/summarize', {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    throw new Error('Failed to summarize document.');
  }

  const data = await response.json();
  return {
    summary: data.summary ?? '',
    nextSteps: data.next_steps ?? ''
  };
}
