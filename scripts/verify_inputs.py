"""Check packed source chunks and byte-identical recovery against original SHA-256."""
from pathlib import Path
import csv
import gzip
import hashlib
import json
import shutil
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data_inputs'
manifest = json.loads((DATA / 'manifest.json').read_text(encoding='utf-8'))

def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for piece in iter(lambda: f.read(1024 * 1024), b''):
            h.update(piece)
    return h.hexdigest()

def verify_format(path):
    if path.suffix == '.csv':
        with path.open(encoding='utf-8-sig', newline='') as f:
            assert {'well_ID', 'date', 'gw_level_abs'}.issubset(set(next(csv.reader(f))))
    elif path.suffix == '.parquet':
        with path.open('rb') as f:
            assert f.read(4) == b'PAR1'
            f.seek(-4, 2)
            assert f.read(4) == b'PAR1'
    elif path.suffix == '.xlsx':
        with zipfile.ZipFile(path) as z:
            assert 'xl/workbook.xml' in z.namelist()
    elif path.suffix == '.geojson':
        with path.open(encoding='utf-8') as f:
            assert 'FeatureCollection' in f.read(1000)

errors = []
with tempfile.TemporaryDirectory(prefix='grande_input_verify_') as tmp:
    for name, meta in manifest['sources'].items():
        try:
            source = DATA / meta['file']
            if meta.get('storage') == 'gzip_parts':
                packed_path = Path(tmp) / (source.name + '.gz')
                with packed_path.open('wb') as joined:
                    for part in meta['parts']:
                        p = DATA / part['file']
                        assert p.is_file(), f'Missing archived chunk {p}'
                        assert p.stat().st_size == part['bytes'], f'Incorrect size {p}'
                        assert digest(p) == part['sha256'], f'Incorrect SHA-256 {p}'
                        with p.open('rb') as f:
                            shutil.copyfileobj(f, joined, 1024 * 1024)
                source = Path(tmp) / meta['file']
                with gzip.open(packed_path, 'rb') as f, source.open('wb') as out:
                    shutil.copyfileobj(f, out, 1024 * 1024)
            assert source.is_file() and source.stat().st_size == meta['bytes'], f'Wrong size for {name}'
            assert digest(source) == meta['sha256'], f'Incorrect SHA-256 for {name}'
            verify_format(source)
            print(f'OK  {name}: {meta["bytes"]:,} original bytes, exact SHA-256')
        except Exception as exc:
            errors.append(f'{name}: {exc}')
            print(f'FAIL {name}: {exc}', file=sys.stderr)
if errors:
    sys.exit(1)
print(f'All {len(manifest["sources"])} research inputs passed lossless restoration and format checks.')
