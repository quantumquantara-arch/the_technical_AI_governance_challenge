# Testing Guide
- Run individual tests: `.\test_zero_return.ps1`
- Each test is isolated with try-catch; failures dont stop others.
- For batch: Use `demo.ps1`-processes one at a time, logs errors, continues.
- Metrics: Included in demo for accuracy on ground truth.
