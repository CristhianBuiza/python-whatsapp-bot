# Construye Bots de WhatsApp con IA usando Python Puro

Esta guía te llevará a través del proceso de creación de un bot de WhatsApp utilizando la Meta Cloud API (anteriormente Facebook) con Python puro, y en particular, Flask. También integraremos eventos de webhook para recibir mensajes en tiempo real y utilizaremos OpenAI para generar respuestas de IA. Para más información sobre la estructura de la aplicación Flask.

## Prerrequisitos

1. Una cuenta de desarrollador de Meta — Si no tienes una, puedes [crear una cuenta de desarrollador de Meta aquí](https://developers.facebook.com/).
2. Una aplicación de negocio — Si no tienes una, puedes [aprender a crear una aplicación de negocio aquí](https://developers.facebook.com/docs/development/create-an-app/). Si no ves la opción de crear una aplicación de negocio, selecciona **Otro** > **Siguiente** > **Negocio**.
3. Familiaridad con Python para seguir el tutorial.

## Tabla de Contenidos

- [Construye Bots de WhatsApp con IA usando Python Puro](#construye-bots-de-whatsapp-con-ia-usando-python-puro)
  - [Prerrequisitos](#prerrequisitos)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Comenzar](#comenzar)
  - [Paso 1: Seleccionar Números de Teléfono](#paso-1-seleccionar-números-de-teléfono)
  - [Paso 2: Enviar Mensajes con la API](#paso-2-enviar-mensajes-con-la-api)
  - [Paso 3: Configurar Webhooks para Recibir Mensajes](#paso-3-configurar-webhooks-para-recibir-mensajes)
    - [Iniciar tu aplicación](#iniciar-tu-aplicación)
    - [Lanzar ngrok](#lanzar-ngrok)
    - [Integrar WhatsApp](#integrar-whatsapp)
    - [Probar la Integración](#probar-la-integración)
  - [Paso 4: Entender la Seguridad de Webhook](#paso-4-entender-la-seguridad-de-webhook)
    - [Solicitudes de Verificación](#solicitudes-de-verificación)
    - [Validando Solicitudes de Verificación](#validando-solicitudes-de-verificación)
    - [Validando Cargas Útiles](#validando-cargas-útiles)
  - [Paso 5: Aprender sobre la API y Construir Tu Aplicación](#paso-5-aprender-sobre-la-api-y-construir-tu-aplicación)
  - [Paso 6: Integrar IA en la Aplicación](#paso-6-integrar-ia-en-la-aplicación)
  - [Paso 7: Añadir un Número de Teléfono](#paso-7-añadir-un-número-de-teléfono)

## Comenzar

1. **Visión General & Configuración**: Comienza tu viaje [aquí](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started).
2. **Localiza Tus Bots**: Tus bots se pueden encontrar [aquí](https://developers.facebook.com/apps/).
3. **Documentación de la API de WhatsApp**: Familiarízate con la [documentación oficial](https://developers.facebook.com/docs/whatsapp).
4. **Guía Útil**: Aquí hay una [guía basada en Python](https://developers.facebook.com/blog/post/2022/10/24/sending-messages-with-whatsapp-in-your-python-applications/) para enviar mensajes.
5. **Documentación de la API para Enviar Mensajes**: Revisa [esta documentación](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages).

## Paso 1: Seleccionar Números de Teléfono

- Asegúrate de que WhatsApp esté añadido a tu aplicación.
- Comienzas con un número de prueba que puedes usar para enviar mensajes a hasta 5 números.
- Ve a Configuración de la API y localiza el número de prueba desde el cual estarás enviando mensajes.
- Aquí, también puedes añadir números para enviar mensajes. Introduce tu **propio número de WhatsApp**.
- Recibirás un código en tu teléfono vía WhatsApp para verificar tu número.

## Paso 2: Enviar Mensajes con la API

1. Obtén un token de acceso de 24 horas desde la sección de acceso de la API.
2. Se mostrará un ejemplo de cómo enviar mensajes usando un comando `curl` que puede ser enviado desde el terminal o con una herramienta como Postman.
3. Convertamos eso en una [función de Python con la biblioteca request]
4. Crea archivos `.env` basados en `example.env` y actualiza las variables requeridas.
5. Recibirás un mensaje de "Hola Mundo" (Espera un retraso de 60-120 segundos para el mensaje).

Creando un acceso que funciona más de 24 horas

1. Crea un [usuario del sistema a nivel de cuenta de Meta Business](https://business.facebook.com/settings/system-users).
2. En la página de Usuarios del Sistema, configura los activos para tu Usuario del Sistema, asignando tu aplicación de WhatsApp con control total. No olvides hacer clic en el botón Guardar Cambios.

3. Ahora haz clic en `Generar nuevo token` y selecciona la aplicación, y luego elige cuánto tiempo será válido el token de acceso. Puedes elegir 60 días o que nunca expire.
4. Selecciona todos los permisos, ya que estaba encontrando errores cuando solo seleccionaba los de WhatsApp.
5. Confirma y copia el token de acceso.

Ahora tenemos que encontrar la siguiente información en el **Tablero de Aplicaciones**:

- **APP_ID**: "<TU-WHATSAPP-BUSINESS-APP_ID>" (Encontrado en el Tablero de Aplicaciones)
- **APP_SECRET**: "<TU-WHATSAPP-BUSINESS-APP_SECRET>" (Encontrado en el Tablero de Aplicaciones)
- **RECIPIENT_WAID**: "<TU-NÚMERO-DE-TELÉFONO-DE-PRUEBA-RECIPIENTE>" (Este es tu ID de WhatsApp, es decir, número de teléfono. Asegúrate de que esté añadido a la cuenta como se muestra en el mensaje de prueba de ejemplo.)
- **VERSION**: "v18.0" (La última versión de la Meta Graph API)
- **ACCESS_TOKEN**: "<TU-TOKEN-DE-ACCESO-DE-USUARIO-DEL-SISTEMA>" (Creado en el paso anterior)

> Solo puedes enviar un mensaje de tipo plantilla como tu primer mensaje a un usuario. Por eso tienes que enviar una respuesta primero antes de que continuemos. Me tomó 2 horas darme cuenta de esto.

## Paso 3: Configurar Webhooks para Recibir Mensajes

> Por favor, ten en cuenta que esta es la parte más difícil de este tutorial.

#### Iniciar tu aplicación

- Asegúrate de tener una instalación de python o entorno e instala los requisitos: `pip install -r requirements.txt`
- Ejecuta tu aplicación Flask localmente ejecutando [run.py]

#### Lanzar ngrok

Los pasos a continuación se toman de la [documentación de ngrok](https://ngrok.com/docs/integrations/whatsapp/webhooks/).

> ¡Necesitas un dominio ngrok estático porque Meta valida tu dominio ngrok y certificado!

Una vez que tu aplicación esté funcionando con éxito en localhost, ¡pongámosla en internet de manera segura usando ngrok!

1. Si aún no eres usuario de ngrok, simplemente regístrate en ngrok de forma gratuita.
2. Descarga el agente de ngrok.
3. Ve al tablero de ngrok, haz clic en Tu [Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken), y copia tu Authtoken.
4. Sigue las instrucciones para autenticar tu agente ngrok. Solo tienes que hacer esto una vez.
5. En el menú de la izquierda, expande Cloud Edge y luego haz clic en Dominios.
6. En la página de Dominios, haz clic en + Crear Dominio o + Nuevo Dominio. (aquí todos pueden comenzar con [un dominio gratuito](https://ngrok.com/blog-post/free-static-domains-ngrok-users))
7. Inicia ngrok ejecutando el siguiente comando en una terminal en tu escritorio local:

```
ngrok http 8000 --domain tu-dominio.ngrok-free.app
```

8. ngrok mostrará una URL donde tu aplicación localhost está expuesta a internet (copia esta URL para usarla con Meta).

#### Integrar WhatsApp

En el Tablero de Aplicaciones de Meta, ve a WhatsApp > Configuración, luego haz clic en el botón Editar.

1. En el popup de Editar URL de callback de webhook, ingresa la URL proporcionada por el agente de ngrok para exponer tu aplicación a internet en el campo URL de Callback, con /webhook al final
