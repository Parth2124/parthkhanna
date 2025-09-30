# TODO: Fix Email Sending in Deployed Environment

## Tasks
- [ ] Update portfolioproject/settings.py to use environment variables for EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
- [ ] Add error handling and logging in core/views.py for email sending in contact and subscribe views
- [ ] Provide instructions to user for setting environment variables in Render deployment
- [ ] Test email sending locally and in deployed environment after changes

## Notes
- Root cause: Email credentials not set in deployed environment variables
- Solution: Use env vars in settings.py and add error handling in views.py
