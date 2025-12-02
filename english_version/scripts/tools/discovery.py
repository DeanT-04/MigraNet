# PubMed_Gephi_Refined_v3_NLP.py - Advanced NLP Network Builder
# Uses YAKE for unsupervised keyword extraction from Abstracts

import pandas as pd
import re
import ast
from collections import defaultdict, Counter
import itertools
import os
import yake  # Requires: pip install yake


class PubMedNLPNetwork:
    def __init__(self):
        # Strict medical stopwords
        self.medical_stopwords = {
            "study",
            "studies",
            "research",
            "analysis",
            "effect",
            "effects",
            "patient",
            "patients",
            "group",
            "groups",
            "method",
            "methods",
            "result",
            "results",
            "conclusion",
            "conclusions",
            "objective",
            "background",
            "aim",
            "purpose",
            "significance",
            "review",
            "article",
            "paper",
            "their",
            "with",
            "the",
            "and",
            "or",
            "for",
            "from",
            "this",
            "that",
            "these",
            "those",
            "which",
            "what",
            "when",
            "where",
            "how",
            "why",
            "has",
            "have",
            "had",
            "was",
            "were",
            "is",
            "are",
            "be",
            "been",
            "being",
            "can",
            "could",
            "would",
            "should",
            "may",
            "might",
            "must",
            "author",
            "theory",
            "model",
            "system",
            "process",
            "approach",
            "perspective",
            "overview",
            "summary",
            "current",
            "future",
            "recent",
            "new",
            "novel",
            "various",
            "data",
            "using",
            "used",
            "found",
            "showed",
            "suggest",
            "associated",
            "clinical",
            "significant",
            "significantly",
            "compared",
            "control",
            "treatment",
            "year",
            "years",
        }

        # Categories (Same as V2)
        self.refined_categories = {
            "trigger_mechanisms": {
                "description": "Trigger Mechanisms",
                "keywords": [
                    "trigeminal",
                    "cortical spreading depression",
                    "sensitization",
                    "vascular",
                    "hormonal",
                    "estrogen",
                    "stress",
                    "inflammation",
                ],
            },
            "true_comorbidities": {
                "description": "True Comorbidities",
                "keywords": [
                    "depression",
                    "anxiety",
                    "epilepsy",
                    "stroke",
                    "fibromyalgia",
                    "insomnia",
                    "hypertension",
                ],
            },
            "social_impact": {
                "description": "Social Impact",
                "keywords": [
                    "quality of life",
                    "disability",
                    "productivity",
                    "cost",
                    "burden",
                    "stigma",
                ],
            },
            "interventions": {
                "description": "Interventions",
                "keywords": [
                    "triptans",
                    "cgrp",
                    "erenumab",
                    "botulinum",
                    "acupuncture",
                    "therapy",
                    "medication",
                ],
            },
        }

    def load_pubmed_data(self, file_path):
        try:
            return pd.read_csv(file_path, engine="python", on_bad_lines="skip")
        except Exception as e:
            print(f"Loading failed: {e}")
            return None

    def extract_yake_keywords(self, text):
        """Extract keywords using YAKE"""
        if pd.isna(text) or len(str(text)) < 50:
            return []

        # YAKE configuration
        language = "en"
        max_ngram_size = 2
        deduplication_threshold = 0.9
        numOfKeywords = 5

        kw_extractor = yake.KeywordExtractor(
            lan=language,
            n=max_ngram_size,
            dedupLim=deduplication_threshold,
            top=numOfKeywords,
            features=None,
        )
        keywords = kw_extractor.extract_keywords(text)

        # Filter keywords
        cleaned_keywords = []
        for kw, score in keywords:
            term = kw.lower()
            # Basic cleaning
            if len(term) < 3 or term in self.medical_stopwords:
                continue
            if any(sw in term.split() for sw in self.medical_stopwords):
                continue
            cleaned_keywords.append(kw.title())

        return cleaned_keywords

    def categorize_term(self, term):
        """Categorize a term based on keyword matching"""
        term_lower = term.lower()
        for cat, info in self.refined_categories.items():
            for kw in info["keywords"]:
                if kw in term_lower:
                    return cat
        return "unclassified"

    def build_nlp_network(self, df):
        print("Building NLP network (V3)...")
        print(f"Available columns: {df.columns.tolist()}")

        # Identify Abstract column
        abstract_col = None
        for col in ["Abstract", "Abstract Note", "Description", "Summary", "abstract", "Abstracts"]:
            if col in df.columns:
                abstract_col = col
                break

        if not abstract_col:
            print("WARNING: No Abstract column found!")
        else:
            print(f"Using abstract column: {abstract_col}")

        all_terms = []
        discovered_terms = Counter()

        for idx, row in df.iterrows():
            if idx % 100 == 0:
                print(f"Processing: {idx}/{len(df)}")

            abstract = ""
            if abstract_col:
                abstract = row.get(abstract_col, "")
            if pd.isna(abstract):
                continue

            # Extract terms using YAKE
            yake_terms = self.extract_yake_keywords(abstract)

            # Categorize
            article_terms = []
            for term in yake_terms:
                cat = self.categorize_term(term)
                if cat != "unclassified":
                    article_terms.append({"Label": term, "Category": cat})
                else:
                    discovered_terms[term] += 1

            if article_terms:
                all_terms.append(article_terms)

        # Build Nodes and Edges
        print("Constructing graph...")
        node_freq = Counter()
        edge_weights = defaultdict(int)

        for terms in all_terms:
            labels = [t["Label"] for t in terms]
            node_freq.update(labels)

            for t1, t2 in itertools.combinations(sorted(labels), 2):
                edge_weights[(t1, t2)] += 1

        # Filter
        min_freq = 5
        final_nodes = []
        seen_nodes = set()

        # Re-map categories for final nodes
        term_to_cat = {}
        for terms in all_terms:
            for t in terms:
                term_to_cat[t["Label"]] = t["Category"]

        for term, freq in node_freq.items():
            if freq >= min_freq:
                final_nodes.append(
                    {
                        "Id": re.sub(r"[^\w]", "_", term.lower()),
                        "Label": term,
                        "Category": term_to_cat.get(term, "unclassified"),
                        "Frequency": freq,
                    }
                )
                seen_nodes.add(term)

        final_edges = []
        for (t1, t2), w in edge_weights.items():
            if t1 in seen_nodes and t2 in seen_nodes and w >= 2:
                final_edges.append(
                    {
                        "Source": re.sub(r"[^\w]", "_", t1.lower()),
                        "Target": re.sub(r"[^\w]", "_", t2.lower()),
                        "Weight": w,
                        "Type": "Undirected",
                    }
                )

        return pd.DataFrame(final_nodes), pd.DataFrame(final_edges), discovered_terms


