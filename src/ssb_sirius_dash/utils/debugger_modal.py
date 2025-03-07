from ..setup.variableselector import VariableSelector
from ..utils.functions import sidebar_button
from dash import Input
from dash import Output
from dash import State
from dash import callback

from dash import html
import dash_bootstrap_components as dbc
from dash import callback_context

class DebugInspector:

    def __init__(self, inputs, states):
        self.variableselector = VariableSelector(inputs, states)
        self.callbacks()
        

    def layout(self):
        return html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("DebugInspector")),
                        dbc.ModalBody(
                            [dbc.Row(id="debuggerhelper_output")]
                        )
                    ],
                    id = "debugger_modal",
                    size="xl",
                    fullscreen = "xxl-down"
                ),
                sidebar_button("🥼", "Debugger", "sidebar-debugger-button"),
            ]
        )

    def callbacks(self):
        
        dynamic_states = [
            self.variableselector.get_inputs(),
            self.variableselector.get_states(),
        ]
        @callback(  # type: ignore[misc]
            Output("debugger_modal", "is_open"),
            Input("sidebar-debugger-button", "n_clicks"),
            State("debugger_modal", "is_open"),
        )
        def debugger_toggle(n, is_open):
            if n:
                return not is_open
            return is_open
        
        @callback(Output("debuggerhelper_output", "children"), *dynamic_states)
        def debuggerhelper_dynamic_states(*args):
            ctx = callback_context  # Get callback context
        
            if not ctx.triggered:
                return "No input yet."

            return html.Div([dbc.Row([html.Plaintext(f"state: {str(x)}") for x in args]), dbc.Row(html.Plaintext(f"{ctx.inputs}, {ctx.states}"))])

