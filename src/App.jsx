import { useMemo, useState } from 'react';

export default function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState('');
  const [nextSteps, setNextSteps] = useState('');
  const [isSummarizing, setIsSummarizing] = useState(false);
  const [error, setError] = useState('');
  const [saveMessage, setSaveMessage] = useState('');

  const canProcess = useMemo(() => Boolean(file), [file]);
  const canSavePdf = useMemo(() => Boolean(summary || nextSteps), [summary, nextSteps]);

  const handleFileSelect = (event) => {
    const selectedFile = event.target.files?.[0] ?? null;
    setFile(selectedFile);
    setSummary('');
    setNextSteps('');
    setError('');
    setSaveMessage('');
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload a legal document before running analysis.');
      return;
    }

    setError('');
    setSaveMessage('');
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

  const handleSavePdf = async () => {
    if (!canSavePdf) {
      setError('Run an analysis before saving a PDF.');
      return;
    }

    setError('');
    setSaveMessage('');

    try {
      const pdfBytes = buildAnalysisPdf({
        fileName: file?.name ?? 'legal-document',
        summary,
        nextSteps,
        generatedAt: new Date()
      });
      const pdfName = `${baseFileName(file?.name ?? 'legal-analysis')}-analysis.pdf`;

      await savePdf(pdfBytes, pdfName);
      setSaveMessage('PDF saved.');
    } catch (err) {
      if (err?.name === 'AbortError') {
        return;
      }

      setError(err.message || 'Could not save the PDF.');
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
          <div className="panel-heading-row">
            <div>
              <h2>2. LLM Output</h2>
              <p className="panel-intro">Summary and practical follow-up guidance for attorney review.</p>
            </div>

            <button type="button" className="secondary-button" onClick={handleSavePdf} disabled={!canSavePdf || isSummarizing}>
              Save PDF
            </button>
          </div>

          {saveMessage ? <p className="save-message">{saveMessage}</p> : null}

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

function buildAnalysisPdf({ fileName, summary, nextSteps, generatedAt }) {
  const pageWidth = 612;
  const pageHeight = 792;
  const margin = 54;
  const contentWidth = pageWidth - margin * 2;
  const pages = [[]];
  let y = pageHeight - margin;

  const addPage = () => {
    pages.push([]);
    y = pageHeight - margin;
  };

  const addText = (text, options = {}) => {
    const {
      size = 10,
      bold = false,
      indent = 0,
      lineHeight = Math.max(size + 4, 14),
      gapBefore = 0,
      gapAfter = 0
    } = options;
    const cleanText = plainPdfText(text);
    const maxChars = Math.max(28, Math.floor((contentWidth - indent) / (size * 0.52)));
    const lines = wrapText(cleanText, maxChars);

    if (gapBefore) {
      y -= gapBefore;
    }

    for (const line of lines) {
      if (y - lineHeight < margin) {
        addPage();
      }

      pages[pages.length - 1].push(
        `BT /${bold ? 'F2' : 'F1'} ${size} Tf ${margin + indent} ${y} Td (${escapePdfText(line)}) Tj ET`
      );
      y -= lineHeight;
    }

    if (gapAfter) {
      y -= gapAfter;
    }
  };

  const addSpacer = (height) => {
    if (y - height < margin) {
      addPage();
      return;
    }

    y -= height;
  };

  const addOutputSection = (heading, text) => {
    addText(heading, { size: 14, bold: true, lineHeight: 18, gapBefore: 10, gapAfter: 3 });

    const sections = parseSections(text);
    if (sections.length === 0) {
      addText(text || 'No output generated.', { size: 10, lineHeight: 14 });
      return;
    }

    for (const section of sections) {
      if (section.title && section.title !== heading) {
        addText(section.title, { size: 11, bold: true, lineHeight: 15, gapBefore: 4 });
      }

      for (const paragraph of section.paragraphs) {
        addText(paragraph, { size: 10, lineHeight: 14, gapAfter: 2 });
      }

      for (const bullet of section.bullets) {
        addText(`- ${bullet}`, { size: 10, indent: 12, lineHeight: 14, gapAfter: 1 });
      }

      addSpacer(4);
    }
  };

  addText('Legal Document Analysis', { size: 18, bold: true, lineHeight: 22, gapAfter: 8 });
  addText(`Document: ${fileName}`, { size: 10, lineHeight: 14 });
  addText(`Generated: ${generatedAt.toLocaleString()}`, { size: 10, lineHeight: 14 });
  addSpacer(8);
  addOutputSection('Summary', summary);
  addOutputSection('Attorney Next Steps / Questions', nextSteps);

  return createPdfDocument(pages, pageWidth, pageHeight);
}

function createPdfDocument(pageStreams, pageWidth, pageHeight) {
  const objects = [
    '<< /Type /Catalog /Pages 2 0 R >>',
    '',
    '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
    '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>'
  ];
  const pageObjectNumbers = [];

  for (const streamLines of pageStreams) {
    const pageObjectNumber = objects.length + 1;
    const contentObjectNumber = pageObjectNumber + 1;
    const content = streamLines.join('\n');

    pageObjectNumbers.push(pageObjectNumber);
    objects.push(
      `<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${pageWidth} ${pageHeight}] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents ${contentObjectNumber} 0 R >>`
    );
    objects.push(`<< /Length ${content.length} >>\nstream\n${content}\nendstream`);
  }

  objects[1] = `<< /Type /Pages /Kids [${pageObjectNumbers.map((number) => `${number} 0 R`).join(' ')}] /Count ${pageObjectNumbers.length} >>`;

  let pdf = '%PDF-1.4\n';
  const offsets = [0];

  objects.forEach((object, index) => {
    offsets.push(pdf.length);
    pdf += `${index + 1} 0 obj\n${object}\nendobj\n`;
  });

  const xrefOffset = pdf.length;
  pdf += `xref\n0 ${objects.length + 1}\n`;
  pdf += '0000000000 65535 f \n';
  offsets.slice(1).forEach((offset) => {
    pdf += `${String(offset).padStart(10, '0')} 00000 n \n`;
  });
  pdf += `trailer\n<< /Size ${objects.length + 1} /Root 1 0 R >>\nstartxref\n${xrefOffset}\n%%EOF`;

  return new TextEncoder().encode(pdf);
}

function plainPdfText(text) {
  return String(text ?? '')
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/[“”]/g, '"')
    .replace(/[‘’]/g, "'")
    .replace(/[–—]/g, '-')
    .replace(/•/g, '-')
    .replace(/§/g, 'Section ')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^\x20-\x7E]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function escapePdfText(text) {
  return plainPdfText(text).replace(/([\\()])/g, '\\$1');
}

function wrapText(text, maxChars) {
  if (!text) {
    return [''];
  }

  const words = text.split(' ');
  const lines = [];
  let currentLine = '';

  for (const word of words) {
    if (word.length > maxChars) {
      if (currentLine) {
        lines.push(currentLine);
        currentLine = '';
      }

      for (let start = 0; start < word.length; start += maxChars) {
        lines.push(word.slice(start, start + maxChars));
      }

      continue;
    }

    const nextLine = currentLine ? `${currentLine} ${word}` : word;
    if (nextLine.length > maxChars && currentLine) {
      lines.push(currentLine);
      currentLine = word;
    } else {
      currentLine = nextLine;
    }
  }

  if (currentLine) {
    lines.push(currentLine);
  }

  return lines;
}

async function savePdf(pdfBytes, fileName) {
  const blob = new Blob([pdfBytes], { type: 'application/pdf' });

  if ('showSaveFilePicker' in window) {
    const handle = await window.showSaveFilePicker({
      suggestedName: fileName,
      types: [
        {
          description: 'PDF document',
          accept: {
            'application/pdf': ['.pdf']
          }
        }
      ]
    });
    const writable = await handle.createWritable();
    await writable.write(blob);
    await writable.close();
    return;
  }

  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function baseFileName(fileName) {
  return fileName
    .replace(/\.[^/.]+$/, '')
    .replace(/[^a-z0-9-_]+/gi, '-')
    .replace(/^-+|-+$/g, '')
    .toLowerCase() || 'legal-analysis';
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
