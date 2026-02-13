export default function SummaryPanel({ summary, nextSteps, loading }) {
  return (
    <section className="panel">
      <h2>2. LLM Output</h2>
      <p className="panel-intro">Summary and practical follow-up guidance for attorney review.</p>

      <div className="result-box">
        <h3>Summary</h3>
        {loading ? (
          <p>Generating summary...</p>
        ) : summary ? (
          <p>{summary}</p>
        ) : (
          <p className="placeholder">Placeholder: summary from LLM will be shown here.</p>
        )}
      </div>

      <div className="result-box">
        <h3>Attorney Next Steps / Questions</h3>
        {loading ? (
          <p>Generating next steps...</p>
        ) : nextSteps ? (
          <p>{nextSteps}</p>
        ) : (
          <p className="placeholder">Placeholder: actionable next steps and follow-up questions will be shown here.</p>
        )}
      </div>
    </section>
  );
}
