"""Helper functions for redshift."""

from libs.python_db_connectors.query_redshift import connect
import core.logger as log
import numpy as np


def create_table(df, connection_profile, name_tb, schema, types, creds_or_file, is_incremental):
    """
    Creates table in redshift, full drop or incremental drop.
    types should be of sqlalchemy type. Ex: types.Date(), types.Integer()
    """
    if_exist = 'replace' if not is_incremental else 'append'
    connection = connect(db=connection_profile, creds_or_file=creds_or_file)
    chunksize = 500000
    logger.info('Sending table "{}" to redshift, mode "{}", size "{}", and chunksize "{}".'.format(name_tb, if_exist, len(df), chunksize))
    df.to_sql(name=name_tb, schema=schema, con=connection, if_exists=if_exist, dtype=types, index=False, chunksize=chunksize)
    # TODO: check df.to_sql above for long integers. Noticed long numbers where rounded.
    logger.info("Copied table to redshift '{}', using connection profile '{}'".format(name_tb, connection_profile))


logger = log.setup_logging('Redshift')

if __name__ == '__main__':
    from sqlalchemy import types
    import pandas as pd
    data = [['aaa',10],['bbb',12],['ccc',3]]
    df = pd.DataFrame(data,columns=['session_id','count_events'])
    types = {
        'session_id': types.VARCHAR(16),
        'count_events': types.Integer(),
        }
    connection_profile = 'some_connection_profile'
    name_tb = 'test_table'
    create_table(df, connection_profile, name_tb, types)
