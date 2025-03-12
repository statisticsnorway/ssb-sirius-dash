# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.7
#   kernelspec:
#     display_name: ssb-sirius-dash
#     language: python
#     name: ssb-sirius-dash
# ---

# %%
import logging
from typing import Any

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from scipy.stats import norm
import plotly.express as px
import plotly.graph_objects as go
from dash import callback
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

#from ssb_sirius_dash.utils.functions import sidebar_button

# %%
import eimerdb as db
bucket = "ssb-dapla-felles-data-produkt-prod"
db_name = "produksjonstilskudd"
conn = db.EimerDBInstance(bucket, db_name)

# %%
list(conn.query("SELECT DISTINCT(variable) FROM skjemadata")["variable"].unique())

# %%
variable = "totalareal"


# %%
def get_pivot_data(variable):
    df = conn.query(f"SELECT * FROM skjemadata WHERE variable = '{variable}'")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    
    enhetsinfo = conn.query("SELECT * FROM enhetsinfo")
    
    enhetsinfo = enhetsinfo[enhetsinfo["variable"] == "kommunenr"].assign(kommunenr = lambda x: x["value"].str.zfill(4))
    
    dff = df.merge(enhetsinfo[["orgnr", "soeknads_aar", "kommunenr"]], on = ["orgnr", "soeknads_aar"])

# %%
#dff.pivot_table(index=["soeknads_aar", "kommunenr"], columns=[], values = "value", aggfunc="sum")

# %%
#df[["value"]].describe()

# %%
#px.histogram(df, x="value")

# %%
