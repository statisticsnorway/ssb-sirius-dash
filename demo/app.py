# +
import os

import ssb_sirius_dash

port = 8069
service_prefix = os.getenv("JUPYTERHUB_SERVICE_PREFIX", "/")
domain = os.getenv("JUPYTERHUB_HTTP_REFERER", None)
app = ssb_sirius_dash.app_setup(port, service_prefix, domain, "superhero")

# +
import pandas as pd
import numpy as np

# Set up the parameters
num_idents = 3
budgetary_terms = ["revenue", "expenses", "profit", "taxes", "assets"]
num_felts = len(budgetary_terms)

# Generate the 'ident' column (10 idents, repeated for each budgetary term)
idents = np.repeat([f"orgnr_{i}" for i in range(1, num_idents + 1)], num_felts)

# Generate the 'felt' column (repeat each budgetary term for each ident)
felt_col = budgetary_terms * num_idents

# Generate the 'value' column with random numerical values
values = np.random.randint(1, 100, size=num_idents * num_felts)

# Create the DataFrame
df = pd.DataFrame({"orgnr": idents, "felt": felt_col, "belop": values})
# -

enheter = ["971526920", "972417807", "944117784"]
df["orgnr"] = df["orgnr"].replace(
    {"orgnr_1": "971526920", "orgnr_2": "972417807", "orgnr_3": "944117784"}
)
df

# +
import duckdb

# Create an in-memory DuckDB connection
con = duckdb.connect(database=":memory:")

# Example: Create a table and insert data
con.execute("CREATE TABLE example (id INTEGER, name STRING)")
con.execute("INSERT INTO example VALUES (1, 'Alice'), (2, 'Bob')")

# Query the table
results = con.execute("SELECT * FROM example").fetchall()

# Print the results
print(results)

# -

ssb_sirius_dash.main_layout(modal_list=[], tab_list=[], variable_list=[])

if __name__ == "__main__":
    app.run(debug=True, port=port, jupyter_server_url=domain, jupyter_mode="tab")
