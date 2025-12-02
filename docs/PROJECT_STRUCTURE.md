# 📁 Project Structure

```
migraine-network-analysis/
│
├── 📘 docs/                                # Documentation Hub
│   ├── guides/
│   │   ├── COMPLETE_OPTIMIZATION_GUIDE.md  # Master implementation plan
│   │   ├── CLEANING_METHOD_COMPARISON.md   # Version comparison (V1/V2/V3)
│   │   └── PROJECT_OVERVIEW.md             # Technical architecture
│   │
│   ├── reports/
│   │   ├── network_analysis_log.md         # Analysis history
│   │   ├── CLEANUP_SUMMARY.md              # File organization log
│   │   └── ORGANIZATION_SUMMARY.md         # Directory restructuring
│   │
│   └── templates/
│       ├── friend_review_template.md       # Expert validation form
│       ├── keyword_refinement_plan.md      # Term improvement template
│       ├── methods_section_template.md     # Paper draft (Methods)
│       └── results_section_template.md     # Paper draft (Results)
│
├── 💻 english_version/                     # Main Codebase
│   ├── scripts/
│   │   ├── main.py                         # ⭐ PRIMARY SCRIPT (Run this!)
│   │   ├── archive/
│   │   │   └── legacy_v1.py                # Original version (archived)
│   │   └── tools/
│   │       └── discovery.py                # NLP keyword discovery tool
│   │
│   ├── data/
│   │   ├── raw/
│   │   │   └── PubMed.csv                  # Your input data goes here
│   │   └── processed/
│   │       ├── gephi_nodes.csv             # Import to Gephi
│   │       ├── gephi_edges.csv             # Import to Gephi
│   │       ├── detailed_nodes.csv          # Full node metadata
│   │       └── detailed_edges.csv          # Full edge metadata
│   │
│   ├── config/
│   │   └── gephi_visualization_guide.txt   # Gephi settings
│   │
│   ├── venv/                               # Virtual environment (gitignored)
│   ├── requirements.txt                    # Python dependencies
│   └── README.md                           # Version-specific notes
│
├── 🌐 chinese_version/                     # Localized Version
│   └── [Similar structure to english_version]
│
├── .gitignore                              # Git exclusions
├── requirements.txt                        # Main Python dependencies
└── README.md                               # ⭐ START HERE!
```

## 🗂️ Quick Navigation

- **Getting Started**: [`README.md`](../README.md)
- **Run the Analysis**: [`english_version/scripts/main.py`](../english_version/scripts/main.py)
- **Results**: [`english_version/data/processed/`](../english_version/data/processed/)
- **Guides**: [`docs/guides/`](guides/)
