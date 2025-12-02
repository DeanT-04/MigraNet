<!-- Navigation: [🏠 Home](../../README.md) | [📖 Optimization Guide](COMPLETE_OPTIMIZATION_GUIDE.md) | [📊 Project Overview](PROJECT_OVERVIEW.md) -->

# 🧹 Cleaning & Extraction Method Comparison

This document details the differences in data cleaning, term extraction, and categorization logic between the three versions of the Migraine Network Builder.

## 📊 Quick Comparison Table

| Feature | **Version 1 (Original)** | **Version 2 (Refined & Expanded)** | **Version 3 (NLP Discovery)** |
| :--- | :--- | :--- | :--- |
| **Primary Goal** | Create a clean, noise-free network from MeSH tags. | Maximize coverage by including Abstract text and Author Keywords. | Discover *new* hidden terms using Unsupervised Machine Learning. |
| **Data Sources** | `Manual Tags` column only. | `Manual Tags`, `Abstract Note`, `Keywords`. | `Abstract Note` column only. |
| **Extraction Method** | Direct string splitting & cleaning. | Hybrid: Direct cleaning + Contextual keyword search in abstracts. | **YAKE Algorithm** (Unsupervised Keyword Extraction). |
| **Cleaning Logic** | **Strict**: Regex removal, length limits (3-20), stopword filtering. | **Strict**: Same as V1 (ensures consistency). | **Heuristic**: YAKE scoring + basic stopword/length filtering. |
| **Categorization** | Fixed keyword lists (Manual). | **Expanded** keyword lists (Manual + NLP-discovered terms). | Fixed keyword lists (used to classify discovered terms). |
| **Output Quality** | High precision, lower recall (misses terms not in tags). | **High precision, High recall** (captures terms mentioned in text). | High recall, lower precision (good for discovery, noisy for final graph). |

---

## 🔍 Detailed Breakdown

### 1. Version 1: `migraine_network_builder.py`
**"The Strict Filter"**

*   **Philosophy:** Trust the manual tags (MeSH), but clean them aggressively to remove noise.
*   **Cleaning Process (`strict_term_cleaning`):**
    1.  **Sanitization:** Removes special markers like `*` (major topic), `[]` (brackets), and `()` (parentheses).
    2.  **Normalization:** Converts to lowercase and splits into words.
    3.  **Filtration Loop:**
        *   **Length:** Discards words < 3 or > 20 characters.
        *   **Stopwords:** Checks against a hardcoded list of 60+ medical/academic stopwords (e.g., "study", "effect", "patient").
        *   **Content:** Discards numbers and words with special characters.
    4.  **Formatting:** Re-joins valid words and converts to Title Case.
*   **Limitation:** If a concept like "Vestibular Migraine" wasn't explicitly tagged by a librarian in the `Manual Tags` column, it was **completely ignored**, even if the entire paper was about it.

### 2. Version 2: `migraine_network_builder_v2.py`
**"The Comprehensive Hybrid" (Current Best)**

*   **Philosophy:** Trust the tags, but *verify* and *augment* with the actual text.
*   **Key Improvement:** It looks at the **Abstract** and **Author Keywords**.
*   **Extraction Logic:**
    *   It runs the same `strict_term_cleaning` on the tags.
    *   **PLUS:** It scans the full `Abstract` text for specific high-value keywords.
    *   *Example:* If the abstract says "...patients with **vestibular migraine** showed...", the script detects "vestibular migraine" (because we added it to the keyword list) and adds it as a node, even if the tag is missing.
*   **Categorization Update:**
    *   The keyword lists were updated with terms discovered by Version 3 (see below), such as *Occipital Nerve*, *Cluster Headache*, and *CGRP Receptor*.

### 3. Version 3: `migraine_network_builder_v3_nlp.py`
**"The Miner"**

*   **Philosophy:** Don't assume we know all the important terms. Let the data speak.
*   **Method:** Uses **YAKE (Yet Another Keyword Extractor)**, an unsupervised statistical algorithm.
*   **Process:**
    1.  Reads the raw `Abstract` text.
    2.  YAKE calculates a score for every phrase based on:
        *   Casing
        *   Position in sentence
        *   Frequency
        *   Context
    3.  **Cleaning:** Less aggressive than V1/V2. It relies on YAKE's scoring to filter noise, plus a basic check for length and stopwords.
*   **Purpose:** This script was used to **generate the "Discovered Terms" list**. It found 5,000+ candidates. We manually reviewed the top ones (like "Headache Days", "Emergency Department") and added them to Version 2's logic.

---

## 🏆 Recommendation

*   **For your Final Paper/Graph:** Use **Version 2**. It combines the cleanliness of V1 with the coverage of V3's discoveries.
*   **For Future Research:** Run **Version 3** if you get a new batch of papers and want to see if *new* topics are emerging that you haven't defined yet.
---

## 📚 Related Documentation

- **[🏠 Home](../../README.md)** — Main project page
- **[📖 Complete Guide](../guides/COMPLETE_OPTIMIZATION_GUIDE.md)** — Step-by-step instructions  
- **[📊 Project Overview](../guides/PROJECT_OVERVIEW.md)** — Technical architecture
- **[🧹 Method Comparison](../guides/CLEANING_METHOD_COMPARISON.md)** — Script versions explained
- **[📈 Analysis Log](../reports/network_analysis_log.md)** — Results history

---

*Need help? Check the [main README](../../README.md) or open an issue.*
