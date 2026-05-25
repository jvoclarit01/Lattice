---
name: skill-dataset-documentation
description: Dataset documentation best practices for academic research. Use when documenting datasets, describing data sources, or ensuring data reproducibility. Covers data documentation, metadata, and data sharing.
---

# Dataset Documentation Domain

Dataset documentation best practices for academic research.

## When to Activate

Activate when documenting datasets, describing data sources, or ensuring data reproducibility.

## Core Principles

1. **Document Everything** — Document all data comprehensively
2. **Describe Sources** — Describe data sources clearly
3. **Ensure Reproducibility** — Ensure reproducibility completely
4. **Share Appropriately** — Share data appropriately

## Data Documentation

### Dataset Description

**Dataset name:**
- Clear, descriptive name
- Include version number
- Use consistent naming
- Avoid abbreviations

**Dataset purpose:**
- Intended use cases
- Research questions addressed
- Target applications
- Scope of dataset

**Dataset size:**
- Number of samples
- Number of features
- File sizes
- Storage requirements

**Data format:**
- File formats (CSV, JSON, Parquet, etc.)
- Schema description
- Encoding information
- Compression details

**Example:**
> **Dataset Description:**
> - Name: Medical-Text-Classification-v1.0
> - Purpose: Training and evaluation of medical text classification models
> - Size: 50,000 documents, 12 categories
> - Format: JSON with UTF-8 encoding, gzip compressed

### Data Sources

**Source description:**
- Original source of data
- Collection methodology
- Data provenance
- Collection timeline

**Collection method:**
- How data was collected
- Tools and instruments used
- Sampling strategy
- Quality control measures

**Collection date:**
- Date range of collection
- Timestamp information
- Temporal coverage
- Time zone information

**Collection location:**
- Geographic coverage
- Institutional sources
- Platform information
- Access method

**Example:**
> **Data Sources:**
> - Source: PubMed Central open access articles
> - Method: Automated retrieval using PubMed API
> - Date: January 2019 - December 2020
> - Location: Public biomedical literature database

### Data Characteristics

**Data types:**
- Type of each feature
- Categorical vs numerical
- Text vs numerical
- Special data types

**Data ranges:**
- Min/max values
- Value distributions
- Outlier information
- Missing value patterns

**Data distribution:**
- Class distribution
- Feature distributions
- Statistical properties
- Visualization recommendations

**Data quality:**
- Completeness metrics
- Accuracy information
- Consistency checks
- Known issues

**Example:**
> **Data Characteristics:**
> - Types: Text (documents), categorical (labels), numerical (metadata)
> - Ranges: Document length 50-5000 words, 12 categories
> - Distribution: Balanced classes (4000-4500 per category)
> - Quality: 98% complete, 2% missing metadata

### Data Preprocessing

**Preprocessing steps:**
- Data cleaning procedures
- Normalization methods
- Feature engineering
- Transformation steps

**Feature engineering:**
- How features were created
- Feature selection methods
- Feature importance
- Feature relationships

**Data cleaning:**
- Missing value handling
- Outlier treatment
- Duplicate removal
- Error correction

**Data transformation:**
- Scaling and normalization
- Encoding methods
- Dimensionality reduction
- Format conversions

**Example:**
> **Data Preprocessing:**
> - Cleaning: Removed HTML tags, fixed encoding errors
> - Normalization: Lowercased text, removed punctuation
> - Feature Engineering: TF-IDF vectors, medical term embeddings
> - Transformation: Standardized numerical features

## Metadata Standards

### Dublin Core

**Title:** Name of the dataset
**Creator:** Person or organization responsible
**Subject:** Keywords or subject categories
**Description:** Abstract or summary
**Publisher:** Entity publishing the dataset
**Date:** Publication or creation date
**Type:** Nature of the resource (Dataset)
**Format:** File format
**Identifier:** Unique identifier (DOI, URL)
**Language:** Language of the content

**Example:**
> **Dublin Core Metadata:**
> - Title: Medical Text Classification Dataset
> - Creator: Smith, John A.; Jones, Mary B.
> - Subject: Medical NLP, Text Classification
> - Description: Dataset of 50,000 medical documents...
> - Publisher: University Data Repository
> - Date: 2021-03-15
> - Type: Dataset
> - Format: JSON
> - Identifier: https://doi.org/10.xxxx/xxxxx
> - Language: en

### Schema.org

**Dataset:** Main dataset description
**DataCatalog:** Catalog containing the dataset
**DataDownload:** Downloadable file information
**Distribution:** Distribution information
**SpatialCoverage:** Geographic coverage
**TemporalCoverage:** Time period covered

