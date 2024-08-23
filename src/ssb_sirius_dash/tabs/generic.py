import dash_ag_grid as dag
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

input_options = {
    "orgb": Input("var-bedrift", "value"),
    "orgf": Input("var-foretak", "value"),
    "oppgavegiver": Input("var-oppgavegiver", "value"),
    "skjemaident": Input("var-skjemaident", "value"),
}

states_options = [
    {
        "aar": ("var-aar", "value"),
        "termin": ("var-termin", "value"),
        "nace": ("var-nace", "value"),
    }
]


class EditingTable:
    def __init__(
        self,
        label,
        database,
        tables,
        var_input,
        states,
        get_data_func,
        update_table_func,
    ):
        dropdown_options = [{"label": table, "value": table} for table in tables]

        self.selected_ident = input_options[var_input]
        self.states = states
        self.get_data = get_data_func
        self.update_table = update_table_func
        self.database = database
        self.dropdown_options = dropdown_options
        self.callbacks()
        self.label = label

    def layout(self):
        layout = html.Div(
            style={"height": "100vh", "display": "flex", "flexDirection": "column"},
            children=[
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="tab-tabelleditering-dd1",
                            options=self.dropdown_options,
                            value=self.dropdown_options[0]["value"],
                            placeholder="Velg tabell",
                            className="dbc",
                        ),
                        dag.AgGrid(
                            defaultColDef={"editable": True},
                            id="tab-tabelleditering-table1",
                            className="ag-theme-alpine-dark header-style-on-filter",
                        ),
                        html.P(id="tab-tabelleditering-status1"),
                    ],
                ),
            ],
        )
        return layout

    def callbacks(self):
        states_dict = states_options[0]
        dynamic_states = [
            State(states_dict[key][0], states_dict[key][1]) for key in self.states
        ]

        @callback(
            Output("tab-tabelleditering-table1", "rowData"),
            Output("tab-tabelleditering-table1", "columnDefs"),
            Input("tab-tabelleditering-dd1", "value"),
            self.selected_ident,
            *dynamic_states,
        )
        def load_ag_grid(tabell, ident, *dynamic_states):
            states_values = dynamic_states[: len(self.states)]
            state_params = {
                key: value for key, value in zip(self.states, states_values)
            }

            args = []
            for key in self.states:
                var = state_params.get(key)
                if var is not None:
                    args.append(var)
            if "nace" in state_params and state_params["nace"] is not None:
                n = len(state_params["nace"])
                args.append(n)
            df = self.get_data(self.database, ident, tabell, *args)
            columns = [
                {
                    "headerName": col,
                    "field": col,
                    "hide": True if col == "row_id" else False,
                }
                for col in df.columns
            ]
            columns[0]["checkboxSelection"] = True
            columns[0]["headerCheckboxSelection"] = True
            return df.to_dict("records"), columns

        @callback(
            Output("tab-tabelleditering-status1", "children"),
            Input("tab-tabelleditering-table1", "cellValueChanged"),
            State("tab-tabelleditering-dd1", "value"),
            *dynamic_states,
        )
        def update_table(edited, tabell, *dynamic_states):
            states_values = dynamic_states[: len(self.states)]
            state_params = {
                key: value for key, value in zip(self.states, states_values)
            }

            args = []
            for key in self.states:
                var = state_params.get(key)
                if var is not None:
                    args.append(var)
            variable = edited[0]["colId"]
            old_value = edited[0]["oldValue"]
            new_value = edited[0]["value"]
            row_id = edited[0]["data"]["row_id"]
            try:
                self.update_table(
                    self.database, variable, new_value, row_id, tabell, *args
                )
                return f"{variable} updatert fra {old_value} til {new_value}"
            except:
                return "Error"