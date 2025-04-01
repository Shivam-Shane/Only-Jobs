templates = (
    "You are a helpful AI assistant whose task is to classify the given user post "
    "as a valid job description or job title.\n\n"
    "{post_content}\n\n"
    "Note: Carefully check its authenticity and validity before responding. "
    "Only classify it as 'valid' if you are more than 95% sure; otherwise, state it as 'invalid'.\n"
    "Valid return responses are: ['valid', 'invalid']\n"
    "NO PREAMBLE"
)
