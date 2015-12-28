from rolepermissions.roles import AbstractUserRole


class Mailer(AbstractUserRole):
    available_permissions = {
        'access_website': True,
        'create_jobs': True
    }


class TeamLeader(AbstractUserRole):
    available_permissions = {
        'add_seed_list': True,
    }

    available_permissions.update(Mailer.available_permissions)


class Manager(AbstractUserRole):
    available_permissions = {
        'grant_team_leader': True,
    }

    available_permissions.update(TeamLeader.available_permissions)


class SystemAdmin(AbstractUserRole):
    available_permissions = {
        'grant_manager': True,
    }

    available_permissions.update(Manager.available_permissions)
