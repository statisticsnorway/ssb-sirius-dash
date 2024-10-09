# +
import os

import ssb_sirius_dash

port = 8069
service_prefix = os.getenv("JUPYTERHUB_SERVICE_PREFIX", "/")
domain = os.getenv("JUPYTERHUB_HTTP_REFERER", None)
app = ssb_sirius_dash.app_setup(port, service_prefix, domain, "superhero")
# -

ssb_sirius_dash.main_layout(modal_list=[], tab_list=[], variable_list=[])

if __name__ == "__main__":
    app.run(debug=True, port=port, jupyter_server_url=domain, jupyter_mode="tab")
