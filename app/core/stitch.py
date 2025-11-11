# app/core/stitch.py
from pathlib import Path
import cv2
import glob

def _list_images(folder):
    exts = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tif", "*.tiff")
    files = []
    for e in exts:
        files.extend(glob.glob(str(Path(folder) / e)))
    return sorted(files)

def stitch_from_folder(input_dir, output_path, mode="panorama", conf_thresh=0.6, work_megapix=0.6, compose_megapix=-1, verbose=True):
    """
    Cose todas las imágenes de una carpeta (ej: UNDISTORTED/) y guarda un panorama.
    Entradas:
      - input_dir (str|Path): carpeta con imágenes (ordenadas preferentemente)
      - output_path (str|Path): ruta del archivo de salida (ej: .../panorama.jpg)
      - mode: "panorama" (por defecto) o "scans"
      - conf_thresh (float): umbral de confianza del Stitcher
      - work_megapix (float): resolución de trabajo (Mpx) para etapas iniciales
      - compose_megapix (float): resolución de composición final (-1 = auto/full)
      - verbose (bool)
    Salida:
      - output_path (str): ruta escrita del panorama
    Efecto:
      - Escribe el archivo panorama en output_path.
    """
    input_dir = Path(input_dir)
    output_path = Path(output_path)

    paths = _list_images(input_dir)
    if verbose:
        print(f"[stitch] {len(paths)} imágenes en {input_dir}")
    if not paths:
        raise RuntimeError("No hay imágenes para coser.")

    imgs = []
    for p in paths:
        im = cv2.imread(p)
        if im is None:
            if verbose: print(f"[skip] No pude leer: {p}")
            continue
        imgs.append(im)

    if not imgs:
        raise RuntimeError("No pude cargar ninguna imagen válida.")

    if mode.lower() == "scans":
        stitcher = cv2.Stitcher_create(cv2.STITCHER_SCANS)
    else:
        stitcher = cv2.Stitcher_create(cv2.STITCHER_PANORAMA)

    # Ajustes útiles
    # (Nota: la API de Stitcher en OpenCV varía por versión; si tu build no expone setters,
    # puedes omitirlos sin problema.)
    try:
        stitcher.setPanoConfidenceThresh(conf_thresh)
    except Exception:
        pass
    try:
        stitcher.setSeamEstimationResol(-1)  # auto
        stitcher.setCompositingResol(-1)     # auto
        stitcher.setRegistrationResol(work_megapix)
        stitcher.setCompositingResol(compose_megapix)
    except Exception:
        pass

    if verbose:
        print("[stitch] ejecutando cosido...")
    status, pano = stitcher.stitch(imgs)
    if status != cv2.STITCHER_OK:
        raise RuntimeError(f"Stitcher error: {status}")

    ok = cv2.imwrite(str(output_path), pano)
    if not ok:
        raise RuntimeError("No pude guardar el panorama.")
    if verbose:
        h, w = pano.shape[:2]
        print(f"[stitch] listo -> {output_path} ({w}x{h})")

    return str(output_path)
