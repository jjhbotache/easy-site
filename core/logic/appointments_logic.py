from django.utils.dateparse import parse_datetime
from django.urls import reverse
from core.models import Appointment
from core.logic.helpers.logic_helpers import send_gmail

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

    # Enviar correo electrónico de notificación al cliente
    if appointment.email:
        subject = "Confirmación de Cita"
        body = f"""
        Estimado/a {appointment.full_name},

        Su cita ha sido programada exitosamente.

        Detalles de la cita:
        Fecha y Hora de Inicio: {appointment.start_datetime.strftime('%d/%m/%Y %H:%M')}
        Fecha y Hora de Fin: {appointment.end_datetime.strftime('%d/%m/%Y %H:%M')}
        Mensaje: {appointment.message}

        Puede editar su cita en el siguiente enlace:
        

        Puede eliminar su cita en el siguiente enlace:
        

        Gracias,
        {company.name}
        """
        
        # {reverse('edit_appointment', args=[appointment.id])}
        # {reverse('delete_appointment', args=[appointment.id])}
        send_gmail(appointment.email, subject, body)

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

    # Enviar correo electrónico de notificación al cliente
    if appointment.email:
        subject = "Actualización de Cita"
        body = f"""
        Estimado/a {appointment.full_name},

        Su cita ha sido actualizada exitosamente.

        Detalles de la cita:
        Fecha y Hora de Inicio: {appointment.start_datetime.strftime('%d/%m/%Y %H:%M')}
        Fecha y Hora de Fin: {appointment.end_datetime.strftime('%d/%m/%Y %H:%M')}
        Mensaje: {appointment.message}

        Puede editar su cita en el siguiente enlace:
        {reverse('edit_appointment', args=[appointment.id])}

        Puede eliminar su cita en el siguiente enlace:
        {reverse('delete_appointment', args=[appointment.id])}

        Gracias,
        {company.name}
        """
        send_gmail(appointment.email, subject, body)

    return {
        'status': 'success',
        'appointment_id': appointment.id,
        'message': 'Cita actualizada exitosamente.'
    }