from collections.abc import Callable

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import dcc
from dash import html
from dash.development.base_component import Component
from dash.exceptions import PreventUpdate

from ..control.framework import Kvalitetsrapport
from .modal_functions import sidebar_button


class KvalitetsindikatorerModule:
    """Class for å sette opp visningen for valgte kvalitetsindikatorer.

    Attributes:
    -----------
    indicators : list
        Liste over kvalitetsindikatorer. F.eks. indicators = [KvalitetsindikatorEditeringsandel(), KvalitetsindikatorEffektaveditering()]

    Notes:
    ------
    Alle indikatorene antar et langt format på dataene med minimum ident | variabel | verdi som kolonner.
    """

    def __init__(self, indicators: list) -> None:
        """Setter opp modulen for kvalitetsindikatorer med alle valgte indikatorer."""
        self.indicators = indicators
        self.callbacks()

    def layout(self) -> Component:
        """Lager layouten til kvalitetsindikator modalen."""
        return html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader([dbc.ModalTitle("kvalitetsindikatorer")]),
                        dbc.ModalBody(
                            [
                                html.Div(
                                    [indicator.card for indicator in self.indicators],
                                    style={
                                        "display": "grid",
                                        "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
                                        "gridGap": "20px",
                                    },
                                )
                            ]
                        ),
                    ],
                    id="kvalitetsindikatorer-modal",
                    size="xl",
                    fullscreen="xxl-down",
                ),
                sidebar_button(
                    "🎯", "Kvalitetsindikatorer", "sidebar-kvalitetsindikatorer-button"
                ),
            ]
        )

    def callbacks(self) -> None:
        """Brukes for å gjøre at modalen kan åpnes."""

        @callback(
            Output("kvalitetsindikatorer-modal", "is_open"),
            Input("sidebar-kvalitetsindikatorer-button", "n_clicks"),
            State("kvalitetsindikatorer-modal", "is_open"),
        )
        def kvalitetsindikatorermodal_toggle(n: int, is_open: bool) -> bool:
            """Åpner og lukker modalen."""
            if n:
                return not is_open
            return is_open


