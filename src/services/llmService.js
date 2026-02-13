export async function summarizeDocument(file) {
  // TODO: Replace this mock with a call to your backend endpoint that uses an LLM.
  // Example shape:
  // const formData = new FormData();
  // formData.append('file', file);
  // const response = await fetch('/api/summarize', { method: 'POST', body: formData });
  // return response.json();

  await sleep(900);

  return {
    summary: `Mock summary for "${file.name}": This legal document appears to establish key obligations, deadlines, and risk areas that need review.`,
    nextSteps:
      'Mock next steps: confirm filing deadlines, validate jurisdiction requirements, and prepare clarifying questions for the client before attorney review.'
  };
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
