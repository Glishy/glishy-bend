from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    available_permissions = {
        'deactivate_user': True,
        'activate_user': True,
        'change_user_permissions': True,
    }


class ContentCreator(AbstractUserRole):
    available_permissions = {
        "create_content": True,
        "view_content": True,
    }


class AudienceMember(AbstractUserRole):
    available_permissions = {
        "view_content": True,
    }
