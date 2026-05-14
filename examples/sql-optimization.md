# AutoResearch — SQL Query Optimization

> Autonomous optimization of SQL queries to minimize execution time.

## Domain Configuration

- **Domain**: SQL query performance
- **Target file**: `target.py` (contains SQL queries as strings + execution logic)
- **Eval command**: `python evaluate.py`
- **Metric name**: `score`
- **Metric direction**: **lower** is better (seconds)
- **Time budget per run**: 2 minutes
- **Timeout**: 4 minutes

## What You CAN Do

- Rewrite SQL queries (same results, faster execution)
- Add/change indexes (via CREATE INDEX in target.py)
- Change query order, use CTEs, window functions
- Batch queries, reduce round-trips
- Use EXPLAIN ANALYZE to guide optimization

## What You CANNOT Do

- Modify `evaluate.py` or `program.md`
- Change the database schema (tables are fixed)
- Change the expected query results
- Drop or truncate tables
- Use database-specific extensions not in SQLite

## Adaptation Notes

Your `evaluate.py` should:
1. Create an in-memory SQLite database with test data
2. Import `get_queries()` from target.py → list of SQL strings
3. Execute each query, verify results match expected output
4. Time total execution
5. Print `score: <total_seconds>`
