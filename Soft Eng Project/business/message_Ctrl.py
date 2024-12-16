from data_access.adminMessageDatabase import insert_message

def create_message(course_id, only_prof, content):
    """
    Business logic for creating a new message.
    """
    if not course_id or not content:
        raise ValueError("Course ID and message content are required.")
    
    if len(content) > 100:
        raise ValueError("Message content cannot exceed 100 characters.")
    
    return insert_message(course_id, only_prof, content)

from data_access.adminMessageDatabase import retrieve_messages

def fetch_messages():
    """
    Fetch all messages through the business layer.
    """
    return retrieve_messages()