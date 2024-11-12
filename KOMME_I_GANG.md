# Komme i gang

I denne veiledningen vil du lære det du trenger for å sette opp et eget editeringsdashbord.

Det du trenger for å starte er:
- Data på Dapla
- En datalagringsløsning (må ha annet ord her)
    - For eksempel [EimerDB](https://github.com/statisticsnorway/ssb-eimerdb)
-

Om du ønsker å lage **egne komponenter** til dashbordet eller bidra til å utvide rammeverket, se [contributor guide]. Her forklares rammeverket mer i dybden og noen valg som er tatt begrunnes.

#### Ordliste

Her finner du en kort forklaring av hva som menes med visse ord i veiledningen.

- App : Applikasjonen du setter opp
- Modul : Komponent i dashbordet
- Modal : Et vindu som inneholder en modul og åpnes med en knapp i venstre marg
- Tab : En fane i skjermbildet under variabelvelgeren som inneholder en modul

## Rammeverkets deler

Rammeverket baserer seg på at man plukker ut moduler man ønsker å bruke og at variabelvelgeren knytter disse sammen.

Som bruker kan du gjøre endringer på

![rammeverkets deler](komme_i_gang_rammeverk_deler.drawio.svg "Illustrasjon av hvordan rammeverket er satt sammen")

En modul er enten i form av en modal eller en tab.

### Variabelvelger

Dette er limet som holder applikasjonen sammen og gjør at de ulike komponentene kan dele informasjon. Den skal kunne brukes av andre moduler for å koordinere visninger mellom moduler og gjøre at du kan endre f.eks. næringskoden i variabelvelgeren, og alle skjermbilder vil vise den næringskoden.

Variabelvelgeren skal gi inputs til andre skjermbilder og fungere som et søkefelt, den skal __ikke__ brukes for å vise informasjon om enheten man er inne på.

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

## Sette opp data

### Anbefalt datastruktur

## Sette opp rammeverket

### Hvis du bruker jupyter

For å få appen til å fungere i jupyter trenger du å inkludere dette i starten
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


<!-- github-only -->
[contributor guide]: https://github.com/statisticsnorway/ssb-sirius-dash/blob/main/CONTRIBUTING.md
