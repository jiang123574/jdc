import sqlalchemy as sqla
import pandas as pd
import configparser


def config():
    cp = configparser.RawConfigParser()
    cp.read('config.ini')
    sqlservice=cp.get('sql', 'sql')
    tgt = cp.get('jdc', 'WSKEY')
    return sqlservice,tgt

def read_sql(sql_tab, inorout, model="append", data=0, ):
    engine = sqla.create_engine(config()[0], pool_timeout=30)
    con = engine.connect()
    if inorout == "out":
        read_data = pd.read_sql('select * from %s' % sql_tab, engine)
        return read_data
    elif inorout == "in":
        data.to_sql(name=sql_tab, con=con, if_exists=model, index=False)
        return "写入数据库成功"


if __name__ == "__main__":
    print(read_sql("name", "in",'replace',))
