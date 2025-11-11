# app/core/undistort.py
from pathlib import Path
import numpy as np
import cv2
import glob

def load_intrinsics(npz_path):
    """
    Lee parámetros intrínsecos desde un .npz.
    Entradas:
      - npz_path (str|Path): ruta a intrinsics.npz con K, dist, img_size, (opc) reproj_error, model.
    Salidas:
      - K (np.ndarray 3x3)
      - dist (np.ndarray Nx1)
      - img_size (tuple) -> (w, h)
    """
    data = np.load(str(npz_path))
    K = data["K"]
    dist = data["dist"]
    img_size = tuple(int(x) for x in data["img_size"])
    return K, dist, img_size

def undistort_image(img, K, dist, free_scale=0.0):
    """
    Corrige la distorsión de una imagen usando intrínsecas.
    Entradas:
      - img (np.ndarray BGR)
      - K, dist: intrínsecas
      - free_scale: 0.0 recorta un poco (menos bordes negros), 1.0 conserva más campo
    Salida:
      - img_und (np.ndarray BGR) imagen corregida
    """
    h, w = img.shape[:2]
    newK, _ = cv2.getOptimalNewCameraMatrix(K, dist, (w, h), free_scale)
    map1, map2 = cv2.initUndistortRectifyMap(K, dist, None, newK, (w, h), cv2.CV_16SC2)
    img_und = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return img_und

def _list_images(folder):
    exts = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tif", "*.tiff")
    files = []
    for e in exts:
        files.extend(glob.glob(str(Path(folder) / e)))
    return sorted(files)

def undistort_folder(raw_dir, out_dir, intrinsics_npz, free_scale=0.0, max_side=None, verbose=True):
    """
    Procesa todas las imágenes de RAW/ -> UNDISTORTED/ conservando nombres.
    Entradas:
      - raw_dir (str|Path): carpeta origen (RAW/)
      - out_dir (str|Path): carpeta destino (UNDISTORTED/)
      - intrinsics_npz (str|Path): ruta a intrinsics.npz
      - free_scale (float): 0.0..1.0 (ver undistort_image)
      - max_side (int|None): si no es None, redimensiona la imagen corregida para que
                             su lado mayor sea max_side (útil p/ahorrar RAM/tiempo)
      - verbose (bool)
    Salida:
      - count (int): número de imágenes procesadas
    Efecto:
      - Escribe archivos en out_dir con el MISMO nombre que en raw_dir.
    """
    raw_dir = Path(raw_dir); out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    K, dist, _ = load_intrinsics(intrinsics_npz)
    paths = _list_images(raw_dir)
    if verbose:
        print(f"[undistort] {len(paths)} imágenes en {raw_dir}")
    if not paths:
        return 0

    processed = 0
    for i, p in enumerate(paths, 1):
        img = cv2.imread(p)
        if img is None:
            if verbose: print(f"[skip] No pude leer: {p}")
            continue
        und = undistort_image(img, K, dist, free_scale=free_scale)

        if max_side is not None:
            h, w = und.shape[:2]
            s = max(h, w)
            if s > max_side:
                scale = max_side / float(s)
                und = cv2.resize(und, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)

        out_path = out_dir / Path(p).name
        ok = cv2.imwrite(str(out_path), und)
        if verbose:
            status = "ok" if ok else "error"
            print(f"[{status}] {i}/{len(paths)} -> {out_path.name}")
        if ok:
            processed += 1

    if verbose:
        print(f"[undistort] Listo: {out_dir}")
    return processed