class KvalitetsindikatorEditeringsandel:
    """Kvalitetsindikator for editeringsandel.

    Attributes:
    -----------
    get_current_data_func: Callable
        Funksjon som henter nåværende data.
    get_change_data_func: Callable
        Funksjon som henter rader med endringer
    periode:
        Gjeldende periode
    var_name: str
        Navnet på kolonnen i datasettet som sier hvilken variabel verdien tilhører.
    ident_var: str
        Variabelnavn på identifikasjonsvariabelen. F.eks. orgf
    grouping_vars: list[str]
        Variabler som datasettet kan grupperes etter. F.eks. nace eller kommune
    key_vars: list[str]
        Viktige variabler som kvalitetsindikatoren
    """

    def __init__(
        self,
        get_current_data_func: Callable,
        get_change_data_func: Callable,
        var_name: str,
        ident_var: str,
        grouping_vars: list[str] | None = None,
        key_vars: list[str] | None = None,
    ) -> None:
        """Setter opp visningen for editeringsandel i kvalitetsindikator modalen."""
        self.ident_var = ident_var
        self.var_name = var_name
        self.grouping_vars = grouping_vars if grouping_vars else []
        self.get_current_data = get_current_data_func
        self.get_change_data = get_change_data_func
        if key_vars:
            self.key_vars = key_vars  # TODO

        self.callbacks()

        self.card = html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H5("1 - Editeringsandel", className="card-title"),
                                dcc.Graph(
                                    figure=go.Figure(
                                        go.Indicator(
                                            mode="number+delta",
                                            value=self.editeringsandel(),
                                            number={"prefix": ""},
                                            # delta={"position": "bottom", "reference": self.editeringsandel(self.periode-1)}, # TODO
                                            domain={"x": [0, 1], "y": [0, 1]},
                                        )
                                    ).update_layout(
                                        height=150,
                                        margin=dict(l=20, r=20, t=20, b=20),
                                    ),
                                    config={"displayModeBar": False},
                                ),
                            ]
                        ),
                        dbc.CardFooter(
                            dbc.Button(
                                "Detaljer",
                                id="kvalitet-editeringsandel-button-details",
                            )
                        ),
                    ],
                    style={
                        "width": "18rem",
                        "margin": "10px",
                    },
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader("1 - Editeringsandel"),
                        dbc.ModalBody(
                            [
                                html.Div(
                                    children=[
                                        dcc.Dropdown(
                                            id="kvalitet-editeringsandel-dropdown",
                                            options=[
                                                {"label": x, "value": x}
                                                for x in [var_name, *self.grouping_vars]
                                            ],
                                        )
                                    ],
                                ),
                                dcc.Loading(
                                    id="kvalitet-editeringsandel-details",
                                ),
                            ]
                        ),
                    ],
                    id="editeringsandel-modal",
                ),
            ]
        )

    def editeringsandel(self) -> float:
        """Metode for å beregne editeringsandel."""
        total = pd.DataFrame(self.get_current_data().agg({self.ident_var: "nunique"}))
        changes = pd.DataFrame(self.get_change_data().agg({self.ident_var: "nunique"}))
        return (changes / total * 100).iloc[0][0]

    def editeringsandel_details(self, group: list[str] | str) -> pd.DataFrame:
        """Metode for å beregne editeringsandel for ulike deler av utvalget."""
        if isinstance(group, str):
            group = [group]
        total = (
            self.get_current_data()
            .groupby(group)
            .agg({self.ident_var: "nunique"})
            .rename(columns={self.ident_var: "units"})
        )
        changes = (
            self.get_change_data()
            .groupby(group)
            .agg({self.ident_var: "nunique"})
            .rename(columns={self.ident_var: "edited_units"})
        )
        c = pd.merge(total, changes, on=group, how="left").fillna(0)
        c["editeringsandel"] = c["edited_units"] / c["units"] * 100
        return c.reset_index()

    def callbacks(self) -> None:
        """Setter opp callbacks for å åpne detaljvisningen og for å velge gruppering man vil ha detaljer for."""

        @callback(
            Output("editeringsandel-modal", "is_open"),
            Input("kvalitet-editeringsandel-button-details", "n_clicks"),
            State("editeringsandel-modal", "is_open"),
        )
        def kvalitetediteringsandel_modaltoggle(n: int, is_open: bool) -> bool:
            """Åpner og lukker detalj-visningen for editeringsandel."""
            if n:
                return not is_open
            return is_open

        @callback(
            Output("kvalitet-editeringsandel-details", "children"),
            Input("kvalitet-editeringsandel-dropdown", "value"),
        )
        def editeringsandel_detailed(grouping_var: str) -> Component:
            """Kjører beregning av detaljert indikator for valgt gruppering."""
            if grouping_var:
                detail_data = self.editeringsandel_details(grouping_var, self.periode)
                return dcc.Graph(
                    figure=px.bar(
                        detail_data,
                        x="editeringsandel",
                        y=grouping_var,
                        orientation="h",
                    )
                )
            else:
                raise PreventUpdate


