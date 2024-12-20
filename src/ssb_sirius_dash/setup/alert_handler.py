import logging

import dash_bootstrap_components as dbc
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import html

from ..utils.functions import sidebar_button

logger = logging.getLogger(__name__)


class AlertHandler:
    """Handler class to manage and display alerts within the application.

    This class provides functionality to:
    - Display alerts categorized as "info", "warning", or "danger".
    - Filter alerts based on their type using buttons.
    - Maintain a modal interface for viewing alerts.

    Methods:
        layout(): Generates the layout for the alert modal and sidebar button.
        callbacks(): Defines and registers Dash callbacks for managing alerts.
    """

    def __init__(self) -> None:
        """Initialize the AlertHandler class and set up the callbacks."""
        self.callbacks()

    def layout(self) -> html.Div:
        """Generate the layout for the alert modal and sidebar button.

        Returns:
            html.Div: The layout containing the modal and the sidebar button.
        """
        return html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Feilmeldinger")),
                        dbc.ModalBody(
                            [
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            dbc.Button(
                                                "Vis alle beskjeder",
                                                id="error_log_button_show_all",
                                            ),
                                            width="auto",  # Adjust width as needed
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "Vis kun info",
                                                id="error_log_button_show_info",
                                            ),
                                            width="auto",
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "Vis kun advarsler",
                                                id="error_log_button_show_warning",
                                            ),
                                            width="auto",
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "Vis kun feil",
                                                id="error_log_button_show_danger",
                                            ),
                                            width="auto",
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Row(html.Div(id="error_log"), className="g-3"),
                            ]
                        ),
                    ],
                    id="alerts-modal",
                    size="xl",
                    fullscreen="xxl-down",
                ),
                sidebar_button("❗", "Feilmeldinger", "sidebar-alerts-button"),
            ]
        )

    def callbacks(self) -> None:
        """Define and register the Dash callbacks for the alert modal and alerts."""

        @callback(  # type: ignore[misc]
            Output("sidebar-alerts-button", "children"),
            Input("error_log", "children"),
        )
        def feilmelding_update_button_label(alerts: list[dbc.Alert]) -> str:
            """Updates the label on the button for opening error logs with the current number of errors.

            Args:
                alerts (list): List of existing errors.

            Returns:
                str: New label with the count of errors.
            """
            return f"Feilmeldinger: {len(alerts)}"  # Should probably rather be len alert for alert in alerts where style == visible or something

        @callback(  # type: ignore[misc]
            Output("alerts-modal", "is_open"),
            Input("sidebar-alerts-button", "n_clicks"),
            State("alerts-modal", "is_open"),
        )
        def feilmelding_toggle(n: int | None, is_open: bool) -> bool:
            """Toggle the state of the modal window.

            Args:
                n (int | None): Number of clicks on the toggle button. None if never clicked.
                is_open (bool): Current state of the modal (open/closed).

            Returns:
                bool: New state of the modal (open/closed).
            """
            if n:
                return not is_open
            return is_open

        @callback(  # type: ignore[misc]
            Output("error_log", "children"),
            [
                Input("error_log_button_show_all", "n_clicks"),
                Input("error_log_button_show_info", "n_clicks"),
                Input("error_log_button_show_warning", "n_clicks"),
                Input("error_log_button_show_danger", "n_clicks"),
            ],
            State("error_log", "children"),
        )
        def filter_alerts(
            show_all: int | None,
            show_info: int | None,
            show_warning: int | None,
            show_danger: int | None,
            current_alerts: list[dbc.Alert] | None,
        ) -> list[dbc.Alert]:
            """Filter alerts based on the button clicked.

            Args:
                show_all (int | None): Clicks for "Show All" button.
                show_info (int | None): Clicks for "Show Info" button.
                show_warning (int | None): Clicks for "Show Warning" button.
                show_danger (int | None): Clicks for "Show Danger" button.
                current_alerts (list[dbc.Alert] | None): Current list of alerts.

            Returns:
                list[dbc.Alert]: Filtered alerts as a list of Dash components.

            Notes:
                - If no filters are clicked, all alerts are displayed.
                - Filters alerts by `level` ("info", "warning", "danger").
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
