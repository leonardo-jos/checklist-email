import mailslurp_client

# create a mailslurp configuration
configuration = mailslurp_client.Configuration()
configuration.api_key['x-api-key'] = "ca64c3ff8e0e942e3733cef53e678ab36181edd811088892e2f3ba8ff1f11ba4"
with mailslurp_client.ApiClient(configuration) as api_client:
    # create an inbox
    inbox_controller = mailslurp_client.InboxControllerApi(api_client)
    inbox = inbox_controller.create_inbox()