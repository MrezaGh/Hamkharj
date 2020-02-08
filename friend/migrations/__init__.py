from invitations.utils import get_invitation_model
from simple_history import register


invitation = get_invitation_model()
register(invitation, app='friend')
