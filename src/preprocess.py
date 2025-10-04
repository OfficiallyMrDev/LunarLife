# src/preprocess.py
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import logging
from pathlib import Path
import aiohttp
import asyncio
from nltk.tokenize import sent_tokenize
import nltk
from concurrent.futures import ThreadPoolExecutor
from functools import partial

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('maxent_ne_chunker', quiet=True)
    nltk.download('words', quiet=True)
except Exception as e:
    logger.warning(f"Failed to download NLTK data: {e}")

@dataclass
class PublicationMetadata:
    """Structured metadata for publications"""
    organisms: List[str]
    experiment_types: List[str]
    missions: List[str]
    keywords: List[str]
    publication_date: Optional[str]
    authors: List[str]
    institutions: List[str]

class TextCleaner:
    """Text cleaning and preprocessing utilities"""
    
    @staticmethod
    def clean_html(text: str) -> str:
        """Remove HTML tags and decode entities"""
        if pd.isna(text):
            return ""
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize all forms of whitespace"""
        return ' '.join(text.split())
    
    @staticmethod
    def clean_special_chars(text: str) -> str:
        """Remove special characters while preserving meaning"""
        # Keep meaningful punctuation
        text = re.sub(r'[^\w\s\-.,;:?!()"\']+', ' ', text)
        # Normalize spaces around punctuation
        text = re.sub(r'\s*([.,;:?!])\s*', r'\1 ', text)
        return text.strip()
    
    @staticmethod
    def extract_sentences(text: str) -> List[str]:
        """Split text into sentences using NLTK"""
        try:
            return sent_tokenize(text)
        except Exception as e:
            logger.warning(f"Failed to split sentences: {e}")
            return [text]
    
    @classmethod
    def clean_text(cls, text: str) -> str:
        """Apply all cleaning steps"""
        if pd.isna(text):
            return ""
        text = cls.clean_html(text)
        text = cls.clean_special_chars(text)
        text = cls.normalize_whitespace(text)
        return text

class MetadataExtractor:
    """Extract metadata from publication text"""
    
    # Comprehensive taxonomies
    ORGANISMS = {
        "mammals": ["mice", "rats", "humans", "primates", "rabbits"],
        "plants": ["arabidopsis", "wheat", "rice", "algae"],
        "microorganisms": ["bacteria", "yeast", "fungi"],
        "cells": ["stem cells", "cancer cells", "neurons", "fibroblasts"]
    }
    
    EXPERIMENT_TYPES = {
        "physical": ["microgravity", "radiation", "bone loss", "muscle atrophy"],
        "biological": ["genomics", "proteomics", "metabolism", "immune response"],
        "psychological": ["cognitive", "behavioral", "stress", "sleep"],
        "technological": ["life support", "habitat", "monitoring", "protection"]
    }
    
    MISSIONS = {
        "stations": ["ISS", "Mir", "Skylab"],
        "vehicles": ["Shuttle", "Soyuz", "Dragon"],
        "specific": ["Apollo", "Artemis", "Bion-M1"],
        "future": ["Mars", "Lunar Gateway", "Moon Base"]
    }
    
    @classmethod
    def extract_dates(cls, text: str) -> List[str]:
        """Extract potential publication dates"""
        date_patterns = [
            r'\b(19|20)\d{2}\b',  # Years
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (19|20)\d{2}\b'  # Month Year
        ]
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, text))
        return list(set(dates))
    
    @classmethod
    def extract_authors(cls, text: str) -> List[str]:
        """Extract author names using NLTK NER"""
        try:
            tokens = nltk.word_tokenize(text)
            tagged = nltk.pos_tag(tokens)
            entities = nltk.chunk.ne_chunk(tagged)
            authors = []
            for entity in entities:
                if isinstance(entity, nltk.Tree) and entity.label() == 'PERSON':
                    authors.append(' '.join([leaf[0] for leaf in entity.leaves()]))
            return list(set(authors))
        except Exception as e:
            logger.warning(f"Failed to extract authors: {e}")
            return []
    
    @classmethod
    def extract_institutions(cls, text: str) -> List[str]:
        """Extract institution names using NLTK NER"""
        try:
            tokens = nltk.word_tokenize(text)
            tagged = nltk.pos_tag(tokens)
            entities = nltk.chunk.ne_chunk(tagged)
            institutions = []
            for entity in entities:
                if isinstance(entity, nltk.Tree) and entity.label() == 'ORGANIZATION':
                    institutions.append(' '.join([leaf[0] for leaf in entity.leaves()]))
            return list(set(institutions))
        except Exception as e:
            logger.warning(f"Failed to extract institutions: {e}")
            return []

    @classmethod
    def extract_metadata(cls, text: str) -> PublicationMetadata:
        """Extract all metadata from text"""
        # Convert text to lowercase for matching
        text_lower = text.lower()
        
        # Extract organisms
        organisms = []
        for category, terms in cls.ORGANISMS.items():
            organisms.extend([term for term in terms if term.lower() in text_lower])
        
        # Extract experiment types
        experiment_types = []
        for category, terms in cls.EXPERIMENT_TYPES.items():
            experiment_types.extend([term for term in terms if term.lower() in text_lower])
        
        # Extract missions
        missions = []
        for category, terms in cls.MISSIONS.items():
            missions.extend([term for term in terms if term.lower() in text_lower])
        
        # Extract other metadata
        dates = cls.extract_dates(text)
        authors = cls.extract_authors(text)
        institutions = cls.extract_institutions(text)
        
        # Extract keywords (simple approach - can be improved with RAKE or similar)
        keywords = re.findall(r'\b\w+\b', text_lower)
        keywords = [w for w in set(keywords) if len(w) > 3]  # Simple filtering
        
        return PublicationMetadata(
            organisms=list(set(organisms)),
            experiment_types=list(set(experiment_types)),
            missions=list(set(missions)),
            keywords=keywords[:10],  # Top 10 keywords
            publication_date=dates[0] if dates else None,
            authors=authors,
            institutions=institutions
        )

async def fetch_publication_content(url: str) -> Tuple[str, str, str]:
    """Fetch publication content asynchronously"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract sections
                    results = ""
                    conclusion = ""
                    abstract = ""
                    
                    # Find abstract
                    abstract_elem = soup.find('section', {'id': 'abstract'}) or \
                                 soup.find('div', {'class': 'abstract'})
                    if abstract_elem:
                        abstract = abstract_elem.get_text(strip=True)
                    
                    # Find results and conclusion
                    for section in soup.find_all(['section', 'div']):
                        text = section.get_text(strip=True).lower()
                        if 'results' in text[:20]:
                            results = section.get_text(strip=True)
                        elif 'conclusion' in text[:20] or 'discussion' in text[:20]:
                            conclusion = section.get_text(strip=True)
                    
                    return abstract, results, conclusion
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
        
        return "", "", ""

