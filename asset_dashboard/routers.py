class GISRouter:
    """
    Route queries for tables in the specied schemas to the "fp_postgis" database.
    """
    GIS_DB_ALIAS = 'fp_postgis'
    GIS_APP_LABEL = 'asset_dashboard_gis'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.GIS_APP_LABEL:
            return self.GIS_DB_ALIAS
        return None

    def db_for_write(self, model, **hints):
        """
        Specify where to write GIS data so we can create test data using the
        ORM.

        N.b., we probably should not modify CCFP's data. This method assumes
        that they've granted us read-only access, i.e., the database will raise
        an exception for any write requests against the live server.
        """
        if model._meta.app_label == self.GIS_APP_LABEL:
            return self.GIS_DB_ALIAS
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        From the Django docs:

        > If no router has an opinion (i.e. all routers return None), only
        relations within the same database are allowed.

        https://docs.djangoproject.com/en/3.2/topics/db/multi-db/#allow_relation

        Thus, this should disallow the relation of tables in the specified
        schemas to objects in the default database. This should be ok because
        we will copy necessary GIS data to the default database for subsequent
        relation and manipulation.
        """
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Only create and run migrations for models that are not marked by the
        GIS_APP_LABEL. This prevents the creation of migrations for GIS models
        and stops Django from trying to create a django_migrations table in the
        GIS_DB_ALIAS database, since we won't have write access. Reference:
        https://stackoverflow.com/a/43553063
        """
        if app_label == self.GIS_APP_LABEL:
            return False
        return db == 'default'
