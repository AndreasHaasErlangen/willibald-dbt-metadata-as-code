import json
import sqlite3
import lib
import json
import yaml

def to_rules(source:json, cursor:sqlite3.Cursor, table_name:str):
    out_list = []
    single_tuple = ()
    attribute_list = lib.def_list_to_att_list(table_name)

    for item in source:
        if item['_type'] == 'Rule' and item['ruleOf'].lower().endswith('fdm'):
            id = item['id']
            ruleOf = item['ruleOf'].lower()
            stereotype = item['stereotype'].lower()
            transformsFrom = item.get('transformsFrom', [])
            status = item.get('status', '')
            if transformsFrom and status != 'INACTIVE':
                print(transformsFrom[0])
                sourcesystem = transformsFrom[0].split('/')[2].lower()
                sourcetable = transformsFrom[0].split('/')[3].lower()
                sourcecolumn = transformsFrom[0].split('/')[4].lower()
                list_sourcecolumn = [s.split("/")[-1] for s in transformsFrom]
            else:
                sourcesystem = sourcetable = sourcecolumn = ''
                list_sourcecolumn = []
            transformsTo = item.get('transformsTo', [])
            if transformsTo:
                #print(str(transformsTo))
                if '/' in str(transformsTo):
                    #print(str(transformsFrom) + '->' + str(transformsTo[0]))
                    targettable = transformsTo[0].split('/')[0].lower()
                    targetcolumn = transformsTo[0].split('/')[1].lower()
                else:
                    targettable = targetcolumn = ''
            else:
                targettable = targetcolumn = ''  
            #print(str(targettable) + '->' + str(targetcolumn))
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
                single_tuple = lib.maketuple(vars(), attribute_list)
                out_list.append(single_tuple)

    lib.insert_rows(data_tuple_list=out_list, in_attribute_list=attribute_list, table_name=table_name, cursor=cursor)


def to_relationships(source:json, cursor:sqlite3.Cursor, table_name:str):
    out_list = []
    single_tuple = ()
    attribute_list = lib.def_list_to_att_list(table_name)

    for item in source:
        if item['_type'] == 'Relationship' and 'AdditionalInfo' in item:
            table1 = item['linksDomain'][0].split('/')[0].lower()
            column1 = item['linksDomain'][0].split('/')[1].lower()
            table2 = item['linksRange'][0].split('/')[0].lower()
            column2 = item['linksRange'][0].split('/')[1].lower()
            relationship_name = item['name']
            # parse the JSON string
            json_data = json.loads(item['AdditionalInfo'])
            # extract the required values
            linkname = json_data['link'].get('name', None)
            has_statustracking = json_data['link'].get('has_statustracking', False)
            driving_key = json_data['link'].get('driving_key', None)
            id = item['id']        
            single_tuple = lib.maketuple(vars(), attribute_list)
            out_list.append(single_tuple)
    lib.insert_rows(data_tuple_list=out_list, in_attribute_list=attribute_list, table_name=table_name, cursor=cursor)



def to_business_attribute(source:json, cursor:sqlite3.Cursor, table_name:str):
    out_list = []
    single_tuple = ()
    attribute_list = lib.def_list_to_att_list(table_name)

    for item in source:
        if item['_type'] == 'BusinessAttribute' and 'identifying' in item:
            id = item['id']        
            hasDomain = item['hasDomain'].lower()
            label = item['label'].lower()
            identifying = item['identifying']
            single_tuple = lib.maketuple(vars(), attribute_list)
            out_list.append(single_tuple)
    lib.insert_rows(data_tuple_list=out_list, in_attribute_list=attribute_list, table_name=table_name, cursor=cursor)


def to_business_object(source:json, cursor:sqlite3.Cursor, table_name:str):
    out_list = []
    single_tuple = ()
    attribute_list = lib.def_list_to_att_list(table_name)

    for item in source:
        if item['_type'] == 'BusinessObject' and 'AdditionalInfo' in item:
            id = item['id']      
            label = item['label'].lower()          
            incollection = item['inCollection'].lower()
            json_data = {}
            nh_linkname = ''
            json_data = json.loads(item['AdditionalInfo'])
            is_not_automatically_generated_in_raw_vault = json_data.get('not_automatically_generated_in_raw_vault', 0)
            is_not_automatically_generated_in_raw_vault = 1 if is_not_automatically_generated_in_raw_vault else 0
            is_nh_link = 'nh_link' in json_data
            is_ref_object = 'reference_data' in json_data
            if is_nh_link:
                nh_linkname = json_data.get('nh_link').get('name', '')
            single_tuple = lib.maketuple(vars(), attribute_list)
            out_list.append(single_tuple)
    lib.insert_rows(data_tuple_list=out_list, in_attribute_list=attribute_list, table_name=table_name, cursor=cursor)