def load_and_clean(csv_path: str = "data/publications_with_abstracts.csv") -> pd.DataFrame:
    """
    Load and preprocess the publications dataset
    """
    logger.info(f"Loading data from {csv_path}")
    
    try:
        # Read CSV
        df = pd.read_csv(csv_path)
        
        # Standardize column names
        df.rename(columns={
            'Title': 'title',
            'Abstract': 'abstract',
            'Link': 'link'
        }, inplace=True)
        
        # Clean text fields
        cleaner = TextCleaner()
        df['title'] = df['title'].apply(cleaner.clean_text)
        df['abstract'] = df['abstract'].apply(lambda x: cleaner.clean_text(x) or "Abstract not available.")
        
        # Remove duplicates and handle missing values
        df.drop_duplicates(subset=['title'], inplace=True)
        df.fillna({
            "abstract": "Abstract not available.",
            "results": "",
            "conclusion": ""
        }, inplace=True)
        
        # Extract metadata
        logger.info("Extracting metadata from publications")
        metadata = []
        for _, row in df.iterrows():
            text = f"{row['title']} {row['abstract']}"
            metadata.append(MetadataExtractor.extract_metadata(text))
        
        # Add metadata columns
        df['organisms'] = [m.organisms for m in metadata]
        df['experiment_types'] = [m.experiment_types for m in metadata]
        df['missions'] = [m.missions for m in metadata]
        df['keywords'] = [m.keywords for m in metadata]
        df['publication_date'] = [m.publication_date for m in metadata]
        df['authors'] = [m.authors for m in metadata]
        df['institutions'] = [m.institutions for m in metadata]
        
        # Add processing metadata
        df['processed_at'] = datetime.now().isoformat()
        df['processing_version'] = "2.0.0"
        
        logger.info(f"Successfully processed {len(df)} publications")
        return df
        
    except Exception as e:
        logger.error(f"Error processing publications: {e}")
        raise