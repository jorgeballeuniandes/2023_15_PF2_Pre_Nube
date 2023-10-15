from .create_interview import CreateInterview

class PublicCreateInterview(BaseCommannd):
  def __init__(self, data):
    self.data = data

  def execute(self):
    #validar  que el usuario tenga relacionada la compañia
    #validateUserHasCompany()
    #validar que proyecto pertenece a la compañia
    #validateCompanyHasProyect()
    #validar que el candidato exista
    #validate
    interview = CreateInterview(self.data).execute()
    return interview