def to_transformation(source:json, cursor:sqlite3.Cursor, table_name:str):
    out_list = []
    single_tuple = ()
    attribute_list = lib.def_list_to_att_list(table_name)

    for item in source:
        if item['_type'] == 'Transformation' and 'tags' in item and 'transformationOf' in item:
            id = item['id']     
            transformationOf = item.get('transformationOf').lower()
            label = item['label'].lower()          
            tags = item['tags'][0].lower()
            status = item['status'].lower()
            single_tuple = lib.maketuple(vars(), attribute_list)
            out_list.append(single_tuple)            
    lib.insert_rows(data_tuple_list=out_list, in_attribute_list=attribute_list, table_name=table_name, cursor=cursor)


def to_physical_source_table(source:json, cursor:sqlite3.Cursor, table_name:str):
    out_list = []
    single_tuple = ()
    attribute_list = lib.def_list_to_att_list(table_name)

    for item in source:
        if item['_type'] == 'UmlClass':
            id = item['id']      
            label = item['label'].lower()          
            source_short = item.get('inCollection','').lower()
            physicalName = item.get('physicalName', '').lower()
            dub_check= ''
            key_check= ''
            date_format =  ''
            HWM = ''
            decimal_separator = ''
            materialization = ''
            AdditionalInfo_str = str(item.get("AdditionalInfo",''))
            if AdditionalInfo_str != "":
                # print(table_name + AdditionalInfo_str)
                AdditionalInfo=json.loads(AdditionalInfo_str)
                decimal_separator = ''
                dub_check_list=  AdditionalInfo['table'].get('dub_check', '')
                if dub_check is not None:
                    dub_check = yaml.dump(dub_check_list, explicit_start=True, default_flow_style=False)
                    dub_check = dub_check.replace('---', 'dub_check:')
                key_check_list=  AdditionalInfo['table'].get('key_check', '')
                if key_check is not None:
                    key_check = yaml.dump(key_check_list, explicit_start=True, default_flow_style=False)
                    key_check = key_check.replace('---', 'key_check:')
                date_format =  AdditionalInfo["table"].get("date_format", '')
                HWM =  AdditionalInfo["table"].get("HWM", '')
                JediTest =  AdditionalInfo["table"].get("JediTest", "True")
                materialization =  AdditionalInfo["table"].get("materialization", '')
            single_tuple = lib.maketuple(vars(), attribute_list)
            out_list.append(single_tuple)
    lib.insert_rows(data_tuple_list=out_list, in_attribute_list=attribute_list, table_name=table_name, cursor=cursor)

def to_physical_source_attributes(source:json, cursor:sqlite3.Cursor, table_name:str):
    out_list = []
    single_tuple = ()
    attribute_list = lib.def_list_to_att_list(table_name)
    for item in source:
        id = None
        if item['_type'] == 'UmlAttribute':
            id = item['id']      
            label = item['label'].lower()          
            source_short = item['hasDomain'].split('/')[0].lower()
            source_table_name = item['hasDomain'].split('/')[1].lower()
            type_source_short = item['hasRange'].split('/')[0].lower()
            type_name = item['hasRange'].split('/')[1].lower()
            attribute_order = item.get('order',-1)

        if not id is None:
            single_tuple = lib.maketuple(vars(), attribute_list)
            out_list.append(single_tuple)


    lib.insert_rows(data_tuple_list=out_list, in_attribute_list=attribute_list, table_name=table_name, cursor=cursor)

