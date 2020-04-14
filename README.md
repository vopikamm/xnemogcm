# xnemogcm

Interface to open NEMO global circulation model output dataset and create a xgcm grid.

One can be interested by the [XORCA](https://github.com/willirath/xorca)
python package, that does a similar work for
all NEMO output grid. xnemogcm is designed to be more simple
and adapted to a simple idealized configuration.

# Usage

```python
from xnemogcm import open_nemo_and_domain_cfg
ds = open_nemo_and_domain_cfg(datadir='/path/to/data')

# Interface with xgcm
from xnemogcm import get_metrics
import xgcm
grid = xgcm.Grid(ds, metrics=get_metrics(ds), periodic=False)
```

# Installation

Installation via pip:
```bash
pip install git+https://github.com/rcaneill/xnemogcm.git@master
```
