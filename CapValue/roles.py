from rolepermissions.roles import AbstractUserRole


class TeamLeader(AbstractUserRole):
    available_permissions = {
        'create_medical_record': True,
    }


class Manager(AbstractUserRole):
    available_permissions = {
        'edit_pacient_file': True,
    }


class Mailer(AbstractUserRole):
    available_permissions = {
        'edit_pacient_file': True,
    }
