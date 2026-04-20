# Evaluation Dataset

This folder stores evaluation materials for the legal summarizer.

The purpose of this dataset is to measure output quality over time, not to power the application at runtime.

## Suggested Workflow

1. Place a source document directly into `evals/cases/<case-id>/`.
2. Run the app against the source document.
3. Save the generated output in `evals/cases/<case-id>/generated-output.md`.
4. Have the attorney fill out `evals/Attorney-Review-Worksheet.docx`.
5. Compare the generated output against the attorney's notes.

## Folder Layout

`evals/cases/`
Each case gets its own folder.

`evals/Attorney-Review-Worksheet.docx`
Single worksheet for attorney review notes.

## Do I literally put documents here?

Yes. For evaluation, you can literally place your test documents in `evals/cases/<case-id>/`.

Examples:
- `evals/cases/contract-notice-dispute/notice_agreement.pdf`
- `evals/cases/motion-to-dismiss/motion_to_dismiss.docx`
- `evals/cases/complaint-employment/complaint.txt`

If documents contain sensitive or confidential data, do one of these instead:
- use redacted copies
- use synthetic mock documents
- keep private eval files out of git with `.gitignore`

## Naming Advice

Use stable, descriptive case ids:
- `contract-notice-dispute`
- `employment-complaint-retaliation`
- `motion-to-compel-discovery`

That makes it easier to compare results over time.
