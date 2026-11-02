# Multilingual build

The source rows are in Processing/selected_sources_for_3_languages.csv, derived from actual Bukvarix exports in Processed/.

GitHub Actions workflow Build multilingual search-intent dataset uses Helsinki-NLP/opus-mt-ru-en and Helsinki-NLP/opus-mt-ru-uk. The workflow generates Ready/queries_multilingual.csv, Ready/queries_provenance.csv and Ready/quality_report.json.

UNKNOWN cannot be translated semantically, so keyboard adaptation is labeled separately. Any shortfall is documented instead of filling it with invented queries.

Machine translations are drafts and need human review to qualify as gold labels.
