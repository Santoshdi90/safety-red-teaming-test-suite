# Safety & Red-Teaming Test Suite

A local, harmless regression suite for identifying common prompt-injection and unsafe-output patterns in text. It includes categorized test cases and a baseline output scanner.

## Run
```bash
pip install -r requirements.txt
python run_tests.py
pytest
```

## Scope and safety
This starter uses static sample inputs and a simple pattern-based scanner; it does not connect to or attack external models. Its counts are scanner detections on the included examples, not model jailbreak success rates. False positives and false negatives are expected. Do not claim a mitigation success percentage without running a documented before/after evaluation against a specified model and dataset.
