# %%
import numpy as np
import pandas as pd

from ssb_sirius_dash import ControlType
from ssb_sirius_dash import automatisk_oppretting
from ssb_sirius_dash import kontroll
from ssb_sirius_dash import create_quality_report

# %%
eksempel_data = pd.DataFrame(
    {"Alder": [120, 90, -50, 10, 20, 40], "ident": [1, 2, 3, 4, 5, 6]}
)


# %%
@control(
    id_column="ident",
    result_type=ControlType.MULIG_FEIL,
    error_description="Veldig høy alder",
)
def min_kontrollfunksjon_1(data):
    """Sjekker etter ekstremt høy alder"""
    data["utslag"] = False
    betingelse = data["Alder"] > 100
    data.loc[betingelse, "utslag"] = True
    return data


@control(
    id_column="ident",
    result_type=ControlType.ABSOLUTT_FEIL,
    error_description="Ugyldig verdi",
)
def min_kontrollfunksjon_2(data):
    """Sjekker at alder har gyldig verdi"""
    data["utslag"] = False
    betingelse = data["Alder"] < 0
    data.loc[betingelse, "utslag"] = True
    data = min_kontrollfunksjon_2_automatisk_retting(data)
    return data


@automatisk_oppretting(
    id_column="ident", correction_description="Erstatter ugyldig alder med nan"
)
def min_kontrollfunksjon_2_automatisk_retting(data):
    data["maskinelt_rettet"] = False
    betingelse = data["utslag"] == True
    data.loc[betingelse, "Alder"] = np.nan
    data.loc[betingelse, "maskinelt_rettet"] = True
    return data


# %%
min_kontrollfunksjon_1(eksempel_data[eksempel_data["Alder"].notna()])
min_kontrollfunksjon_2(eksempel_data)

# %%
feilrapport, kontrollrapport = create_quality_report(
    statistics_name="Demo",
    data_location="path/to/data",
    data_period="2024K1",
)

# %%
feilrapport.to_dict()

# %%
pd.DataFrame().from_dict(feilrapport.to_dict()["kontrollutslag"])

# %%
pd.DataFrame().from_dict(feilrapport.to_dict()["kontrolldokumentasjon"], orient="index")

# %%
kontrollrapport

# %%
