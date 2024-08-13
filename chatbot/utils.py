def merge_chat_history(chat_history):
    chat_text = "\n"
    for message in chat_history:
        chat_text += message["role"]+ ": "+message["content"]
    return chat_text
def merge_document(documents):
    return "\n\n".join([f"Document{i}: {document}" for i,document in enumerate(documents)])