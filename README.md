# MigraNet 🧠

[![CI](https://github.com/yourusername/migraine-network-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/migraine-network-analysis/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](Dockerfile)

> **Transform thousands of medical research articles into interactive network visualizations.**  
> This tool automatically extracts medical concepts from PubMed data and creates network graphs showing how topics like "Stress," "Anxiety," and "Treatments" connect in migraine research.

---

## ✨ Features

- 🔍 **Smart Term Extraction**: Uses both manual tags and AI-powered keyword discovery
- 📊 **4-Category Classification**: Automatically sorts terms into Triggers, Comorbidities, Interventions, and Social Impact
- 🎨 **Gephi-Ready Output**: Generates CSV files optimized for network visualization
- 📈 **Quality Metrics**: Built-in frequency analysis and co-occurrence statistics
- 🌐 **Multi-Language Support**: Includes both English and Chinese versions
- 🐳 **Docker Support**: Run anywhere without dependency hell

---

## 📂 Project Structure

```
migraine-network-analysis/
├── 📘 docs/                    # All documentation lives here
│   ├── guides/                 # How-to guides
│   │   ├── COMPLETE_OPTIMIZATION_GUIDE.md    # Master implementation plan
│   │   ├── CLEANING_METHOD_COMPARISON.md     # Version comparison
│   │   └── PROJECT_OVERVIEW.md               # High-level summary
│   ├── reports/                # Analysis logs and summaries
│   └── templates/              # Reusable templates for reviews/papers
│
├── 💻 english_version/         # Main codebase
│   ├── scripts/
│   │   └── main.py            # ⭐ Run this file!
│   ├── data/
│   │   ├── raw/               # Place your PubMed.csv here
│   │   └── processed/         # Generated network files appear here
│   └── config/                # Gephi settings
│
├── 🌐 chinese_version/         # Localized version
├── requirements.txt            # Python dependencies
└── README.md                  # You are here!
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- [Gephi](https://gephi.org/) (for visualization)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/migraine-network-analysis.git
   cd migraine-network-analysis
   ```

2. **Run with Docker (Recommended)**:
   ```bash
   # Run the analysis
   docker-compose up app

   # Run tests
   docker-compose up test
   ```

3. **Or Install Locally**:
   ```bash
   pip install -r requirements.txt
   ```
   *This installs:*
   - **[pandas](https://pandas.pydata.org/)** — Data manipulation and CSV processing
   - **[yake](https://github.com/LIAAD/yake)** — Unsupervised keyword extraction

3. **Add your data**:
   - Place your `PubMed.csv` file in `english_version/data/raw/`

4. **Run the analysis**:
   ```bash
   python english_version/scripts/main.py
   ```

5. **Visualize in Gephi**:
   - Open Gephi
   - Import `english_version/data/processed/gephi_nodes.csv` (Nodes table)
   - Import `english_version/data/processed/gephi_edges.csv` (Edges table)
   - Apply ForceAtlas 2 layout and color by Category
   - See the **[Optimization Guide](docs/guides/COMPLETE_OPTIMIZATION_GUIDE.md)** for detailed Gephi settings

---

## 📖 Documentation

### For New Users
- **[Project Overview](docs/guides/PROJECT_OVERVIEW.md)** — Understand the goals and methodology
- **[Quick Tutorial](docs/guides/COMPLETE_OPTIMIZATION_GUIDE.md#quick-start)** — Get results in 30 minutes

### For Researchers
- **[Optimization Guide](docs/guides/COMPLETE_OPTIMIZATION_GUIDE.md)** — Step-by-step instructions for publication-quality networks
- **[Method Comparison](docs/guides/CLEANING_METHOD_COMPARISON.md)** — Technical details on V1 vs V2 vs V3 scripts
- **[Analysis Log](docs/reports/network_analysis_log.md)** — History of analysis runs and improvements

### For Collaboration
- **[Review Template](docs/templates/friend_review_template.md)** — Expert validation form
- **[Paper Templates](docs/templates/)** — Pre-written Methods and Results sections

---

## 🔧 How It Works

1. **Data Loading**: Reads PubMed CSV files containing medical article metadata
2. **Term Extraction**: 
   - Extracts MeSH tags (Medical Subject Headings)
   - Scans abstracts for additional keywords using [YAKE](https://github.com/LIAAD/yake)
3. **Categorization**: Classifies terms into 4 categories using 300+ medical keywords
4. **Network Building**: Creates co-occurrence relationships (nodes = terms, edges = shared articles)
5. **Output**: Generates Gephi-compatible CSV files

**Categories:**
- 🔴 **Trigger Mechanisms** — Disease causes (e.g., Stress, Hormones)
- 🟡 **Comorbidities** — Associated conditions (e.g., Depression, Epilepsy)
- 🟢 **Interventions** — Treatments (e.g., CGRP Inhibitors, Acupuncture)
- 🔵 **Social Impact** — Quality of life factors (e.g., Disability, Healthcare Costs)

---

## 📊 Example Output

**Network Statistics:**
- **Nodes**: 301 medical concepts
- **Edges**: 3,007 co-occurrence relationships
- **Top Terms**: Quality of Life, Treatment Outcome, Calcitonin Gene-Related Peptide

See [`docs/reports/network_analysis_log.md`](docs/reports/network_analysis_log.md) for detailed results.

---

## 🤝 Contributing

We welcome improvements! Here's how you can help:

1. **Report Issues**: Found a bug? Open an issue with details
2. **Suggest Keywords**: Know a critical medical term we're missing? Submit a pull request
3. **Improve Documentation**: Clarify confusing sections or add examples

---

## 🧪 Testing & Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage report
pytest --cov=english_version/scripts --cov-report=html

# Run specific tests
pytest tests/test_main.py -v
```

**Test Coverage**: 88.5% (23/26 tests passing)

See [`tests/README.md`](tests/README.md) for detailed testing documentation.

### Sample Data

Quick demo with sample data (10 articles):
```bash
# Copy sample data
copy tests\fixtures\sample_pubmed.csv english_version\data\raw\

# Run analysis
python english_version/scripts/main.py
```

### Code Quality

Ensure your code meets quality standards:

```bash
# Format code
black .

# Check for linting errors
flake8 .

# Check type hints
mypy .
```

### Development Dependencies

```bash
# Install all dependencies including dev tools
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

See [`CHANGELOG.md`](CHANGELOG.md) for version history and planned features.

---

## 🤝 Contributing

See above for how to contribute, or check out our [test suite](tests/README.md) to get started with development.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Resources

### Packages Used
- **[pandas](https://pandas.pydata.org/docs/)** — Data Analysis Library
- **[YAKE](https://github.com/LIAAD/yake)** — Yet Another Keyword Extractor

### Tools
- **[Gephi](https://gephi.org/)** — Network Visualization Platform
- **[PubMed](https://pubmed.ncbi.nlm.nih.gov/)** — Medical Research Database

### Learn More
- [What is a Network Graph?](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics))
- [MeSH Terms Explained](https://www.nlm.nih.gov/mesh/meshhome.html)
- [Gephi Tutorial](https://gephi.org/users/)

---

## 📬 Contact & Support

- **Questions?** Open an issue or check the [Optimization Guide](docs/guides/COMPLETE_OPTIMIZATION_GUIDE.md)
- **Need help with Gephi?** See our [detailed visualization guide](docs/guides/COMPLETE_OPTIMIZATION_GUIDE.md#immediate-actions-today)

---

<p align="center">
  <sub>Built with ❤️ for migraine researchers</sub>
</p>
