# PubMed_Gephi_Refined_v2.py - Advanced PubMed Network Builder
# Includes Abstract and Author Keywords processing for higher accuracy

import pandas as pd
import re
from collections import defaultdict, Counter
import itertools
import os
from typing import List, Tuple, Optional, Any


class PubMedRefinedNetworkV2:
    def __init__(self) -> None:
        # Strict medical stopwords (extensively expanded)
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
        }

        # Precise category system based on research framework
        self.refined_categories = {
            # 1. Trigger Mechanisms (strictly defined)
            "trigger_mechanisms": {
                "description": "Trigger Mechanisms",
                "keywords": [
                    # Neural mechanisms
                    "trigeminal",
                    "trigeminovascular",
                    "cortical spreading depression",
                    "central sensitization",
                    "neurogenic inflammation",
                    "neural mechanism",
                    # Vascular mechanisms
                    "vascular",
                    "cerebral blood flow",
                    "vasodilation",
                    "vasoconstriction",
                    # Hormonal mechanisms
                    "hormonal",
                    "estrogen",
                    "progesterone",
                    "menstrual",
                    "menopause",
                    # Inflammatory mechanisms
                    "inflammatory",
                    "cytokines",
                    "neuroinflammation",
                    "mast cells",
                    # Environmental triggers
                    "stress",
                    "sleep deprivation",
                    "weather",
                    "barometric",
                    "light sensitivity",
                    # NLP Discovered
                    "occipital nerve",
                    "vestibular",
                    "brainstem",
                ],
            },
            # 2. True Comorbidities (strict medical definitions)
            "true_comorbidities": {
                "description": "True Comorbidities",
                "keywords": [
                    # Psychiatric conditions
                    "depression",
                    "anxiety",
                    "panic disorder",
                    "bipolar",
                    "ptsd",
                    # Neurological conditions
                    "epilepsy",
                    "stroke",
                    "restless legs",
                    "parkinson",
                    "alzheimer",
                    # Pain conditions
                    "fibromyalgia",
                    "chronic pain",
                    "neuropathic pain",
                    # Autoimmune/Allergic conditions
                    "allergic rhinitis",
                    "asthma",
                    "irritable bowel",
                    "inflammatory bowel",
                    # Sleep disorders
                    "insomnia",
                    "sleep apnea",
                    "circadian rhythm",
                    # Cardiovascular conditions
                    "hypertension",
                    "patent foramen ovale",
                    "stroke risk",
                    # NLP Discovered
                    "vestibular migraine",
                    "cluster headache",
                    "tension type headache",
                    "tth",
                    "medication overuse headache",
                    "moh",
                    "restless legs syndrome",
                    "rls",
                ],
            },
            # 3. Social Impact
            "social_impact": {
                "description": "Social Impact",
                "keywords": [
                    "quality of life",
                    "disability",
                    "work productivity",
                    "absenteeism",
                    "presenteeism",
                    "economic burden",
                    "healthcare cost",
                    "stigma",
                    "social isolation",
                    "family burden",
                    "daily functioning",
                    # NLP Discovered
                    "emergency department",
                    "headache days",
                    "monthly migraine days",
                    "hospitalization",
                ],
            },
            # 4. Interventions
            "interventions": {
                "description": "Interventions",
                "keywords": [
                    # Medications
                    "triptans",
                    "CGRP",
                    "erenumab",
                    "fremanezumab",
                    "galcanezumab",
                    "propranolol",
                    "topiramate",
                    "amitriptyline",
                    "valproate",
                    "botulinum",
                    # Non-pharmacological
                    "cognitive behavioral therapy",
                    "biofeedback",
                    "acupuncture",
                    "physical therapy",
                    "relaxation",
                    "mindfulness",
                    "yoga",
                    # Lifestyle modifications
                    "diet",
                    "exercise",
                    "sleep hygiene",
                    "stress management",
                    "neuromodulation",
                    "monoclonal antibodies",
                    "gene therapy",
                    # NLP Discovered
                    "nerve stimulation",
                    "transcranial magnetic",
                    "tms",
                    "pfo closure",
                    "calcitonin gene-related",
                    "cgrp receptor",
                    "gepants",
                    "lasmiditan",
                ],
            },
        }

        # Research methodology terms to exclude (separate category)
        self.research_methods = {
            "randomized controlled trial",
            "cohort study",
            "case control",
            "cross sectional",
            "systematic review",
            "meta analysis",
            "clinical trial",
            "observational study",
            "diagnostic criteria",
            "assessment scale",
            "statistical analysis",
            "epidemiology",
        }

    def load_pubmed_data(self, file_path: str) -> Optional[pd.DataFrame]:
        """Load PubMed data from CSV file"""
        try:
            # Try multiple encoding formats
            for encoding in ["utf-8", "latin-1", "cp1252"]:
                for sep in [",", "\t", ";"]:
                    try:
                        df = pd.read_csv(
                            file_path, encoding=encoding, sep=sep, quoting=1, on_bad_lines="skip"
                        )
                        if len(df.columns) > 3:
                            print(f"Successfully loaded: {encoding}, separator: '{sep}'")
                            return df
                    except Exception:
                        continue
            return pd.read_csv(file_path, engine="python", on_bad_lines="skip")
        except Exception as e:
            print(f"Loading failed: {e}")
            return None

    def strict_term_cleaning(self, term: Any) -> Optional[str]:
        """Strictly clean medical terms"""
        if pd.isna(term) or not term.strip():
            return None

        term = str(term).strip()

        # 1. Remove all special markers
        term = re.sub(r"^\*+|\*+$", "", term)  # Leading/trailing asterisks
        term = re.sub(r"/\*.*", "", term)  # Content after slash-asterisk
        term = re.sub(r"\[.*?\]|\(.*?\)", "", term)  # Brackets content

        # 2. Convert to lowercase and split
        term = term.lower()
        words = term.split()

        # 3. Strict filtering
        filtered_words = []
        for word in words:
            # Length requirements
            if len(word) < 3 or len(word) > 20:
                continue
            # Stopword filtering
            if word in self.medical_stopwords:
                continue
            # Number filtering
            if word.isdigit():
                continue
            # Special character check
            if re.search(r"[^a-z\-]", word):
                continue

            filtered_words.append(word)

        if not filtered_words:
            return None

        term = " ".join(filtered_words)

        # 4. Title case and return
        return term.title()

    def precise_categorization(self, term: str) -> str:
        """Precisely categorize medical terms"""
        term_lower = term.lower()

        # First check if it's a research method (to be excluded)
        for research_term in self.research_methods:
            if research_term in term_lower:
                return "research_methods"  # Separately marked, filtered later

        # Exact match categorization
        for category, info in self.refined_categories.items():
            for keyword in info["keywords"]:
                if keyword in term_lower:
                    return category

        # Content-based inference (stricter)
        trigger_words = ["mechanism", "pathophysiology", "etiology", "trigger", "sensitization"]
        comorbidity_words = ["comorbidity", "comorbid", "coexisting", "associated with"]
        impact_words = ["burden", "cost", "productivity", "quality", "disability"]
        intervention_words = ["therapy", "treatment", "medication", "management", "intervention"]

        if any(word in term_lower for word in trigger_words):
            return "trigger_mechanisms"
        elif any(word in term_lower for word in comorbidity_words):
            return "true_comorbidities"
        elif any(word in term_lower for word in impact_words):
            return "social_impact"
        elif any(word in term_lower for word in intervention_words):
            return "interventions"

        return "unclassified"  # Unclassified terms will be filtered

    def extract_high_quality_terms(
        self, tags_str: Any, abstract_text: Any = "", keywords_text: Any = ""
    ) -> List[str]:
        """Extract high-quality medical terms from multiple fields"""
        high_quality_terms = set()

        # 1. Process Manual Tags (existing logic)
        if not pd.isna(tags_str):
            tags_str = str(tags_str)
            segments = re.split(r"[;,]", tags_str)
            for segment in segments:
                cleaned_term = self.strict_term_cleaning(segment)
                if cleaned_term:
                    category = self.precise_categorization(cleaned_term)
                    if category != "unclassified" and category != "research_methods":
                        high_quality_terms.add(cleaned_term)

        # 2. Process Author Keywords
        if not pd.isna(keywords_text):
            keywords_str = str(keywords_text)
            kw_segments = re.split(r"[;,]", keywords_str)
            for kw in kw_segments:
                cleaned = self.strict_term_cleaning(kw)
                if cleaned:
                    category = self.precise_categorization(cleaned)
                    if category != "unclassified" and category != "research_methods":
                        high_quality_terms.add(cleaned)

        # 3. Process Abstract text (Simple Contextual Extraction)
        if not pd.isna(abstract_text):
            abstract = str(abstract_text).lower()

            # Check for presence of category keywords in abstract
            for category, info in self.refined_categories.items():
                for keyword in info["keywords"]:
                    if keyword in abstract:
                        # If a keyword is found in abstract, we add it as a term
                        # This captures terms mentioned in text even if not in tags
                        cleaned = self.strict_term_cleaning(keyword)
                        if cleaned:
                            high_quality_terms.add(cleaned)

        return list(high_quality_terms)

    def build_refined_network(
        self, df: pd.DataFrame, min_frequency: int = 3, min_weight: int = 2
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Build refined network"""
        print("Building refined network (V2 - with Abstract processing)...")

        article_keywords = []

        for idx, row in df.iterrows():
            if idx % 200 == 0 and idx > 0:
                print(f"Processing: {idx}/{len(df)}")

            # Identify Abstract column
            abstract_col = None
            for col in ["Abstract", "Abstract Note", "Description", "Summary"]:
                if col in df.columns:
                    abstract_col = col
                    break

            # Extract high-quality terms from ALL fields
            manual_tags = self.extract_high_quality_terms(
                tags_str=row.get("Manual Tags", ""),
                abstract_text=row.get(abstract_col, "") if abstract_col else "",
                keywords_text=row.get(
                    "Keywords", ""
                ),  # Assuming 'Keywords' column exists, if not it will be empty string
            )

            # Limit terms per article (prevent single article from contributing too many nodes)
            if len(manual_tags) > 20:  # Increased slightly for V2
                manual_tags = manual_tags[:20]

            if manual_tags:
                article_keywords.append(manual_tags)

        print(f"Valid articles: {len(article_keywords)}")

        # Calculate node frequency
        node_frequency = Counter()
        for keywords in article_keywords:
            node_frequency.update(keywords)

        # Strict filtering: only keep high-frequency terms
        filtered_terms = {
            term: freq for term, freq in node_frequency.items() if freq >= min_frequency
        }

        print(f"Filtered terms: {len(filtered_terms)} (original: {len(node_frequency)})")

        # Calculate edge weights (only consider filtered terms)
        edge_weights = defaultdict(int)
        for keywords in article_keywords:
            # Only consider filtered terms
            filtered_keywords = [kw for kw in keywords if kw in filtered_terms]
            for kw1, kw2 in itertools.combinations(sorted(filtered_keywords), 2):
                edge_weights[(kw1, kw2)] += 1

        # Create node data
        nodes_data = []
        for term, freq in filtered_terms.items():
            category = self.precise_categorization(term)
            nodes_data.append(
                {
                    "Id": re.sub(r"[^\w]", "_", term.lower())[:30],
                    "Label": term,
                    "Category": category,
                    "Frequency": freq,
                    "Category_Description": self.refined_categories.get(category, {}).get(
                        "description", "Other"
                    ),
                }
            )

        # Create edge data (apply weight threshold)
        edges_data = []
        for (term1, term2), weight in edge_weights.items():
            if weight >= min_weight:  # Weight threshold
                source_id = next(
                    (node["Id"] for node in nodes_data if node["Label"] == term1), None
                )
                target_id = next(
                    (node["Id"] for node in nodes_data if node["Label"] == term2), None
                )

                if source_id and target_id:
                    edges_data.append(
                        {
                            "Source": source_id,
                            "Target": target_id,
                            "Weight": weight,
                            "Type": "Undirected",
                            "Source_Label": term1,
                            "Target_Label": term2,
                        }
                    )

        nodes_df = pd.DataFrame(nodes_data)
        edges_df = pd.DataFrame(edges_data)

        print(f"Final network size: {len(nodes_df)} nodes, {len(edges_df)} edges")

        return nodes_df, edges_df

    def analyze_refined_network(self, nodes_df: pd.DataFrame, edges_df: pd.DataFrame) -> None:
        """Analyze refined network"""
        print("\n" + "=" * 60)
        print("Refined Network Analysis Report (V2)")
        print("=" * 60)

        # Basic statistics
        print("Network scale:")
        print(f"  - Nodes: {len(nodes_df):,}")
        print(f"  - Edges: {len(edges_df):,}")
        if len(nodes_df) > 1:
            print(
                f"  - Network density: {len(edges_df) / (len(nodes_df) * (len(nodes_df) - 1) / 2):.6f}"
            )

        # Category distribution
        print("\nNode category distribution:")
        category_stats = nodes_df["Category"].value_counts()
        for category, count in category_stats.items():
            desc = self.refined_categories.get(category, {}).get("description", "Other")
            percentage = (count / len(nodes_df)) * 100
            print(f"  - {desc}: {count} nodes ({percentage:.1f}%)")

        # High-frequency terms
        print("\nTop 20 high-frequency terms:")
        top_terms = nodes_df.nlargest(20, "Frequency")
        for idx, row in top_terms.iterrows():
            desc = self.refined_categories.get(row["Category"], {}).get("description", "Other")
            print(
                f"  {idx + 1:2d}. {row['Label']:25s} (frequency: {row['Frequency']:2d}, category: {desc})"
            )


def main() -> None:
    """Main function"""
    converter = PubMedRefinedNetworkV2()

    # File path - Standardized for 'raw' directory
    file_path = r"../data/raw/PubMed.csv"

    if not os.path.exists(file_path):
        # Fallback if running from root
        file_path = r"english_version/data/raw/PubMed.csv"

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        print("Please place your PubMed CSV file in the 'english_version/data/raw/' directory")
        return

    # Load data
    print("Loading PubMed data...")
    df = converter.load_pubmed_data(file_path)

    if df is None or df.empty:
        print("Data loading failed")
        return

    print(f"Data size: {len(df)} rows × {len(df.columns)} columns")

    # Build refined network (with thresholds)
    nodes_df, edges_df = converter.build_refined_network(df, min_frequency=3, min_weight=2)

    if nodes_df.empty:
        print("Network construction failed")
        return

    # Analyze network
    converter.analyze_refined_network(nodes_df, edges_df)

    # Save files to 'processed' directory
    output_dir = "../data/processed"
    if not os.path.exists("../data"):
        # Handle running from root
        output_dir = "english_version/data/processed"

    os.makedirs(output_dir, exist_ok=True)

    # Gephi files
    nodes_df[["Id", "Label", "Category", "Frequency"]].to_csv(
        os.path.join(output_dir, "gephi_nodes.csv"), index=False, encoding="utf-8-sig"
    )

    edges_df[["Source", "Target", "Weight", "Type"]].to_csv(
        os.path.join(output_dir, "gephi_edges.csv"), index=False, encoding="utf-8-sig"
    )

    # Detailed files (for analysis)
    nodes_df.to_csv(
        os.path.join(output_dir, "detailed_nodes.csv"), index=False, encoding="utf-8-sig"
    )
    edges_df.to_csv(
        os.path.join(output_dir, "detailed_edges.csv"), index=False, encoding="utf-8-sig"
    )

    print(f"\n[SUCCESS] Network files generated in {output_dir}!")


if __name__ == "__main__":
    main()
