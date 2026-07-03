# Curated StatCan census first-name list

Adapted from Statistics Canada, **First names in Canada, 2021 Census
of Population**, Catalogue no. 98-505-X2021007, released March 19,
2025. This does not constitute an endorsement by Statistics Canada
of this product.

Curated 2026-07-03 by `benchmark/curate_statcan_names.py`
from raw file sha256 `bb487b198d863389fbd2f90f961f988391a4e4d7d66da3e2cc4de598e6eb5570` (9152 names, national level).

Cleaning: title-cased (hyphen/apostrophe aware); name and total
count only. Source publishes names UNACCENTED and excludes names
with count < 250; counts are randomly rounded to multiples of 5/10.
The benchmark generator compensates for accent-stripping with a
small accented supplement pool (see pii_generators.py).

Aggregated frequency data — contains no personal information.
This file is a committed source artifact: CI cannot regenerate it,
so it is intentionally absent from benchmark/data/checksums.json.
