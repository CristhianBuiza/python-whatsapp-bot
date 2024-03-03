from openai import OpenAI
import shelve
import time
from dotenv import load_dotenv
import os
import time
import logging
from .micro import procesar_dni

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = "asst_ISNyN5kj7rlwzG8Q11Ipjzol"
client = OpenAI(api_key=OPENAI_API_KEY)

# Use context manager to ensure the shelf file is closed properly

def check_if_thread_exists(wa_id):
    with shelve.open("threads_db") as threads_shelf:
        thread_info = threads_shelf.get(wa_id, None)
        if thread_info:
            return thread_info["thread_id"]  # Si solo necesitas el thread_id
        return None

def store_thread(wa_id, thread_id, dni=None):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id] = {"thread_id": thread_id, "dni": dni}

def update_dni_in_thread(wa_id, dni):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id]["dni"] = dni
        
def update_confirm_dni_in_thread(wa_id, confirm_dni):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id]["confirm_dni"] = confirm_dni

def run_assistant(thread, name):
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve(OPENAI_ASSISTANT_ID)

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        # instructions=f"You are having a conversation with {name}",
    )

    # Wait for completion
    # https://platform.openai.com/docs/assistants/how-it-works/runs-and-run-steps#:~:text=under%20failed_at.-,Polling%20for%20updates,-In%20order%20to
    while run.status != "completed":
        # Be nice to the API
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    logging.info(f"Generated message: {new_message}")
    return new_message


def generate_response(message_body, wa_id, name):
    thread_id = None
    # es una tipo de base de datos, para persistir
    with shelve.open("threads_db") as threads_shelf:
        thread_info = threads_shelf.get(wa_id, None)
        
    # If a thread doesn't exist, create one and store it
    if not thread_info:
        logging.info(f"Creating new thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.create()
        store_thread(wa_id, thread.id)  # DNI is None by default
        thread_id = thread.id
        return "Hola, proporcione su DNI para continuar."
    else: 
        thread_id = thread_info['thread_id']
        if thread_info and thread_info.get("dni") is None or thread_info.get("confirm_dni") is False:
            # set dni in thread_info
            dni = procesar_dni(message_body)
            if dni == "error":
                return "No se encontro el dni, por favor ingrese un dni valido."
            else:
                update_dni_in_thread(wa_id, dni)
                return "Eres " + dni + "? responde con si o no"
        elif thread_info and thread_info.get("dni") is not None and thread_info.get("confirm_dni") is None:
            if message_body.lower() == "si":
                update_confirm_dni_in_thread(wa_id, True)
                return "En que te puedo ayudar?"
            elif message_body.lower() == "no":
                update_confirm_dni_in_thread(wa_id, False)
                return "Por favor, proporcione su DNI para continuar."
            else:
                return "Por favor, responda con 'si' o 'no'"
            
        thread = client.beta.threads.retrieve(thread_id)

        # Add message to thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_body,
        )

        # Run the assistant and get the new message
        new_message = run_assistant(thread, name)

        return new_message  