export default function RelatedCasesPanel({ cases, loading }) {
  return (
    <section className="panel">
      <h2>3. Related Cases (Courtbase API)</h2>
      <p className="panel-intro">Placeholder list below. TODO: replace with live Courtbase API response mapping.</p>

      {loading ? <p>Searching for related cases...</p> : null}

      {!loading && cases.length === 0 ? (
        <p className="placeholder">No related cases yet. Results will appear here after API integration.</p>
      ) : null}

      <ul className="cases-list">
        {cases.map((caseItem) => (
          <li key={caseItem.id} className="case-item">
            <strong>{caseItem.caseName}</strong>
            <span>{caseItem.citation}</span>
            <p>{caseItem.reason}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
