<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Available Services -->
<!-- Lines: 2114-2133 -->

## Available Services

The following table summarizes all available NLP service clients:

| Service Client | Purpose | Input Format | Output Format | Endpoint Host |
|---|---|---|---|---|
| `ArgumentQualityClient` | Score argument quality of sentence-topic pairs | `[{'sentence': str, 'topic': str}]` | `[float]` (0-1) | `arg-quality.debater.res.ibm.com` |
| `ClaimDetectionClient` | Detect claims in sentence-topic pairs | `[{'sentence': str, 'topic': str}]` | `[float]` (0-1) | `claim-sentence.debater.res.ibm.com` |
| `EvidenceDetectionClient` | Detect evidence in sentence-topic pairs | `[{'sentence': str, 'topic': str}]` | `[float]` (0-1) | `motion-evidence.debater.res.ibm.com` |
| `ClaimBoundariesClient` | Extract claim boundaries from sentences | `[str]` | `[{'claim': str}]` | `claim-boundaries.debater.res.ibm.com` |
| `ClusteringClient` | Cluster sentences by similarity | `sentences=[str], num_of_clusters=int` | `[[str]]` | `clustering.debater.res.ibm.com` |
| `ProConClient` | Score pro/con stance of sentence-topic pairs | `[{'sentence': str, 'topic': str}]` | `[float]` (-1 to 1) | Various |
| `NarrativeGenerationClient` | Generate structured narratives | Complex parameters | Speech object | Various |
| `TermRelaterClient` | Score relatedness between term pairs | `[[str, str]]` | `[float]` (0-1) | Various |
| `TermWikifierClient` | Wikify terms in sentences | `[str]` | `[[annotation]]` | Various |
| `ThemeExtractionClient` | Extract themes from clustered sentences | `topic, dominant_concept, clusters` | `[themes]` | Various |
| `IndexSearcherClient` | Search sentence-level index | `SentenceQueryRequest` | `[sentences]` | Various |

Sources: [debater_python_api/integration_tests/api/clients/ServicesIT.py:28-238](), [debater_python_api/api/clients/argument_quality_client.py:11-23]()

