import dash_bootstrap_components as dbc
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import html

from .modal_functions import sidebar_button


class AlertHandler:
    """Handler class to keep track of alerts the app.

    In order to add an alert to this list:
    add the below to your callback:
    Output("error_log", "children",allow_duplicates=True),
    State("error_log", "children")

    Add this in the callback function:
    new_alert = dbc.Alert(
        f"{datetime.datetime.now()} - your_error_message",
        color=, # use one of "info", "warning", "danger" as the argument for color.
        dismissable=True,
    )
    return [*existing_errors, new_alert]

    """

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
                                dbc.Row(
                                    dbc.Button(
                                        "Vis alle beskjeder",
                                        id="error_log_button_show_all",
                                    ),
                                    dbc.Button(
                                        "Vis kun info", id="error_log_button_show_info"
                                    ),
                                    dbc.Button(
                                        "Vis kun advarsler",
                                        id="error_log_button_show_warning",
                                    ),
                                    dbc.Button(
                                        "Vis kun feil",
                                        id="error_log_button_show_danger",
                                    ),
                                ),
                                dbc.Row(html.Div(id="error_log")),
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

        @callback(
            Output("feilmeldinger_logg", "children"),
            [
                Input("error_log_button_show_all", "n_clicks"),
                Input("error_log_button_show_info", "n_clicks"),
                Input("error_log_button_show_warning", "n_clicks"),
                Input("error_log_button_show_danger", "n_clicks"),
            ],
            State("feilmeldinger_logg", "children"),
        )
        def filter_alerts(
            show_all: int | None,
            show_info: int | None,
            show_warning: int | None,
            show_danger: int | None,
            current_alerts: list[dict] | None,
        ) -> list[dbc.Alert]:
            """Filter alerts based on the button clicked.

            Parameters
            ----------
            show_all : Optional[int]
                Clicks for "Show All" button.
            show_info : Optional[int]
                Clicks for "Show Info" button.
            show_warning : Optional[int]
                Clicks for "Show Warning" button.
            show_danger : Optional[int]
                Clicks for "Show Danger" button.
            current_alerts : List[Dict]
                Current list of alerts.

            Returns:
            -------
            List[html.Div]
                Filtered alerts as a list of Dash components.
            """
            if not current_alerts:
                return []

            if show_info:
                level = "info"
            elif show_warning:
                level = "warning"
            elif show_danger:
                level = "danger"
            else:
                return [
                    dbc.Alert(alert["message"], color=alert["color"], dismissable=True)
                    for alert in current_alerts
                ]

            filtered_alerts = [
                alert for alert in current_alerts if alert.get("level") == level
            ]

            return [
                dbc.Alert(alert["message"], color=alert["color"], dismissable=True)
                for alert in filtered_alerts
            ]
