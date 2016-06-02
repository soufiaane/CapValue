import dns.resolver

with open("cvc1.txt") as ips:
    for ip in ips:
        ip = ip.replace("\n", "")
        x = ip.split(".")
        x.reverse()
        rip = ".".join(x)
        try:
            x = dns.resolver.query("%s.pbl.spamhaus.org." % rip, "A")
            with open(".\\cvc1\\pbl_spamhaus.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

        try:
            dns.resolver.query("%s.sbl.spamhaus.org." % rip, 'A')
            with open(".\\cvc1\\sbl_spamhaus.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

        try:
            dns.resolver.query("%s.xbl.spamhaus.org." % rip, 'A')
            with open(".\\cvc1\\xbl_spamhaus.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

        try:
            dns.resolver.query("%s.b.barracudacentral.org." % rip, 'A')
            with open(".\\cvc1\\b_barracudacentral.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

with open("cvc3.txt") as ips:
    for ip in ips:
        ip = ip.replace("\n", "")
        x = ip.split(".")
        x.reverse()
        rip = ".".join(x)
        try:
            dns.resolver.query("%s.pbl.spamhaus.org." % rip, 'A')
            with open(".\\cvc3\\pbl_spamhaus.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

        try:
            dns.resolver.query("%s.sbl.spamhaus.org." % rip, 'A')
            with open(".\\cvc3\\sbl_spamhaus.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

        try:
            dns.resolver.query("%s.xbl.spamhaus.org." % rip, 'A')
            with open(".\\cvc3\\xbl_spamhaus.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

        try:
            dns.resolver.query("%s.b.barracudacentral.org." % rip, 'A')
            with open(".\\cvc3\\b_barracudacentral.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

with open("opm16.txt") as ips:
    for ip in ips:
        ip = ip.replace("\n", "")
        x = ip.split(".")
        x.reverse()
        rip = ".".join(x)
        try:
            dns.resolver.query("%s.pbl.spamhaus.org." % rip, 'A')
            with open(".\\opm16\\pbl_spamhaus.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

        try:
            dns.resolver.query("%s.sbl.spamhaus.org." % rip, 'A')
            with open(".\\opm16\\sbl_spamhaus.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

        try:
            dns.resolver.query("%s.xbl.spamhaus.org." % rip, 'A')
            with open(".\\opm16\\xbl_spamhaus.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

        try:
            dns.resolver.query("%s.b.barracudacentral.org." % rip, 'A')
            with open(".\\opm16\\b_barracudacentral.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

with open("opm40.txt") as ips:
    for ip in ips:
        ip = ip.replace("\n", "")
        x = ip.split(".")
        x.reverse()
        rip = ".".join(x)
        try:
            dns.resolver.query("%s.pbl.spamhaus.org." % rip, 'A')
            with open(".\\opm40\\pbl_spamhaus.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

        try:
            dns.resolver.query("%s.sbl.spamhaus.org." % rip, 'A')
            with open(".\\opm40\\sbl_spamhaus.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

        try:
            dns.resolver.query("%s.xbl.spamhaus.org." % rip, 'A')
            with open(".\\opm40\\xbl_spamhaus.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass

        try:
            dns.resolver.query("%s.b.barracudacentral.org." % rip, 'A')
            with open(".\\opm40\\b_barracudacentral.txt", 'a') as file:
                file.write("%s\n" % ip)
        except:
            pass
