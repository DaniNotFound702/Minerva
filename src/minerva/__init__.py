"""Minerva - Zermelo data API en import toolkit."""

# Exporteer de belangrijkste klassen en functies naar het hoogste niveau
from .Blueprints.Appointment import Appointment
from .Blueprints.Student import Student
from .ImportData.ZermeloMain import ZermeloMain

# Optioneel: metadata
__version__ = "0.1.0"
__author__ = "Dani"

# __all__ bepaalt wat er geïmporteerd wordt bij: from minerva import *
# En het vertelt IDE's en linters wat de officiële publieke API is.
__all__ = [
    "__version__",
    "Appointment",
    "Student",
    "ZermeloMain",
]