

# def upload_file(path):
#     # Upload a file with an "assistants" purpose
#     file = client.files.create(
#         file=open("../../fuente.pdf", "rb"), purpose="assistants"
#     )


# def create_assistant(file):
#     """
#     You currently cannot set the temperature for Assistant via the API.
#     """
#     assistant = client.beta.assistants.create(
#         name="WhatsApp AirBnb Assistant",
#         instructions="Eres un asistente",
#         tools=[{"type": "retrieval"}],
#         model="gpt-4-1106-preview",
#         file_ids=[file.id],
#     )
#     return assistant
