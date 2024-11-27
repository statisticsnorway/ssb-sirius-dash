import datetime

import dash_bootstrap_components as dbc
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import html

from .modal_functions import sidebar_button


class AlertHandler:
    """Handler class to keep track of alerts the app."""

    def __init__(self) -> None:
        """Initialize the AlertHandler class and set up the callbacks."""
        self.callbacks()

    def layout(self) -> html.Div:
        """Generate the layout for the alert modal and sidebar button.

        Returns:
        -------
        html.Div
            The layout containing the modal and the sidebar button.
        """
        return html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Feilmeldinger")),
                        dbc.ModalBody(
                            [
                                dbc.Row("Feilmeldinger"),
                                dbc.Row(
                                    dbc.Button(
                                        "Add Alert - Demo", id="add-alert-button"
                                    )
                                ),  # For demo purposes
                                dbc.Row(html.Div(id="feilmeldinger_logg", children=[])),
                            ]
                        ),
                    ],
                    id="feilmeldinger-modal",
                    size="xl",
                    fullscreen="xxl-down",
                ),
                sidebar_button("❗", "Feilmeldinger", "sidebar-feilmeldinger-button"),
            ]
        )

    def callbacks(self) -> None:
        """Define and register the Dash callbacks for the alert modal and alerts."""

        @callback(
            Output("feilmeldinger-modal", "is_open"),
            Input("sidebar-feilmeldinger-button", "n_clicks"),
            State("feilmeldinger-modal", "is_open"),
        )
        def feilmelding_toggle(n: int | None, is_open: bool) -> bool:
            """Toggle the state of the modal window.

            Parameters
            ----------
            n : int or None
                Number of clicks on the toggle button. None if never clicked.
            is_open : bool
                Current state of the modal (open/closed).

            Returns:
            -------
            bool
                New state of the modal (open/closed).
            """
            if n:
                return not is_open
            return is_open

        @callback(  # For demo purposes
            Output("feilmeldinger_logg", "children"),
            Input("add-alert-button", "n_clicks"),
            State("feilmeldinger_logg", "children"),
        )
        def add_alert(
            n_clicks: int | None, existing_errors: list[html.Div]
        ) -> list[html.Div]:
            """Add a new alert to the error log when the button is clicked.

            Parameters
            ----------
            n_clicks : int or None
                Number of clicks on the add-alert button. None if never clicked.
            existing_errors : list of html.Div
                Existing list of alerts in the error log.

            Returns:
            -------
            list of html.Div
                Updated list of alerts including the new alert if the button was clicked.
            """
            if n_clicks:
                new_alert = dbc.Alert(
                    f"{datetime.datetime.now()} - Advarsel - Add alert trykket på",
                    color="primary",
                    dismissable=True,
                )
                return [*existing_errors, new_alert]
            return existing_errors
