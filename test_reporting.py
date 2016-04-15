from new_tasks import report_hotmail
import requests, datetime
from openpyxl import Workbook


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
        print(("*"*25 + "%s" + "*"*25) % team.get("team_name", None))
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
    wb.save("sample.xlsx")

get_planning()
# report_hotmail(actions='FM', subject='Anniversaire', email={'login': 'juliannadauermy5880@hotmail.com', 'password': 'WEmy5612'}, proxy=None)
# report_hotmail(actions='FM,AC', subject='Anniversaire', email={'login': 'marthalexandrexh1730@hotmail.com', 'password': 'GCxh2312'}, proxy=None)
# report_hotmail(actions='SS', subject='Art', email={'login': 'report-serv2@hotmail.com', 'password': 'capvalue2016'}, proxy=None)
# report_hotmail(actions='SS', subject='Art', email={'login': 'test-soufyane26@hotmail.com', 'password': 'capvalue2016'}, proxy=None)
# report_hotmail.apply_async(kwargs={'actions': 'NS,RI', 'subject': 'ssf',
#                                    'email': {'login': 'mbennett900@hotmail.com', 'password': 'cvc22015'},
#                                    'proxy': None}, queue='smghanen')
