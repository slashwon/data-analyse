KEY_ID = 'id'
KEY_LAT='lat'
KEY_LON='lon'
KEY_USER='user'
KEY_UID='uid'
KEY_VERSION='version'
KEY_CHANGESET='changeset'
KEY_TIMESTAMP='timestamp'
KEY_KEY='key'
KEY_VALUE='value'
TB_NODES='nodes'
TB_WAYS='ways'
TB_NODETAGS='nodes_tags'
TB_WAYSTAGS='ways_tags'

SQL_CREATE_NODES = "CREATE TABLE nodes ( \
    id INTEGER PRIMARY KEY NOT NULL, \
    lat REAL, \
    lon REAL, \
    user TEXT,\
    uid INTEGER, \
    version INTEGER, \
    changeset INTEGER,\
    timestamp TEXT\
);"

SQL_CREATE_NODES_TAGS = "CREATE TABLE nodes_tags (\
    id INTEGER,\
    key TEXT,\
    value TEXT,\
    type TEXT,\
    FOREIGN KEY (id) REFERENCES nodes(id)\
);"

SQL_CREATE_WAYS = "CREATE TABLE ways (\
    id INTEGER PRIMARY KEY NOT NULL,\
    user TEXT,\
    uid INTEGER,\
    version TEXT,\
    changeset INTEGER,\
    timestamp TEXT\
);"

SQL_CREATE_WAY_TAGS = "CREATE TABLE ways_tags (\
    id INTEGER NOT NULL,\
    key TEXT NOT NULL,\
    value TEXT NOT NULL,\
    type TEXT,\
    FOREIGN KEY (id) REFERENCES ways(id)\
);"