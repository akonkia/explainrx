# ExplainRx PGx

> *Given this pharmacogenomic result, medication, source evidence, and assay coverage — what recommendation is justified, and why?*

ExplainRx PGx is a **source-aware pharmacogenomics interpretation workbench** for clinical labs and research teams. It ingests structured PGx evidence from multiple upstream sources, stores it with full version provenance, maps gene diplotypes to traceable clinical recommendations, and presents everything through an interactive Shiny viewer with PDF reporting, patient profile management, and a growing biological knowledge graph.

It is not a raw variant caller and not a static lookup table. It is an explainable, auditable, reproducible interpretation layer on top of curated public sources.

---

## Table of contents

1. [Architecture](#architecture)
2. [Repository layout](#repository-layout)
3. [Databases](#databases)
4. [Data sources](#data-sources)
5. [Migration system](#migration-system)
6. [R ingestion pipeline](#r-ingestion-pipeline)
7. [Python evidence pipeline](#python-evidence-pipeline)
8. [Bio Knowledge Base](#bio-knowledge-base)
9. [Viewer](#viewer)
10. [ExplainRx score](#explainrx-score)
11. [Patient database](#patient-database)
12. [Quick start](#quick-start)
13. [Environment variables](#environment-variables)
14. [Docker](#docker)
15. [Design principles](#design-principles)
16. [Known gaps and roadmap](#known-gaps-and-roadmap)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Upstream sources                            │
│                                                                     │
│  CPIC v1.58.0   PharmVar 6.2.25   RxNorm 05-2026   ClinPGx/PharmGKB│
│  openFDA 2026-06-10   SIGNOR   Reactome   STRING   ChEMBL   UniProt │
│  PharmGKB pathways   PubMed/PubTator3 (literature mining)           │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
           ┌───────────────▼────────────────────────┐
           │           Ingestion layer               │
           │                                        │
           │  R/ingest/       Versioned R scripts   │
           │  (manifest-driven, provenance-tracked) │
           │                                        │
           │  scripts/pgx_pipeline/                 │
           │  (Python: collect → curate →           │
           │   aggregate → ingest)                  │
           │                                        │
           │  scripts/ingest_kb.py                  │
           │  (SIGNOR, Reactome, STRING,            │
           │   ChEMBL, UniProt, PharmGKB)           │
           │                                        │
           │  scripts/expand_kb.py                  │
           │  (PubTator3 BFS literature mining)     │
           └───────────────┬────────────────────────┘
                           │
       ┌───────────────────▼───────────────────────────────────────┐
       │                explainrx_dev  (PostgreSQL)                │
       │                                                           │
       │  provenance · biology · interpretation · clinical rules   │
       │  drug normalisation · external evidence · Bio KB          │
       └───────────────────┬───────────────────────────────────────┘
                           │
       ┌───────────────────▼───────────────────────────────────────┐
       │               Shiny viewer  (viewer/app.R)                │
       │                                                           │
       │  recommendations · gene info + Bio KB · gene-drug pairs   │
       │  alleles · rules · VCF calling · patient profiles · PDF   │
       └───────────────────┬───────────────────────────────────────┘
                           │
       ┌───────────────────▼──────────────────────┐
       │         explainrx_patients (PostgreSQL)   │
       │         per-clinic patient profiles        │
       └──────────────────────────────────────────┘
```

### Design philosophy

ExplainRx PGx is built around one constraint: **clinical output must be deterministic, sourced, and reproducible**.

- Recommendations come from structured `clinical_rule` rows, not from free-text summarisation.
- Every recommendation links back to the exact upstream source release that was used.
- New upstream releases append records and deactivate prior rules — they never delete or overwrite history.
- Multiple guidelines (CPIC, DPWG, FDA) are stored independently; ExplainRx never silently picks one.
- The viewer's two-phase loading shows the overview table immediately while full detail loads in the background, so large databases remain responsive.

---

## Repository layout

```
explainrx/
│
├── viewer/                        Shiny workbench
│   ├── app.R                      Main application (~4 500 lines)
│   ├── vcf_caller.R               VCF parsing and star-allele calling
│   ├── ddi_data.R                 DDI phenoconversion tables and logic
│   ├── report_template.Rmd        PDF report template (rmarkdown / pdflatex)
│   └── www/styles.css             Custom CSS
│
├── R/ingest/                      R ingestion scripts (manifest-driven)
│   ├── 00_ingest_utils.R          Shared DB helpers, logging, manifest I/O
│   ├── 10_register_release_manifest.R     Generic release registration
│   ├── 11_register_cpic_release.R         CPIC manifest + source rows
│   ├── 12_register_pharmvar_release.R     PharmVar manifest + source rows
│   ├── 13_register_rxnorm_release.R       RxNorm CPC manifest + source rows
│   ├── 14_register_clinpgx_snapshot.R     ClinPGx/PharmGKB manifest + rows
│   ├── 15_register_openfda_snapshot.R     openFDA manifest + source rows
│   ├── 20_load_cpic_core_from_stage.R     CPIC: genes, pairs, phenotypes, recs
│   ├── 21_load_clinpgx_clinical_variants.R  ClinPGx variant annotations
│   ├── 22_load_clinpgx_guidelines.R       ClinPGx drug label summaries
│   ├── 23_load_openfda_labels.R           openFDA: drug labels + PGx sections
│   ├── 24_load_pharmvar_alleles.R         PharmVar: allele definitions
│   ├── 25_populate_rxnorm_cuis.R          RxNorm: drug normalisation
│   └── 99_register_priority_sources.R     Run all register scripts in order
│
├── scripts/
│   ├── migrate.sh                 Numbered DB migration runner
│   ├── bootstrap_dev_db.sh        Full local dev reset from scratch
│   ├── run_viewer.sh              Launch Shiny viewer
│   ├── setup_patients_db.sh       Create + seed explainrx_patients
│   ├── rebuild_cpic_stage.sh      Restore cpic_stage from dump
│   ├── docker_ingest.sh           Docker-based full ingest
│   ├── load_cpic_core.sh          Per-source ingest launchers
│   ├── load_pharmvar.sh
│   ├── load_clinpgx.sh
│   ├── load_openfda_labels.sh
│   ├── fetch_hgnc_genes.R         Fetch HGNC gene list for normalisation
│   ├── add_viewer_indexes.sql     Performance indexes (see V002 migration)
│   ├── ingest_kb.py               Bio KB: SIGNOR, Reactome, STRING, ChEMBL,
│   │                                        UniProt, PharmGKB pathways
│   ├── expand_kb.py               Bio KB: PubTator3 literature mining (BFS)
│   └── pgx_pipeline/              Python evidence search pipeline
│       ├── collect.py             Fetch from PharmGKB, ClinVar, PubMed
│       ├── curate.py              Normalise + tag evidence records
│       ├── aggregate.py           Group by (gene, drug, variant)
│       ├── ingest.py              Upsert into external_evidence
│       ├── run_pipeline.sh        Orchestrator
│       └── README.md              Pipeline documentation
│
├── migrations/                    Viewer-layer SQL migrations (V001–V007)
│   ├── V001__baseline_schema.sql
│   ├── V002__add_viewer_indexes.sql
│   ├── V003__external_evidence.sql
│   ├── V004__add_evidence_level.sql
│   ├── V005__explainrx_score.sql
│   ├── V006__common_variants_seed.sql
│   └── V007__bio_kb.sql
│
├── data/
│   └── ingestion_manifests/       Pinned release metadata per source (JSON)
│       ├── cpic_v1_58_0.json
│       ├── pharmvar_snapshot_2026_06_05.json
│       ├── clinpgx_api_2026_06_10.json
│       ├── openfda_labels_2026_06_10.json
│       └── rxnorm_cpc_05042026.json
│
├── db/                            Original schema seed files
│   ├── schema.sql
│   ├── migrations/                Early schema migrations (pre-viewer)
│   ├── queries/                   Reference SQL queries
│   └── seeds/                     Seed data files
│
├── docs/                          Architecture and strategy documentation
│   ├── architecture.md
│   ├── source-strategy.md
│   ├── ingestion-readiness.md
│   ├── ingestion-priority.md
│   └── product-positioning.md
│
├── sql/patients_schema.sql        explainrx_patients schema
├── pgx_pipeline_output/           Pipeline output artefacts (gitignored in prod)
├── Dockerfile
└── docker-compose.yml
```

---

## Databases

### `explainrx_dev` — main knowledge base

#### Source provenance layer

| Table | Purpose |
|---|---|
| `source` | One row per upstream source (CPIC, PharmVar, ClinPGx, openFDA, RxNorm, …) |
| `source_license` | License per source: attribution requirements, share-alike, redistribution, commercial-use flags |
| `source_release` | Each ingested snapshot or release version with timestamp, checksum, upstream URL |
| `source_document` | Individual documents within a release (guideline PDFs, TSV exports, API snapshots) |

Every recommendation and allele definition traces back to a `source_release` row. Re-ingesting a new release creates new rows; historical rows are never deleted.

#### Biology layer

| Table | Purpose |
|---|---|
| `gene` | Normalised pharmacogene entities (symbol, HGNC ID, full name, NCBI Gene ID) |
| `variant` | Individual variants (rsID, HGVS notation, chromosome, position) |
| `allele` | Named alleles (*1, *2, …) per gene |
| `allele_definition` | Star allele definitions linking alleles to PharmVar |
| `allele_definition_variant` | Many-to-many: which variants define which allele |
| `diplotype` | Diplotype records per gene (e.g. `CYP2C19 *1/*2`) |

#### Interpretation layer

| Table | Purpose |
|---|---|
| `phenotype` | Phenotype labels per gene (Poor Metabolizer, Normal Metabolizer, …) |
| `gene_drug_pair` | CPIC-registered gene + drug pairings with CPIC level |
| `diplotype_phenotype_map` | Diplotype → phenotype translation per source release |

#### Clinical rules layer

| Table | Purpose |
|---|---|
| `source_recommendation` | Source-native recommendation text (one row per source × gene × drug × phenotype) |
| `clinical_rule` | ExplainRx deterministic rules; each rule has source, version, conditions, and actions |
| `clinical_rule_action` | The action produced when a rule fires (recommend, avoid, reduce dose, …) |
| `clinical_rule_condition` | The match conditions for a rule (gene, phenotype, drug, population context) |

#### Drug normalisation layer

| Table | Purpose |
|---|---|
| `drug` | Normalised drug entities anchored to RxNorm CUIs |
| `label_product` | FDA-labelled products linked to a drug |
| `label_section` | Extracted label sections (clinical pharmacology, warnings, dosing, …) |

#### External evidence layer

| Table | Purpose |
|---|---|
| `external_evidence` | Evidence gathered by the Python pipeline: PharmGKB, ClinVar, PubMed |

Schema (created by `V003__external_evidence.sql` + `V004__add_evidence_level.sql` + `V005__explainrx_score.sql`):

```sql
external_evidence (
  id                         serial PRIMARY KEY,
  gene                       text,
  drug                       text,
  variant_or_allele          text,
  source                     text NOT NULL,   -- 'ClinPGx/PharmGKB' | 'ClinVar' | 'PubMed'
  source_tier                text NOT NULL,   -- 'actionable' | 'informative'
  evidence_count             integer,
  relationship_summary       text,
  cpic_level                 text,            -- A / B / C / D (CPIC prescribing-action tier)
  pharmgkb_evidence_level    text,            -- 1A/1B/2A/2B/3/4 (PharmGKB evidence strength)
  evidence_tags              jsonb,
  relationship_counts        jsonb,
  cpic_level_counts          jsonb,
  pharmgkb_evidence_level_counts jsonb,
  actionability_class        text,            -- ExplainRx axis-1: A1/A2/B/C/D/X
  evidence_weight            text,            -- ExplainRx axis-2: R1/R2/R3/R4
  explainrx_score            text,            -- Combined, e.g. 'A1·R1'
  pipeline_run_id            text,
  ingested_at                timestamptz,
  updated_at                 timestamptz
)
```

#### Bio Knowledge Base layer

Created by `V007__bio_kb.sql`. A curated molecular knowledge graph that grows through `ingest_kb.py` and `expand_kb.py`.

| Table | Purpose |
|---|---|
| `kb_entity` | Genes, proteins, drugs, chemicals, diseases, pathways — anything that can be a graph node |
| `kb_entity_synonym` | Alternative names and aliases per entity (PAI-1→SERPINE1, tPA→PLAT, …) |
| `kb_relationship` | Directed cause-effect edges: source→target with type, direction, PMID, mechanism |
| `kb_pathway` | Canonical pathway definitions |
| `kb_pathway_entity` | Pathway membership (gene or drug → pathway) |
| `kb_function` | Biological function / molecular process descriptors |
| `kb_entity_function` | Association of entities with biological functions |

The `kb_relationship.external_id` column enables idempotent re-runs — each edge from an external source carries a unique identifier (e.g. `signor:SIGNOR-R-12345`, `pt3:12345678:CYP2C19:SERPINE1:activation`) so re-ingesting the same source never creates duplicate rows.

#### Schema versioning

| Table | Purpose |
|---|---|
| `schema_version` | Applied migrations: version number, description, filename, timestamp, MD5 checksum |

---

### `explainrx_patients` — patient profiles

Per-clinic patient gene entries and demographics. In production each clinic runs its own instance, isolated from the shared knowledge base.

| Table | Purpose |
|---|---|
| `clinic` | Clinic identity and metadata |
| `patient` | Patient record (clinic-scoped) |
| `patient_demographics` | Age, sex, ethnicity, smoking, alcohol, renal function, current medications |
| `patient_gene_entry` | Per-patient gene result: gene + diplotype or phenotype (or both) |

View `patient_summary` joins all four tables for fast viewer queries.

---

## Data sources

### Ingestion timeline

| Source | Version / snapshot | Retrieved | Status |
|---|---|---|---|
| CPIC | v1.58.0 (released 2026-05-14) | 2026-06-05 | ✅ Ingested |
| PharmVar | 6.2.25 snapshot | 2026-06-05 | ✅ Ingested |
| RxNorm CPC | RxNorm_full_prescribe_05042026 (released 2026-05-04) | 2026-06-05 | ✅ Ingested |
| ClinPGx / PharmGKB | API snapshot | 2026-06-10 | ✅ Ingested |
| openFDA drug labels | API snapshot | 2026-06-10 | ✅ Ingested |
| SIGNOR | Human dataset (organism 9606) | on-demand | Bio KB |
| Reactome | NCBI2Reactome_All_Levels.txt | on-demand | Bio KB |
| STRING | REST API per-gene | on-demand | Bio KB |
| ChEMBL | REST API per-drug | on-demand | Bio KB |
| UniProt | Swiss-Prot REST API | on-demand | Bio KB |
| PharmGKB pathways | pathways-tsv.zip | on-demand | Bio KB |
| PubMed / PubTator3 | BFS literature mining | continuous | Bio KB expand |

---

### CPIC (Clinical Pharmacogenomics Implementation Consortium)

**Role:** Primary guideline backbone — gene-drug recommendations, phenotype maps, diplotype-to-phenotype rules, activity score logic, allele function assignments.

**Version ingested:** `v1.58.0`, released 2026-05-14, retrieved 2026-06-05.

**Access:** Full SQL database export via GitHub releases at `https://files.cpicpgx.org/data/database/cpic_db_dump-v1.58.0.sql.gz`. Also accessible via REST API at `https://cpicpgx.org/api-and-database/`.

**License:** Permissive; designed for open implementation use. Attribution encouraged.

**Ingestion flow:**
1. Restore the SQL dump into the `cpic_stage` database: `./scripts/rebuild_cpic_stage.sh`
2. Register the release: `Rscript R/ingest/11_register_cpic_release.R`
3. Load content: `./scripts/load_cpic_core.sh` → calls `R/ingest/20_load_cpic_core_from_stage.R`

**What is loaded:**
- `gene` rows for all CPIC pharmacogenes
- `gene_drug_pair` rows with CPIC evidence levels (A / B / C / D)
- `phenotype` rows per gene (Poor Metabolizer, Intermediate Metabolizer, Normal Metabolizer, Rapid Metabolizer, Ultrarapid Metabolizer, Indeterminate)
- `diplotype_phenotype_map` rows for every diplotype in the CPIC data
- `source_recommendation` rows for all CPIC recommendations (one per gene × drug × phenotype combination)

**Current counts (after ingestion):**
- 13 genes in CPIC core scope
- 88 gene-drug pairs
- 727 source recommendations
- 61 phenotype rows

---

### PharmVar (Pharmacogene Variation Consortium)

**Role:** Star allele nomenclature and allele definitions — the authoritative source for what variants compose each named allele.

**Version ingested:** Snapshot of download page, retrieved 2026-06-05. Local file: `data/pharmvar-6.2.25.zip`.

**Access:** `https://www.pharmvar.org/download` — versioned database download in TSV, VCF, and FASTA. REST API at `https://www.pharmvar.org/documentation` (beta, ≤ 2 requests/second).

**License:** Open academic use. Attribution required.

**Ingestion flow:**
1. Register: `Rscript R/ingest/12_register_pharmvar_release.R`
2. Load: `./scripts/load_pharmvar.sh` → calls `R/ingest/24_load_pharmvar_alleles.R`

**What is loaded:**
- `allele` rows (star allele names per gene)
- `allele_definition` rows (PharmVar-linked definitions)
- `allele_definition_variant` rows (variant composition of each allele)

**Key genes covered:** CYP2D6, CYP2C19, CYP2C9, TPMT, DPYD, UGT1A1, SLCO1B1, VKORC1, CYP3A5, CYP1A2.

**Caveat:** PharmVar's downloads do not currently include structural variants (gene duplications, deletions, hybrid alleles) — these require separate handling for genes like CYP2D6.

---

### RxNorm Current Prescribable Content (NLM)

**Role:** Drug normalisation — stable RxCUIs, generic names, brand names, ingredient relationships. Loaded before label ingestion so all downstream tables share a consistent drug identity.

**Version ingested:** `RxNorm_full_prescribe_05042026`, release date 2026-05-04, retrieved 2026-06-05.

**Access:** `https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_prescribe_05042026.zip` — public domain, no UMLS license required for the Current Prescribable Content subset.

**Ingestion flow:**
1. Register: `Rscript R/ingest/13_register_rxnorm_release.R`
2. Load: `Rscript R/ingest/25_populate_rxnorm_cuis.R`

**What is loaded:**
- `drug` rows normalised to RxCUIs
- Generic name, brand names, ingredient mappings
- Brand-to-generic and multi-ingredient product links

---

### ClinPGx / PharmGKB

**Role:** Clinical variant annotations (PharmGKB Clinical Annotation levels), drug label summaries, guideline overlays (including DPWG via PharmGKB delivery).

**Version ingested:** Bulk download snapshot, retrieved 2026-06-10. Source: `https://s3.pgkb.org/data/`.

**License:** CC BY-SA 4.0. Attribution is required; derivative works must carry the same license. Do not use as a commercial backbone without legal review.

**Ingestion flow:**
1. Register: `Rscript R/ingest/14_register_clinpgx_snapshot.R`
2. Load annotations: `./scripts/load_clinpgx.sh`
   - `R/ingest/21_load_clinpgx_clinical_variants.R` → loads `clinicalAnnotations.tsv`
   - `R/ingest/22_load_clinpgx_guidelines.R` → loads `drugLabels.tsv`

**What is loaded:**
- PharmGKB Clinical Annotation records (evidence level: 1A/1B/2A/2B/3/4)
- CPIC level tags where PharmGKB provides them (A/B/C/D)
- Drug label guideline annotations with gene-drug associations

**Rate limit:** 2 requests/second when using the ClinPGx live API. Bulk TSV downloads are preferred for reproducible ingestion.

---

### openFDA Drug Labels

**Role:** Structured FDA drug label text — PGx-relevant sections extracted from SPL submissions.

**Version ingested:** API snapshot, retrieved 2026-06-10.

**Access:** `https://api.fda.gov/drug/label.json` (live JSON API) and bulk JSON downloads at `https://open.fda.gov/`. CC0 1.0 public domain.

**Ingestion flow:**
1. Register: `Rscript R/ingest/15_register_openfda_snapshot.R`
2. Load: `./scripts/load_openfda_labels.sh` → calls `R/ingest/23_load_openfda_labels.R`

**Sections extracted per drug:**
- `clinical_pharmacology`
- `pharmacogenomics`
- `boxed_warning`
- `warnings_and_precautions`
- `dosage_and_administration`
- `contraindications`

**Query strategy:** Per-RxCUI queries so labels are linked to the normalised drug model.

**Current counts:**
- 701 drugs with openFDA labels
- 2 863 label sections
- 766 PGx recommendations from FDA labels

**Caveat:** openFDA explicitly states data are not validated for clinical production use. Treat as label-evidence input alongside CPIC, not as a standalone recommendation engine.

---

### Python evidence pipeline — PharmGKB, ClinVar, PubMed

**Role:** Supplementary evidence for `external_evidence` table. Fills in literature context, variant-level significance, and actionable clinical annotation tiers that are not in the R-ingested core.

**Retrieval:** On-demand by running the pipeline. Output artefacts land in `pgx_pipeline_output/`.

**Pipeline steps:**

```
collect.py  →  curate.py  →  aggregate.py  →  ingest.py
```

| Step | What it does |
|---|---|
| `collect.py` | Queries PharmGKB Clinical Annotations API (per gene), ClinVar via E-utilities, PubMed via E-utilities + efetch. Resumable via `checkpoint.json`. |
| `curate.py` | Normalises gene symbols (HGNC aliases), drug names (dictionary match or SciSpacy NER), extracts star alleles and phenotype mentions, tags relationship types, classifies evidence. |
| `aggregate.py` | Groups records by `(gene, drug, variant_or_allele, source)`. Counts occurrences, relationship types, CPIC levels, PharmGKB levels. |
| `ingest.py` | Upserts rows into `external_evidence`. Idempotent: re-running the same `pipeline_run_id` updates counts in place. Assigns `source_tier` and `explainrx_score`. |

**Usage:**

```bash
EXPLAINRX_DB=explainrx_dev \
NCBI_EMAIL=your@email.com \
./scripts/pgx_pipeline/run_pipeline.sh \
  --query "CYP2D6 OR CYP2C19 OR DPYD OR TPMT OR UGT1A1 OR SLCO1B1" \
  --mode general
```

**Search modes:**

| Mode | Query expansion | Best for |
|---|---|---|
| `general` | 9 sub-queries: base, PGx synonyms, CPIC terms, gene panel, drug panel, gene×drug cross, CPIC×gene, dosing terms, genotype terms | Broad first-pass |
| `cpic` | Base + CPIC terminology block | CPIC-specific literature |
| `gene` | Base + gene panel | Targeted gene-level search |
| `drug` | Base + drug panel | Targeted drug-level search |

**Rate limits:** NCBI allows 3 requests/second unauthenticated. Set `NCBI_API_KEY` to unlock 10 requests/second.

**Evidence tier assignment:**

| Tier | Criteria | Viewer display |
|---|---|---|
| `actionable` | Source is `ClinPGx/PharmGKB` **and** `cpic_level` is A or B | Blue "Supporting Evidence" section alongside primary recommendations |
| `informative` | Everything else: ClinVar variants, PubMed literature, PharmGKB without CPIC A/B | Collapsed "Supporting Literature" panel; labelled "for context only" |

**Critical distinction — `cpic_level` vs. `pharmgkb_evidence_level`:**

These are two separate classification systems stored in separate columns and must never be conflated:

| Field | Values | What it measures |
|---|---|---|
| `cpic_level` | A / B / C / D | CPIC **prescribing-action tier** — whether CPIC has issued a guideline recommending clinical action |
| `pharmgkb_evidence_level` | 1A / 1B / 2A / 2B / 3 / 4 | PharmGKB **evidence strength** — how well-replicated the variant–drug association is, independent of CPIC guidelines |

`source_tier = 'actionable'` requires a real `cpic_level` of A or B. PharmGKB evidence level 1A alone does **not** promote a record to actionable.

---

### Bio Knowledge Base — SIGNOR, Reactome, STRING, ChEMBL, UniProt, PharmGKB pathways

The Bio KB is a molecular knowledge graph stored in the `kb_*` tables (created by `V007__bio_kb.sql`). It is designed to show the broader biological context for PGx genes — what they regulate, what regulates them, which pathways they belong to, what drugs they interact with.

**`scripts/ingest_kb.py`** — six open-source data loaders:

| Source | What is loaded | Access endpoint | Notes |
|---|---|---|---|
| **SIGNOR** | Curated directed causal relationships with mechanism, effect, PMID, SIGNOR-ID | `https://signor.uniroma2.it/getData.php?organism=9606&format=tab` | 27-column TSV, no header; all human relationships loaded (no gene filter) |
| **Reactome** | Human gene → pathway membership | `https://reactome.org/download/current/NCBI2Reactome_All_Levels.txt` | Filtered to `Homo sapiens` only; NCBI Gene ID → symbol resolved from `kb_entity` |
| **STRING** | Protein-protein interactions (scored 0–1000) | `https://string-db.org/api/tsv/network` | Per-gene REST queries for all genes in `kb_entity`; default `--min-score 700` (high confidence) |
| **ChEMBL** | Drug-target binding / mechanism-of-action | Official FTP snapshot: `https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/` | Prefers the official SQLite snapshot when available locally; stores mechanism-level provenance including release metadata, upstream ChEMBL IDs, and reference links when present |
| **UniProt** | Swiss-Prot function descriptions, subcellular location | `https://rest.uniprot.org/uniprotkb/search` | One gene per query (avoids 400 errors from compound OR expressions); updates `kb_entity.description` in place |
| **PharmGKB pathways** | Pathway definitions + gene members | `https://api.pharmgkb.org/v1/download/file/data/pathways-tsv.zip` | ZIP of per-pathway TSVs |

**Usage:**

```bash
cd ~/Documents/New\ project/explainrx

# Apply DB migrations first (once, then whenever a new migration is added)
EXPLAINRX_DB=explainrx_dev bash scripts/migrate.sh

# Individual sources
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py signor
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py reactome
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py uniprot
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py pharmgkb
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py chembl
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py string --min-score 700

# Small ChEMBL snapshot smoke test
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py chembl --chembl-source sqlite --max-drugs 10

# Use a local ChEMBL SQLite archive or extracted DB explicitly
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py chembl --chembl-source sqlite --chembl-local-sqlite-tar /path/to/chembl_37_sqlite.tar.gz --drug-name dasatinib
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py chembl --chembl-source sqlite --chembl-local-sqlite /path/to/chembl_37.db --drug-name dasatinib

# Download the latest official ChEMBL snapshot into data/raw/chembl if needed
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py chembl --chembl-source sqlite --chembl-download-sqlite --drug-name dasatinib

# Or all at once
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py all
```

For ChEMBL, the script now checks `data/raw/chembl/` first, then optional `CHEMBL_LOCAL_SQLITE` / `CHEMBL_LOCAL_SQLITE_TAR` environment variables, and only uses the live API when no snapshot is available and `--chembl-source` is left on `auto`.

ChEMBL relationships also populate `kb_relationship.provenance` with structured upstream metadata such as the ChEMBL release, mechanism ID(s), primary PMID when available, and all mechanism reference links carried by the ChEMBL snapshot.

**Deduplication:** All relationships carry `external_id` (e.g. `signor:SIGNOR-R-12345`). Re-running any source never creates duplicate edges; existing edges are skipped and can have missing provenance fields backfilled on rerun.

---

### Bio KB expansion — PubTator3 literature mining

**`scripts/expand_kb.py`** mines PubMed abstracts via the PubTator3 API to discover molecular relationships beyond what the curated databases contain. It grows the knowledge graph through BFS expansion, starting from the entities already in `kb_entity`.

**Algorithm:**

1. Seed: every entity in `kb_entity` is added to `kb_crawl_queue` with priority proportional to its existing edge count (entities with more known connections are processed first).
2. Worker threads dequeue one entity at a time using `SELECT … FOR UPDATE SKIP LOCKED` — safe for parallel workers and Ctrl-C at any point.
3. Per entity, pages through PubTator3 search results. For each publication, fetches BioC-JSON entity annotations and finds entity pairs that co-occur in the same sentence.
4. Infers relationship type and direction from keyword patterns in the text between the two entities:
   - `activates / upregulates / induces / stimulates` → `activation` (A→B)
   - `inhibits / downregulates / represses / suppresses / blocks` → `inhibition` (A→B)
   - `phosphorylates` → `phosphorylation` (A→B)
   - `ubiquitinates / SUMOylates` → `ubiquitination` (A→B)
   - `methylates / acetylates` → `methylation` (A→B)
   - `cleaves` → `cleavage` (A→B)
   - `transcriptionally activates / transactivates` → `transcriptional_regulation` (A→B)
   - `binds / interacts / associates / complexes` → `binding` (symmetric)
   - `regulates / modulates / controls` → `regulation` (A→B)
   - (fallback) `co-mention` (symmetric)
   Relationship inference resolves to one of three confidence tiers:
   - **Typed** (`activation`, `inhibition`, `phosphorylation`, …) — a relational verb matched and, for protein-modification types, the entity types are compatible.
   - **`association`** (symmetric) — a protein-modification verb (`phosphorylation`, `ubiquitination`, `methylation`, `cleavage`) matched a pair that includes a drug or disease, so the connection is real but its type/direction is untrustworthy. The edge is kept and demoted rather than asserting an impossible mechanism (a gene cannot methylate a disease). Gated by `_GENE_ONLY_TYPES`.
   - **`co-mention`** (symmetric) — no relational language at all; the two entities merely share a sentence. Weakest signal.
5. Newly discovered entities are added to the queue at `depth+1`.
6. When the queue at the current depth is exhausted, the entity with the highest edge count that has not yet been processed at `depth+1` seeds the next wave.

**Checkpoint granularity:** Each search-results page is committed independently. Kill the process at any time; restart to continue from the last committed page. Interrupted items (`status='processing'`) are automatically reset to `pending` on restart.

**Deduplication:** Edge `external_id` format: `pt3:{pmid}:{SRC_SYMBOL}:{TGT_SYMBOL}:{rel_type}`. `ON CONFLICT (external_id) DO NOTHING` makes re-runs fully idempotent.

**Usage:**

```bash
# First run — seeds queue and starts crawling
EXPLAINRX_DB=explainrx_dev python scripts/expand_kb.py

# With options
EXPLAINRX_DB=explainrx_dev python scripts/expand_kb.py \
  --workers 3 \       # threads (PubTator3 asks <= 3 req/s)
  --max-depth 3       # BFS depth (each level can add thousands of new entities)

# Check queue status without running
EXPLAINRX_DB=explainrx_dev python scripts/expand_kb.py --status

# Clear queue and re-seed from scratch
EXPLAINRX_DB=explainrx_dev python scripts/expand_kb.py --reset
```

**Laptop -> Pi DB runbook**

Use `scripts/run_expand_kb_on_pi_db.sh` when you want the crawl process to run on the laptop, but write into the PostgreSQL database on the Raspberry Pi over an SSH tunnel.

```bash
# Check the remote queue without crawling.
# --status prints statistics and exits immediately.
./scripts/run_expand_kb_on_pi_db.sh --status

# Gentle shared-queue crawl from the laptop into the Pi DB.
# Recommended bounded default for demo coverage: enough literature to enrich
# the network without letting a few giant hubs monopolise the run.
nice -n 10 ./scripts/run_expand_kb_on_pi_db.sh \
  --workers 1 \
  --request-delay 10 \
  --page-pause 8 \
  --batch-pause 5 \
  --max-depth 99 \
  --max-pages 200 \
  --snapshot-interval 60
```

Operational notes:

- `--status` is exit-only. If you want the crawl to continue, omit `--status`.
- `--max-pages 200` is the recommended demo-oriented cap. It is usually rich enough to populate important hubs, while still keeping wall-clock time predictable. Remove it only when you intentionally want very deep per-entity exhaustion.
- The wrapper defaults to `--db-commit-mode page`, which is gentler on a remote PostgreSQL instance because writes are committed once per PubTator search-results page instead of after every sub-batch.
- The laptop wrapper now points `EXPLAINRX_HISTORY_FILE` at a canonical Pi-side history log over SSH, so both the Pi crawler and the laptop crawler append to the same daily progress source of truth. By default that shared log is `ssh://agnes@192.168.1.21/home/agnes/explainrx-worker/logs/crawl_health_history.log`.
- The laptop still keeps its human-readable `crawl_health.txt` locally, but it rebuilds the local `scripts/crawl_daily_progress.csv` and `docs/metrics/crawl_daily_growth.svg` from the shared Pi history. That means the local plot reflects both machines whenever the laptop crawl is running.
- Avoid `--from-seed`, `--from-id`, or `--reset` from multiple machines at once. Those options reshape the shared crawl queue, so use them from one machine, then let both the Pi and laptop drain the same queue.
- If startup fails in `_ensure_ddl(...)` with `psycopg2.errors.DeadlockDetected`, that is a schema-lock collision, not a PubTator problem. The current `scripts/expand_kb.py` now does a read-only schema check first and only runs DDL if something is genuinely missing, so update to the latest copy and rerun. If it still happens, another older crawler or schema-changing session is probably touching the same tables.
- If the wrapper says `Local tunnel port 55432 is already in use`, an older SSH tunnel is still listening locally. Either kill that tunnel or choose a different local port:

```bash
kill "$(lsof -tiTCP:55432 -sTCP:LISTEN)"
# or
EXPLAINRX_PI_LOCAL_PORT=55433 ./scripts/run_expand_kb_on_pi_db.sh --status
```

**Relationship confidence score**

Every edge carries a numeric `kb_relationship.confidence_score` (1–5, higher = more informative relationship type) so queries can rank by signal strength. This is distinct from the categorical `confidence` column (`high`/`medium`/`low` evidence quality) written by `ingest_kb.py`. The ranking, defined by `_REL_CONFIDENCE` in `expand_kb.py`, is the single source of truth:

| Score | Relationship types |
|---|---|
| 5 | `activation`, `inhibition` (directed functional effect) |
| 4 | `phosphorylation`, `methylation`, `ubiquitination`, `cleavage`, `expression`, `metabolism`, … (specific directed mechanism) |
| 3 | `binding`, `regulation` (specific-but-undirected, or vague) |
| 2 | `association` (connection real, type/direction unknown) |
| 1 | `co-mention` (bare sentence proximity) |

New PubTator edges are scored as they're written. To (re)score **all** existing rows from every source (SIGNOR, STRING, ChEMBL, ClinPGx, V007 seed) — useful the first time the column is added, or after changing the mapping:

```bash
EXPLAINRX_DB=explainrx_dev python scripts/expand_kb.py --backfill-scores
```

**Species tagging**

The crawl keeps literature from all organisms (PubTator searches are not species-filtered) but records the species context of each edge in `kb_relationship.species`: `human`, `non-human`, `mixed`, or `NULL`. It's derived from the gene endpoint's NCBI Gene ID (PubTator normalises genes to species-specific IDs — human STAT3 = `6774`, mouse Stat3 = `20848`) against a human whitelist built from HGNC's `entrez_id` column. The whitelist is downloaded once and cached at `viewer/data/human_gene_ids.txt`; if the download fails, the crawl continues with `species = NULL`. Edges with no gene endpoint (e.g. drug–disease) are `NULL`.

```sql
-- Human-only view of the graph, without having dropped anything at crawl time
SELECT * FROM kb_relationship WHERE species = 'human';
```

To instead **drop** non-human genes at crawl time (rather than tag them), add `--human-only`:

```bash
EXPLAINRX_DB=explainrx_dev python scripts/expand_kb.py --symbol CYP2C19 --human-only
```

**Queue table (`kb_crawl_queue`) columns:**

| Column | Purpose |
|---|---|
| `entity_id` | FK to `kb_entity` |
| `symbol` | Gene / drug symbol for display and API queries |
| `status` | `pending` / `processing` / `done` / `error` |
| `priority` | Edge count at queue time — higher-connectivity entities go first |
| `depth` | BFS depth level (0 = initial seed, 1 = first expansion, …) |
| `next_page` | Last committed PubTator3 search page — enables page-level resume |
| `total_pages` | Total pages for this entity's search results |
| `n_pmids` | Cumulative PMIDs processed |
| `n_edges` | Cumulative edges added |

**Troubleshooting the PubTator3 search API**

The PubTator3 search endpoint is `https://www.ncbi.nlm.nih.gov/research/pubtator3-api/search/`. Two non-obvious traps are baked into `_pt3_search` — both were live bugs fixed on 2026-06-15:

- **Do not send a bare `sort=score`.** The endpoint returns `HTTP 400 Bad Request` (with an empty body) for `sort=score`; it expects a sort *direction*, e.g. `sort=score desc`. The `page` and `size` parameters work fine on their own. Since results are relevance-ranked by default, `expand_kb.py` omits `sort` entirely. A 400 on *every* search — `[SYMBOL] search page 1 failed: HTTP Error 400: Bad Request` for every entity, ending in `Total PMIDs: 0  Total edges: 0` — is the signature of this bug.
- **The response is *not* Elasticsearch-shaped.** It returns:

  ```json
  {"results": [ {"_id": "...", "pmid": 39117533, ...}, ... ],
   "count": 129776, "total_pages": 12978, "current": 1, "page_size": 10}
  ```

  PMIDs come from `results[].pmid` (or `results[]._id`), and the page count from the top-level `total_pages` field. Parsing a `hits.hits` / `total.value` structure (the older assumption) silently yields zero articles and therefore zero edges even when the request succeeds.

To sanity-check the endpoint by hand:

```bash
# Works (200, JSON with "results"):
curl 'https://www.ncbi.nlm.nih.gov/research/pubtator3-api/search/?text=STAT3&page=1&size=10'
# Fails (400, empty body):
curl 'https://www.ncbi.nlm.nih.gov/research/pubtator3-api/search/?text=STAT3&sort=score'
```

The BioC export endpoint (`.../publications/export/biocjson?pmids=…`) returns `{"PubTator3": [ <bioc-doc>, … ]}` and is parsed correctly by `_pt3_fetch` / `_parse_doc`.

---

## Migration system

Migrations live in `migrations/V{NNN}__description.sql` and are applied by `scripts/migrate.sh`.

```bash
# Apply all pending migrations
EXPLAINRX_DB=explainrx_dev bash scripts/migrate.sh

# Check applied / pending status
EXPLAINRX_DB=explainrx_dev bash scripts/migrate.sh --status

# Stamp existing schema as already applied (first-time only, on pre-migration DBs)
EXPLAINRX_DB=explainrx_dev bash scripts/migrate.sh --baseline
```

Each migration is recorded in `schema_version` with version number, description, filename, application timestamp, and MD5 checksum of the SQL file.

### Applied migrations

| Migration | Description | What it adds |
|---|---|---|
| `V001` | Baseline schema marker | Creates `schema_version` table; documents that the main schema was set up via `db/schema.sql` or Docker ingest |
| `V002` | Viewer performance indexes | 15+ indexes on `source_recommendation`, `gene_drug_pair`, `diplotype_phenotype_map`, `external_evidence` for fast viewer queries |
| `V003` | External evidence table | `external_evidence` with source tier, CPIC level, relationship counts, PharmGKB tags, JSONB evidence fields |
| `V004` | Evidence level separation | Adds `pharmgkb_evidence_level` and `pharmgkb_evidence_level_counts` — separates PharmGKB's evidence-strength grading from CPIC's prescribing-action tier |
| `V005` | ExplainRx score columns | Adds `actionability_class`, `evidence_weight`, `explainrx_score` to `external_evidence`, `source_recommendation`, and `gene_drug_pair`; backfills scores from existing CPIC levels |
| `V006` | Common variants seed | Seeds `allele_definition_variant` with well-known SNVs for CYP2C19, CYP2D6, CYP2C9, VKORC1, SLCO1B1 for VCF calling demonstration |
| `V007` | Bio Knowledge Base schema | Creates `kb_entity`, `kb_entity_synonym`, `kb_relationship`, `kb_pathway`, `kb_pathway_entity`, `kb_function`, `kb_entity_function`; seeds ~35 PGx gene entities, ~30 drug entities, 5 canonical pathways, ~100 curated relationships |

---

## R ingestion pipeline

The R pipeline registers each upstream release as a provenance record, then loads content in dependency order.

### Full ingest sequence

```bash
# 1. Restore CPIC staging database from the official SQL dump
./scripts/rebuild_cpic_stage.sh

# 2. Register all source releases (creates source, source_release, source_document rows)
EXPLAINRX_DB=explainrx_dev Rscript R/ingest/99_register_priority_sources.R

# 3. Load content in dependency order
EXPLAINRX_DB=explainrx_dev ./scripts/load_cpic_core.sh      # genes, pairs, phenotypes, recs
EXPLAINRX_DB=explainrx_dev ./scripts/load_pharmvar.sh        # allele definitions
EXPLAINRX_DB=explainrx_dev ./scripts/load_clinpgx.sh         # variant annotations, drug labels
EXPLAINRX_DB=explainrx_dev ./scripts/load_openfda_labels.sh  # drug labels + PGx sections
EXPLAINRX_DB=explainrx_dev Rscript R/ingest/25_populate_rxnorm_cuis.R  # drug normalisation
```

### Ingestion manifest files

Every source release is pinned in `data/ingestion_manifests/`. These JSON files record:
- `source_slug` — machine identifier
- `version_label` — human-readable version
- `release_date` — upstream release date
- `retrieved_at` — ISO-8601 timestamp of when ExplainRx fetched it
- `upstream_url` — canonical download URL
- `artifacts` — list of actual files loaded with their roles and formats
- `notes` — any caveats or implementation notes

### R package dependencies

```r
# Database connectivity
install.packages(c("DBI", "RPostgres", "pool"))

# Viewer
install.packages(c(
  "bslib", "bsicons", "shiny", "reactable", "htmltools",
  "dplyr", "jsonlite", "rmarkdown", "knitr", "kableExtra",
  "DT", "plotly"
))

# PDF reporting
tinytex::install_tinytex()
```

---

## Python evidence pipeline

See `scripts/pgx_pipeline/README.md` for full documentation.

```bash
# Full run
EXPLAINRX_DB=explainrx_dev \
NCBI_EMAIL=your@email.com \
NCBI_API_KEY=your_api_key \
./scripts/pgx_pipeline/run_pipeline.sh \
  --query "CYP2D6 OR CYP2C19 OR DPYD OR TPMT OR UGT1A1 OR SLCO1B1" \
  --mode general \
  --outdir pgx_pipeline_output/

# Typical output volume (mode=general, 6-gene query)
# ClinVar:  500–2 000 raw records → hundreds of (gene, variant) pairs
# PubMed:   5 000–15 000 PMIDs   → tens of (gene, drug) pairs (drug dict limited)
# PharmGKB: 5–15 pathway records  → 5–15 pathway groups
# Runtime:  10–20 minutes (NCBI rate limit: 3 req/s unauthenticated)
```

### Python package dependencies

```bash
pip install requests psycopg2-binary

# Optional: NER-based drug extraction (improves PubMed drug normalisation substantially)
pip install scispacy
python -m spacy download en_core_sci_sm
```

---

## Bio Knowledge Base

### Seed content (V007__bio_kb.sql)

Loaded automatically by the migration. Provides a working knowledge graph before any external ingestion:

- **~35 PGx gene entities:** CYP2C19, CYP2D6, CYP2C9, CYP3A4, CYP3A5, CYP1A2, VKORC1, SERPINE1, PLAT, SLCO1B1, DPYD, TPMT, UGT1A1, HLA-B, G6PD, and key interactors
- **~30 drug/chemical entities:** warfarin, clopidogrel, simvastatin, metoprolol, omeprazole, codeine, fluorouracil, and others
- **5 disease entities:** cardiovascular disease, venous thromboembolism, cancer, psychiatric disorders, autoimmune disease
- **5 canonical pathways:** CYP-mediated drug metabolism, VKORC1-warfarin anticoagulation, fibrinolysis/PAI-1, SLCO1B1-statin PK, TPMT-thiopurine
- **~100 curated relationships** with PMIDs from primary literature
- **10 biological functions** with entity associations
- **~20 synonyms** (PAI-1→SERPINE1, tPA→PLAT, OATP1B1→SLCO1B1, …)

### Extending with open databases

```bash
# Priority order: SIGNOR first (highest-quality directed edges)
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py signor
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py reactome
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py uniprot    # enriches descriptions
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py pharmgkb
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py chembl
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py string --min-score 700
```

### Continuous literature expansion

```bash
# Seed queue from current kb_entity and begin crawling
EXPLAINRX_DB=explainrx_dev python scripts/expand_kb.py --workers 3 --max-depth 2

# Monitor progress
EXPLAINRX_DB=explainrx_dev python scripts/expand_kb.py --status
```

While the crawl runs, `scripts/expand_kb.py` also maintains these progress artifacts:

- `crawl_health.txt` — latest human-readable snapshot
- `crawl_health_history.log` — minute-level history log
- `crawl_daily_progress.csv` — one row per day with start/end counts and daily relationship gain, ready for plotting
- `docs/metrics/crawl_daily_growth.svg` — tracked SVG growth plot for the ExplainRx repo

You can rebuild the daily CSV and SVG plot at any time from the raw history:

```bash
python scripts/crawl_progress_rollup.py
```

## Crawl Progress

![ExplainRx crawl progress](docs/metrics/crawl_daily_growth.svg)

---

## Viewer

```bash
EXPLAINRX_DB=explainrx_dev ./scripts/run_viewer.sh
# Open http://127.0.0.1:8765
```

The viewer uses **two-phase loading**: phase 1 (fast) fetches overview data — gene, drug, CPIC level, score — and populates the table immediately. Phase 2 loads full detail (label sections, citations, diplotype maps) in the background. Reactives that need full detail are guarded with `req(!isTRUE(data$overview_only))` so they fire only after phase 2 completes.

### Sidebar controls

- **Gene filter** — multi-select; `(All)` means no gene filter
- **Drug filter** — multi-select
- **Source filter** — multi-select (CPIC, openFDA, ClinPGx, …)
- **ExplainRx score filter** — filter by actionability class (A1/A2/B/C/D/X) and/or evidence weight (R1/R2/R3/R4)
- **Search box** — free-text search across gene, drug, recommendation text

### Tabs

| Tab | Description |
|---|---|
| **Overview** | DB counts, source registry, latest schema version, ingestion timestamps |
| **Recommendations** | Full `source_recommendation` table; click-to-expand row shows full text, citations, DDI context |
| **Gene-Drug Pairs** | CPIC-levelled gene-drug pairs with evidence summary and score badge |
| **Phenotype Map** | Diplotype → phenotype mapping table |
| **Alleles** | Star allele definitions with variant positions (from PharmVar) |
| **Sources** | Source registry, release history, document index |
| **Clinical Rules** | ExplainRx deterministic rules with conditions, actions, source, status |
| **Gene Info** | Gene information card: NCBI Entrez gene summary (live, cached), chromosomal location, then Bio KB section with pathway chips, function chips, relationship list with PubMed links |
| **Patient VCF** | Upload VCF; calls star alleles from variant coordinates; maps diplotypes to phenotypes; generates recommendations |
| **Patient Profile** | Multi-gene manual entry, demographics, DDI phenoconversion, save/load from patient DB, PDF export |
| **QC** | Data quality checks, source coverage gaps, missing diplotype maps |

### Gene Info card — NCBI Entrez integration

When a gene is searched in the Gene Info tab, the viewer:
1. Queries NCBI E-utilities `esearch` + `esummary` for the gene summary, chromosomal location, NCBI Gene ID
2. Caches the result in-process (persists for the session)
3. Displays the Entrez summary as the primary description; falls back to the database description if Entrez returns nothing
4. Shows the NCBI Gene ID as a direct link to `https://www.ncbi.nlm.nih.gov/gene/{id}`
5. Queries `kb_entity`, `kb_relationship`, `kb_pathway`, `kb_function` for the Bio KB section

### Patient Profile features

- **Multi-gene rows:** add or remove gene rows with + / − buttons
- **Diplotype or phenotype entry:** enter a full diplotype (`*1/*2`) or phenotype-only ("Poor Metabolizer") for an artificial profile
- **Optional demographics:** sex, age, ethnicity, smoking status, alcohol use, renal function, current medications
- **DDI phenoconversion:** detects CYP inhibitors and inducers in the current medications list; shifts the phenotype by steps along the metaboliser scale; shows inline DDI warnings per gene; carries DDI-adjusted phenotypes into recommendations and PDF
- **Save / load / delete:** profiles stored in `explainrx_patients` under the clinic's namespace
- **PDF export:** patient header, gene profile with DDI-adjusted phenotypes, DDI warnings, full recommendations table filtered to the patient's drugs, data provenance stamp

### Performance and caching

- Query results cached to disk in `viewer/.cache/*.rds` (default TTL: 3 600 seconds)
- Cache busted by clicking the ↺ Refresh button in the toolbar
- Key indexes applied by `V002__add_viewer_indexes.sql`
- Persistent DB connections via `DBI` / `RPostgres` / `pool` required for performance

---

## ExplainRx score

A two-axis scoring system applied to every recommendation and evidence record.

### Axis 1 — Actionability class

| Code | Meaning |
|---|---|
| `A1` | Strong prescribing action; broad source agreement (CPIC A with ≥ 2 independent sources) |
| `A2` | Prescribing action with context (indication, dose threshold, co-medications) |
| `B` | Monitor or caution; no simple switch rule |
| `C` | Informational; association present, no action currently justified |
| `D` | Not actionable; sources do not support a recommendation |
| `X` | Assay-limited; result is ambiguous or assay coverage is insufficient |

### Axis 2 — Evidence weight

| Code | Corresponds to | Meaning |
|---|---|---|
| `R1` | CPIC A / PharmGKB 1A–1B | Replicated, guideline-endorsed |
| `R2` | CPIC B / PharmGKB 2A–2B | Moderate; single good study or preliminary replication |
| `R3` | CPIC C / PharmGKB 3 | Limited; conflicting, early, or case-level data |
| `R4` | CPIC D / PharmGKB 4 | Insufficient; annotated but no pharmacogenomic data |

### Combined score

Always expressed as both axes: `A1·R1`, `A2·R2`, `B·R1`, `X·R1`. The `X·R1` combination is important: it signals that the underlying gene-drug evidence is guideline-level, but the assay could not make the call — a very different clinical message from `X·R4`.

**Derivation:** Scores are computed by `ingest.py` (for external evidence) and backfilled by `V005__explainrx_score.sql` (for `source_recommendation` from CPIC levels). They are stored in derived columns alongside the original source-native values, which are never overwritten.

---

## Patient database

```bash
# Default setup
./scripts/setup_patients_db.sh

# With clinic details
EXPLAINRX_CLINIC_NAME="St. Mary Pharmacy" \
EXPLAINRX_CLINIC_ID="st-mary" \
./scripts/setup_patients_db.sh
```

Schema (`sql/patients_schema.sql`):

```sql
clinic           (id, name, slug, created_at)
patient          (id, clinic_id, mrn, created_at)
patient_demographics (patient_id, sex, age, ethnicity, smoking, alcohol,
                      renal_function, current_medications jsonb)
patient_gene_entry   (id, patient_id, gene, diplotype, phenotype,
                      entered_by, entered_at, notes)
```

View `patient_summary` provides a single-query join for the viewer's profile loader and PDF exporter.

---

## Quick start

### Prerequisites

- PostgreSQL ≥ 14
- R ≥ 4.3
- Python ≥ 3.10
- `pdflatex` or TinyTeX (for PDF reports)

### 1. Create databases

```bash
psql -c "CREATE DATABASE explainrx_dev;"
psql -c "CREATE DATABASE cpic_stage;"
```

### 2. Apply migrations

```bash
EXPLAINRX_DB=explainrx_dev bash scripts/migrate.sh --baseline  # first run only, on existing DB
EXPLAINRX_DB=explainrx_dev bash scripts/migrate.sh
```

### 3. Ingest core sources

```bash
# Restore CPIC staging DB
./scripts/rebuild_cpic_stage.sh

# Register all releases
EXPLAINRX_DB=explainrx_dev Rscript R/ingest/99_register_priority_sources.R

# Load in dependency order
EXPLAINRX_DB=explainrx_dev ./scripts/load_cpic_core.sh
EXPLAINRX_DB=explainrx_dev ./scripts/load_pharmvar.sh
EXPLAINRX_DB=explainrx_dev ./scripts/load_clinpgx.sh
EXPLAINRX_DB=explainrx_dev ./scripts/load_openfda_labels.sh
EXPLAINRX_DB=explainrx_dev Rscript R/ingest/25_populate_rxnorm_cuis.R
```

### 4. Run the Python evidence pipeline

```bash
EXPLAINRX_DB=explainrx_dev \
NCBI_EMAIL=your@email.com \
./scripts/pgx_pipeline/run_pipeline.sh \
  --query "CYP2D6 OR CYP2C19 OR DPYD OR TPMT OR UGT1A1" \
  --mode general
```

### 5. Ingest the Bio KB

```bash
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py signor
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py reactome
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py uniprot
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py pharmgkb
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py chembl
EXPLAINRX_DB=explainrx_dev python scripts/ingest_kb.py string
```

### 6. (Optional) Expand KB from literature

```bash
EXPLAINRX_DB=explainrx_dev python scripts/expand_kb.py --workers 3 --max-depth 2
```

### 7. Create the patient database

```bash
./scripts/setup_patients_db.sh
```

### 8. Launch the viewer

```bash
EXPLAINRX_DB=explainrx_dev ./scripts/run_viewer.sh
# Open http://127.0.0.1:8765
```

---

## Environment variables

### Viewer

| Variable | Default | Description |
|---|---|---|
| `EXPLAINRX_DB` | `explainrx_dev` | Main knowledge base PostgreSQL database name |
| `EXPLAINRX_PATIENTS_DB` | `explainrx_patients` | Patient profiles database name |
| `EXPLAINRX_VIEWER_HOST` | `127.0.0.1` | Bind host for the Shiny server |
| `EXPLAINRX_VIEWER_PORT` | `8765` | Bind port |
| `EXPLAINRX_CACHE_TTL` | `3600` | Query cache TTL in seconds (`0` = disable cache) |

### Python pipeline

| Variable | Default | Description |
|---|---|---|
| `EXPLAINRX_DB` | `explainrx_dev` | Target PostgreSQL database |
| `NCBI_EMAIL` | — | Required by NCBI E-utilities policy |
| `NCBI_API_KEY` | — | Optional; raises NCBI rate limit from 3 to 10 req/s |
| `HGNC_ALIASES_FILE` | — | TSV of `alias → symbol`; improves gene normalisation in `curate.py` |
| `PGX_OUTDIR` | `pgx_pipeline_output/` | Working directory for raw / curated / aggregated files |
| `RETMAX_PUBMED` | `500` | Max PubMed records per sub-query |
| `RETMAX_CLINVAR` | `200` | Max ClinVar records per sub-query |

---

## Docker

```bash
# Full ingest + viewer
docker-compose up

# Ingest only
./scripts/docker_ingest.sh
```

The `Dockerfile` and `docker-compose.yml` build a single image containing R, Python, PostgreSQL client tools, and all dependencies. The compose file mounts `data/` for source files and exposes port `8765` for the viewer.

---

## Design principles

**Source-native truth first.** CPIC, DPWG, and FDA recommendations are stored separately in their native form. ExplainRx harmonisation is a layer on top, never a replacement for source-specific positions.

**No in-place mutation.** New source releases append records and deactivate prior rules. Historical recommendations remain queryable.

**Deterministic rules.** Clinical output comes from structured `clinical_rule` rows, not from free-text summarisation or LLM inference.

**Provenance at the source-release level.** Every recommendation, allele definition, and evidence record links back to the exact upstream release used.

**Two classification axes.** Actionability (what to do) is separated from evidence weight (how well-supported the association is). A strong evidence claim (`R1`) about a contextual recommendation (`A2`) is expressed as `A2·R1`, not flattened into a single tier.

**Research use only.** ExplainRx is not validated or cleared for direct patient-care decisions. All outputs are for research, educational, and clinical decision-support development purposes only.

---

## Known gaps and roadmap

| Gap | Impact | Planned fix |
|---|---|---|
| DPWG not directly ingested | Only CPIC recommendations shown; DPWG comparison absent | Add `R/ingest/26_load_dpwg.R` using ClinPGx DPWG delivery |
| Drug dictionary in `curate.py` is sparse (~10 entries) | Most PubMed records get `drug=None`; gene-drug pairs under-aggregated | Seed from the `drug` table in `explainrx_dev`, or enable SciSpacy NER (already scaffolded) |
| PharmGKB gene field is a flattened string | Gene names like `"CYP2D6 \| warfarin pathway"` don't normalise cleanly | Add proper PharmGKB gene-array parser in `collect.py` |
| Star allele calling is demonstration-quality | VCF tab: SNV/indel only; no copy-number variants, structural alleles, or phasing | Integrate PharmCAT for allele calling, or substantially expand `vcf_caller.R` |
| ClinVar accessions not linked to star alleles | No cross-reference from `external_evidence` to `allele_definition_variant` | Add variant-coordinate join (rsID / HGVS position matching) |
| Multi-gene recommendations partially modelled | Antidepressant combination guidance (CYP2D6 + CYP2C19 interaction) incomplete | Extend `clinical_rule` schema with multi-gene condition support |
| Bio KB gene info shown only for searched gene | Relationships for partner entities visible only if the partner is also searched | Add "expand" action in Gene Info card to navigate to related entities |
| `expand_kb.py` relationship inference is keyword-based | Co-mention with keyword heuristics — misses negation, indirect relationships, complex syntax | Add dependency-parse or SciSpacy-based NER for higher-precision extraction |

---

## Data counts (June 2026, after full ingest)

| Content | Count |
|---|---|
| Genes (CPIC core) | 13 |
| Gene-drug pairs (CPIC-registered) | 88 |
| Source recommendations | 727 |
| Phenotype rows | 61 |
| Drugs with openFDA labels | 701 |
| FDA label sections extracted | 2 863 |
| PGx recommendations from FDA labels | 766 |
| External evidence records (pipeline) | 1 354+ |
| Bio KB entities (seed) | ~70 |
| Bio KB relationships (seed + SIGNOR) | ~100 + growing |

---

## License and attribution

ExplainRx ingests content from multiple upstream sources, each with its own terms:

| Source | License | Key requirement |
|---|---|---|
| CPIC | Permissive open use | Attribution encouraged |
| PharmVar | Open academic use | Attribution required |
| RxNorm CPC | Public domain (NLM) | No restrictions for CPC subset |
| openFDA | CC0 1.0 | No restrictions (third-party content may differ) |
| ClinPGx / PharmGKB | CC BY-SA 4.0 | Attribution required; derivative works must carry same license |
| SIGNOR | Open academic use | PMID: 30476227 |
| Reactome | CC0 / CC BY 4.0 | Attribution for CC BY content |
| STRING | CC BY 4.0 | Attribution required |
| ChEMBL | CC BY-SA 3.0 | Attribution; share-alike |
| UniProt / Swiss-Prot | CC BY 4.0 | Attribution required |
| PubMed abstracts | PubMed open access | NCBI terms of use |

**ExplainRx is for research and educational use only. It is not a medical device and has not been validated or cleared for clinical decision-making.**
