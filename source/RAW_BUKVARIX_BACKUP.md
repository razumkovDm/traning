# Bukvarix source exports backup (2026-11-03)

This source package was extracted from the user-provided archive `для классификатора.zip`.

- **6 source classes**: INFORMATIONAL, COMMERCIAL, TRANSACTIONAL, NAVIGATIONAL, LOCAL, MIXED.
- **UNKNOWN is not present** in this archive.
- **9 original CSV exports**, totaling **2,440,940 rows**, approximately **196.8 MB** uncompressed.
- Original archive SHA-256: `531900570b25ea51183371435f88e1350b019e6eacba955c0ce3ef235093e8aa`.

## Where the source files are saved

The raw unpacked files and the original ZIP are backed up in the user's persistent **ChatGPT Library**:

`/pgF-traning-source-backup/2026-11-03/`

Six subdirectories contain the 9 original CSV exports. `manifest.json` lists every file's original filename, renamed path, row count, SHA-256 hash, and column structure. Long names were shortened for safe transfer; the CSV contents were **not modified**. The original ZIP is also preserved.

The original large CSV files themselves **were not committed to GitHub** because the available integration is not suitable for transferring the 196.8 MB raw dataset. This directory contains its inspectable metadata and the produced selections. If a standalone public GitHub copy is required, use a suitable bulk upload method / Git LFS separately.

## Dataset selections

- `Processed/INFORMATIONAL_900_ru.csv`: 900 original Russian informational queries.
- `Processed/COMMERCIAL_900_ru.csv`: 900 original Russian commercial queries.
- `Processing/COMMERCIAL_900_sources.csv`: original source provenance including exact frequency, source CSV record number, 21 topic categories, and future RU/UK/EN allocation (300 each).
- `Processing/COMMERCIAL_900_qa.md`: preliminary selection QA.

The allocations **do not indicate translation**; all 900 entries are currently in Russian. No query in the commercial selection was generated or translated by the assistant. **The class labels are preliminary and still benefit from independent manual review.**

Read `source/bukvarix_manifest_2026-11-03.json` for source-file details.
