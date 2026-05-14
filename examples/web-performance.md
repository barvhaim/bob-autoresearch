# AutoResearch — Web Performance Optimization

> Autonomous optimization of web app configuration to minimize load time.

## Domain Configuration

- **Domain**: Web performance (server response time)
- **Target file**: `target.py` (server config, caching strategy, middleware)
- **Eval command**: `python evaluate.py`
- **Metric name**: `score`
- **Metric direction**: **lower** is better (milliseconds)
- **Time budget per run**: 2 minutes
- **Timeout**: 4 minutes

## What You CAN Do

- Change caching strategies
- Reorder middleware pipeline
- Adjust compression settings
- Optimize database queries
- Change connection pooling config

## What You CANNOT Do

- Modify `evaluate.py` or `program.md`
- Change the test endpoints or request patterns
- Install new packages
- Modify the core application logic (only config/middleware)

## Adaptation Notes

Your `evaluate.py` should:
1. Start the web server from target.py config
2. Send a fixed set of HTTP requests (warm-up + measured)
3. Measure p50/p95/p99 response times
4. Compute composite score
5. Print `score: <total_ms>`
6. Kill the server
