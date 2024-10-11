# Oppsett
Ta en kikk på demo/app.py for å se et eksempel!

## Første steg er å sette opp rammeverket
### For jupyter
port = 8069
service_prefix = os.getenv("JUPYTERHUB_SERVICE_PREFIX", "/")
domain = os.getenv("JUPYTERHUB_HTTP_REFERER", None)
app = ssb_sirius_dash.app_setup(port, service_prefix, domain, "superhero")
ssb_sirius_dash.app_setup()

### Modaler

### Tabs

### Variabler

### Sett opp layouten
For at appen skal fungere må det settes opp en liste over modaler, tabs og variabler som skal inkluderes.

```
modals = [
    Modal_1,
    Modal_2
]

tab_list = [
    Tab_1,
    Tab_2
]

variable_list = [
    Variabel_1,
    Variabel_2
]

ssb_sirius_dash.main_layout(
    modal_list=modals,
    tab_list=tab_list,
    variable_list=variable_list
)
```
