## Dimer Analysis – Code and Data Overview

This repository contains code, input data, and figures used in the manuscript  
**“Differential conservation analysis identifies residues defining constitutive internalization in beta‑adrenergic receptors”** .

There are two main components:
- Structural visualization of the TM1/TM7/H8 dimer interface (Figure 1B), which is **independent of RRCS**.
- Quantitative analysis of dimerization interface contacts from MD simulations using the **residue–residue contact score (RRCS)** algorithm of Zhou and co‑workers, implemented following Jones *et al.*, eLife 2020 [https://doi.org/10.7554/eLife.54895](https://doi.org/10.7554/eLife.54895).

### Ortholog Multiple Sequence Alignment (MSA)

- **`BAR_orthologs_MSA.fasta`**  
  - Multiple sequence alignment of β-adrenergic receptor orthologs used to calculate residue conservation within orthologs of each β-adrenergic receptor subtype.  
  - The file is organized in a structured format where:
    - **Human sequences** (ADRB1_HUMAN, ADRB2_HUMAN, ADRB3_HUMAN) appear first for each subtype
    - **Ortholog sequences** from other species immediately follow each human sequence
    - This pattern repeats for all three β-adrenergic receptor subtypes (β₁AR, β₂AR, β₃AR)

#### Example structure of the fasta file:

```
>sp|P08588|ADRB1_HUMAN|9606/1-477          # Human β₁AR
[alignment sequence...]
>tr|G3SE09|G3SE09_GORGO|9595/1-291         # Gorilla β₁AR ortholog
[alignment sequence...]
>tr|...|..._PANTR|...                       # Chimpanzee β₁AR ortholog
[alignment sequence...]
[... additional β₁AR orthologs ...]

>sp|P07550|ADRB2_HUMAN|9606/1-413          # Human β₂AR
[alignment sequence...]
[... β₂AR orthologs ...]

>sp|P13945|ADRB3_HUMAN|9606/1-408          # Human β₃AR
[alignment sequence...]
[... β₃AR orthologs ...]
```

This organization enables subtype-specific conservation analysis by grouping each human receptor with its respective orthologs.

### Structural visualization for Figure 1B (independent of RRCS)

- **`structural_visualization_adrb1_turkey.pse`**  
  - PyMOL session used to generate structural views of the BAR dimer based on the ligand‑free turkey β1‑adrenergic receptor template.  
  - Encodes the representation, coloring, selection of TM1/TM7/H8, and orientation used in the manuscript.

- **`dimer_figure1B.png`**  
  - Exported PyMOL image from the above session.  
  - Used as **Figure 1B** in the manuscript to illustrate the TM1/TM7/H8 dimer interface and the differentially conserved residues.

### RRCS‑based dimer interface analysis (Figure 3)

#### Core RRCS implementation

- **`RRCS.py`**  
  - Stand‑alone Python implementation of the RRCS algorithm.  
  - Takes a single PDB file as input and writes a corresponding `*.cscore` text file.  
  - Each line of the output lists a residue pair and its RRCS value:  
    `CHAIN:RESNUM_RESNAME  CHAIN:RESNUM_RESNAME  CONTACT_SCORE`.

#### Batch scoring of MD snapshots

- **`rrcs_complier.py`**  
  - Convenience script to run `RRCS.py` on many MD snapshots.  
  - Assumes two main snapshot directories on disk:
    - `Active-Inactive`
    - `Inactive-Inactive` (mirrored here under `Inactive-Inactive/WT`, `Inactive-Inactive/V34A`, `Inactive-Inactive/S41A`, `Inactive-Inactive/V34A_S41A`, `Inactive-Inactive/F49A`).  
  - Recursively finds all `*.pdb` snapshots in these folders and executes  
    `python RRCS.py <snapshot.pdb>`  
    to generate matching `*.cscore` files for every frame and mutant.

#### MD snapshot and RRCS data layout

- **`Inactive-Inactive/`**  
  - Contains subfolders for each mutant (`WT`, `V34A`, `S41A`, `V34A_S41A`, `F49A`).  
  - Each mutant folder holds multiple trajectory replicas, e.g. `WT_II_1_PDB`, `WT_II_2_PDB`, …  
  - Within each replica folder:
    - `*.pdb` — individual MD snapshots of the dimer.  
    - `*.pdb.cscore` — RRCS output from `RRCS.py` for the corresponding snapshot.
  - These `.cscore` files are the raw input for the downstream total interface score calculations.

#### Aggregating interface contact scores

- **`total_rrcs_dimer_boxplot.py`**  
  - Walks the project directory tree, reads every `*.cscore` file, and extracts **A–B dimer interface** contact scores.  
  - For each snapshot, it **sums all RRCS values between chain A and chain B residues** to obtain a single total interface contact score.  
  - Aggregates these totals by mutation (e.g. `WT_II`, `V34A_II`, `S41A_II`, `V34A_S41A_II`, `F49A_II`).  
  - Writes a long‑format CSV:
    - **`boxplot_data_II.csv`** – columns: `Mutation`, `Contact Score`; each row is one MD frame’s A–B interface total.

#### Statistical analysis and visualization

- **`interface_contact_score_boxplot.R`**  
  - R script that reads `boxplot_data_II.csv` and prepares **Figure 3** of the manuscript.  
  - Steps:
    - Recodes the `Mutation` factor to human‑readable labels (`WT`, `V34A`, `S41A`, `V34A-S41A`, `F49A`).  
    - Performs one‑way ANOVA on `Contact.Score ~ Mutation` and, if significant, Tukey HSD post‑hoc tests.  
    - Produces a ggplot2 box‑and‑jitter plot of interface contact scores by mutation.  
  - Saves the final vector figure as:
    - **`MD_boxplot.svg`** – boxplot of total dimer interface contact scores (used as **Figure 3** in the manuscript).

### Typical workflow

1. **Generate RRCS scores for MD snapshots**  
   - Use `rrcs_complier.py` (or manually call `RRCS.py`) on all PDB snapshots in the MD folders to produce `*.cscore` files.
2. **Aggregate A–B interface scores**  
   - Run `total_rrcs_dimer_boxplot.py` to create `boxplot_data_II.csv` from the `.cscore` outputs.
3. **Analyze and plot**  
   - Run `interface_contact_score_boxplot.R` to perform ANOVA/Tukey tests and generate `MD_boxplot.svg` (Figure 3).
4. **Structural figure generation**  
   - Open `structural_visualization_adrb1_turkey.pse` in PyMOL and export `dimer_figure1B.png` (Figure 1B).


