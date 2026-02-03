# UCS654-assignment3
# TOPSIS Implementation
This repository contains an implementation of the TOPSIS
(Technique for Order Preference by Similarity to Ideal Solution) method.

### Part I: Command Line TOPSIS

### Description
A Python script that applies the TOPSIS algorithm on a CSV file and
generates a ranked result file.
### Usage
```bash
python topsis.py <input_file> <weights> <impacts> <output_file>
 ```
### Input
- CSV file with at least 3 columns
- First column: alternatives
- Remaining columns: numeric criteria values
### Output
CSV file with two additional columns:
- Topsis Score
- Rank
### Validations
- Correct number of arguments
- File existence check
- Numeric values validation
- Matching number of weights, impacts, and criteria
- Impacts must be + or -

### Part III: TOPSIS Web Application

### Description
A Flask-based web application that allows users to upload input data,
enter weights and impacts, and receive the TOPSIS result via email.
### Features
- CSV file upload
- Email format validation
- Weights and impacts validation
- Automatic TOPSIS computation
- Result file sent through email
