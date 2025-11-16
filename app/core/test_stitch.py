import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.core.stitch import stitch_from_folder

stitch_from_folder(
    input_dir="/home/jazmin/Escritorio/ProyectoGrafica/data/sessions/raw2",
    output_path="/home/jazmin/Escritorio/ProyectoGrafica/data/sessions/raw2/panorama.jpg",
    mode="panorama",
    conf_thresh=0.6
)
