class GISRouter:
    """
    Route queries for tables in the specied schemas to the "fp_postgis" database.
    """

    GIS_SCHEMAS = {'quercus'}
    DB_ALIAS = 'fp_postgis'

    def db_for_read(self, model, **hints):
        if self._db_table_in_gis_schemas(model._meta.db_table):
            return 'fp_postgis'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write "quercus" models go to fp_postgis.

        N.b., we probably should not modify CCFP's data. This method assumes
        that they've granted us read-only access, i.e., the database will raise
        an exception for any write requests.
        """
        if self._db_table_in_gis_schemas(model._meta.db_table):
            return 'fp_postgis'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        From the Django docs:

        > If no router has an opinion (i.e. all routers return None), only
        relations within the same database are allowed.

        https://docs.djangoproject.com/en/3.2/topics/db/multi-db/#allow_relation

        Since "quercus" models are write only, this should disallow the
        relation of non-"quercus" models to objects in the default database.
        """
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model := hints.get('model', None):
            if self._db_table_in_gis_schemas(model._meta.db_table):
                return db == 'fp_postgis'
        return None

    def _db_table_in_gis_schemas(self, db_table):
        return any(
            db_table.startswith(f'"{schema}"') for schema in self.GIS_SCHEMAS
        )