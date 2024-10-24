from django.utils.dateparse import parse_datetime
from core.models import Appointment

def create_appointment_logic(data, company):
    start_datetime = parse_datetime(data['start_datetime'])
    end_datetime = parse_datetime(data['end_datetime'])
    appointment = Appointment(
        company=company,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        full_name=data['full_name'],
        email=data.get('email', ''),
        phone_number=data.get('phone_number', ''),
        message=data.get('message', '')
    )
    appointment.full_clean()  # Llama a clean() y valida el modelo antes de guardar
    appointment.save()
    return {
        'status': 'success',
        'appointment_id': appointment.id,
        'message': 'Cita creada exitosamente.'
    }

def update_appointment_logic(data, company):
    appointment = Appointment.objects.get(id=data['event_id'], company=company)
    start_datetime = parse_datetime(data['start_datetime'])
    end_datetime = parse_datetime(data['end_datetime'])
    appointment.start_datetime = start_datetime
    appointment.end_datetime = end_datetime
    appointment.full_name = data['full_name']
    appointment.email = data.get('email', '')
    appointment.phone_number = data.get('phone_number', '')
    appointment.message = data.get('message', '')
    appointment.full_clean()  # Llama a clean() y valida el modelo antes de guardar
    appointment.save()
    return {
        'status': 'success',
        'appointment_id': appointment.id,
        'message': 'Cita actualizada exitosamente.'
    }