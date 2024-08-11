# Shape Processing and Regularization

## Overview

This project processes and regularizes polylines from a CSV file. It involves reading polylines, performing shape checking, removing outliers, regularizing curves, checking for symmetry.

## Requirements

- Python 3.x
- Required libraries: `numpy`

## Files

- `main.py`: Main script for processing polylines.
- `io_process.py`: Handles reading from CSV and plotting functions.
- `checking_shapes.py`: Contains shape checking functionalities.
- `make_curve.py`: Generates curves for identified shapes.
- `regularization.py`: Contains functions for outlier removal and regularization.
- `symmetry.py`: Functions for symmetry checking.

## Usage

### Prepare Your Environment

Make sure you have Python 3.x installed and the required libraries. You may need to install them via pip if they are not already available.

### CSV Files

Place your CSV files in the `problems` directory. The script currently uses `isolated.csv` by default, but you can uncomment other files to use them.

### Running the Script

Run the `main.py` script to process the polylines. The script will read the CSV file, process the polylines, and plot the results.

```bash
python main.py
```