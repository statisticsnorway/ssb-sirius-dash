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

Rammeverket baserer seg på at man plukker ut moduler man ønsker å bruke og at variabelvelgeren knytter disse sammen. Mer om hvordan du setter opp rammeverket kommer senere, men her blir du forklart hvordan de ulike delene henger sammen.

Som bruker kan du gjøre endringer i variabelvelgeren, modalene og tabs. Det er disse tre bitene som utgjør grensesnittet.

![rammeverkets deler](Rammeverkets deler.drawio.svg "Illustrasjon av hvordan rammeverket er satt sammen")

Variabelvelgeren fungerer som et felles punkt for informasjon som skal deles mellom ulike modaler og tabs i appen. Hvis du for eksempel sjekker et skjermbilde hvor det vises en enhet som du vil se på i et annet skjermbilde, så kan du i noen moduler klikke på enheten for å få enheten sin id overført til variabelvelgeren. Variabelvelgeren vil da formidle at det er den enheten vi vil se på til de andre modulene i appen slik at alle viser den samme enheten. På samme måte, hvis du vet at det er én spesifikk enhet du skal se på kan du skrive den direkte inn i variabelvelgeren.

### Variabelvelger

Dette er limet som holder applikasjonen sammen og gjør at de ulike komponentene kan dele informasjon. Den skal brukes av andre moduler for å koordinere visninger mellom moduler og gjøre at du kan endre f.eks. næringskoden i variabelvelgeren, og alle skjermbilder vil vise informasjon om enheter med den næringskoden.

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
