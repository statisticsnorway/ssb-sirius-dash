# Komme i gang

I denne veiledningen vil du lære det du trenger for å sette opp et eget editeringsdashbord.

Minimum du trenger for å starte er:
- Data på Dapla
- En datalagringsløsning (må ha annet ord her)
    - For eksempel [EimerDB](https://github.com/statisticsnorway/ssb-eimerdb)
-

Om du ønsker å lage **egne komponenter** til dashbordet eller bidra til å utvide rammeverket, se [contributor guide]. Her forklares rammeverket mer i dybden og noen valg som er tatt begrunnes.

(Bilde av appen)

#### Ordliste

- App :
- Modul : Komponent i dashbordet


## Første steg er å sette opp rammeverket

### Hvis du bruker jupyter

For å få appen til å fungere i jupyter trenger du å inkludere dette
```
port = 8069
service_prefix = os.getenv("JUPYTERHUB_SERVICE_PREFIX", "/")
domain = os.getenv("JUPYTERHUB_HTTP_REFERER", None)
app = ssb_sirius_dash.app_setup(port, service_prefix, domain, "superhero")
ssb_sirius_dash.app_setup()
```

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

## Rammeverkets deler



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


<!-- github-only -->
[contributor guide]: https://github.com/statisticsnorway/ssb-sirius-dash/blob/main/CONTRIBUTING.md