class KvalitetsindikatorKontrollutslagsandel:
    """Indikator for å vise andel av mulige utslag for en kontroll som slår ut.

    Kontrolldokumentasjon skal være et datasett med kolonnene vist nedenfor.
    kontroll_id | Enheter kontrollert | Kontrollutslag

    Attributes:
    -----------
    kontrolldokumentasjon: Kvalitetsrapport | None
        Kvalitetsrapport som skal brukes for beregning.
    kvalitetsrapport_path: str | None
        Filsti til lagret kvalitetsrapport i json.format på Dapla.
    """

    def __init__(
        self,
        kontrolldokumentasjon: Kvalitetsrapport | None = None,
        kvalitetsrapport_path: str | None = None,
    ) -> None:
        """Setter opp visningen for kontrollutslagsandel i kvalitetsindikator modalen."""
        if kvalitetsrapport_path and kontrolldokumentasjon:
            raise ValueError(
                "Remove either kontrolldokumentasjon or kvalitetsrapport_path. KvalitetsindikatorTreffsikkerhet() requires that only one of kontrolldokumentasjon and kvalitetsrapport_path is defined. If both are defined, it will not work."
            )
        if kvalitetsrapport_path:
            import json

            import dapla as dp

            with dp.FileClient.gcs_open(kvalitetsrapport_path, "r") as outfile:
                data = json.load(outfile)
            self.kontrolldokumentasjon = (
                pd.DataFrame(data["kontrolldokumentasjon"])
                .T.reset_index()
                .rename(columns={"index": "kontroll_id"})
            )
        elif kontrolldokumentasjon:
            self.kontrolldokumentasjon = kontrolldokumentasjon
        else:
            raise ValueError(
                "Either kontrolldokumentasjon or kvalitetsrapport_path needs to have a value."
            )
        self.kontrollutslagsandel_total, self.kontrollutslagsandel_detaljer = (
            self.kontrollutslag()
        )

        self.callbacks()

        self.card = html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H5(
                                    "2 - Kontrollutslagsandel", className="card-title"
                                ),
                                dcc.Graph(
                                    figure=go.Figure(
                                        go.Indicator(
                                            mode="number+delta",
                                            value=self.kontrollutslagsandel_total,
                                            number={"prefix": ""},
                                            # delta={"position": "bottom", "reference": self.editeringsandel(self.periode-1)}, # TODO
                                            domain={"x": [0, 1], "y": [0, 1]},
                                        )
                                    ).update_layout(
                                        height=150,
                                        margin=dict(l=20, r=20, t=20, b=20),
                                    ),
                                    config={"displayModeBar": False},
                                ),
                            ]
                        ),
                        dbc.CardFooter(
                            dbc.Button(
                                "Detaljer",
                                id="kvalitet-kontrollutslagsandel-button-details",
                            )
                        ),
                    ],
                    style={
                        "width": "18rem",
                        "margin": "10px",
                    },
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader("2 - Kontrollutslagsandel"),
                        dbc.ModalBody(
                            [
                                html.Div(
                                    children=[
                                        dag.AgGrid(
                                            columnDefs=[
                                                {"field": x}
                                                for x in self.kontrollutslagsandel_detaljer[
                                                    [
                                                        "kontroll_id",
                                                        "kontrollutslagsandel",
                                                        "Enheter kontrollert",
                                                        "Kontrollutslag",
                                                    ]
                                                ].columns
                                            ],
                                            rowData=self.kontrollutslagsandel_detaljer[
                                                [
                                                    "kontroll_id",
                                                    "kontrollutslagsandel",
                                                    "Enheter kontrollert",
                                                    "Kontrollutslag",
                                                ]
                                            ].to_dict("records"),
                                        )
                                    ],
                                ),
                                dcc.Loading(
                                    id="kvalitet-kontrollutslagsandel-details",
                                ),
                            ]
                        ),
                    ],
                    id="kontrollutslagsandel-modal",
                ),
            ]
        )

    def kontrollutslag(self) -> tuple[float, pd.DataFrame]:
        """Beregner andelen kontrollutslag basert på kontrolldokumentasjonen."""
        total = (
            self.kontrolldokumentasjon["Kontrollutslag"].sum()
            / self.kontrolldokumentasjon["Enheter kontrollert"].sum()
        )

        self.kontrolldokumentasjon["kontrollutslagsandel"] = (
            self.kontrolldokumentasjon["Kontrollutslag"]
            / self.kontrolldokumentasjon["Enheter kontrollert"]
        )

        return total, self.kontrolldokumentasjon

    def callbacks(self) -> None:
        """Funksjon som brukes for å lage callback for åpning og lukking av detaljert visning."""

        @callback(
            Output("kontrollutslagsandel-modal", "is_open"),
            Input("kvalitet-kontrollutslagsandel-button-details", "n_clicks"),
            State("kontrollutslagsandel-modal", "is_open"),
        )
        def kvalitetkontrollutslagsandel_modaltoggle(n: int, is_open: bool) -> bool:
            """Åpner eller lukker modalen med detaljer."""
            if n:
                return not is_open
            return is_open


