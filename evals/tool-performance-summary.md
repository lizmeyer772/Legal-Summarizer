# Tool Performance Summary

This summary synthesizes the attorney rating worksheets and review worksheets across the evaluated case folders. The main pattern is clear: the tool is usually good at identifying the broad case type, parties, posture, and high-level claims, but it is less reliable at extracting the facts an attorney would actually need next. It often gives a useful first-pass orientation, but it should not yet be treated as a complete attorney workup.

## Aggregate Scores

Attorney ratings were available for 8 evaluated outputs: CivilRightsADA, Discrimination, Drugs, HumanTrafficking, Immigration, SexualHarassment, Trademark, and UnpaidEarnings.

| Category | Average Score | Takeaway |
|---|---:|---|
| Factual Accuracy | 4.25 / 5 | Strongest category. The tool usually identified the right parties, claims, posture, and broad facts. |
| Completeness | 3.25 / 5 | Mixed. The tool often missed the most attorney-relevant details, especially specific incidents, dates, product names, evidence, and claim details. |
| Legal Precision | 3.50 / 5 | Adequate but uneven. The tool generally recognized legal categories, but sometimes misstated posture, charges, statutory bases, or claim timing. |
| Attorney Usefulness | 3.00 / 5 | Useful as a first orientation, but not yet reliably useful as a litigation-planning memo. |
| Actionability | 2.88 / 5 | Weakest category. Suggested next steps were often generic, directed at the wrong side, or asked questions already answered in the complaint. |

Overall average: 3.38 / 5.

## Case-Level Takeaways

| Case | Scores | Summary |
|---|---:|---|
| CivilRightsADA | 4 / 3 / 3 / 3 / 3 | Broadly accurate, but omitted the facility name/address, specific access barriers, and some claims. Questions about remediation were partly already answered by the complaint. |
| Discrimination | 4 / 2 / 4 / 2 / 3 | Captured the VWP/MOU theory, but missed major plaintiff-specific incidents and key dates. The deadline section was poor. |
| Drugs | 4 / 3 / 3 / 2 / 2 | Correct basic charges, but too generic for criminal practice. Missed the search-warrant angle, quantity of methamphetamine, firearm details, and suppression-relevant facts. |
| HumanTrafficking | 4 / 2 / 3 / 4 / 3 | Broad context was right, but it misstated the charged offenses in the executive summary and missed core kidnapping facts and evidence. |
| Immigration | 5 / 4 / 5 / 2 / 2 | Most accurate legally and factually, but action items were too broad and not well tailored to a FOIA case. |
| SexualHarassment | 5 / 5 / 4 / 4 / 4 | Strongest output. It captured the core facts, claims, and employment timeline, with only modest corrections needed. |
| Trademark | 4 / 3 / 3 / 4 / 3 | Directionally accurate, but too generic for IP litigation. It should have named the accused products, marks, patents, and the 12 separate counts. |
| UnpaidEarnings | 4 / 4 / 3 / 3 / 3 | Accurate basic unpaid-commission summary, but it needed more focus on the commission plan, payment history, and contract details. |

Scores are listed in this order: factual accuracy, completeness, legal precision, attorney usefulness, actionability.

ClassAction and Treason have attorney review worksheets, but their generated-output markdown files still contain placeholders, so they were not included in the scored averages.

## Recurring Strengths

- The tool usually identifies the correct parties and broad procedural posture.
- It usually recognizes the main legal category: FOIA, Title VII, criminal complaint, ADA, trademark/patent, breach of contract, etc.
- It performs best on shorter, cleaner complaints with a narrow legal theory, such as Immigration and SexualHarassment.
- It can produce a helpful first-read orientation for someone unfamiliar with the case.

## Recurring Weaknesses

- The output is often too generic. It summarizes the type of case rather than the concrete facts that make the case strong or weak.
- It frequently misses high-value details: specific barriers in ADA, plaintiff incidents in Discrimination, seized evidence in Drugs, accused products in Trademark, and the kidnapping timeline in HumanTrafficking.
- It sometimes asks questions already answered in the complaint.
- The "Missing Facts" section often confuses facts missing from the complaint with facts that would naturally be developed in discovery.
- The "Attorney Next Steps" section often does not know the intended audience. Plaintiff-side, defense-side, prosecution, and criminal-defense next steps are different.
- It overuses witness interviews/depositions without accounting for litigation realities, such as represented parties, government witnesses, criminal discovery limits, and whether the attorney represents plaintiff or defendant.
- It sometimes misstates or over-compresses legal posture, such as calling a FOIA civil complaint a criminal complaint, treating diversity jurisdiction as the breach-of-contract claim, or calling background human-trafficking facts the charged offense.

## Most Important Product Takeaway

The tool is better at summarizing what the case is about than at producing attorney-ready next steps. Its factual summaries are generally reliable enough for triage, but the action plan needs stronger legal-context awareness and better audience targeting.

## Recommended Improvements

1. Add an audience selector before generating next steps: plaintiff counsel, defense counsel, prosecutor, criminal defense, neutral evaluator, or unknown.
2. Force the model to separate "facts alleged in the complaint" from "facts to verify in discovery."
3. Add a complaint-grounding check: if a question is already answered in the source document, rewrite it as a verification or discovery issue.
4. Make next steps case-type specific. For example, criminal cases should emphasize discovery, warrants, probable cause, chain of custody, bodycam, lab reports, and suppression issues. FOIA cases should emphasize search declarations, Vaughn index, production schedule, exemptions, and agency compliance.
5. Require extraction of concrete anchors: dates, locations, named people, specific products, statutes, counts, exhibits, seized evidence, requested relief, and deadlines.
6. Add a "possible inaccuracies or uncertainties" section so the tool flags when it is unsure rather than stating allegations as established facts.
7. Improve legal precision by distinguishing claims, jurisdictional statutes, remedies, and background facts.

## Bottom Line

The tool is a promising intake and triage assistant. It is consistently useful for getting a quick read on the broad nature of a complaint, but its current outputs are not yet complete or targeted enough for attorney workflow without review. The highest-impact next improvement is not better prose; it is better extraction of specific facts and better role-aware next steps.