def main():
    converter = PubMedNLPNetwork()
    file_path = r"../../data/raw/PubMed.csv"

    if not os.path.exists(file_path):
        file_path = r"../data/raw/PubMed.csv"

    if not os.path.exists(file_path):
        print("Input file not found.")
        return

    df = converter.load_pubmed_data(file_path)
    nodes, edges, discovered = converter.build_nlp_network(df)

    output_dir = "../../data/discovery"
    if not os.path.exists("../../data"):
        output_dir = "../data/discovery"
    os.makedirs(output_dir, exist_ok=True)

    nodes.to_csv(os.path.join(output_dir, "nlp_nodes.csv"), index=False, encoding="utf-8-sig")
    edges.to_csv(os.path.join(output_dir, "nlp_edges.csv"), index=False, encoding="utf-8-sig")

    # Save discovered terms (potential new keywords)
    with open(os.path.join(output_dir, "discovered_terms.csv"), "w", encoding="utf-8") as f:
        f.write("Term,Frequency\n")
        for term, freq in discovered.most_common(100):
            f.write(f"{term},{freq}\n")

    print(f"Done! NLP Network: {len(nodes)} nodes, {len(edges)} edges.")
    print(f"Discovered {len(discovered)} potential new terms.")


if __name__ == "__main__":
    main()
