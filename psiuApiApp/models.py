from django.db import models

class Atividade(models.Model): 
    id = models.AutoField(primary_key=True) 
    criador_id = models.IntegerField(db_column='criador_id') # Field name made lowercase.
    adicionais = models.TextField(db_column='adicionais') # Field name made lowercase.
    data = models.DateField(db_column='data') # Field name made lowercase.
    hora = models.TimeField(db_column='hora') # Field name made lowercase.
    tipo_atividade = models.TextField(db_column='tipo_atividade')
    
    class Meta: 
        managed = True 
        db_table = 'Atividade' 
        ordering = ['id'] 
    def __str__(self): 
        return str(self.id)

class Carona(Atividade): 

    local_saida = models.TimeField(db_column='local_saida') # Field name made lowercase.

    class Meta: 
        managed = True 
        db_table = 'Carona' 
        ordering = ['local_saida'] 

    def __str__(self): 
        return str(self.id)