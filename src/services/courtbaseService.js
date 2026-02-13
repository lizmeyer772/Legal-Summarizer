export async function findRelatedCases(file, summaryText) {
  // TODO: Replace this mock with Courtbase API integration.
  // Example placeholder request:
  // const response = await fetch('/api/courtbase/related-cases', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ fileName: file.name, summary: summaryText })
  // });
  // return response.json();

  void file;
  void summaryText;

  await sleep(900);

  return [
    {
      id: 'case-1',
      caseName: 'Sample v. Example Corp.',
      citation: '123 F.3d 456 (9th Cir. 2018)',
      reason: 'Mock match based on contract interpretation and notice requirements.'
    },
    {
      id: 'case-2',
      caseName: 'Doe v. Placeholder LLC',
      citation: '789 U.S. 101 (2021)',
      reason: 'Mock match based on procedural posture and disputed obligations.'
    }
  ];
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
