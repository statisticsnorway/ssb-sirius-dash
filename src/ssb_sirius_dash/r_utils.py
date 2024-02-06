from rpy2.robjects.packages import importr, InstalledSTPackage
import timeit
import logging

logger = logging.getLogger(__name__)

# Global variable to store the R package Kostra
_kostra_r: InstalledSTPackage | None = None


def get_kostra_r() -> InstalledSTPackage:
    """
    Loads the R package Kostra

    :return: Kostra
    """
    if _kostra_r is not None:
        return _kostra_r

    start_time = timeit.default_timer()
    globals()["_kostra_r"] = importr("Kostra")
    logger.info("Finished loading Kostra in %3g seconds", (timeit.default_timer() - start_time))
    return globals()["_kostra_r"]
