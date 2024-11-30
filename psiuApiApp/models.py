from django.db import models

class Atividade(models.Model): 
    id = models.AutoField(primary_key=True) 
    criador_id = models.TextField(db_column='criador_id')
    adicionais = models.TextField(db_column='adicionais', blank=True)
    data = models.DateField(db_column='data')
    hora = models.TimeField(db_column='hora')
    tipo_atividade = models.TextField(db_column='tipo_atividade')
    vagas = models.PositiveIntegerField(db_column='vagas', default=4)
    
    class Meta: 
        managed = True 
        db_table = 'Atividade' 
        ordering = ['id'] 
    def __str__(self): 
        return str(self.id)

class Carona(Atividade): 

    local_saida = models.TextField(db_column='local_saida')
    local_chegada = models.TextField(db_column='local_chegada')

    class Meta: 
        managed = True 
        db_table = 'Carona' 
        ordering = ['local_chegada'] 

    def __str__(self): 
        return str(self.id)

class Extracurriculares(Atividade): 

    atividade = models.TextField(db_column='atividade')
    local = models.TextField(db_column='local')

    class Meta: 
        managed = True 
        db_table = 'Extracurriculares' 
        ordering = ['atividade'] 

    def __str__(self): 
        return str(self.id)
    
class Estudos(Atividade): 

    materia = models.TextField(db_column='materia')
    local = models.TextField(db_column='local')

    class Meta: 
        managed = True 
        db_table = 'Estudos' 
        ordering = ['materia'] 

    def __str__(self): 
        return str(self.id)

class Liga(Atividade): 

    nome = models.TextField(db_column='nome')
    local = models.TextField(db_column='local')

    class Meta: 
        managed = True 
        db_table = 'Liga' 
        ordering = ['nome'] 

    def __str__(self): 
        return str(self.id)

class ConhecerPessoas(Atividade): 

    atividade = models.TextField(db_column='atividade')
    local = models.TextField(db_column='local')

    class Meta: 
        managed = True 
        db_table = 'ConhecerPessoas' 
        ordering = ['atividade'] 

    def __str__(self): 
        return str(self.id)

class ParticipaAtividade(models.Model): 
    atividade = models.ForeignKey(Atividade, db_column='atividade', on_delete=models.CASCADE)
    usuario = models.TextField(db_column='usuario')

    class Meta: 
        managed = True 
        db_table = 'ParticipaAtividade' 
        ordering = ['atividade'] 
    def __str__(self): 
        return str(self.atividade)