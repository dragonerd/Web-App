

def admin_get_status(status):

  if status == "True":
      return "Activo"
  elif status == "False":
      return "Inactivo"
  else:
      return  status.status