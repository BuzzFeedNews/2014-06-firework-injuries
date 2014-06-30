#!/usr/bin/env python
import pandas as pd

# Read injuries
# Data from https://www.cpsc.gov/cgibin/NEISSQuery/Home.aspx
injuries = pd.read_csv("data/firework-injuries-2013.tsv", sep="\t")

# Combine narrative columns
injuries["narrative"] = injuries.narr1.fillna("") + " " + injuries.narr2.fillna("")

# Read diagnosis codes
# via https://www.cpsc.gov//Global/Neiss_prod/completemanual%20.pdf
codes = pd.read_csv("data/niess-codes.tsv", sep="\t").set_index("code")

# Join diagnosis names to injuries
diagnosed = injuries.set_index("diag").join(codes).set_index("diagnosis")

# Tweak the order for rhythm
diagnosis_order = [
    "Amputation",
    "Dislocation",
    "Hemorrhage",
    "Anoxia",
    "Avulsion",
    "Puncture",
    "Dermatitis, Conjunctivitis",
    "Internal organ injury",
    "Foreign body",
    "Fracture",
    "Strain or Sprain",
    "Contusions, Abrasions",
    "Laceration",
    "Burns, thermal",
    "Other/Not Stated"
]

diagnosed_sorted = diagnosed.ix[diagnosis_order]

# Make sure we haven't forgotten a diagnosis
if len(diagnosed_sorted) != len(injuries):
    raise Exception("At least one diagnosis missing from `diagnosis_order`")

# Group into diagnoses
narratives_by_diagnosis = diagnosed_sorted.reset_index()\
    .groupby("diagnosis")["narrative"]\
    .apply(list)\
    .dropna()\
    .ix[diagnosis_order]\
    .reset_index()

# Somewhat sloppy function for giving each injury a unique id
injury_i = 0
def get_injury_i():
    global injury_i
    injury_i += 1
    return injury_i

# Hello, world
print("<ol class='bfdata-firework-list'>")
for d in narratives_by_diagnosis.values:
    diag, narr = d
    print("<h3>{0}</h3>".format(diag))
    print("".join("<li id='injury-{0}'><span>{1}</span></li>".format(get_injury_i(), n) for n in narr))
print("</ol>")
