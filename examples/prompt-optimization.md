# AutoResearch — LLM Prompt Optimization

> Autonomous optimization of LLM prompts to maximize quality score.

## Domain Configuration

- **Domain**: Prompt engineering optimization
- **Target file**: `target.py` (contains the prompt template + call logic)
- **Eval command**: `python evaluate.py`
- **Metric name**: `score`
- **Metric direction**: **higher** is better (0.0 to 1.0)
- **Time budget per run**: 3 minutes
- **Timeout**: 6 minutes

## What You CAN Do

- Rewrite the prompt template
- Change few-shot examples
- Adjust system message
- Change output parsing logic
- Try chain-of-thought, structured output, etc.

## What You CANNOT Do

- Modify `evaluate.py` or `program.md`
- Change the LLM model (fixed in evaluate.py)
- Change the evaluation dataset
- Hard-code answers from the test set

## Adaptation Notes

Your `evaluate.py` should:
1. Load a golden test set (input → expected output pairs)
2. Call `target.py`'s `generate(input)` function for each test case
3. Score each output (exact match, BLEU, semantic similarity, etc.)
4. Print `score: <average_score>`
