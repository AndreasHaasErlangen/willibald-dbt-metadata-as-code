import json
import sqlite3
import requests

# Load metadata from dataspot into FDM_Willibald.json
with open('credentials.json') as f:
    credentials = json.load(f)

url = "https://academy.dataspot.io/api/ahaas/schemes/FDM_Willibald/download.json?v=2"
username = credentials["username"]
password = credentials["password"]

response = requests.get(url, auth=(username, password))

if response.status_code == 200:
    json_data = response.json()
    with open('FDM_Willibald.json', 'w') as outfile:
        json.dump(json_data, outfile)    
    # Process the JSON data here
else:
    print("Error downloading JSON:", response.status_code)



# Load JSON data from file
with open('FDM_willibald.json', 'r') as f:
    data = json.load(f)

# Create SQLite database and table
conn = sqlite3.connect('dataspotparameters.db')
c = conn.cursor()

c.execute('''DROP TABLE if exists fdm_dataspot_rules;''')
c.execute('''CREATE TABLE IF NOT EXISTS fdm_dataspot_rules
             (id text, ruleOf text, stereotype text, sourcesystem text, sourcetable text, sourcecolumn text, targettable text, targetcolumn text, title text, description text, has_statustracking boolean)''')

c.execute('''DROP TABLE if exists fdm_dataspot_relationship;''')
c.execute('''CREATE TABLE IF NOT EXISTS fdm_dataspot_relationship
             (id text, table1 text, column1 text, table2 text, column2 text, linkname , has_statustracking bool, driving_key text )''')

c.execute('''DROP TABLE if exists fdm_dataspot_businessattribute;''')
c.execute('''CREATE TABLE IF NOT EXISTS fdm_dataspot_businessattribute
             (id text, hasDomain text, label text, identifying boolean)''')

c.execute('''DROP TABLE if exists fdm_dataspot_businessobject;''')
c.execute('''CREATE TABLE IF NOT EXISTS fdm_dataspot_businessobject
             (id text, label text, incollection text, is_nh_link boolean, nh_linkname text)''')

c.execute('''DROP TABLE if exists fdm_dataspot_transformation;''')
c.execute('''CREATE TABLE IF NOT EXISTS fdm_dataspot_transformation
             (id TEXT, transformationOf TEXT, label TEXT, tags TEXT, status TEXT)''')

# define views as turbovault-interface
c.execute('''drop view if exists source_data;''')
c.execute('''create view source_data as
select distinct
sourcesystem||'_'||sourcetable as source_table_identifier
, sourcesystem as source_system
, sourcetable as source_object
, 'dwh_02_load' as source_schema_physical_name
, 'load_'||sourcesystem||'_'||sourcetable as source_table_physical_name
, 'rsrc' as record_source_column
, '*/'||sourcesystem||'/'||sourcetable||'/*' as static_part_of_record_source_column
, 'ldts' as load_date_column
from fdm_dataspot_rules;''')

c.execute('''drop view if exists hub_entities''')
c.execute('''create view hub_entities as 
with cte_business_keys as
(
	select 
	hasDomain as targettable
	, label as targetcolumn
	from fdm_dataspot_businessattribute
	where identifying 
)
, cte_source2target as
(
	SELECT 
	targettable
	, targetcolumn
	, sourcesystem
	, sourcetable
	, sourcecolumn
	, ruleOf
	, stereotype as ruletype
	, description
	, has_statustracking
	from fdm_dataspot_rules
)
, cte_source2target_business_keys as
(
	select
	cte_source2target.targettable
	, cte_source2target.targetcolumn
	, sourcesystem
	, sourcetable
	, sourcecolumn
	, ruleOf
	, ruletype
	, description
	, has_statustracking
	from cte_source2target
	inner join cte_business_keys
	on cte_source2target.targettable=cte_business_keys.targettable
	and cte_source2target.targetcolumn=cte_business_keys.targetcolumn
)
SELECT 
replace(targetcolumn, '_bk', '_h') as hub_identifier
, replace(targetcolumn, '_bk', '_h') as target_hub_table_physical_name
, sourcesystem||'_'||sourcetable as source_table_identifier
, 'load_'||sourcesystem||'_'||sourcetable as source_table_physical_name
,  sourcecolumn as source_column_physical_name
, targetcolumn as business_key_physical_name
, row_number() over (partition by sourcesystem||'_'||sourcetable order by targetcolumn) as target_column_sort_order
, 'hk_'||replace(targetcolumn, '_bk', '_h') as target_primary_key_physical_name
, case when lower(cte_source2target_business_keys.ruletype) = 'described'
       then description
       else '' end as transformation_rule
, cte_source2target_business_keys.has_statustracking
from cte_source2target_business_keys
left join fdm_dataspot_transformation
on cte_source2target_business_keys.ruleOf = fdm_dataspot_transformation.transformationOf ||'/'||fdm_dataspot_transformation.label;''')

