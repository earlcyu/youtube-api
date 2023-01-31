# End-to-End Data Engineering and Visualization with the YouTube API

This is an end-to-end data engineering and visualization project using the YouTube API. 

Specifically, this project aims to:
1. Create a `Channel` class using object-oriented programming principles to easily obtain channel and video statistics data of a given YouTube channel
2. Load the data from (1) into a BigQuery table using the BigQuery API 
3. Visualize the data from (2) using Looker Studio 

Check out my Medium article series where I go through each phase of the project step by step: [Part 1](https://medium.com/@earlc.yu/how-to-apply-oop-principles-in-data-engineering-creating-a-class-object-with-the-youtube-api-ceaffabb07bc), [Part 2](https://medium.com/@earlc.yu/how-to-load-a-dataframe-into-bigquery-using-python-and-the-bigquery-api-9da0fdda1dfb), and [Part 3](https://medium.com/@earlc.yu/how-to-make-a-dashboard-in-looker-studio-5ae12b8ba909).

---

# Context

I started learning object-oriented programming awhile back and needed to apply what I have learned. Inspired by Thu Vu data analytics' [video](https://www.youtube.com/watch?v=D56_Cx36oGY&t=453s) about creating a data portfolio project with the YouTube API, I decided to create a YouTube channel class using OOP principles. 

After finishing the above project, I decided to take it a step further by ingesting the data into BigQuery and visualizing the results.

# Files

```
.gitignore          - list of files/types to exclude in git commits
bigquery.py         - contains the logic for the `BigQuery` class 
main.py             - imports and applies the `Channel` class
README.md           - documentation
youtube.py          - contains the logic for the `Channel` class
```