def to_physical_source(source:json, cursor:sqlite3.Cursor, table_name:str):
    out_list = []
    single_tuple = ()
    attribute_list = lib.def_list_to_att_list(table_name)

    for item in source:
        if item['_type'] == 'Collection':
            id = item['id']      
            source_short = item['label'].lower()          
            source_long = item['title'].lower()          
            source_type= ''
            info1 = ''
            info2 = ''
            info3 = ''
            info4 = ''
            info5 = ''
            info6 = ''
            type_schema=''
            load_completeness_type=''
            effective_date_type = ''
            effective_date_attribute = ''
            AdditionalInfo_str = str(item.get("AdditionalInfo",''))
            if AdditionalInfo_str != "":
                AdditionalInfo=json.loads(AdditionalInfo_str)
                source_type= AdditionalInfo['source'].get('source_type', '')
                info1= AdditionalInfo['source'].get('info1', '')
                info2= AdditionalInfo['source'].get('info2', '')
                info3= AdditionalInfo['source'].get('info3', '')
                info4= AdditionalInfo['source'].get('info4', '')
                info5= AdditionalInfo['source'].get('info5', '')
                info6= AdditionalInfo['source'].get('info6', '')
                type_schema=AdditionalInfo['source'].get('type_schema', None)
                load_completeness_type=AdditionalInfo['source'].get('load_completeness_type', None)
                effective_date_type=AdditionalInfo['source'].get('effective_date_type', '')
                effective_date_attribute=AdditionalInfo['source'].get('effective_date', '')
            single_tuple = lib.maketuple(vars(), attribute_list)
            out_list.append(single_tuple)
    lib.insert_rows(data_tuple_list=out_list, in_attribute_list=attribute_list, table_name=table_name, cursor=cursor)


def to_source_add_attributes(source:json, cursor:sqlite3.Cursor, table_name:str):
    out_list = []
    single_tuple = ()
    attribute_list = lib.def_list_to_att_list(table_name)
    for item in source:
        id = None
        if item['_type'] == 'Collection':
            id = item['id']  
            source_short = item['label'].lower()  
            AdditionalInfo_str = str(item.get("AdditionalInfo",''))
            if AdditionalInfo_str != "":
                AdditionalInfo=json.loads(AdditionalInfo_str)
                source_type = AdditionalInfo['source'].get('source_type', '')
                default_columns=AdditionalInfo['source'].get('default_columns', '[]')
                if default_columns != []:
                    for column in default_columns:
                        selection = 'default_columns'
                        name = column['name'].lower()
                        value = column['value'].lower()
                        data_type = column['data_type']
                        format = column.get('format')
                        single_tuple = lib.maketuple(vars(), attribute_list)
                        out_list.append(single_tuple)

                additional_columns=AdditionalInfo['source'].get('additional_columns', '[]')
                if additional_columns != []:
                    for column in additional_columns:
                        selection = 'additional_columns'
                        name = column['name'].lower()
                        value = column['value'].lower()
                        data_type = column['data_type']
                        format = column.get('format')
                        single_tuple = lib.maketuple(vars(), attribute_list)
                        out_list.append(single_tuple)
    lib.insert_rows(data_tuple_list=out_list, in_attribute_list=attribute_list, table_name=table_name, cursor=cursor)


def to_source_datatypes(source:json, cursor:sqlite3.Cursor, table_name:str):
    out_list = []
    single_tuple = ()
    attribute_list = lib.def_list_to_att_list(table_name)
    for item in source:
        id = None
        if item['_type'] == 'UmlDatatype':
            id = item['id']      
            label = item['label'].lower()          
            source_short = item['inCollection'].lower()
            hasRange = item.get('hasRange','').lower()
            physicalName= item.get('physicalName', 'unknown')
            baseType= item.get('baseType', 'unknown')
            integerDigits= item.get('integerDigits', -1)
            fractionDigits= item.get('fractionDigits', -1)
            format = ''
            decimal_separator = ''

            AdditionalInfo_str = str(item.get("AdditionalInfo",''))
            if AdditionalInfo_str != "":
                AdditionalInfo=json.loads(AdditionalInfo_str)
                format = AdditionalInfo['datatype'].get('format', '')
                decimal_separator =  AdditionalInfo["datatype"].get("decimal_separator", '')

        if not id is None:
            single_tuple = lib.maketuple(vars(), attribute_list)
            out_list.append(single_tuple)


    lib.insert_rows(data_tuple_list=out_list, in_attribute_list=attribute_list, table_name=table_name, cursor=cursor)