c.execute('''drop view if exists hub_satellites''')
c.execute('''create view hub_satellites as 
with cte_business_keys as
(
	select 
	hasDomain as targettable
	, label as targetcolumn
	from fdm_dataspot_businessattribute
	where identifying 
)
, cte_source2target as
(
	SELECT 
	targettable
	, targetcolumn
	, sourcesystem
	, sourcetable
	, sourcecolumn
	, title
	from fdm_dataspot_rules
	--where sourcetable='bestellung'
	--and sourcesystem='roadshow'
	)
, cte_source2target_business_keys as
(
	select
	cte_source2target.targettable
	, cte_source2target.targetcolumn
	, sourcesystem
	, sourcetable
	, sourcecolumn
	from cte_source2target
	inner join cte_business_keys
	on cte_source2target.targettable=cte_business_keys.targettable
	and cte_source2target.targetcolumn=cte_business_keys.targetcolumn
)
, cte_source2target_business_keys_unique as
(
	select
	cte_source2target.targettable
	, cte_source2target.targetcolumn
	, sourcesystem
	, sourcetable
	, group_concat(sourcecolumn, ',')
	from cte_source2target
	inner join cte_business_keys
	on cte_source2target.targettable=cte_business_keys.targettable
	and cte_source2target.targetcolumn=cte_business_keys.targetcolumn
	group by 	cte_source2target.targettable
	, cte_source2target.targetcolumn
	, sourcesystem
	, sourcetable
)
--select * from cte_source2target_business_keys_unique;
, cte_source2target_non_business_keys as
(
	select 
	cte_source2target.targettable
	, cte_source2target.targetcolumn
	, sourcesystem
	, sourcetable
	, sourcecolumn
	, title
	from cte_source2target
	left join cte_business_keys
	on cte_source2target.targettable=cte_business_keys.targettable
	and cte_source2target.targetcolumn=cte_business_keys.targetcolumn
	where cte_business_keys.targettable is null
)
--select * from cte_source2target_non_business_keys;
select 
cte_source2target_non_business_keys.targettable||'_'||cte_source2target_non_business_keys.sourcesystem||'_'||'s' as satellite_identifier
, cte_source2target_non_business_keys.targettable||'_'||cte_source2target_non_business_keys.sourcesystem||'_'||'s' as target_satellite_table_physical_name
, cte_source2target_non_business_keys.sourcesystem||'_'||cte_source2target_non_business_keys.sourcetable as source_table_identifier
, cte_source2target_non_business_keys.sourcecolumn as source_column_physical_name
, 'hk_'||replace(cte_source2target_business_keys_unique.targetcolumn, 'bk', 'h') as hub_primary_key_physical_name
, cte_source2target_business_keys_unique.targetcolumn
, cte_source2target_non_business_keys.targetcolumn as target_column_physical_name
, ROW_NUMBER() over (partition by cte_source2target_non_business_keys.targettable||'_'||cte_source2target_non_business_keys.sourcesystem order by cte_source2target_non_business_keys.targetcolumn) as target_column_sort_order
, case when lower(cte_source2target_non_business_keys.title) = 'ma' then true else false end as ma_attribute
from cte_source2target_non_business_keys
inner join cte_source2target_business_keys_unique
on cte_source2target_non_business_keys.sourcesystem=cte_source2target_business_keys_unique.sourcesystem
and cte_source2target_non_business_keys.sourcetable=cte_source2target_business_keys_unique.sourcetable
and cte_source2target_non_business_keys.targettable=cte_source2target_business_keys_unique.targettable
--> exclude nh_links
left join fdm_dataspot_businessobject
on fdm_dataspot_businessobject.label = cte_source2target_non_business_keys.targettable
and fdm_dataspot_businessobject.is_nh_link 
where fdm_dataspot_businessobject.label is NULL
--< exclude nh_links;''')


