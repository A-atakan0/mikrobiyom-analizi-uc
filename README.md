# Gut Microbiome in Ulcerative Colitis by Disease Severity (Full-Length Nanopore 16S)

## Objective

Compare gut microbiome composition and diversity between ulcerative colitis (UC) patients in endoscopic remission (Mayo endoscopic subscore **MES 0**) and patients with severe active disease (**MES 3**), using full-length Oxford Nanopore 16S rRNA sequencing data.

## Data

- **Source:** Zenodo (public DOI), study *"Microbial selenoproteins in ulcerative colitis"*, January 2026
- **Samples:** 9 stool samples: 5 MES 0 (remission), 4 MES 3 (severe active UC)
- **Sequencing:** Oxford Nanopore, full-length (~1,500 bp) 16S rRNA gene
- **Metadata:** data/Metadata_MES0_MES3.xlsx (from the same Zenodo record)

## Pipeline

~~~
FASTQ (per barcode) → NanoPlot (QC) → Chopper (Q≥10, 1200–1650 bp) → Emu (species-level abundance)
→ pandas (species × sample table) → Shannon diversity + Mann–Whitney U → plots
~~~

| Step | Tool |
|---|---|
| Read QC | NanoPlot |
| Quality / length filtering | Chopper (Q ≥ 10, 1200–1650 bp, matching the expected ~1,500 bp full-length 16S) |
| Taxonomic profiling | Emu (minimap2 alignment + expectation–maximization, species level) |
| Merging, diversity, statistics, plots | Python: pandas, NumPy, SciPy, matplotlib, seaborn (scripts/analyze_microbiome.py) |

**Methodological note:** DADA2, the standard denoiser for short-read Illumina amplicons, was deliberately *not* used. After inspecting the raw data (measured read length ~1,389 bp), Emu, which is designed for full-length Nanopore 16S reads, was chosen instead, i.e. the pipeline was adapted to the data type.

## Results

### Filtering and classification

- Read loss during filtering was low for all 9 samples (on average 3–4%); about **485,000** high-quality full-length 16S reads were analysed.
- Emu classified 99.6–100% of reads in most samples.

### Alpha diversity (Shannon index)

![Shannon diversity](figures/shannon_diversity.png)

| Sample | Group | Shannon |
|---|---|---|
| BC27_01 | MES 0 | 2.95 |
| BC28_01 | MES 0 | 3.55 |
| BC52_01 | MES 0 | 3.50 |
| BC73_01 | MES 0 | 3.79 |
| BC86_01 | MES 0 | 3.82 |
| BC35_01 | MES 3 | 3.69 |
| BC49_01 | MES 3 | 3.79 |
| BC61_01 | MES 3 | 4.05 |
| BC62_01 | MES 3 | 2.93 |

Mann–Whitney U test: **p = 0.73**. There is no significant difference in overall diversity between MES 0 and MES 3.

### Species composition

![Top 15 species per sample](figures/taxa_barplot.png)

Although the groups do not differ overall, one sample stands out. **BC61_01** (MES 3) shows a classic UC-associated dysbiosis pattern: the butyrate-producing *Faecalibacterium prausnitzii* is almost absent (~0.1% relative abundance), while *Christensenella* species reach ~20% combined. Notably, BC61_01 has the *highest* Shannon index in the dataset, so this dysbiosis is a shift in composition rather than a loss of diversity.

The pattern is not shared by the whole MES 3 group: BC35_01 and BC62_01 contain *F. prausnitzii* at levels similar to MES 0 samples (~17%).

## Repository Structure

~~~
mikrobiyom-analizi-uc/
├── data/      # metadata and run info (FASTQ files not included)
├── results/   # Emu outputs, combined species abundance table, pipeline log
├── scripts/   # analyze_microbiome.py
└── figures/   # Shannon diversity and species barplot
~~~

## Limitations

- Small sample size (5 vs 4) limits statistical power for group-level differences.
- Within-group variation (e.g. BC61_01 vs BC62_01 in MES 3) is larger than the between-group difference.
- Beta diversity (e.g. Bray–Curtis PCoA) and formal differential abundance testing (e.g. ANCOM-BC) were not performed; they are natural next steps.
- Emu's default database has not been updated since 2020, so recently described species may be missing.
- Learning/portfolio project; not for clinical diagnosis or treatment decisions.

## Author

**Atakan Aslan** · Molecular Biology and Genetics, Sivas Cumhuriyet University
