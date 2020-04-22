import os
import intake
import pytest

def get_master_catalog():
    # TODO: replace with environment variable
    fname = os.path.join(os.path.dirname(__file__),
                         '../intake-catalogs/master.yaml')
    return intake.open_catalog(fname)


@pytest.fixture
def catalog():
    return get_master_catalog()


ALL_ENTRIES = list(get_master_catalog().walk(depth=10))
@pytest.mark.parametrize("dataset_name", ALL_ENTRIES)
def test_get_intake_source(catalog, dataset_name):
    item = catalog[dataset_name]
    if item.container == "catalog":
        item.reload()
    else:
        if item._driver in ["csv", "rasterio", "zarr"]:
            ds = item.to_dask()
        elif item._driver in ["intake_esm.esm_datastore", "parquet"]:
            col = item.get()
