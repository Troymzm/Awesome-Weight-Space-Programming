# Contributing

Suggest a missing paper, replication, dataset, or tool through an issue or pull request. Include the primary source, the best-fitting section, and one sentence about what the work adds.

1. Verify the title, date and publication status against a proceedings page, arXiv record or author page. Use the same entry for a paper, its revisions and its code. Prefer the publication record when one is available.
2. State which artifact the programmer reads or changes. Describe the role of training, fitting or behavioral feedback when it changes how an experiment should be interpreted.
3. For benchmarks and replications, record the evaluated target, budget, relevant baselines and any material limitations in the [research review](docs/research-review.md). Include code or logs where the authors provide them.
4. Edit [the catalog](data/catalog.json) and regenerate the two tables and BibTeX with `python scripts/wsp_catalog.py --write`. Check titles, DOIs and arXiv identifiers for duplicates. Add citations for arXiv records with the `arxiv_YYMM_NNNNN` key format.

The [scope](README.md#scope) describes the boundary between the direct WSP catalog and closely related foundations.

## Weekly arXiv review

GitHub Actions scans arXiv on Mondays at 09:17 Asia/Shanghai. It looks back at least 14 days and checks the current versions of the catalog's arXiv IDs separately. Publication proposals use the withdrawal status on the official page for the exact version. An unavailable status leaves that record pending and retains the previous checkpoint. The workflow stores the search window, result counts and source errors in its run summary.

Review proposals in the draft **Weekly WSP literature update** pull request. The automated descriptions classify candidates from titles and abstracts. Follow the primary links to verify both descriptions, the evaluation conditions and any claimed venue. If arXiv changes a linked revision, check that the description still applies. Revise proposals in the catalog, regenerate the files, then review and merge the pull request.

To exclude a candidate from future scans, remove its catalog row and BibTeX entry and record its bare arXiv ID and a short reason in the top-level `excluded_arxiv_ids` object in `data/catalog.json`. Regenerate the published files and include the decision in the reviewed pull request. Remove the exclusion to reconsider the paper later.

The coverage date at the top of the READMEs describes the baseline literature review. Weekly arXiv scans are tracked separately in the catalog and in Actions.
