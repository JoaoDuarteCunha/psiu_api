class DBRouter(): 

    tabelas = ['Atividade', 'Carona', 'Estudos', 'Liga', 'Extracurriculares', 'ConhecerPessoas', 'ParticipaAtividade']

    def db_for_read(self, model, **hints): 
        if model._meta.db_table in self.tabelas: 
            return 'DBPsiuApp' 
        return None 
    def db_for_write(self, model, **hints): 
        if model._meta.db_table in self.tabelas: 
            return 'DBPsiuApp' 
        return None 
    def allow_relation(self, obj1, obj2, **hints): 
        if obj1._meta.db_table in self.tabelas or obj2._meta.db_table in self.tabelas: 
            return True 
        return None 
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'psiu_api': 
            return db == 'DBPsiuApp' 
        return None 