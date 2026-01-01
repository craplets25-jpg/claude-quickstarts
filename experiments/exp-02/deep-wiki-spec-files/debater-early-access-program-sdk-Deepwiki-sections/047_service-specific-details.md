<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Service-Specific Details -->
<!-- Lines: 2213-2305 -->

## Service-Specific Details

### Argument Quality Service

The `ArgumentQualityClient` scores the quality of arguments in sentence-topic pairs on a scale from 0 to 1.

**Input Format:** List of dictionaries with `sentence` and `topic` keys  
**Output Format:** List of float scores (0-1)  
**Endpoint:** `/score/` on `arg-quality.debater.res.ibm.com`

```python
argument_quality_client = debater_api.get_argument_quality_client()
scores = argument_quality_client.run(sentence_topic_dicts)
```

Sources: [debater_python_api/api/clients/argument_quality_client.py:8-23](), [debater_python_api/integration_tests/api/clients/ServicesIT.py:28-44]()

### Claim and Evidence Detection Services

Both `ClaimDetectionClient` and `EvidenceDetectionClient` use the same input/output format as argument quality but serve different purposes:

- **Claim Detection**: Identifies whether sentences contain claims related to a topic
- **Evidence Detection**: Identifies whether sentences contain evidence related to a topic

```python
claim_detection_client = debater_api.get_claim_detection_client()
evidence_detection_client = debater_api.get_evidence_detection_client()

claim_scores = claim_detection_client.run(sentence_topic_dicts)
evidence_scores = evidence_detection_client.run(sentence_topic_dicts)
```

Sources: [debater_python_api/integration_tests/api/clients/ServicesIT.py:45-77]()

### Claim Boundaries Service

The `ClaimBoundariesClient` extracts claim boundaries from sentences without requiring topic information.

**Input Format:** List of strings (sentences)  
**Output Format:** List of dictionaries with `claim` key

```python
claim_boundaries_client = debater_api.get_claim_boundaries_client()
boundaries = claim_boundaries_client.run(sentences)
```

Sources: [debater_python_api/integration_tests/api/clients/ServicesIT.py:79-90]()

### Clustering Service

The `ClusteringClient` groups sentences by semantic similarity.

**Input Format:** `sentences` list and `num_of_clusters` parameter  
**Output Format:** List of lists (clusters of sentences)

```python
clustering_client = debater_api.get_clustering_client()
clusters = clustering_client.run(sentences=sentences, num_of_clusters=2)
```

The service also supports distance-based clustering:
```python
arguments_and_distances = clustering_client.run_with_distances(sentences, num_clusters)
```

Sources: [debater_python_api/integration_tests/api/clients/ServicesIT.py:91-116]()

### Pro/Con Service

The `ProConClient` scores the stance (pro or con) of sentence-topic pairs on a scale from -1 to 1.

**Input Format:** List of dictionaries with `sentence` and `topic` keys  
**Output Format:** List of float scores (-1 to 1)

```python
pro_con_client = debater_api.get_pro_con_client()
scores = pro_con_client.run(sentence_topic_dicts)
```

Sources: [debater_python_api/integration_tests/api/clients/ServicesIT.py:131-147]()

### Advanced Services

Several services provide more complex functionality:

- **Narrative Generation**: Creates structured speeches from arguments and scores
- **Term Relater**: Scores semantic relatedness between term pairs
- **Term Wikifier**: Annotates terms in sentences with Wikipedia concepts
- **Theme Extraction**: Extracts themes from clustered sentences
- **Index Searcher**: Searches a sentence-level index using complex queries

Sources: [debater_python_api/integration_tests/api/clients/ServicesIT.py:148-238]()