**Example:**
> **Schema.org Metadata:**
> ```json
> {
>   "@type": "Dataset",
>   "name": "Medical Text Classification Dataset",
>   "description": "Dataset of 50,000 medical documents...",
>   "creator": {
>     "@type": "Person",
>     "name": "John A. Smith"
>   },
>   "distribution": {
>     "@type": "DataDownload",
>     "encodingFormat": "application/json",
>     "contentUrl": "https://example.com/dataset.json"
>   }
> }
> ```

## Data Documentation Templates

### README Template

```markdown
# Dataset Name

## Description
[Brief description of dataset purpose and content]

## Dataset Statistics
- Number of samples: [X]
- Number of features: [Y]
- File size: [Z]
- Format: [format]

## Data Sources
- Source: [description]
- Collection method: [description]
- Collection date: [date range]

## Data Structure
[Description of data structure and schema]

## Usage
[Example code for loading and using the dataset]

## License
[License information]

## Citation
[How to cite the dataset]

## Contact
[Contact information for questions]
```

### Data Dictionary Template

```markdown
# Data Dictionary

## Overview
[Description of data dictionary purpose]

## Field Descriptions

| Field Name | Type | Description | Values | Notes |
|------------|------|-------------|--------|-------|
| field1 | string | Description | enum values | Notes |
| field2 | integer | Description | range | Notes |

## Relationships
[Description of relationships between fields]

## Quality Notes
[Known quality issues and limitations]
```

## Best Practices

### Documentation

**Document all data:**
- Every dataset documented
- Every feature described
- Every transformation recorded
- Every decision justified

**Use standard formats:**
- README files
- Data dictionaries
- Metadata standards
- Documentation templates

**Include metadata:**
- Descriptive metadata
- Structural metadata
- Technical metadata
- Administrative metadata

**Update regularly:**
- Keep documentation current
- Note changes and versions
- Update contact information
- Review periodically

### Sharing

**Share data appropriately:**
- Choose appropriate repository
- Follow institutional policies
- Consider ethical implications
- Respect participant privacy

**Use appropriate licenses:**
- Choose suitable license
- Understand license terms
- Specify usage restrictions
- Note attribution requirements

**Consider privacy:**
- Remove personal identifiers
- Anonymize sensitive data
- Follow privacy regulations
- Obtain necessary permissions

**Follow guidelines:**
- FAIR principles (Findable, Accessible, Interoperable, Reusable)
- Institutional guidelines
- Funder requirements
- Journal requirements

### Reproducibility

**Document preprocessing:**
- Record all preprocessing steps
- Provide preprocessing code
- Document parameter choices
- Note software versions

**Share code:**
- Provide analysis code
- Include dependencies
- Document installation
- Use version control

**Use version control:**
- Track dataset versions
- Document changes
- Maintain history
- Tag releases

**Report random seeds:**
- Record random seeds used
- Document random number generators
- Note reproducibility limitations
- Provide reproduction instructions

## Data Sharing Platforms

### General Repositories

**Zenodo:**
- Free, open access
- DOI assignment
- Large file support
- Version control

**Figshare:**
- Free tier available
- DOI assignment
- Multiple file types
- Citation tracking

**OSF (Open Science Framework):**
- Free, open access
- Project management
- Collaboration features
- Version control

### Domain-Specific Repositories

**UCI Machine Learning Repository:**
- Machine learning datasets
- Well-curated
- Citation tracking
- Community review

**Kaggle Datasets:**
- Large community
- Discussion forums
- Kernel support
- Competition datasets

**Domain repositories:**
- Check for field-specific repositories
- Often have better visibility
- May have specific requirements
- Better for specialized data

## Evaluation Checklist

Before sharing your dataset:

- [ ] Dataset name and description provided
- [ ] Data sources documented
- [ ] Collection method described
- [ ] Data characteristics documented
- [ ] Preprocessing steps recorded
- [ ] Metadata included
- [ ] License specified
- [ ] Citation information provided
- [ ] Contact information included
- [ ] Privacy considerations addressed
- [ ] Reproducibility ensured
- [ ] Appropriate repository selected

## Resources

### Data Documentation Tools
- [DVC](https://dvc.org/) — Data Version Control
- [MLflow](https://mlflow.org/) — Machine Learning lifecycle management
- [DataLad](https://www.datalad.org/) — Data management and distribution

### Metadata Standards
- [Dublin Core](https://www.dublincore.org/) — Standard metadata schema
- [Schema.org](https://schema.org/) — Structured data markup
- [DataCite](https://datacite.org/) — Data citation standards

### Data Sharing Platforms
- [Zenodo](https://zenodo.org/) — Open access repository
- [Figshare](https://figshare.com/) — Research data repository
- [OSF](https://osf.io/) — Open Science Framework

### FAIR Principles
- [FAIR Principles](https://www.go-fair.org/fair-principles/) — Findable, Accessible, Interoperable, Reusable
- [FAIR Data](https://www.force11.org/fairdata) — FAIR data guidelines

### Academic Writing Guides
- [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) — Scientific writing best practices
