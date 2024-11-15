# EasySite

### todo
- migrate to postgres db
- ~~add whatsbtn~~
- ~~create date mer~~
- ~~create user scheduler page~~
- calendar crud for company admin 
   - c 
      - --limit the hours the company admin can book an appointment-- (can only multipliers)
      - --send an email to the user--
      - --autofill the form when a minibox is clicked--
   - r ead the appointments
      - ~~show the details in the modal~~
      - ~~use the configs~~
   - u pdate the 
      - ~~take in account the restrictions~~
   - d elete
      - ~~send an email to the user with a msg~~
- solve bugs:
   - ~~show the hour right in the editor of a busy time~~
---
- calendar crud for user
   - identifies if user o company admin
   - hide info according to de user:
      - c ~~allow creates to the user~~
      - r hide:
         - ~~cancel token~~
         - ~~each appointmentinfo~~
      - u ~~dont allow update~~
      - d ~~dont allow delete~~

   - update ui to sync it with the functions:
      - ~~don't show info in dialog when busy is cliked~~
- solve bugs:
   - ~~can`t schedule an appointment in the last time colinding with the resthours~~

- ~~Turn off/on calendar function from django panel~~
- ~~Check responsiveness of all pages~~
- ~~Create easy site landing page~~
- ~~migrate db to postgres supabase ~~
- solve appointments bug
- fix colors
- new layout when 1 or 2 products


### **Estructura General del Proyecto**

#### **1. Roles del Usuario**
- **Administrador Global:**
   - Gestiona todas las empresas dentro de la plataforma.
   - Tiene acceso a un panel completo donde puede crear, editar y eliminar empresas.
   
- **Administrador Empresa:**
   - Acceso limitado al panel de administración.
   - Puede modificar su página web (landing, catálogo, nosotros, contacto, botón de WhatsApp y agenda de citas).
   - Gestiona las citas a través de un calendario propio.
   
- **Usuario Final:**
   - Accede a la página web pública de la empresa.
   - Puede interactuar con el catálogo de productos/servicios.
   - Agenda citas, si la empresa tiene esta funcionalidad habilitada.

#### **2. Características de las Páginas Personalizables**
1. **Landing Page:**
   - Dos tipos de layout a elegir:
     - **Tipo A:** Carrusel de productos, secciones de "Nosotros" y "Contacto".
     - **Tipo B:** Video con botón que redirige a productos, secciones de "Nosotros" y "Contacto".
   
2. **Nosotros:**
   - Carrusel de imágenes.
   - Texto con descripciones detalladas.

3. **Catálogo:**
   - Lista de productos/servicios, cada uno con imagen, texto y precio.

4. **Contacto:**
   - Formulario que envía correos a la empresa.
   - Posibilidad de incluir un botón de WhatsApp con número y mensaje predeterminado.

5. **Información Obligatoria en Todas las Páginas:**
   - Icono (logo pequeño).
   - Logo mediano.
   - Nombre de la empresa.
   - Ubicación de la empresa.
   - Teléfono.
   - Correo electrónico.
   - Opcionales: Enlaces a Instagram y Facebook.

#### **3. Funcionalidad de Citas**
   - **Botón "Agenda tu cita":** 
     - Configurable: Puede aparecer en la navbar, landing page, y popup en la página de productos.
     - Activación opcional.

   - **Sistema de Citas:**
     - Calendario: El administrador de la empresa puede configurar horarios disponibles, días hábiles, duración de las citas, y tiempo de antelación mínima y máxima para agendar.
     - El usuario final elige día y hora, proporcionando su correo, número y nombre. Recibe una confirmación por correo.
     - El administrador de la empresa recibe un correo por cada nueva cita agendada.

---

### **Descripción Detallada del Proyecto**

#### **Nombre del Proyecto:** 
**EasySite** - Plataforma de creación de páginas web simples y personalizables para empresas.

**Descripción:**
EasySite es una plataforma que permite a las empresas crear, administrar y personalizar páginas web sencillas. Con un enfoque minimalista pero funcional, la plataforma está diseñada para proporcionar herramientas intuitivas para la creación de contenido empresarial, la gestión de citas y el contacto con los clientes. El administrador de la plataforma gestiona todas las empresas, mientras que cada empresa tiene su propio panel de administración con acceso limitado.

#### **Tecnologías Principales:**
- **Backend:** Django (manejo de usuarios, gestión de citas, administración de empresas).
- **Frontend:** Tailwind CSS + Shadcn (UI y estilos personalizables).
- **Bases de datos:** PostgreSQL (gestión de usuarios, empresas, citas y configuraciones).
- **Correo:** Django Email Backend (para el envío de confirmaciones de citas y correos de contacto).
- **Autenticación:** Django Allauth o similar (para el manejo de roles de administrador global y empresas).

#### **Características Clave:**
1. **Administrador Global:**
   - Creación y gestión de empresas.
   - Visualización de todas las páginas creadas por las empresas.

2. **Administrador Empresa:**
   - Personalización de la página web (landing, nosotros, catálogo, contacto).
   - Gestión de citas y calendarios.

3. **Usuario Final:**
   - Interacción con las páginas públicas de las empresas.
   - Posibilidad de agendar citas y contactar a la empresa.

#### **Flujo de Trabajo:**
1. El administrador global crea las empresas y les otorga acceso al panel de administración limitado.
2. Las empresas personalizan su página web con un editor sencillo que les permite ajustar el contenido de la landing page, la sección "Nosotros", el catálogo de productos, y el formulario de contacto.
3. Si lo desean, las empresas pueden activar la funcionalidad de agendar citas, gestionando su disponibilidad desde el panel de administración.
4. Los usuarios finales interactúan con la página web de la empresa, pudiendo ver productos, contactar por correo o WhatsApp, y agendar citas.

---

### **Pasos Detallados para la Implementación**

#### **1. Configuración del Entorno:**
- Instalar Django y configurar un nuevo proyecto.
  ```bash
  django-admin startproject EasySite
  cd EasySite
  python manage.py startapp core