c.execute('''drop view if exists link_entities''')
# diese Logik ist noch sehr unausgereift, funktioniert nur bei fest definierten Konventionen
# gegenchecken
c.execute('''create view link_entities as
with relationship as
(
	SELECT 
	linkname 
	, table1 
	, column1 
	, table2 
	, column2 
	, has_statustracking
	, driving_key 
	from fdm_dataspot_relationship
)
, source2target AS 
( 
	SELECT 
	sourcesystem
	, targettable 
	, targetcolumn
	, sourcetable 
	, group_concat(sourcecolumn ) sourcecolumns
	, identifying
	from fdm_dataspot_rules
	left join fdm_dataspot_businessattribute
	on hasDomain = targettable
	and label = targetcolumn
	--where identifying=1
	--where targettable in ('orderposition', 'product')
	group by sourcesystem, targettable, targetcolumn, sourcetable 
)
, relationship_source2target AS 
(
	select
	*
	, count(*) over (partition by linkname, sourcesystem, sourcetable) no_of_rows
	from relationship 
	inner join source2target
	on (table1=targettable or table2=targettable)
	and targetcolumn in (column1, column2)
	--where relationship.linkname ='orderposition_product'
)
--select * from relationship_source2target;
select 
linkname as link_identifier
, linkname||'_l' as target_link_table_physical_name
, sourcesystem||'_'||sourcetable as Source_Table_Identifier
, targetcolumn as source_column_physical_name
, '' as Prejoin_Table_Identifier
, '' Prejoin_Table_Column_Name
, '' Prejoin_Extraction_Column_Name
, '' Prejoin_Target_Column_Alias
, 'hk_'||replace(targetcolumn, '_bk','_h') as hub_primary_key_physical_name
, 'hk_'||replace(targetcolumn, '_bk','_h') as target_column_physical_name
, ROW_NUMBER() over (PARTITION by linkname, sourcesystem, sourcetable order by targetcolumn desc) target_column_sort_order
, 'hk_'||linkname||'_l' target_primary_key_physical_name
, has_statustracking
, driving_key 
from relationship_source2target
where no_of_rows>1;''')

# link_satellites still missing 
c.execute('''drop view if exists link_satellites''')
c.execute('''create view link_satellites as
select 
's0002' as Satellite_Identifier
,'xx' as Target_satellite_table_physical_name
,'xx' as Source_table_identifier
,'xx' as Source_column_physical_name
,'xx' as Link_primary_key_physical_name
,'xx' as Target_column_physical_name
,'1' as Target_Column_Sort_Order;''')

# nh_link_entites - non-historized
c.execute('''drop view if exists nh_link_entities''')
c.execute('''create view nh_link_entities as
SELECT 
fdm_dataspot_businessobject.nh_linkname ||'_nhl' as link_identifier
, fdm_dataspot_businessobject.nh_linkname ||'_nhl' as target_link_table_physical_name
, fdm_dataspot_rules.sourcesystem||'_'||fdm_dataspot_rules.sourcetable as source_table_identifier
, fdm_dataspot_rules.sourcecolumn as source_column_physical_name
, 'hk_'||fdm_dataspot_businessobject.nh_linkname ||'_l' as link_primary_key_physical_name
, case when fdm_dataspot_businessattribute.identifying =1
       then 'hk_'||replace(fdm_dataspot_rules.targetcolumn, '_bk','_h')  
       else fdm_dataspot_rules.targetcolumn end as target_column_physical_name       
, fdm_dataspot_businessattribute.identifying
, ROW_NUMBER() over (PARTITION by fdm_dataspot_businessobject.nh_linkname order by fdm_dataspot_rules.targetcolumn) as target_column_sort_order
from fdm_dataspot_businessobject
inner join fdm_dataspot_rules
on fdm_dataspot_businessobject.label = fdm_dataspot_rules.targettable
inner join fdm_dataspot_businessattribute  
on fdm_dataspot_rules.targettable = fdm_dataspot_businessattribute.hasDomain 
and fdm_dataspot_rules.targetcolumn = fdm_dataspot_businessattribute.label
where is_nh_link;''')


