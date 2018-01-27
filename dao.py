# -*- charset=utf8 -*-
import sqlite3
import pprint

def test():
    DB = 'openstreetmp.db'
    TB_NODES_TAGS = 'nodes_tags'
    db = sqlite3.connect(DB)
    c = db.cursor()
    # get_column_name(c,'nodes')
    c.execute("pragma table_info(nodes);")
    # QUERY = "update nodes_tags set key='name:kor' where id=273092476";
    # QUERY = get_query_where(TB_NODES_TAGS,['id','key','value'],['key',],["'name:en'",])
    # c.execute(QUERY)
    # pprint.pprint(c.description)
    db.commit()
    rows = c.fetchall()
    pprint.pprint(rows)
    db.close()

def query(query,db='openstreetmp.db'):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    raw = cursor.fetchall()
    conn.close
    return raw

def get_column_name(cursor,tb_name):
    """
    获取表中的所有列名
    """
    cursor.execute("pragma table_info(tb_name);")
    print(cursor.fetchall())

def get_query_where(tbname,projections,cols,values,others):
    query = "select "
    for p in projections:
        query = query+p
        query = query+","
    query = query[:-1]
    query = query+" from "+tbname
    if cols != None and cols != '':
        " where ("
        for c ,v in zip(cols,values):
            query = query+c+"="+v+"and"
        query=query[:-3]
        query += ') '
    query += ' '
    query += others
    pprint.pprint(query)
    return query

if __name__=='__main__':
    test()
