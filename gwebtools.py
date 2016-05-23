from urllib.request import urlopen
from bs4 import BeautifulSoup

i = 2969
while i > 0:
    try:
        soup = BeautifulSoup(urlopen("http://whois.gwebtools.com/tld/com/%d" % i).read(), "html.parser")
        lines = soup.find("table").findAll("tr")[1:]

        if len(lines) > 0:
            print("(#) - Page # %d for Extension \".com\" !" % i)
            domains_results_log = open("Zarouali_Domaines_log.txt", 'a')
            domains_results_log.write("(#) - Page # %d for Extension \".com\" !\n" % i)
            domains_results_log.close()
            for line in lines:
                domain = line.find("td").text
                domains_results = open("Zarouali_Domaines.txt", 'a')
                domains_results.write("%s\n" % domain)
                domains_results.close()
        else:
            break
    except Exception as ex:
        domains_results_log_err = open("Zarouali_Domaines_log_Errors.txt", 'a')
        domains_results_log_err.write("(#) - Page # %d for Extension \".com\" !\n" % i)
        domains_results_log_err.close()
        print(type(ex))
    finally:
        i += 1

i = 1
while i > 0:
    try:
        soup = BeautifulSoup(urlopen("http://whois.gwebtools.com/tld/net/%d" % i).read(), "html.parser")
        lines = soup.find("table").findAll("tr")[1:]

        if len(lines) > 0:
            print("(#) - Page # %d for Extension \".com\" !" % i)
            domains_results_log = open("Zarouali_Domaines_log.txt", 'a')
            domains_results_log.write("(#) - Page # %d for Extension \".net\" !\n" % i)
            domains_results_log.close()
            for line in lines:
                domain = line.find("td").text
                domains_results = open("Zarouali_Domaines.txt", 'a')
                domains_results.write("%s\n" % domain)
                domains_results.close()
        else:
            break
    except Exception as ex:
        domains_results_log_err = open("Zarouali_Domaines_log_Errors.txt", 'a')
        domains_results_log_err.write("(#) - Page # %d for Extension \".net\" !\n" % i)
        domains_results_log_err.close()
        print(type(ex))
    finally:
        i += 1
