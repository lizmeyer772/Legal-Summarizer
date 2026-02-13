import { useMemo, useState } from 'react';
import UploadPanel from './components/UploadPanel';
import SummaryPanel from './components/SummaryPanel';
import RelatedCasesPanel from './components/RelatedCasesPanel';
import { summarizeDocument } from './services/llmService';
import { findRelatedCases } from './services/courtbaseService';

export default function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState('');
  const [nextSteps, setNextSteps] = useState('');
  const [relatedCases, setRelatedCases] = useState([]);
  const [isSummarizing, setIsSummarizing] = useState(false);
  const [isLoadingCases, setIsLoadingCases] = useState(false);
  const [error, setError] = useState('');

  const canProcess = useMemo(() => Boolean(file), [file]);

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile);
    setSummary('');
    setNextSteps('');
    setRelatedCases([]);
    setError('');
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload a legal document before running analysis.');
      return;
    }

    setError('');
    setIsSummarizing(true);
    setIsLoadingCases(true);

    try {
      const llmResult = await summarizeDocument(file);
      setSummary(llmResult.summary);
      setNextSteps(llmResult.nextSteps);

      const casesResult = await findRelatedCases(file, llmResult.summary);
      setRelatedCases(casesResult);
    } catch (err) {
      setError(err.message || 'Something went wrong while processing the document.');
    } finally {
      setIsSummarizing(false);
      setIsLoadingCases(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <span className="eyebrow">Attorney Workflow Assistant</span>
        <h1>Legal Document Summarizer</h1>
        <p>
          Upload a document, generate an LLM summary, and review related cases. This scaffold is ready for
          API integrations.
        </p>
      </header>

      <main className="grid-layout">
        <UploadPanel file={file} onFileSelect={handleFileSelect} onAnalyze={handleAnalyze} canProcess={canProcess} />

        <SummaryPanel summary={summary} nextSteps={nextSteps} loading={isSummarizing} />

        <RelatedCasesPanel cases={relatedCases} loading={isLoadingCases} />
      </main>

      {error ? <p className="error-message">{error}</p> : null}
    </div>
  );
}
