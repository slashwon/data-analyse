import pprint as p

import check_data as cd
import constant as cons
import dao


def main():
    count_uniq_user = get_count_uniq_user()
    p.pprint("Count of unique user = "+str(count_uniq_user))

    raw = get_tag_attribute()
    # p.pprint(raw)

    raw = get_count_for_some_place(['highway','shop'])
    p.pprint('Number of highway: '+str(raw[0])+" ; Number of shop: "+str(raw[1]))

    # query number of nodes(1304097) and ways(168667)
    counts = get_data_count(('nodes','ways'))
    p.pprint("number of Nodes :"+str(counts[0])+"; number of ways:"+str(counts[1]))

def parse(datas):
    """
    解析查询结果
    """
    for data in datas :
        if not cd.check_timestamp(data[1]):
            p.pprint("数据非法")
            p.pprint(data)
    pass

def get_tag_attribute():
    query = dao.get_query_where(cons.TB_NODETAGS, (cons.KEY_KEY, 'count(*) as count'), None, None, 'group by ' + cons.KEY_KEY + ' order by count desc')
    raw = query_and_print(query)
    return raw

def get_count_for_some_place(names):
    """
    查询某些地点的个数
    :param names: 
    :return: 
    """
    where_sentence = ''
    for name in names:
        where_sentence += ' key = \''
        where_sentence += name +'\''
        where_sentence += ' or '
    where_sentence = where_sentence[:-3]
    p.pprint(where_sentence)
    query = 'select key, count(*) as count from nodes_tags where '+where_sentence+' group by key order by count desc'
    p.pprint(query)
    return query_and_print(query)

def get_count_uniq_user():
    """
    获取唯一用户的数量的查询语句
    """
    # query = dao.get_query_where(cons.TB_NODES,(cons.KEY_ID,'count(*) as count'),None,None,'group by '+cons.KEY_ID+' order by count desc')
    query = dao.get_query_where(cons.TB_NODES, ('distinct user',), None, None, '')
    raw = query_and_print(query)
    return len(raw)

def get_data_count(tbnames):
    counts=[]
    for tb in tbnames:
        raw = dao.query('select * from ' + tb)
        counts.append(len(raw))
    return counts

def query_and_print(query):
    raw = dao.query(query)
    # p.pprint(raw)
    # p.pprint(len(raw)) #1972
    return raw


if __name__ == '__main__':
    main()
