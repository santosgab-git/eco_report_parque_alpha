# R + PYTHON
library(reticulate)

# ACTIVAR ENTORNO VIRTUAL
use_virtualenv("C:/Users/USER/Documents/GABRIEL/eco_report_parque_alpha/venv", required = TRUE)

# EJECUTAR SCRIPTS DE PROCESAMIENTO
source_python("scripts/1_cleaning.py")

source_python("scripts/2_tables.py")

source_python("scripts/3_plots.py")

