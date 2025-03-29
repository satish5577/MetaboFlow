import os
import logging
from pathlib import Path
from pyopenms import *
import matchms
from datetime import datetime
import pandas as pd  
import numpy as np  

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def analyze_msms_data():
    try:
        # Configuration - UPDATE THESE PATHS
        input_dir = Path(r"F:/Masshunter/Data/16032024_POS_C18/mzml")
        output_dir = Path(r"F:/Masshunter/Data/16032024_POS_C18/mzml/MS")
        
        # Verify paths
        if not input_dir.exists():
            logger.error(f"Input directory not found: {input_dir}")
            return
        
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output will be saved to: {output_dir}")

        # Process files
        mzml_files = list(input_dir.glob("*.mzML"))
        if not mzml_files:
            logger.error("No .mzML files found in input directory")
            return

        logger.info(f"Found {len(mzml_files)} .mzML files to process")

        # Process each file
        for mzml_file in mzml_files:
            logger.info(f"\n{'='*50}\nProcessing: {mzml_file.name}\n{'='*50}")
            
            try:
                # 1. Load file
                start_time = datetime.now()
                exp = MSExperiment()
                MzMLFile().load(str(mzml_file), exp)  # Convert Path to string for OpenMS
                logger.info(f"Loaded {exp.size()} spectra in {(datetime.now()-start_time).total_seconds():.2f}s")

                # 2. Extract MS2 spectra
                ms2_spectra = [s for s in exp if s.getMSLevel() == 2]
                logger.info(f"Found {len(ms2_spectra)} MS2 spectra")

                if not ms2_spectra:
                    continue

                # 3. Process spectra (add your analysis here)
                process_spectra(ms2_spectra, output_dir, mzml_file.stem)

            except Exception as e:
                logger.error(f"Error processing {mzml_file.name}: {str(e)}", exc_info=True)
                continue

        logger.info("\nProcessing completed successfully!")

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)

def process_spectra(spectra, output_dir, sample_name):
    """Example processing function - customize this"""
    output_file = output_dir / f"{sample_name}_results.txt"
    
    with open(output_file, 'w') as f:
        f.write(f"Results for {sample_name}\n")
        f.write("="*30 + "\n")
        
        for i, spec in enumerate(spectra[:10]):  # Only process first 10 for demo
            if spec.getPrecursors():
                precursor_mz = spec.getPrecursors()[0].getMZ()
                rt = spec.getRT()
                peaks = spec.get_peaks()
                
                f.write(f"Spectrum {i+1} - Precursor: {precursor_mz:.4f} m/z, RT: {rt:.2f} s\n")
                f.write(f"Found {len(peaks[0])} peaks\n\n")
    
    logger.info(f"Saved results to {output_file}")
def process_spectra(spectra, output_dir, sample_name):
    """Enhanced processing with MS2 analysis"""
    results = []
    
    for spec in spectra:
        if spec.getPrecursors():
            precursor_mz = spec.getPrecursors()[0].getMZ()
            rt = spec.getRT()
            mz, intensities = spec.get_peaks()
            
            # Basic MS2 analysis
            top5_peaks = sorted(zip(mz, intensities), 
                             key=lambda x: x[1], reverse=True)[:5]
            
            results.append({
                "precursor_mz": precursor_mz,
                "rt": rt,
                "num_peaks": len(mz),
                "base_peak_mz": top5_peaks[0][0],
                "base_peak_intensity": top5_peaks[0][1],
                "top5_peaks": ";".join(f"{mz:.4f}:{intensity:.1f}" 
                                    for mz, intensity in top5_peaks)
            })
    
    # Save as CSV
    df = pd.DataFrame(results)
    output_file = output_dir / f"{sample_name}_results.csv"
    df.to_csv(output_file, index=False)
    logger.info(f"Saved detailed results to {output_file}")
def process_spectra(spectra, output_dir, sample_name):
    """Enhanced processing with MS2 analysis"""
    results = []
    
    for spec in spectra:
        if not spec.getPrecursors():
            continue
            
        precursor_mz = spec.getPrecursors()[0].getMZ()
        rt = spec.getRT()
        mz, intensities = spec.get_peaks()
        
        # Skip empty spectra
        if len(mz) == 0:
            continue
            
        # Basic MS2 analysis with safe peak handling
        try:
            peak_pairs = list(zip(mz, intensities))
            peak_pairs_sorted = sorted(peak_pairs, key=lambda x: x[1], reverse=True)
            top_peaks = peak_pairs_sorted[:min(5, len(peak_pairs_sorted))]
            
            results.append({
                "precursor_mz": precursor_mz,
                "rt": rt,
                "num_peaks": len(mz),
                "base_peak_mz": top_peaks[0][0] if len(top_peaks) > 0 else 0,
                "base_peak_intensity": top_peaks[0][1] if len(top_peaks) > 0 else 0,
                "top_peaks": ";".join(f"{mz:.4f}:{intensity:.1f}" 
                                   for mz, intensity in top_peaks)
            })
        except Exception as e:
            logger.warning(f"Skipping spectrum due to error: {str(e)}")
            continue
    
    # Only save if we have results
    if results:
        df = pd.DataFrame(results)
        output_file = output_dir / f"{sample_name}_results.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"Saved detailed results to {output_file}")
    else:
        logger.warning(f"No valid spectra found for {sample_name}")

def analyze_msms_data():
    try:
        input_dir = Path(r"F:\Masshunter\Data\16032024_POS_C18\mzml")
        output_dir = Path(r"F:\Masshunter\Data\16032024_POS_C18\mzml\Results")
        
        if not input_dir.exists():
            logger.error(f"Input directory not found: {input_dir}")
            return
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        mzml_files = list(input_dir.glob("*.mzML"))
        if not mzml_files:
            logger.error("No .mzML files found")
            return

        for mzml_file in mzml_files:
            logger.info(f"\n{'='*50}\nProcessing: {mzml_file.name}\n{'='*50}")
            
            try:
                exp = MSExperiment()
                MzMLFile().load(str(mzml_file), exp)
                ms2_spectra = [s for s in exp if s.getMSLevel() == 2]
                logger.info(f"Found {len(ms2_spectra)} MS2 spectra")
                
                if ms2_spectra:
                    process_spectra(ms2_spectra, output_dir, mzml_file.stem)
                else:
                    logger.warning("No MS2 spectra found in file")
                
            except Exception as e:
                logger.error(f"Error processing {mzml_file.name}: {str(e)}")

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        
if __name__ == "__main__":
    logger.info("Starting MS/MS data analysis")
    analyze_msms_data()
    