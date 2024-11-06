# Oppsett
Ta en kikk på demo/app.py for å se et eksempel!

#### Ordliste
Modul
Modal
Tab
app

### Variabelvelger
Dette er limet som holder applikasjonen sammen og gjør at de ulike komponentene kan dele informasjon.

For å sikre standardisering og gjenbruk ønsker vi ikke at hver enkelt bruker skal legge inn sine egne alternativer til variabelvelgeren. Gi beskjed hvis du mener det mangler en variabel blant alternativene, det er vanligvis lett å fikse!

### Modaler
Modaler er funksjonalitet som finnes med knapper i venstre marg. De åpner nye skjermbilder og har spesifikke bruksområder.

Et eksempel er kontroll

De settes opp i appen slik:
```
kontroll_modal = Kontroller.layout()
```
### Tabs
Tabs er faner i skjermbildet som viser mer enhet-spesifikk informasjon
## Første steg er å sette opp rammeverket
### Hvis du bruker jupyter
port = 8069
service_prefix = os.getenv("JUPYTERHUB_SERVICE_PREFIX", "/")
domain = os.getenv("JUPYTERHUB_HTTP_REFERER", None)
app = ssb_sirius_dash.app_setup(port, service_prefix, domain, "superhero")
ssb_sirius_dash.app_setup()

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
