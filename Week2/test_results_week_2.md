I dont know why I would put this into three different markdown files.

# Week 2 Results
For each method I ran the exact same queries as the first week, and got the same numerical results, and thus only the processing time will be listed.
## Pandas
note: I don't think I understood the tools to build a good query, It can definitely be made faster. Probably easily.
### 1 Hour Span
    1912.4ms
### 3 Hour Span
    2489.6ms
### 6 Hour Span
    2843.4ms
## Polars
### 1 Hour Span
    263.0ms
### 3 Hour Span
    418.8ms
### 6 Hour Span
    596.0ms
## DuckDB
this is way fast, and was super easy, just slapped some sql in there and I was good to go. Epic Win
### 1 Hour Span
    123.5ms
### 3 Hour Span
    169.6ms
### 6 Hour Span
    231.1ms