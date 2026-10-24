"""Validate notebook JSON, source-cell syntax and expected manuscript exports."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
nb=json.loads((ROOT/'GRANDE_U_manuscript_reproducible_workflow.ipynb').read_text(encoding='utf-8'))
assert nb.get('nbformat')==4, 'Expected Jupyter v4 notebook'
code_cells=[(i, ''.join(c['source'])) for i,c in enumerate(nb['cells']) if c['cell_type']=='code']
for i, source in code_cells:
    compile(source, f'cell {i}', 'exec')
source='\n'.join(c for _,c in code_cells)
for number in range(1,10):
    label=f'Figure_{number:02d}_'
    assert label in source, f'Missing export for {label}'
for file in ['monthly_wells.csv','static_wells.xlsx','processed_grace.parquet','world_boundaries.geojson']:
    assert file in source, f'Missing input: {file}'
print(f'Notebook structure verified: {len(nb["cells"])} cells, {len(code_cells)} Python cells, 9 manuscript figures.')
