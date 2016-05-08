from bs4 import BeautifulSoup
from urllib.request import urlopen

extentions = ["com", "net", "org", "info", "cn", "de", "ru", "co.uk", "com.br", "it", "jp", "nl", "fr", "pl", "co.cc",
              "com.au", "co.jp", "biz", "es", "eu", "us", "com.cn", "ca", "tk", "in", "se", "ro", "cz", "ch", "at",
              "co.za", "tv", "ir", "gr", "dk", "hu", "be", "com.ar", "bz.cm", "org.uk", "no", "cc", "com.ua", "fi",
              "com.mx", "co.kr", "com.tw", "co.il", "ws", "com.tr", "sk", "ie", "cl", "co.in", "pt", "gov.cn", "co",
              "co.tv", "co.nz", "vn", "lt", "kz", "gov", "by", "com.pl", "lv", "bg", "ne.jp", "nu", "si", "com.my",
              "org.br", "hr", "ua", "net.cn", "name", "ac.jp", "com.vn", "com.hk", "to", "ee", "co.id", "edu.cn",
              "org.cn", "com.sg", "az", "fm", "org.ua", "gov.uk", "hk", "mp", "ac.uk", "cz.cc", "com.co", "tw", "co.th",
              "br", "ae", "com.ve", "in.th", "net.au", "lu", "ac.in", "com.pe", "com.pk", "mx", "bz", "am", "gov.in",
              "ac.ir", "org.au", "pk", "ge", "net.ru", "kr", "gr.jp", "ba", "com.ph", "ma", "lk", "sg", "is", "ph",
              "im", "gov.br", "gov.tr", "md", "net.ua", "my", "uk.com", "org.tr", "org.tw", "in.ua", "net.pl", "com.es",
              "edu.mx", "org.ru", "edu.pl", "com.pt", "edu.tw", "edu.br", "mn", "com.uy", "com.sa", "ac.th", "gov.tw",
              "ly", "pe", "travel", "cv.ua", "edu.vn", "uz", "li", "gov.au", "org.za", "pro", "edu.pk", "org.pl",
              "net.br", "org.in", "edu.hk", "ac.id", "org.mx", "gov.co", "gov.my", "edu.co", "coop", "gov.sa", "ne",
              "gov.ar", "edu.au", "kg", "co.ke", "com.ec", "com.ru", "ag", "org.il", "org.ar", "edu.tr", "st", "com.do",
              "com.mk", "ac.kr", "cm", "com.bd", "edu.pe", "ca.us", "org.nz", "co.nr", "com.com", "dz", "fr.nf",
              "com.np", "cu", "tc", "uz.ua", "co.at", "gov.vn", "edu.ar", "net.in", "cx", "edu.my", "ms", "us.com",
              "aero", "org.hk", "com.nu", "int", "com.py", "gov.pl", "edu.ms", "gov.ph", "gov.pk", "al", "ps", "gov.za",
              "ac.cn", "com.cy", "com.eg", "io", "mu", "com.hr", "gov.sg", "ac", "ac.at", "info.pl", "vc", "gov.eg",
              "sh.cn", "vg", "net.nz", "edu.sa", "gs", "mk", "gov.hk", "com.gt", "gov.bd", "as", "ec", "net.id",
              "co.cr", "edu.in", "pl.ua", "com.ng", "net.tr", "uk", "", "edu.eg", "sc", "co.ir", "om", "sy", "co.yu",
              "gov.ua", "com.gr", "com.sv", "edu.sg", "eu.com", "gov.ec", "org.sg", "gd.cn", "net.my", "sh", "cd",
              "com.bo", "mil", "vn.ua", "com.kh", "com.kw", "com.pa", "de.vu", "org.co", "edu.ng", "co.be", "org.pe",
              "org.pk", "gov.ng", "net.pk", "ac.za", "gov.il", "net.tw", "co.tz", "edu.ph", "gov.az", "net.sa", "so",
              "tj", "ac.il", "com.qa", "dj", "edu.ve", "mn.us", "pro.br", "gov.ae", "hn", "jo", "pe.kr", "com.ni",
              "name.vn", "org.es", "org.sa", "sn", "ac.ma", "com.lb", "edu.ru", "gov.ve", "cr", "nc.us", "id.au",
              "net.vn", "org.my", "edu.ec", "gov.ir", "co.mz", "edu.uy", "org.vn", "at.ua", "cn.mu", "co.ug", "com.mt",
              "mg", "co.ao", "com.ro", "net.com", "org.ir", "ac.nz", "co.zw", "com.na", "sm", "tm.fr", "c", "co.de",
              "gov.lk", "is.com", "co.us", "gov.ma", "tl", "tr.gg", "org.eg", "sd", "co.bw", "edu.ua", "gov.kw",
              "net.tc", "ad.jp", "com.fr", "gd", "uk.net", "bj.cn", "gi", "nc", "net.ve", "org.ve", "biz.pl", "bm",
              "bo", "eu.org", "gov.by", "il.us", "ma.us", "org.bd", "re", "co.hu", "es.tl", "ac.ae", "co.cu", "fo",
              "gov.do", "gov.mo", "gov.om", "i", "bf", "co.nl", "com.bh", "do", "edu.sv", "fr.cr", "gov.ge", "gov.qa",
              "gov.sy", "lu.tl", "org.uy", "va.us", "ac.cr", "com.gh", "de.tl", "edu.jo", "edu.lb", "gov.jo", "gov.pt",
              "inf", "net.co", "org.np", "pf", "tm", "tv.br", "ac.bd", "ao", "com.ly", "edu.do", "lc", "vu", "af", "ar",
              "au", "com.mo", "cx.cc", "edu.gr", "edu.kw", "es.kr", "gov.iq", "mr", "net.bd", "net.gr", "net.mx", "pr",
              "ug", "bh", "bz.it", "do.am", "edu.bd", "ac.tz", "cn.com", "com.bn", "com.net", "gg", "gl", "gov.bh",
              "gov.ly", "je", "mc", "museum", "net.uk", "org.gr", "pa.us", "sk.ca", "sn.cn", "tt", "bt", "com.in",
              "edu.az", "edu.bo", "edu.np", "gov.lb", "gov.mk", "ms.kr", "net.ph", "ve", "ac.be", "az.us", "co.ae",
              "co.zm", "com.be", "com.mv", "gov.cy", "gov.py", "gov.ye", "gp", "gy", "md.us", "net.il", "qa", "tr",
              "ac.ke", "bb", "com.pr", "com.uk", "de.com", "edu.om", "edu.sy", "fi.cr", "ga.us", "gov.bn", "gov.bo",
              "gov.dz", "gov.gh", "gov.gr", "gov.lv", "gov.rw", "ht", "in.us", "mo.us", "net.ar", "org.mk", "re.kr",
              "sl", "vi", "au.com", "co.tt", "com.fj", "cv", "de.de", "edu.gt", "edu.ly", "fi.it", "gm", "gov.it",
              "id.us", "info.tr", "nz", "org.ng", "sc.us", "sr", "to.it"]

# soup = BeautifulSoup(urlopen("http://whois.gwebtools.com/tld/to.it/5").read(), "html.parser")
for ext in extentions:
    i = 1
    while i > 0:
        soup = BeautifulSoup(urlopen("http://whois.gwebtools.com/tld/%s/%s" % (ext, str(i))).read(), "html.parser")
        lines = soup.find("table").findAll("tr")[1:]

        if len(lines) > 0:
            print("(#) - Page # %d for Extension \".%s\" !" % (i, ext))
            domains_results_log = open("Zarouali_Domaines_log.txt", 'a')
            domains_results_log.write("(#) - Page # %d for Extension \".%s\" !\n" % (i, ext))
            domains_results_log.close()
            for line in lines:
                domain = line.find("td").text
                domains_results = open("Zarouali_Domaines.txt", 'a')
                domains_results.write("%s\n" % domain)
                domains_results.close()
            i += 1
        else:
            break
