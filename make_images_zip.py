"""
Build images.zip for Colab, containing only the images the pipeline
actually references, deduplicated, and namespaced by corpus so filenames
cannot collide between Roboflow and DFUC.

Run this LOCALLY, after notebooks 01-04 have produced the fold CSVs.

    python make_images_zip.py

Reads:
    data/interim/folds_severity.csv   (column: representative)
    data/interim/folds_infection.csv  (column: path)

Writes:
    images.zip
        roboflow/<filename>.jpg   -- one file per severity photograph
        dfuc/<filename>.jpg       -- one file per infection image

Why filtered rather than the whole raw folder
    Notebook 01 found real duplicate and near-duplicate structure in both
    corpora (2.39 augmented copies per Roboflow photograph). Zipping
    everything uploads and transfers copies the pipeline never reads.
    Zipping only what folds_*.csv reference cuts this to exactly what
    training needs.

Why two subfolders, not one flat pool
    Both corpora use the same "<id>_jpg.rf.<hash>.jpg" naming convention
    from their Roboflow exports. A filename collision between the two
    corpora is unlikely but not structurally impossible, and a collision
    would silently overwrite one image with another in a flat pool.
    Namespacing by corpus removes the risk rather than hoping it doesn't
    happen.
"""
import shutil, zipfile
from pathlib import Path
import pandas as pd

INTERIM = Path('data/interim')
SEV = INTERIM / 'folds_severity.csv'
INF = INTERIM / 'folds_infection.csv'
OUT_ZIP = Path('images.zip')

missing = [str(p) for p in [SEV, INF] if not p.exists()]
if missing:
    print('STOPPING. Missing inputs:')
    for m in missing:
        print('  -', m)
    print('Run notebooks 01-04 first.')
    raise SystemExit(1)

sev = pd.read_csv(SEV)
inf = pd.read_csv(INF)

rf_paths = sorted(set(sev.representative.tolist()))
dfuc_paths = sorted(set(inf.path.tolist()))

print(f'severity photographs (Roboflow) : {len(rf_paths):,}')
print(f'infection images (DFUC)         : {len(dfuc_paths):,}')

# check for filename collisions across the two corpora before zipping,
# since that is exactly the failure mode namespacing avoids
rf_names = {Path(p).name for p in rf_paths}
df_names = {Path(p).name for p in dfuc_paths}
collide = rf_names & df_names
if collide:
    print(f'\n{len(collide)} filenames appear in BOTH corpora.')
    print('These are namespaced into roboflow/ and dfuc/ subfolders, so no')
    print('overwrite occurs, but note it for the record:')
    for n in list(collide)[:5]:
        print('  ', n)
else:
    print('\nno filename collisions between corpora (checked before zipping)')

missing_rf = [p for p in rf_paths if not Path(p).exists()]
missing_df = [p for p in dfuc_paths if not Path(p).exists()]
if missing_rf or missing_df:
    print(f'\nWARNING: {len(missing_rf)} Roboflow + {len(missing_df)} DFUC '
          'paths do not exist on disk. They will be skipped.')

print(f'\nbuilding {OUT_ZIP} ...')
n_written = 0
with zipfile.ZipFile(OUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in rf_paths:
        if Path(p).exists():
            z.write(p, arcname=f'roboflow/{Path(p).name}')
            n_written += 1
    for p in dfuc_paths:
        if Path(p).exists():
            z.write(p, arcname=f'dfuc/{Path(p).name}')
            n_written += 1

size_mb = OUT_ZIP.stat().st_size / 1e6
print(f'wrote {OUT_ZIP.resolve()}  ({n_written:,} files, {size_mb:.0f} MB)')
print('\nupload this single file to your Drive project folder, then run')
print('05_feature_extraction_colab.ipynb from Cell 3.')
