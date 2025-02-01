from app.models.activity import Activity
from app.models.user import UserProfile
from datetime import datetime, timedelta
import random
import json

def generate_activities_for_profile(user_profile, narrative, num_days=7):
    """
    Genera actividades automáticas para un perfil de usuario ficticio.
    
    :param user_profile: Objeto UserProfile
    :param narrative: Objeto Narrative asociado al perfil
    :param num_days: Número de días para generar actividades
    :return: Lista de objetos Activity
    """
    activities = []
    current_time = datetime.now()

    for day in range(num_days):
        for _ in range(random.randint(2, 5)):  # Generar entre 2 y 5 actividades por día
            activity_time = current_time - timedelta(days=day, hours=random.randint(0, 23), minutes=random.randint(0, 59))
            description = f"Actividad generada para {user_profile.name} en el contexto de '{narrative.title}'"
            
            # Simular patrones de comportamiento
            pattern = json.loads(user_profile.behavior_pattern)
            details = {
                "time": activity_time.strftime('%Y-%m-%d %H:%M:%S'),
                "pattern": pattern
            }
            
            activities.append(Activity(
                user_profile_id=user_profile.id,
                timestamp=activity_time,
                description=description,
                details=json.dumps(details)
            ))

    return activities
