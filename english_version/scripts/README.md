# Scripts Documentation

## 📄 File List

### `migraine_network_builder.py`
Main data processing and network construction script

## 🔧 Functionality

### Core Class: `PubMedRefinedNetwork`

#### Main Methods:

1. **`load_pubmed_data(file_path)`**
   - Function: Load PubMed CSV data
   - Supports multiple encoding formats (UTF-8, Latin-1, CP1252)
   - Auto-detects delimiters

2. **`strict_term_cleaning(term)`**
   - Function: Strict medical term cleaning
   - Removes stopwords (66 common medical research terms)
   - Filters special characters and invalid terms
   - Standardizes format

3. **`precise_categorization(term)`**
   - Function: Precisely categorize medical terms
   - Four main categories:
     - Trigger Mechanisms (trigger_mechanisms)
     - True Comorbidities (true_comorbidities)
     - Social Impact (social_impact)
     - Interventions (interventions)

4. **`build_refined_network(df, min_frequency, min_weight)`**
   - Function: Build refined network
   - Parameters:
     - `min_frequency`: Minimum term frequency threshold (default 3)
     - `min_weight`: Minimum edge weight threshold (default 2)
   - Output: DataFrames for nodes and edges

## 🎯 Usage

### Basic Execution:
```python
python migraine_network_builder.py
```

### Modify Input File Path:
Update line 337 in the script with your file path:
```python
file_path = r"data/input/PubMed.csv"
```

### Adjust Filtering Thresholds:
Modify parameters on line 354:
```python
nodes_df, edges_df = converter.build_refined_network(
    df, 
    min_frequency=3,  # Adjust minimum frequency
    min_weight=2      # Adjust minimum weight
)
```

## 📊 Output Files

The script generates the following files in the data source directory:
- `gephi_refined_nodes.csv` - Gephi node file
- `gephi_refined_edges.csv` - Gephi edge file
- `detailed_refined_nodes.csv` - Detailed node data
- `detailed_refined_edges.csv` - Detailed edge data

## ⚙️ Configuration Parameters

### Medical Stopword List:
66 common medical research terms (study, research, patient, etc.)

### Category Keywords:
- Trigger Mechanisms: 150+ keywords
- True Comorbidities: Neurological, psychiatric, pain conditions
- Social Impact: Quality of life, economic burden
- Interventions: Pharmacological and non-pharmacological treatments

## 🐛 Troubleshooting

### Common Issues:

1. **File Reading Failure**
   - Check if the file path is correct
   - Verify CSV file encoding format

2. **Too Few Nodes**
   - Lower the `min_frequency` threshold
   - Check data quality

3. **Too Many Edges**
   - Increase the `min_weight` threshold
   - Consider adding more term filtering rules

## 📝 Important Notes

- Ensure input CSV file contains "Manual Tags" column
- Script automatically handles various CSV formats
- Generated files use UTF-8-sig encoding for international support
- Relative paths are used for cross-platform compatibility
