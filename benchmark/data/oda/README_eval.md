# ODA address evaluation holdout

Contains information licensed under the Open Government Licence - Canada.
Source: Statistics Canada, **Open Database of Addresses** (ODA).

Curated 2026-07-03 by `benchmark/curate_oda_eval.py` (seed 1042, 200 rows/province). Used only by
`benchmark/generate_address_eval.py` — not by the main benchmark
address generator.

Raw inputs (gitignored):

- `ODA_AB_v1.csv` (sha256 `3837d3de74e555011d5693aa6549a72efb8bd14d44a4147db4fa28a3e5936f48`): 891356 usable rows, 200 eval-sampled
- `ODA_ON_v1.csv` (sha256 `77b2f0d591806007bf8b5797cc7f570af5f1910f3842dcd47d5b61e761bbb809`): 2112353 usable rows, 200 eval-sampled
- `ODA_QC_v1.csv` (sha256 `9768b1b10362e2254f863e2382c70ea3f5e1d4769581b700e9824c9fff66c7e3`): 1173894 usable rows, 200 eval-sampled
