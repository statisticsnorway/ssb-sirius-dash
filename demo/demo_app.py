import os

import duckdb as duckdb
import numpy as np
import pandas as pd

import ssb_sirius_dash

# +
conn = duckdb.connect()

ident_var = "foretak"
registrering_id = "nokkel"
var_name = "felt"
periode_var = "aar"

conn.execute(
    f"CREATE TABLE registrering ({registrering_id} STRING, {ident_var} STRING, {var_name} STRING)"
)

conn.execute(
    f"CREATE TABLE individdata ({registrering_id} STRING, {var_name} STRING, value TEXT)"
)

conn.execute(
    f"CREATE TABLE enhetsinfo ({periode_var} STRING, {ident_var} STRING, kilde STRING, opplysning STRING, verdi TEXT)"
)

conn.execute(
    f"CREATE TABLE kommentarfelt ({ident_var} STRING, kommentar STRING, endret_av STRING, endret_dato DATETIME)"
)

conn.execute(
    f"CREATE TABLE historikk ({registrering_id} STRING, {var_name} STRING, value TEXT, endret_av STRING, endret_dato DATETIME, operation_type STRING, process_type STRING)"
)
# -

orgnr = {
    "971526920": ["1", "2"],
    "972417807": ["3", "4"],
    "923609016": ["5", "6"],
    "883409442": ["7", "8"],
}

df = pd.DataFrame(
    [
        (k, v, year)
        for k, values in orgnr.items()
        for v, year in zip(values, [2023, 2024])
    ],
    columns=[ident_var, registrering_id, "aar"],
)
tuples = list(df.itertuples(index=False, name=None))
conn.executemany("INSERT INTO registrering VALUES (?,?,?)", tuples)

conn.query("SELECT * FROM registrering")

# +
demodata_individ = {
    registrering_id: np.repeat(list(orgnr.values()), 4),
    var_name: ["revenue", "profit", "assets", "liabilities"]
    * len(np.repeat(list(orgnr.values()), 1)),
    "value": np.random.uniform(
        100000, 5000000, size=4 * len(np.repeat(list(orgnr.values()), 1))
    ).round(2),
}

df = pd.DataFrame(demodata_individ)

tuples = list(df.itertuples(index=False, name=None))

conn.executemany("INSERT INTO individdata VALUES (?,?,?)", tuples)
# -

conn.query("SELECT * FROM individdata")

# +
demodata_enhetsinfo = {
    "periode": ["2024"] * 2 * len(orgnr.keys()),
    ident_var: list(orgnr.keys()) * 2,
    "kilde": ["brreg"] * 2 * len(orgnr.keys()),
    "opplysning": ["kommunenr"] * len(orgnr.keys()) + ["nace"] * len(orgnr.keys()),
    "verdi": ["0301", "0301", "1103", "0301", "84.110", "84.110", "06.100", "77.400"],
}


df = pd.DataFrame(demodata_enhetsinfo)

tuples = list(df.itertuples(index=False, name=None))

conn.executemany("INSERT INTO enhetsinfo VALUES (?,?,?,?,?)", tuples)

demodata_enhetsinfo = {
    "periode": ["2023"] * 2 * len(orgnr.keys()),
    ident_var: list(orgnr.keys()) * 2,
    "kilde": ["brreg"] * 2 * len(orgnr.keys()),
    "opplysning": ["kommunenr"] * len(orgnr.keys()) + ["nace"] * len(orgnr.keys()),
    "verdi": ["0301", "0301", "1103", "0301", "84.110", "84.110", "06.100", "77.400"],
}

df = pd.DataFrame(demodata_enhetsinfo)

tuples = list(df.itertuples(index=False, name=None))

conn.executemany("INSERT INTO enhetsinfo VALUES (?,?,?,?,?)", tuples)
# -

conn.query("SELECT * FROM enhetsinfo")

port = 8069
service_prefix = os.getenv("JUPYTERHUB_SERVICE_PREFIX", "/")
domain = os.getenv("JUPYTERHUB_HTTP_REFERER", None)
app = ssb_sirius_dash.app_setup(port, service_prefix, domain, "superhero")


selected_variables = ["aar", "nace", "foretak"]
variable_list = ssb_sirius_dash.generate_skjermcards(selected_variables)

visualiseringsbygger = ssb_sirius_dash.VisualiseringsbyggerModule(
    database=conn
).layout()
modal_list = [visualiseringsbygger]

vofforetaktab = ssb_sirius_dash.VoFForetakTab()
tab_list = [vofforetaktab]

app.layout = ssb_sirius_dash.main_layout(modal_list, tab_list, variable_list)

if __name__ == "__main__":
    app.run(debug=False, port=port, jupyter_server_url=domain, jupyter_mode="tab")
