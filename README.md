# MetaboFlow - MS/MS Data Processing Pipeline

## Overview

MetaboFlow is a Python-based pipeline for processing and analyzing MS/MS (tandem mass spectrometry) data. The tool extracts MS2 spectra from .mzML files, performs basic spectral analysis, and outputs structured results in CSV format.

## Key Features

- **mzML File Processing**: Reads and processes mass spectrometry data in standard .mzML format
- **MS2 Spectrum Extraction**: Identifies and isolates MS2 spectra from raw data files
- **Spectral Analysis**: 
  - Precursor m/z values
  - Retention times
  - Peak counts
  - Base peak identification
  - Top 5 most intense peaks
- **CSV Output**: Generates structured, tabular output for easy downstream analysis

## Requirements

- Python 3.7+
- Required packages:
  - pyOpenMS (for mzML handling)
  - pandas (for data structuring)
  - matchms (for spectrum processing)
  - numpy

Install requirements with:
```bash
pip install pyopenms pandas matchms numpy
```

## Usage

1. **Configure Paths**: 
   - Modify `input_dir` and `output_dir` in the `analyze_msms_data()` function to point to your data directory and desired output location

2. **Run the Script**:
```bash
python MetaboFlow.py
```

3. **Output**:
   - The script creates CSV files in the output directory with naming convention: `[sample_name]_results.csv`
   - Each file contains processed spectral data for one input file

## Output Format

The generated CSV files contain the following columns:

| Column | Description |
|--------|-------------|
| precursor_mz | Precursor mass-to-charge ratio (m/z) |
| rt | Retention time (seconds) |
| num_peaks | Number of peaks in the spectrum |
| base_peak_mz | m/z of the most intense peak |
| base_peak_intensity | Intensity of the most intense peak |
| top_peaks | Semicolon-separated list of top 5 peaks (mz:intensity pairs) |

## Error Handling

The script includes comprehensive error handling and logging:
- Missing input directories are reported
- Files without MS2 spectra are flagged
- Individual file processing errors don't stop the entire pipeline
- Detailed logs are printed to console

## Customization

The `process_spectra()` function can be modified to include additional analysis steps such as:
- Spectral filtering
- Noise reduction
- Peak alignment
- Advanced feature extraction

## License

This project is open-source under the MIT License.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## Support

For issues or questions, please open an issue in the GitHub repository.
