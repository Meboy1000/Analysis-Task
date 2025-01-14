
# Week 1 Results
## 1-Hour Timeframe
- **Timeframe:** 2022-04-04 00 to 2022-04-01 01
- **Execution Time:** 77.048 s
- **Most Placed Color:** #000000
- **Most Placed Pixel Location:** (0, 0)
## 3-Hour Timeframe
- **Timeframe:** 2022-04-04 00 to 2022-04-04 03
- **Execution Time:** 81.765 s
- **Most Placed Color:** #000000
- **Most Placed Pixel Location:** (0, 0)
## 6-Hour Timeframe
- **Timeframe:** 2022-04-04 00 to 2022-04-04 06
- **Execution Time:** 82.13 s
- **Most Placed Color:** #000000
- **Most Placed Pixel Location:** (0, 0)

these runtimes are awful, guess that's what happens when you have a 20 gig table. Notably the runtimes don't get any worse with larger timeframes, I'm assuming that its because the data isn't sorted to begin with, so it's iterating through the entire table to find everything within the range, and that just takes the same time regardless.