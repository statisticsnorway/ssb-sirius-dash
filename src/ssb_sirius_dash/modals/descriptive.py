import pandas as pd
import eimerdb as db

# +
import dash_ag_grid as dag


class Descriptive:

    def __init__(self):
        pass

    def layout(self):
        return html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Descriptive")),
                        dbc.ModalBody(
                            [
                                dbc.Row(dag.AgGrid(id="descriptive_table"))
                            ]
                        )
                    ]
                )
            ]
        )

    def callbacks(self):
        @callback(Output("descriptive_table", "rowData"), Output("descriptive_table", "columnDefs"))


# -

bucket = "ssb-dapla-felles-data-produkt-prod"
db_name = "produksjonstilskudd"
conn = db.EimerDBInstance(bucket, db_name)

# + active=""
# data = conn.query(f"""SELECT * FROM skjemadata WHERE soeknads_aar = '2024'""")
# df = data.pivot_table(index="orgnr", columns="variable", values="value", aggfunc="max").reset_index()
# for column in data["variable"].unique():
#     df[column] = df[column].astype(float)
# df.describe(percentiles=[.25, .5, .75]).T
# -

list(conn.query(f"""SELECT DISTINCT(variable) FROM skjemadata""")["variable"].unique())

data = conn.query(f"""SELECT soeknads_aar, orgnr, variable, value FROM skjemadata""")
data["value"] = pd.to_numeric(data["value"], errors="coerce")
data = data.dropna(subset="value")
data

data.groupby(["variable", "soeknads_aar"], as_index=False).sum().pivot_table(index = "variable", columns = "soeknads_aar", values = "value").reset_index()

data.loc[data["soeknads_aar"] == 2024].pivot_table(index = "orgnr", columns = "variable", values = "value").reset_index().describe().T


