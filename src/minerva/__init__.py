"""Minerva - Zermelo data API en import toolkit."""

# Exporteer de belangrijkste klassen en functies naar het hoogste niveau
from .Blueprints.Appointment import Appointment
from .Blueprints.Student import Student
from .ImportData.ZermeloMain import ZermeloMain
from .ImportData.MassImportAppointments import saveAll
from .ImportData.ImportStudents import saveStudents
from .helper.api import ZermeloAPIClient, ZermeloAPIError
from .ZermeloApiWrapper import configure_api_wrapper


def get_api_token(*args, **kwargs):
    """Retrieve a token with the optional Selenium-based login helper."""
    from .helper.get_api_token import get_api_token as retrieve_api_token

    return retrieve_api_token(*args, **kwargs)


def get_api_urlpatterns():
    """Return the optional Django API URL patterns."""
    from .ZermeloApiWrapper.urls import urlpatterns

    return urlpatterns


# Optioneel: metadata
__version__ = "0.1.0"
__author__ = "Dani"

# __all__ bepaalt wat er geïmporteerd wordt bij: from minerva import *
# En het vertelt IDE's en linters wat de officiële publieke API is.
__all__ = [
    "__version__",
    "__author__",
    "Appointment",
    "Student",
    "ZermeloMain",
    "ZermeloAPIClient",
    "ZermeloAPIError",
    "saveStudents",
    "saveAll",
    "get_api_token",
    "configure_api_wrapper",
    "get_api_urlpatterns",
]   