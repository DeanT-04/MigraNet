# Migraine Research Network Analysis - English Version

## 📌 Project Description

This is the **English version** of the Migraine Research Network Analysis project. All code comments and documentation are in English.

## 📂 Directory Structure

```
english_version/
├── README.md                    # This file - Project overview
├── scripts/                     # Scripts folder
│   ├── migraine_network_builder.py  # Main processing script
│   └── README.md               # Scripts documentation
├── data/                       # Data folder
│   ├── input/                  # Input data directory
│   │   └── README.md          # Input data instructions
│   ├── output/                 # Output results directory
│   │   └── README.md          # Output files documentation
│   └── README.md              # Data directory documentation
└── config/                     # Configuration folder
    ├── gephi_visualization_guide.txt  # Gephi visualization guide
    └── README.md              # Configuration documentation
```

## 🚀 Quick Start

### 1. Prepare Data
Place your PubMed exported CSV file into the `data/input/` directory

### 2. Run Script
```bash
python scripts/migraine_network_builder.py
```

### 3. View Results
Generated network files are located in the `data/output/` directory

### 4. Gephi Visualization
- Import `gephi_refined_nodes.csv` and `gephi_refined_edges.csv`
- Follow the layout settings in `config/gephi_visualization_guide.txt`

## 📊 Project Overview

- **Node Count**: 238 medical terms
- **Edge Count**: 863 co-occurrence relationships
- **Category System**: 4 main categories (Trigger Mechanisms, True Comorbidities, Social Impact, Interventions)

## 📖 Detailed Documentation

Please check the README.md files in each subdirectory for detailed information.

## 👥 Users

This version is for English-speaking users and collaborators.

## 🔄 Differences from Chinese Version

- All comments translated to English
- Documentation in English
- Same functionality and output
- Identical data structure
