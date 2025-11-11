# ProyectoGrafica
Estructura


product/
  README.md
  requirements.txt
  config.yaml
  .gitignore

  data/
    calib/                      ← aquí irá la calibración (intrinsics.npz)
    sessions/
      2025-11-10-lab-180/       ← crea 1 carpeta por sesión
        RAW/                    ← fotos crudas de la sesión
        UNDISTORTED/            ← (se llenará el día 2)
        CYL_WARP/               ← (se llenará en días 3–4)
        manifest.json           ← metadatos de la sesión

  viewer/
    index.html                  ← visor web (carga panorama.jpg más adelante)
    assets/                     ← (iconos, logo, css opcional)

  app/
    __init__.py
    config.py                   ← lectura de config.yaml (rutas)
    utils/
      io_utils.py               ← helpers para carpetas y manifest
    imaging/
      exif_utils.py             ← ordenar por EXIF / renombrar
      chessboard.py             ← utilidades p/ detección de tablero (D2)
      undistort.py              ← funciones de “undistort” (D2)
    cli/
      capture.py                ← opcional: captura a RAW con webcam/DSLR
      calibrate.py              ← genera intrinsics.npz (D2)
      undistort.py              ← procesa RAW → UNDISTORTED (D2)

  scripts/
    build_zip.py                ← empaquetado final (lo usarás al final)

  docs/
    tecnica/                    ← luego: documentación técnica (PDF/Latex)
    usuario/                    ← luego: guía de usuario (PDF)
    slides/                     ← luego: presentación final
