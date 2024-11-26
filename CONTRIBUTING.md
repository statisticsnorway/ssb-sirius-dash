# Contributor Guide

Thank you for your interest in improving this project.
This project is open-source under the [MIT license] and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- [Source Code]
- [Documentation]
- [Issue Tracker]
- [Code of Conduct]

## How to report a bug

Report bugs on the [Issue Tracker].

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.

## How to request a feature

Request features on the [Issue Tracker].

## Our design and making a new module

### Should your module be a tab or a modal?

Generally, in this framework, tabs are for micro-level information while modals are more macro oriented. This is not a rule, but it is often more intuitive this way.

### The user should modify data to fit the requirements of your module

In order to keep the code easier to work with, describe how the required data should look instead of creating functionality to handle different formats. If a user wants to use your module, they need to do the legwork to make their data fit (within reason).

### Variabelvelger (variable picker)

If you need to add an alternative to the Variabelvelger, have it added into the package. In order to keep the modules cross-compatible and standardized, we do not want users to add their own custom fields.

#### Dynamic states

In order to use the Variabelvelger in modules you can use dynamic states to include fields in callbacks.

Your component should include all variabelvelger fields that can be used as a State() in your module in the way depicted below.

Firstly include the supported Variabelvelger options for your module:

    states_options = [
        {
            "aar": ("var-aar", "value"),
            "termin": ("var-termin", "value"),
            "nace": ("var-nace", "value"),
            "nspekfelt": ("var-nspekfelt", "value"),
        }
    ]

Secondly include this in the callback method in your module class.

    dynamic_states = [
        State(states_dict[key][0], states_dict[key][1])
        for key in selected_state_keys
    ]

Third add *dynamic_states in the callback to make the values included in the callback.

    @callback(
        callback_components_here,
        *dynamic_states,
    )


### The class structure

Each module is written as a class containing its layout and callbacks:

    class Module:
        def __init__(self, database):
            self.database = database
            self.callbacks()

        def layout():
            layout = html.Div(
                [
                    dbc.Modal(
                        [
                            dbc.ModalHeader(
                                [
                                    dbc.ModalTitle("MODALNAVN")
                                ]
                            ),
                            dbc.ModalBody(
                                [
                                    "Din layout her"
                                ]
                            )
                        ]
                    ),
                    sidebar_button("icon", "label", "sidebar-MODALNAVN-button")
                ]
            )

        def callbacks():
            @callback(
                Output("MODALNAVN-modal", "is_open"),
                Input("sidebar-MODALNAVN-button", "n_clicks"),
                State("MODALNAVN-modal", "is_open")
            )
            def MODALNAVN_modal_toggle(n, is_open):
                if n:
                    return not is_open
                return is_open

### Deliberate design choices

#### Include the layout as a method in the class

Our reason for having the layout returned from a method instead of an attribute of the class is that having it as a method makes it possible to pass parameters. While it is possible to modify an attribute in the __init__ we consider it more readable if layout-specific parameters can be passed to the layout directly, making it clear what it is affecting.

While not all modules will need parameters to its layout, it will be confusing for users if some layouts are attributes and some are returned from methods.

#### Use @callback

In order for this to work you need to use @callback and not @app.callback. This is to make the callback code more modular and simplifying imports.

More information: https://community.plotly.com/t/dash-2-0-prerelease-candidate-available/55861#from-dash-import-callback-clientside_callback-5

#### User defined functions

If you need the user to define a function for some use case in your module you can include user-created functions in the class by adding a parameter to the __init__:

    class Module:
        def __init__(self, database, selected_state_keys, selected_ident, variable, custom_function):
            self.database = database
            self.custom_function = custom_function
            self.callbacks(selected_state_keys, selected_ident, variable)

An example of a use-case for this is a function to get/transform data to adhere to a specific format.

#### All in one (AiO) components

As our goal is to make a library of easily reusable, customizable and expandable modules/views we have decided to avoid using AiO when possible. They require more complicated syntax and it requires more effort to understand and contribute, which we want to avoid.





## How to set up your development environment

You need Python 3.9+ and the following tools:

- [Poetry]
- [Nox]
- [nox-poetry]

Install [pipx]:

```console
python -m pip install --user pipx
python -m pipx ensurepath
```

Install [Poetry]:

```console
pipx install poetry
```

Install [Nox] and [nox-poetry]:

```console
pipx install nox
pipx inject nox nox-poetry
```

Install the pre-commit hooks

```console
nox --session=pre-commit -- install
```

Install the package with development requirements:

```console
poetry install
```

You can now run an interactive Python session, or your app:

```console
poetry run python
poetry run ssb-sirius-dash
```

## How to test the project

Run the full test suite:

```console
nox
```

List the available Nox sessions:

```console
nox --list-sessions
```

You can also run a specific Nox session.
For example, invoke the unit test suite like this:

```console
nox --session=tests
```

Unit tests are located in the _tests_ directory,
and are written using the [pytest] testing framework.

## How to submit changes

Open a [pull request] to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

To run linting and code formatting checks before committing your change, you can install pre-commit as a Git hook by running the following command:

```console
nox --session=pre-commit -- install
```

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.

[mit license]: https://opensource.org/licenses/MIT
[source code]: https://github.com/statisticsnorway/ssb-sirius-dash
[documentation]: https://statisticsnorway.github.io/ssb-sirius-dash
[issue tracker]: https://github.com/statisticsnorway/ssb-sirius-dash/issues
[pipx]: https://pipx.pypa.io/
[poetry]: https://python-poetry.org/
[nox]: https://nox.thea.codes/
[nox-poetry]: https://nox-poetry.readthedocs.io/
[pytest]: https://pytest.readthedocs.io/
[pull request]: https://github.com/statisticsnorway/ssb-sirius-dash/pulls

<!-- github-only -->

[code of conduct]: CODE_OF_CONDUCT.md
