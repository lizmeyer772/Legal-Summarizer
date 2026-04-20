# Evaluation Dataset

This folder stores evaluation materials for the legal summarizer.

The purpose of this dataset is to measure output quality over time, not to power the application at runtime.

## Suggested Workflow

1. Place a source document into `evals/cases/<case-id>/source/`.
2. Add a rubric file in `evals/cases/<case-id>/rubric.json`.
3. Optionally save strong reference outputs in `evals/cases/<case-id>/references/`.
4. Run the app against the source document.
5. Compare the generated summary and next steps against the rubric.

## Folder Layout

`evals/cases/`
Each case gets its own folder.

`evals/templates/`
Reusable rubric templates and examples.

`evals/results/`
Optional place to save generated outputs or scored evaluations.

## Do I literally put documents here?

Yes. For evaluation, you can literally place your test documents in `evals/cases/<case-id>/source/`.

Examples:
- `evals/cases/contract-notice-dispute/source/notice_agreement.pdf`
- `evals/cases/motion-to-dismiss/source/motion_to_dismiss.docx`
- `evals/cases/complaint-employment/source/complaint.txt`

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
