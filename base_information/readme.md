In the old implementation, the conceptual model, the source model and the mappings between where in dataspot (now extracted as: FDM_Willibald.json and TDM_Willibald.json)
All the necessary information was extracted from the jsons and saved into the sqllite database dataspotparameters.db. All this information is available in this folder.

The new Implementation should contain all necessary metadata in yaml files,  
like Jaco van der Laan describes it in his series beginning with: https://medium.com/towards-data-engineering/from-business-concepts-to-database-blueprint-bridging-conceptual-and-logical-data-models-in-a-48391484ce75

Goal:
Create YAML definitions for the source systems of the Willibald example (e.g., roadshow, webshop), one yaml for each source table.
Each YAML should contain:

Technical metadata about the source table.

Mappings/transformations between source columns and conceptual entities/attributes defined in the existing conceptual YAMLs (/entities folder).

A possible structure could be:

source_system:
  name: <source_system>
  description: <short description of source system>
  owner: <team or domain owner>

  tables:
    - name: <table_name>
      description: <short description of the table>
      technical_metadata:
        schema: <schema_name>
        primary_key: [<col1>, <col2>]
        columns:
          - name: <column_name>
            datatype: <type from DDL>
            nullable: true|false
            description: <optional column comment from DDL>

      mappings:
        - conceptual_entity: <entity_name_from_entities_yaml>
          attributes:
            - conceptual_attribute: <attribute_name>
              source_column: <column_name>
              transformation: <optional SQL expression>
              note: <optional comment or mapping logic>