class KvalitetsindikatorEffektaveditering:
    """Indikator for å vise effekten av editering som er gjort.

    Attributes:
    -----------
    get_current_data_func: Callable
        Funksjon for å hente nåværende oppdatert data
    get_original_data_func: Callable
        Funksjon for å hente originalt mottatt data
    periode: str | int  # TODO sjekk dette
        Perioden det gjelder
    ident_var: str
        Variabelnavn på identifikasjonsvariabelen. F.eks. orgf
    key_vars: list[str]
        Liste over de viktigste variablene for indikatoren
    grouping_vars: list[str]
        Liste over grupperingsvariabler for stratum.
    """

    def __init__(
        self,
        get_current_data_func: Callable,
        get_original_data_func: Callable,
        periode: str | int,  # TODO sjekk dette
        ident_var: str,
        key_vars: list[str],
        grouping_vars: list[str],
    ) -> None:
        """Setter opp visningen for effekt av editering i kvalitetsindikator modalen."""
        self.get_current_data = get_current_data_func
        self.get_original_data = get_original_data_func
        self.periode = periode
        self.ident_var = ident_var
        self.key_vars = key_vars
        if isinstance(grouping_vars, str):
            grouping_vars = [grouping_vars]
        self.grouping_vars = grouping_vars if grouping_vars else []

        self.callbacks()

        self.card = html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H5(
                                    "4 - Effekten av editering", className="card-title"
                                ),
                                dcc.Graph(
                                    figure=go.Figure(
                                        go.Indicator(
                                            mode="number+delta",
                                            value=self.get_comparison_data(
                                                self.periode
                                            )["effekt av editering"][0],
                                            number={"prefix": ""},
                                            # delta={"position": "bottom", "reference": self.editeringsandel(self.periode-1)}, # TODO
                                            domain={"x": [0, 1], "y": [0, 1]},
                                        )
                                    ).update_layout(
                                        height=150,
                                        margin=dict(l=20, r=20, t=20, b=20),
                                    ),
                                    config={"displayModeBar": False},
                                ),
                            ]
                        ),
                        dbc.CardFooter(
                            dbc.Button(
                                "Detaljer",
                                id="kvalitet-effekt-button-details",
                            )
                        ),
                    ],
                    style={
                        "width": "18rem",
                        "margin": "10px",
                    },
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader("4 - Effekten av editering"),
                        dbc.ModalBody(
                            [
                                html.Div(
                                    children=[
                                        dcc.Dropdown(
                                            id="kvalitet-effekt-dropdown",
                                            options=[
                                                {"label": x, "value": x}
                                                for x in [*grouping_vars]
                                            ],
                                        )
                                    ],
                                ),
                                dcc.Loading(
                                    id="kvalitet-effekt-details",
                                ),
                            ]
                        ),
                    ],
                    id="effekt-modal",
                ),
            ]
        )

    def get_comparison_data(
        self, periode: str | int, grouping: list[str] | None = None
    ) -> pd.DataFrame:
        """Bruker innsendte funksjoner for å beregne effekten av editeringer som er gjort."""
        if grouping is None:
            grouping = []
        elif isinstance(grouping, str):
            grouping = [grouping]
        edited = (
            self.get_current_data()
            .melt(id_vars=[self.ident_var, *grouping], value_vars=self.key_vars)
            .groupby([*grouping, "variable"])
            .agg({"value": "sum"})
            .rename(columns={"value": "editert"})
            .reset_index()
        )

        ueditert = (
            self.get_original_data()
            .melt(id_vars=[self.ident_var, *grouping], value_vars=self.key_vars)
            .groupby([*grouping, "variable"])
            .agg({"value": "sum"})
            .rename(columns={"value": "ueditert"})
            .reset_index()
        )

        merged = edited.merge(ueditert, on=[*grouping, "variable"])

        merged["effekt av editering"] = (
            (merged["ueditert"] - merged["editert"]) / merged["editert"] * 100
        )

        return merged

    def callbacks(self) -> None:
        """Funksjon som brukes for å lage callback for åpning og lukking av detaljert visning."""

        @callback(
            Output("effekt-modal", "is_open"),
            Input("kvalitet-effekt-button-details", "n_clicks"),
            State("effekt-modal", "is_open"),
        )
        def kvaliteteffekt_modaltoggle(n: int, is_open: bool) -> bool:
            """Åpner og lukker modalen som viser detaljer for indikatoren."""
            if n:
                return not is_open
            return is_open

        @callback(
            Output("kvalitet-effekt-details", "children"),
            Input("kvalitet-effekt-dropdown", "value"),
        )
        def kvalitet_effekt_detailed(grouping_var: str | None) -> Component:
            """Funksjon som beregner indikatoren per gruppe i gruppe-inndelingen som er valgt."""
            if grouping_var:
                detail_data = self.get_comparison_data(self.periode, grouping_var)
                return dcc.Graph(
                    figure=px.bar(
                        detail_data,
                        x="effekt av editering",
                        y=grouping_var,
                        orientation="h",
                    )
                )
            else:
                raise PreventUpdate


