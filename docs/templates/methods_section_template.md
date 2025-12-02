## Methods

### Data Collection
We retrieved 3,162 peer-reviewed articles on migraine research from the PubMed database (search conducted: [Date]). Search query: [Specify if known].

### Term Extraction and Categorization
Medical terms were extracted using a hybrid approach:
1.  **Metadata Extraction**: MeSH (Medical Subject Headings) and Author Keywords were processed.
2.  **NLP Text Mining**: Full abstract texts were analyzed using Unsupervised Machine Learning (YAKE algorithm) to identify high-value concepts missing from metadata.
3.  **Strict Filtering**: Terms underwent validation for length (3-20 chars), stopword removal, and medical relevance.

Extracted terms were categorized into four evidence-based domains:
1.  **Inducing Mechanisms** - Pathophysiological triggers (e.g., "Occipital Nerve", "Brainstem")
2.  **Associated Diseases** - Validated comorbid conditions (e.g., "Vestibular Migraine", "TTH")
3.  **Response Measures** - Therapeutic interventions (e.g., "CGRP Receptor", "TMS")
4.  **Social/Work Impact** - Quality of life outcomes (e.g., "Headache Days", "Emergency Department")

Categorization employed an enhanced keyword-based classification system with **300+ domain-specific medical terms**, refined through NLP discovery.

### Network Construction
A co-occurrence network was constructed where:
-   **Nodes** represent medical concepts (n=301)
-   **Edges** represent co-occurrence within same article (n=3,007)
-   Edge weights reflect co-occurrence frequency

Filtering criteria:
-   Minimum term frequency: 3 articles
-   Minimum co-occurrence: 2 articles

### Network Analysis
Network visualization and analysis performed using Gephi 0.10.1. Layout optimization via ForceAtlas 2 algorithm (repulsion: 5000, gravity: 25, prevent overlap enabled). 

Statistical analyses included:
- Modularity analysis (community detection)
- Betweenness centrality (hub identification)
- Network diameter and clustering coefficient

### Validation
Categorization accuracy validated through expert medical review ([Friend's name], neurology specialist). Inter-rater reliability: [Calculate from feedback].
