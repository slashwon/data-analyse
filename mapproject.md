## OpenStreetMap Data Case Study   

---

## Map Area
##### BeiJing, China
* https://s3.amazonaws.com/mapzen.odes/ex_oMXexDr8EPEf7E8hBiT6dcKTPV2M7.osm.bz2

###### I choose this place mainly because this is where I live and work .And I'm familiar with the data shown in this map .

## Problems Encountered

---
##### **After downloading the map file ,I just parsed it with 'openstreetmap.py' instead of compressing it to a sample file with small size. And I found the data is almost clean. No format error, No date error and No overabbreviated. I just worked hard trying to find something wrong. Finally I noticed these little mistakes:**
* Some keys are marked as 'FixMe' in node 'tag';
* There are several Chinese characters in 'k';
* In 'way_tags', one value shown in Korean but it's key named 'en'

#### Here are solutions for questions above:
### 1. FIXME
##### Filter this tag with value of 'FixMe':
```
if 'fixme' in tag.attrib['k'] or \
'FIXME' in tag.attrib['k']:
          continue
```
### 2. Chinese characters:
```
疏散人数
车库
黄南苑小区
```
#### Just convert them to Chinese Pinyin.


### 3. Value spelt in Korean but its key is 'name:en'

#### Modify the key's value to 'name:korean'
```
update nodes_tags set key='name:kor' where id =273092476 and key='name:en'
```

### 4. Mainly process of my work :
* Parse the .osm file and write the data to .csv file .
* Import the .csv file into database.
* Check the data ,mainly timestamp ,to see if there is any time mistake .
* Use sql command to read from the tables .