class KvalitetsindikatorTreffsikkerhet:
    """Indikator for å vise treffsikkerheten til kontroller man kjører.

    Attributes:
    -----------
    get_edits_list_func: Callable
        Funksjon som henter liste over endringer som er gjort i dataene.
        Den skal returnere en liste med tuples som beskriver endrede felter. Dette brukes for å sjekke mot kontrollutslagene for å se hvor disse identifikasjon og variabel kombinasjonene dukker opp og se om kontrollutslaget sannsynligvis førte til en editering.
        Eks: [(orgnr_1, variabel_1), (orgnr_1, variabel_2), (orgnr_2, variabel_1)]
    kvalitetsrapport: Kvalitetsrapport | None
        Kvalitetsrapport som skal brukes for beregning.
    kvalitetsrapport_path: str | None
        Filsti til lagret kvalitetsrapport i json.format på Dapla.
    """

    def __init__(
        self,
        get_edits_list_func: Callable,
        kvalitetsrapport: Kvalitetsrapport | None = None,
        kvalitetsrapport_path: str | None = None,
    ) -> None:
        """Setter opp visningen for effekt av editering i kvalitetsindikator modalen."""
        if kvalitetsrapport_path and kvalitetsrapport:
            raise ValueError(
                "Remove either kvalitetsrapport or kvalitetsrapport_path. KvalitetsindikatorTreffsikkerhet() requires that only one of kvalitetsrapport and kvalitetsrapport_path is defined. If both are defined, it will not work."
            )
        if kvalitetsrapport_path:
            import json

            import dapla as dp

            with dp.FileClient.gcs_open(kvalitetsrapport_path, "r") as outfile:
                data = json.load(outfile)
            self.kvalitetsrapport = data
        elif kvalitetsrapport:
            self.kvalitetsrapport = kvalitetsrapport
        else:
            raise ValueError(
                "Either kvalitetsrapport or kvalitetsrapport_path needs to have a value."
            )
        self.get_edits_list_func = get_edits_list_func

        self.treffsikkerhet = self.beregn_treffsikkerhet()

        self.card = html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H5("26 - Treffsikkerhet", className="card-title"),
                                dcc.Graph(
                                    figure=go.Figure(
                                        go.Indicator(
                                            mode="number+delta",
                                            value=self.treffsikkerhet["total"],
                                            number={"prefix": ""},
                                            # delta={"position": "bottom", "reference": self.editeringsandel(self.periode-1)}, # TODO
                                            domain={"x": [0, 1], "y": [0, 1]},
                                        )
                                    ).update_layout(
                                        height=150,
                                        margin=dict(l=20, r=20, t=20, b=20),
                                    ),
                                    config={"displayModeBar": False},
                                ),
                            ]
                        ),
                        dbc.CardFooter(
                            dbc.Button(
                                "Detaljer",
                                id="kvalitet-treffsikkerhet-button-details",
                            )
                        ),
                    ],
                    style={
                        "width": "18rem",
                        "margin": "10px",
                    },
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader("26 - Treffsikkerhet"),
                        dbc.ModalBody(
                            [
                                html.Div(
                                    dcc.Graph(
                                        figure=px.bar(
                                            y=self.treffsikkerhet.keys(),
                                            x=self.treffsikkerhet.values(),
                                            orientation="h",
                                        )
                                    )
                                ),
                            ]
                        ),
                    ],
                    id="treffsikkerhet-modal",
                ),
            ]
        )

        self.callbacks()

    def beregn_treffsikkerhet(self) -> dict:
        """Beregner treffsikkerhet indikatoren basert på kvalitetsrapport."""
        if isinstance(self.kvalitetsrapport, Kvalitetsrapport):
            kvalitetsrapport = self.kvalitetsrapport.to_dict()
        else:
            kvalitetsrapport = self.kvalitetsrapport
        edits = self.get_edits_list_func()
        treffsikkerhet = {}
        total_kontrollutslag = 0
        total_celler_markert_editert = 0
        for i in kvalitetsrapport["kontrolldokumentasjon"]:
            kontrollutslag = kvalitetsrapport["kontrolldokumentasjon"][i][
                "Kontrollutslag"
            ]
            total_kontrollutslag = total_kontrollutslag + kontrollutslag
            celler_markert = [
                (x["observasjon_id"], var)
                for x in kvalitetsrapport["kontrollutslag"]
                if x["kontrollnavn"] == i
                for var in x["relevante_variabler"]
            ]
            celler_markert_editert = len([x for x in edits if x in celler_markert])
            total_celler_markert_editert = (
                total_celler_markert_editert + celler_markert_editert
            )
            treffsikkerhet[i] = (celler_markert_editert / kontrollutslag) * 100
        treffsikkerhet["total"] = (
            total_celler_markert_editert / total_kontrollutslag
        ) * 100
        return treffsikkerhet

    def callbacks(self) -> None:
        """Funksjon som brukes for å lage callback for åpning og lukking av detaljert visning."""

        @callback(
            Output("treffsikkerhet-modal", "is_open"),
            Input("kvalitet-treffsikkerhet-button-details", "n_clicks"),
            State("treffsikkerhet-modal", "is_open"),
        )
        def kvalitettreffsikkerhet_modaltoggle(n: int, is_open: bool) -> bool:
            """Åpner og lukker detaljert visning."""
            if n:
                return not is_open
            return is_open
