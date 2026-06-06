# lacli

Linear algebra in your CLI — yayo!

LAcli runs in your terminal and provides a set of linear algebra commands.
All operations are performed using [NumPy](https://github.com/numpy/numpy).

---

### I/O

You can set stdin and stdout to use files, pipes, or both in powerful combinations.

### Argument Parser 

The argument parser should be devided by commands, like BMO (basic matrix operations), checks, rotation, factorization and so on, 
Each command should be devided by single feature, so every final feature should be accessible via a command and not by direct access,
Nothing forbids to organize the command accesible feature in sub-commands and so on 

### Supported File Types

Hint: to support a very big number of filetype, instead to implement a complete parser or worse a huge library for any filetype, read the raw file, every time you encounter a number, consider that number a part of the matrix or the math object, and after based on the file type, delete the unusefull number, or something like that

**General Purpose**

| Format | Extensions |
|--------|------------|
| JSON | `.json` |
| CSV | `.csv` |

**Multidimensional & Big Data Formats**

| Format | Extensions | Description |
|--------|------------|-------------|
| Numpy | `.npy`,`.npz` | A simple format for saving numpy arrays to disk with the full information about them
| Matlab | `.mat` | The official matlab file format to store array and general purpose data
| HDF5 | `.h5`, `.hdf5` | Hierarchical Data Format. Essential for storing massive, highly complex, and multidimensional datasets |
| NetCDF | `.nc` | Network Common Data Form. Heavily utilized in atmospheric, oceanic, and meteorological sciences to store array-oriented scientific data |
| Matrix Market  | `.mtx` | The Matrix Market (MM) exchange formats provide a simple mechanism to facilitate the exchange of matrix data
| PyTorch | `.pt`, `.pth` | The official PyTorch format to store model weights and architecture
| GGML | `.ggml` | GGML is an open-source tensor library written in C and C++ designed for running machine learning models  
| GGUF | `.gguf` | GGUF (GPT-Generated Unified Format) is a highly popular file format designed to store and run large language models (LLMs)
| ONNX | `.onnx` | ONNX is an open format built to represent machine learning model

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

## TODO: 
[1] The first big step for the development of this project is to add the support for a cospicious number of format file, so you need to be able to compute some basic operation
[1] Implement the argument parser with the BSO command and some feature to test the file implementation
[2] Implement support for JSON
[3] Implement support for CSV

## Feature

### [0] Basic Matrix Operations
- [0.1] matrix mul (arbitrary dimensions)
- [0.2] matrix sum
- [0.3] matrix scalar mul
- [0.4] scalar dot product
- [0.5] scalar sum
- [0.6] inverse compute
- [0.7] transpose compute
- [0.8] rank compute

### [1] Checks
- [1.1] invertability check
- [1.2] vectors independence check
- [1.3] vectors orthogonality check
- [1.4] symmetric check
- [1.5] triangular check
- [1.6] positive definite check

### [2] Rotations
- [2.1] rotation matrix computation (input: matrix, angle, [axis], [center], [scale], [shear], [perspective])

### [3] Factorization
- [3.1] gauss-jordan elimination
- [3.2] LU decomposition
- [3.3] LDU decomposition
- [3.4] QR decomposition
- [3.5] Cholesky decomposition
- [3.6] orthogonal decomposition
- [3.7] SVD
- [3.8] eigenvalue decomposition

### [4] Least Squares
- [4.1] least squares
- [4.2] weighted least squares
- [4.3] least squares with regularization
- [4.4] regularization
- [4.5] linear regression

### [5] I/O Support
The support word below means support for input and output (read/write) in combinations between file format
- [5.1] support for JSON 
- [5.2] support for CSV 
- [5.3] support for CLI 
- [5.4] support for Parquet 
- [5.5] support for NetCDF 
- [5.6] support for FASTA/FASTQ 
- [5.7] support for HDF5 
- [5.8] support for SDF 
- [5.9] support for PDB 
- [5.10] support for Numpy 
- [5.11] support for Matlab 
- [5.12] support for GGML 
- [5.13] support for GGUF
- [5.14] support for ONNX
- [5.15] support for Matrix Market
- [5.16] support for PyTorch
