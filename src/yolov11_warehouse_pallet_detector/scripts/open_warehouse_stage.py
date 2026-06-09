"""Open the warehouse USD stage when Isaac Sim starts."""

import os

import omni.usd


def main():
    """Open the USD stage provided by the WAREHOUSE_USD environment variable."""
    warehouse_usd = os.environ.get('WAREHOUSE_USD')
    if not warehouse_usd:
        raise RuntimeError('WAREHOUSE_USD is not set.')

    print(f'Opening warehouse USD stage: {warehouse_usd}')
    omni.usd.get_context().open_stage(warehouse_usd)


main()
