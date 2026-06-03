# lacli

Linear algebra in your CLI — yayo!

LAcli runs in your terminal and provides a set of linear algebra commands.
All operations are performed using [NumPy](https://github.com/numpy/numpy).

---

## I/O

You can set stdin and stdout to use files, pipes, or both in powerful combinations.

### Supported File Types

**General Purpose**

| Format | Extensions |
|--------|------------|
| JSON | `.json` |
| CSV | `.csv` |

**Multidimensional & Big Data Formats**

| Format | Extensions | Description |
|--------|------------|-------------|
| HDF5 | `.h5`, `.hdf5` | Hierarchical Data Format. Essential for storing massive, highly complex, and multidimensional datasets |
| NetCDF | `.nc` | Network Common Data Form. Heavily utilized in atmospheric, oceanic, and meteorological sciences to store array-oriented scientific data |

**Bioinformatics & Genomics**

| Format | Extensions | Description |
|--------|------------|-------------|
| FASTA/FASTQ | `.fasta`, `.fastq` | Industry standards for genomic data |
| BAM/SAM | `.bam`, `.sam` | Compressed binary formats used to store sequence alignments mapped to a reference genome |

**Chemistry & Material Science**

| Format | Extensions | Description |
|--------|------------|-------------|
| PDB | `.pdb` | Protein Data Bank. Used to store 3D structural data for biological macromolecules, such as proteins and nucleic acids |
| SDF | `.sdf` | Structure Data File. Contains chemical structures and associated tabular or numerical properties |

**Tabular Data & Statistics**

| Format | Extensions | Description |
|--------|------------|-------------|
| Parquet | `.parquet` | Highly efficient, columnar storage used extensively in data science |

---

## Roadmap

### [0] Basic Matrix Operations

- [0.1] matrix mul (arbitrary dimensions)
- [0.2] matrix add
- [0.3] matrix scalar mul
- [0.4] scalar dot product
- [0.5] scalar add
- [0.6] add inverse compute
- [0.7] add transpose compute
- [0.8] add rank compute

### [1] Checks

- [1.1] add invertability check
- [1.2] add vectors independence check
- [1.3] add vectors orthogonality check
- [1.4] add symmetric check
- [1.5] add triangular check
- [1.6] add positive definite check

### [2] Rotations

- [2.1] add rotation matrix computation (input: matrix, angle, [axis], [center], [scale], [shear], [perspective])

### [3] Factorization

- [3.1] add gauss-jordan elimination
- [3.2] add LU decomposition
- [3.3] add LDU decomposition
- [3.4] add QR decomposition
- [3.5] add Cholesky decomposition
- [3.6] add orthogonal decomposition
- [3.7] add SVD
- [3.8] add eigenvalue decomposition

### [4] Least Squares

- [4.1] add least squares
- [4.2] add weighted least squares
- [4.3] add least squares with regularization
- [4.4] add regularization
- [4.5] add linear regression

### [5] I/O Support

- [5.1] Add support for JSON input and output
- [5.2] Add support for CSV input and output
- [5.3] Add support for CLI input and output
