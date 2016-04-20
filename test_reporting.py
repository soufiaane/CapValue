from new_tasks import report_hotmail
from openpyxl import Workbook
import requests, datetime
from celery import group
import time


def get_planning(date=datetime.date.today() + datetime.timedelta(days=1)):
    wb = Workbook()
    ws = wb.active
    day_name = date.strftime("%A")
    url = "http://192.168.0.250/workers/ajax.php"
    shifts = {"15": "Day Off", "16": "09H", "17": "14H30", "21": "Congé", "25": "05H", "26": "Maladie"}
    shift_colors = {"15": "999999", "16": "66ff66", "17": "ff9900", "21": "ff6666", "25": "33ccff", "26": "ffff00"}
    teams = requests.post(url, data={"what": "getteams"}).json()

    ws['D2'] = date

    ws['B4'] = "Nom & Prénom"
    ws['C4'] = day_name

    i = 5
    for team in teams:
        print(("*" * 25 + "%s" + "*" * 25) % team.get("team_name", None))
        members = requests.post(url, data={"what": "getmembers", "team": team.get("team", None)}).json()
        for member in members:
            member_name = member.get("name", None)
            shift = shifts.get(
                str(requests.post(url, data={"what": "getshft", "id": member.get("id", None), "date": date}).json()),
                None)
            ws['B%s' % str(i)] = member_name
            ws['C%s' % str(i)] = shift
            print("%s: %s" % (member_name, shift))
            i += 1
    wb.save("%s_%s.xlsx" % (day_name , str(date)))

# get_planning()


report_hotmail(actions='SS', subject='notifica', email={'login': 'ellansourwinebg2194@hotmail.com', 'password': 'RUbg3491'}, proxy=None)
# report_hotmail(actions='FM,CLS', subject='a', email={'login': 'jonathan13247@hotmail.com', 'password': 'cvc22016'}, proxy=None)

# tas = group(report_hotmail.s(actions='', subject='Anniversaire', proxy=None,
#                              email={'login': 'juliannadauermy5880@hotmail.com', 'password': 'WEmy5612'})
#             .set(queue='smghanen') for i in range(1))
#
# tas_results = tas.apply_async()
# time.sleep(60)
# for tas_result in tas_results:
#     print(tas_result.state)
