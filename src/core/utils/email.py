def hide_email(email):
    # Split the email into username and domain
    username, domain = email.split("@")

    # Hide part of the username
    hidden = username[0] + "*" * (len(username) - 2) + username[-1]

    # Reconstruct the hidden email
    return hidden + "@" + domain
