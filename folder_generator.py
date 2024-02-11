from datetime import datetime, timedelta
import os


def folders_by_date(start_date, end_date, path="."):
  """
  Crée des dossiers d'une certaine date à une autre.

  Args:
    start_date: La date de début au format YYYY-MM-DD.
    end_date: La date de fin au format YYYY-MM-DD.
    path: Le chemin du dossier parent où créer les dossiers.

  Returns:
    Une liste des noms des dossiers créés.
  """

  # Convertit les dates en objets datetime.

  start_date = datetime.strptime(start_date, "%Y-%m-%d")
  end_date = datetime.strptime(end_date, "%Y-%m-%d")

  # Crée une liste des dates.

  dates = []
  for day in range((end_date - start_date).days + 1):
    dates.append(start_date + timedelta(days=day))

  folders = []
  for date in dates:
    folder_name = date.strftime("%Y-%m-%d")
    folder_path = os.path.join(path, folder_name)
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)
    folders.append(folder_name)

  return folders


# folders_by_date("2024-02-06", "2024-02-29", "flashcards/")