import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from mcp.server.fastmcp import FastMCP
from .gmail_auth import authenticate_gmail

mcp = FastMCP("Gmail MCP Server")

@mcp.tool()
def get_latest_emails(max_results: int = 5) -> str:
    """
    Reads and summarizes the latest emails from the user's INBOX.
    The AI should use this tool when the user asks to check, read, or summarize their recent emails.
    """
    try:
        creds = authenticate_gmail()
        service = build('gmail', 'v1', credentials=creds)
        
        # Fetching the IDs of the latest emails from the INBOX
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_results).execute()
        messages = results.get('messages', [])
        
        if not messages:
            return "No new messages found in the inbox."
        
        output = []
        # Fetching the details of each email (Sender, Subject, Snippet)
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = msg_data['payload']['headers']
            
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            snippet = msg_data.get('snippet', '') # A short preview of the email body
            
            output.append(f"From: {sender}\nSubject: {subject}\nSnippet: {snippet}\n{'-'*30}")
            
        return "\n".join(output)
    
    except Exception as e:
        return f"An error occurred while reading emails: {str(e)}"

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """
    Sends an email to the specified address (to) with the given subject and body.
    The AI should use this tool when the user requests to send, draft, or compose an email to someone.
    """
    try:
        creds = authenticate_gmail()
        service = build('gmail', 'v1', credentials=creds)
        
        message = EmailMessage()
        message.set_content(body)
        message['To'] = to
        message['From'] = 'me' 
        message['Subject'] = subject
        
        # Converting the message to the URL-safe Base64 format required by the Gmail API
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}
        
        service.users().messages().send(userId='me', body=create_message).execute()
        return f"Email successfully sent to: {to}"
        
    except Exception as e:
        return f"An error occurred while sending the email: {str(e)}"