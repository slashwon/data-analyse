import csv
import pprint
import re
import xml.etree.ElementTree as et
import dao
import common_tools as ct

OUTPUT_NODES = 'nodes.csv'
OUTPUT_NODETAGS = 'nodetags.csv'
OUTPUT_WAYS = 'ways.csv'
OUTPUT_WAYTAGS = 'waytag.csv'
OUTPUT_WAYNODES = 'waynodes.csv'

INPUT_FILE='map_bj.osm'
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def find_tags(root):
    """
    查找tag节点
    :param root: 
    :return: 
    """
    tags = set()
    for child in root.iter():
        tag = child.tag
        tags.add(tag)
    return tags

def __get_root__(input_file):
    """
    获取指定文件下的根节点
    :param input_file: 指定的.osm文件
    :return: 返回根节点
    """
    tree = et.parse(input_file)
    root = tree.getroot()
    return root

def audit_element_key(root):
    """
    审查标签key是否合法
    root xml/osm的根元素
    """
    keys = {"lower":set(),'lower_colon':set(),'problemchars':set(),'others':set()}
    for child in root.iter():
        if child.tag == 'tag':
            k_value = child.get('k')
            if re.match(lower, k_value):
                keys['lower'].add(k_value)
            elif re.match('lower_colon', k_value):
                keys['lower_colon'].add(k_value)
            elif re.match('problemchars',k_value):
                keys['problemchars'].add(k_value)
            else:
                keys['others'].add(k_value)
    return keys

nodes_keys = ['id','lat','lon','user','uid','version','changeset','timestamp']
nodes_tags_keys = ['id','key','value','type']
ways_keys = ['id','user','uid','version','changeset','timestamp']
ways_tags_keys = nodes_tags_keys
ways_nodes_keys=['id','node_id','position']

def get_data_model_nodes(root):
    """
    整理数据模型
    """
    nodes =  []
    for child in root.iter('node'):
        node = {}
        attrib = child.attrib
        try:
            node['id'] = int(attrib['id'])
            node['lat'] = float(attrib['lat']).real
            node['lon'] = float(attrib['lon']).real
            node['user'] = attrib['user']
            node['uid'] = int(attrib['uid'])
            node['version'] = int(attrib['version'])
            node['changeset'] = int(attrib['changeset'])
            node['timestamp'] = attrib['timestamp']
            nodes.append(node)
        except KeyError as keyerror:
            pprint.pprint("没有这个键"+str(keyerror))
            continue
        except ValueError as valueerror:
            pprint.pprint("转换失败"+str(valueerror))
            continue
    return nodes

def get_data_model_nodetags(root):
    """
    获取node标签下面tag的集合
    """
    nodetags = []
    for node in root.iter('node'):
        for tag in node.iter('tag'):
            tag_data={}
            # 不要含有fixme的标签数据
            if 'fixme' in tag.attrib['k'] or 'FIXME' in tag.attrib['k']:
                continue
            if ct.contain_zh(tag.attrib['k']):
                pprint.pprint(tag.attrib)
            tag_data['id'] = int(node.attrib['id'])
            tag_data['key'] = tag.attrib['k']
            tag_data['value'] = tag.attrib['v']
            tag_data['type'] = node.tag
            nodetags.append(tag_data)
    return nodetags

def get_data_mode_ways(root):
    """
    获取ways节点下的数据
    """
    ways = []
    for way in root.iter('way'):
        attrib = way.attrib
        way = {}
        try:
            way = attrib
            way['id'] = int(attrib['id'])
            way['uid'] = int(attrib['uid'])
            way['changeset'] = int(attrib['changeset'])
            ways.append(way)
        except KeyError as key:
            pprint.pprint("没有那个键"+str(key))
        except ValueError as ve:
            pprint.pprint("转换失败"+str(ve))
    return ways

def get_data_ways_tags(root):
    """
    获取way标签下的tag节点数据
    """
    waytags = []
    for way in root.iter('way'):
        for tag in way.iter('tag'):
            tagdata={}
            if 'fixme' in tag.attrib['k'] or 'FIXME' in tag.attrib['k']:
                continue
            if ct.contain_zh(tag.attrib['k']):
                pprint.pprint(tag.attrib)
            tagdata['key'] = tag.attrib['k']
            tagdata['value'] = tag.attrib['v']
            tagdata['id'] = int(way.attrib['id'])
            tagdata['type'] = way.tag
            waytags.append(tagdata)
    return waytags

def write_csv(datas,output_file, keys):
    """
    将字典列表写入csv文件
    """
    with open(output_file,'w') as fileoutput:
        writer = csv.DictWriter(fileoutput, keys)
        writer.writeheader()
        for data in datas:
            writer.writerow(data)

def __get_dict_value__(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    return None

def __insert_csv_to_db__(csv_files,tables,db='openstreetmap.db'):
    """
    将csv文件插入到数据库中
    """
    querys = ['.mode csv']

    for csv_file ,table in zip(csv_files,tables):
        querys.append('.import '+csv_file+' '+table)
    pprint.pprint(querys)
    dao.execute_multy(querys)

def test():
    """
    Test only for this module
    """
    root = __get_root__(INPUT_FILE)
    tags = find_tags(root)
    keys = audit_element_key(root)
    nodes = get_data_model_nodes(root)
    write_csv(nodes,OUTPUT_NODES,nodes_keys)
    nodetags = get_data_model_nodetags(root)
    write_csv(nodetags,OUTPUT_NODETAGS,nodes_tags_keys)
    write_csv(get_data_mode_ways(root),OUTPUT_WAYS,ways_keys)
    write_csv(get_data_ways_tags(root),OUTPUT_WAYTAGS,nodes_tags_keys)

    # csv_files = [OUTPUT_NODES, OUTPUT_NODETAGS, OUTPUT_WAYS, OUTPUT_WAYTAGS]
    # tables = ['nodes','nodes_tags','ways','ways_tags']
    # __insert_csv_to_db__(csv_files,tables)

if __name__ == '__main__':
    test()
