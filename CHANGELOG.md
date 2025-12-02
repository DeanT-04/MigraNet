# Changelog

All notable changes to the Migraine Network Analysis project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite with pytest
- Sample data for quick demonstrations
- MIT LICENSE file
- This CHANGELOG file
- Complete dependency specification (pandas, yake, numpy)
- GitHub-ready project structure

### Changed
- Updated all Python scripts to use correct data paths (`data/raw/` instead of `data/input/`)
- Fixed Unicode encoding issues for Windows compatibility
- Synchronized requirements.txt across root and english_version directories

### Fixed
- Path resolution issues in discovery.py and legacy_v1.py
- Emoji encoding errors in legacy script output

---

## [2.0.0] - 2025-12-02

### Added
- **V2 Main Script** (`english_version/scripts/main.py`) - Enhanced with abstract processing
- **Discovery Tool** (`english_version/scripts/tools/discovery.py`) - NLP-powered keyword extraction using YAKE
- Multi-field term extraction from Manual Tags, Author Keywords, and Abstracts
- Automated categorization into 4 medical categories
- Dedicated output directories for different analysis versions:
  - `data/processed/` - Main V2 output
  - `data/discovery/` - NLP discovery output
  - `data/archive/` - Legacy V1 output

### Changed
- Expanded medical stopwords list for better term filtering
- Improved category keywords based on research framework
- Network density now calculated and reported in analysis
- Minimum frequency threshold set to 3, minimum edge weight to 2

### Performance
- Processes 3,162 PubMed articles in ~10-15 seconds
- Generates 301 nodes and 3,007 edges (V2)
- Discovery tool identifies 5,658 potential new medical terms

---

## [1.0.0] - Initial Release

### Added
- **V1 Legacy Script** (`english_version/scripts/archive/legacy_v1.py`) - Original implementation
- Basic network construction from PubMed CSV data
- Manual MeSH tag processing
- Four-category medical classification system:
  - Trigger Mechanisms (neural, vascular, hormonal, inflammatory)
  - True Comorbidities (psychiatric, neurological, pain conditions)
  - Social Impact (disability, costs, quality of life)
  - Interventions (medications, therapies, lifestyle)
- Gephi-compatible CSV output (nodes and edges)
- Detailed metadata files for downstream analysis
- Chinese version with localized documentation

### Features
- Strict term cleaning with medical stopword filtering
- Co-occurrence edge weight calculation
- Frequency-based node filtering
- Comprehensive analysis reports with top terms and statistics
- Network density calculations
- Gephi visualization guide with recommended settings

---

## Version History Summary

| Version | Date       | Description                           | Nodes | Edges  |
|---------|------------|---------------------------------------|-------|--------|
| 2.0.0   | 2025-12-02 | Abstract processing + NLP discovery   | 301   | 3,007  |
| 1.0.0   | 2025-11-XX | Initial release (Manual tags only)    | 237   | 862    |

---

## Future Roadmap

### Planned Features
- [ ] Automated testing with pytest and coverage reporting
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Docker containerization for reproducibility
- [ ] Web interface for interactive network exploration
- [ ] API for programmatic access
- [ ] Additional language support beyond English/Chinese
- [ ] Integration with more biomedical databases (MEDLINE, Scopus)
- [ ] Machine learning-based category prediction
- [ ] Time-series analysis of research trends
- [ ] Citation network integration

### Under Consideration
- [ ] Jupyter notebook tutorials
- [ ] ReadTheDocs documentation site
- [ ] Performance optimizations for larger datasets (10K+ articles)
- [ ] Graph database backend (Neo4j)
- [ ] Real-time collaboration features

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
