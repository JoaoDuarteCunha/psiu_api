class DBRouter(): 
    def db_for_read(self, model, **hints): 
        if model._meta.db_table == 'Atividade': 
            return 'DBPsiuApp' 
        return None 
    def db_for_write(self, model, **hints): 
        if model._meta.db_table == 'Atividade': 
            return 'DBPsiuApp' 
        return None 
    def allow_relation(self, obj1, obj2, **hints): 
        if obj1._meta.db_table == 'Atividade' or obj2._meta.db_table == 'Atividade': 
            return True 
        return None 
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'psiu_api': 
            return db == 'DBPsiuApp' 
        return None 