import pprint as p

import check_data as cd
import constant as cons
import dao

def main():
    # count_uniq_user = get_count_uniq_user()
    # p.pprint("Count of unique user = "+str(count_uniq_user))
    #
    # raw = get_tag_attribute()
    # # p.pprint(raw)
    #
    # raw = get_count_for_some_place(['highway','shop'])
    # p.pprint('Number of highway: '+str(raw[0])+" ; Number of shop: "+str(raw[1]))
    #
    # # query number of nodes(1304097) and ways(168667)
    # counts = get_data_count(('nodes','ways'))
    # p.pprint("number of Nodes :"+str(counts[0])+"; number of ways:"+str(counts[1]))
    audit_user_uid('nodes')

def audit_user_uid(tb):
    uid_raw = dao.my_execute("select distinct uid from "+tb)
    uid_user = {}
    for uidd in uid_raw:
        uid = uidd[0]
        if uid not in uid_user:
            uid_user[uid]=set()
        user = dao.my_execute("select user from "+tb+" where uid = \'" +str(uid)+"\'")
        for u in user:
            uid_user[uid].add(u[0])

    wrong = {}
    for uid, userset in uid_user.items():
        if len(userset)>1:
            wrong[uid]=userset

    p.pprint("有问题的uid：")
    p.pprint(wrong)
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
    query = dao.get_query_where(cons.TB_NODES, ('distinct user',), None, None, '')
    raw = query_and_print(query)
    return len(raw)

def get_data_count(tbnames):
    counts=[]
    for tb in tbnames:
        raw = dao.my_execute('select * from ' + tb)
        counts.append(len(raw))
    return counts

def query_and_print(query):
    raw = dao.my_execute(query)
    # p.pprint(raw)
    # p.pprint(len(raw)) #1972
    return raw


if __name__ == '__main__':
    main()