# Extract from _type==Rule
for item in data:
    if item['_type'] == 'Rule':
        id = item['id']
        ruleOf = item['ruleOf'].lower()
        stereotype = item['stereotype'].lower()
        transformsFrom = item.get('transformsFrom', [])
        if transformsFrom:
            sourcesystem = transformsFrom[0].split('/')[2].lower()
            sourcetable = transformsFrom[0].split('/')[3].lower()
            sourcecolumn = transformsFrom[0].split('/')[4].lower()
            list_sourcecolumn = [s.split("/")[-1] for s in transformsFrom]
        else:
            sourcesystem = sourcetable = sourcecolumn = ''
            list_sourcecolumn = []
        transformsTo = item.get('transformsTo', [])
        if transformsTo:
            targettable = transformsTo[0].split('/')[0].lower()
            targetcolumn = transformsTo[0].split('/')[1].lower()
        else:
            targettable = targetcolumn = ''            
        if 'title' in item:
            title = item['title']
        else:
            title = ''
        if 'description' in item:
            description = item['description']
        else:
            description = ''            
        if 'AdditionalInfo' in item:
            json_data = json.loads(item['AdditionalInfo'])
            has_statustracking = json_data.get('hub', {}).get('has_statustracking', False)
        else:
            has_statustracking = False
        for sourcecolumn in list_sourcecolumn:
            sourcecolumn = sourcecolumn.lower()
            # Insert data into SQLite table
            c.execute("INSERT INTO fdm_dataspot_rules VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (id, ruleOf, stereotype, sourcesystem, sourcetable, sourcecolumn, targettable, targetcolumn, title, description, has_statustracking))

# Extract from _type==Relationship
for item in data:
    if item['_type'] == 'Relationship' and 'AdditionalInfo' in item:
        table1 = item['linksDomain'][0].split('/')[0].lower()
        column1 = item['linksDomain'][0].split('/')[1].lower()
        table2 = item['linksRange'][0].split('/')[0].lower()
        column2 = item['linksRange'][0].split('/')[1].lower()

        # parse the JSON string
        json_data = json.loads(item['AdditionalInfo'])
        # extract the required values
        linkname = json_data['link'].get('name', None)
        has_statustracking = json_data['link'].get('has_statustracking', False)
        driving_key = json_data['link'].get('driving_key', None)
        id = item['id']        

         # Insert data into SQLite table
        c.execute("INSERT INTO fdm_dataspot_relationship VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (id, table1, column1, table2, column2, linkname, has_statustracking, driving_key))   





# Extract from _type==BusinessAttribute
for item in data:
    if item['_type'] == 'BusinessAttribute' and 'identifying' in item:
        id = item['id']        
        hasDomain = item['hasDomain'].lower()
        label = item['label'].lower()
        identifying = item['identifying']

         # Insert data into SQLite table
        c.execute("INSERT INTO fdm_dataspot_businessattribute VALUES (?, ?, ?, ?)",
                  (id, hasDomain, label, identifying))   

# Extract from _type==BusinessObject
for item in data:
    if item['_type'] == 'BusinessObject' and 'AdditionalInfo' in item:
        id = item['id']      
        label = item['label'].lower()          
        incollection = item['inCollection'].lower()
        json_data = {}
        json_data = json.loads(item['AdditionalInfo'])
        is_nh_link = 'nh_link' in json_data
        nh_linkname = json_data.get('nh_link', False).get('name', '')
         # Insert data into SQLite table
        c.execute("INSERT INTO fdm_dataspot_businessobject VALUES (?, ?, ?, ?, ?)",
                  (id, label, incollection, is_nh_link, nh_linkname ))   

# Extract from _type==Transformation
for item in data:
    if item['_type'] == 'Transformation' and 'tags' in item and 'transformationOf' in item:
        id = item['id']     
        transformationOf = item['transformationOf'].lower()
        label = item['label'].lower()          
        tags = item['tags'][0].lower()
        status = item['status'].lower()
         # Insert data into SQLite table
        c.execute("INSERT INTO fdm_dataspot_transformation VALUES (?, ?, ?, ?, ?)",
                  (id, transformationOf, label, tags, status))   



# Commit changes and close database connection
conn.commit()
conn.close()