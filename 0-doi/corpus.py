import urllib
import arxiv
import requests
import json
import csv
import pandas as pd
from collections import Counter, defaultdict
import numpy as np # for array manipulation
import matplotlib.pyplot as plt # for data visualization
import datetime

results_generator = arxiv.Client(
  page_size=500,
  delay_seconds=3,
  num_retries=3
).results(arxiv.Search(
  #query='((abs:"interpretability" AND abs:"machine learning") OR (abs:"explainability" AND abs:"machine learning")) AND (cat:cs.LG OR cat:cs.AI)',
  query='(abs:"interpretability in machine learning" OR abs:"explainability in machine learning") AND (cat:cs.LG OR cat:cs.AI)',
  id_list=[],
  sort_by=arxiv.SortCriterion.Relevance,
  sort_order=arxiv.SortOrder.Descending,
))

paper_list = []
for paper in results_generator:
  # You could do per-paper analysis here; for now, just collect them in a list.
  paper_list.append(paper)
  
qd_df = pd.DataFrame([vars(paper) for paper in paper_list])
# Add a first_author column: the name of the first author among each paper's list of authors.
qd_df['first_author'] = [authors_list[0].name for authors_list in qd_df['authors']]
# Keep a reference to the original results in the dataframe: this is useful for downloading PDFs.
qd_df['_result'] = paper_list
qd_df['ids'] = qd_df['entry_id'].apply(lambda x: x.replace("http://arxiv.org/abs/", ""))

qd_df.to_csv('metadata.csv', index=False, sep=',')
qd_df['ids'].to_csv('doi.txt', index=False, header=None)

# Narrow our dataframe to just the columns we want for our analysis.
qd_df = qd_df[['title', 'published', 'first_author', '_result']]

plot = qd_df["published"].groupby(qd_df["published"].dt.year).count().plot(kind="bar")
fig = plot.get_figure()
fig.savefig('plot.pdf')

qd_authors = qd_df.groupby(qd_df["first_author"])["first_author"].count().sort_values(ascending=False)
print(qd_authors.head(20))