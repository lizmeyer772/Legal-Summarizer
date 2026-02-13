export default function UploadPanel({ file, onFileSelect, onAnalyze, canProcess }) {
  const handleChange = (event) => {
    const selectedFile = event.target.files?.[0] ?? null;
    onFileSelect(selectedFile);
  };

  return (
    <section className="panel">
      <h2>1. Upload Legal Document</h2>
      <p className="panel-intro">Accepted now as a local file input. TODO: wire to your backend upload endpoint.</p>

      <label className="file-input-label" htmlFor="legalDoc">
        Select file
      </label>
      <input id="legalDoc" type="file" accept=".pdf,.doc,.docx,.txt" onChange={handleChange} />

      <p className="meta-text">{file ? `Selected: ${file.name}` : 'No file selected yet.'}</p>

      <button type="button" onClick={onAnalyze} disabled={!canProcess}>
        Run Analysis
      </button>
    </section>
  );
}
