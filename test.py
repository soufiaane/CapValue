from __future__ import absolute_import
from celeryTasks.celerySettings import app
from IPy import IP
import dns.resolver
import json
import socket
import pprint

pp = pprint.PrettyPrinter(indent=4)


def is_valid_ipv4_address(address):
    if "/" in address:
        address = address[:address.index("/")]
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
    return True


def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True


def spf_check(reputation, domain):
    ret = {"Domain": domain, "Reputation": reputation, "SPF": [], "TXT": []}
    spf1 = {"A": [], "IP4": [], "IP6": [], "MX": [], "PTR": [], "INCLUDE": [], "REDIRECT": []}
    spf2 = {"A": [], "IP4": [], "IP6": [], "MX": [], "PTR": [], "INCLUDE": [], "REDIRECT": []}
    try:
        for answer in dns.resolver.query(domain, 'TXT'):
            for result in answer.strings:
                # region SPF1
                if result.startswith("spf1") or result.startswith("v=spf1"):
                    results_content = result.split(" ")[1:]
                    for spf_value in results_content:
                        if spf_value is "" or spf_value is " ":
                            continue
                        spf_value = spf_value.lower()
                        if spf_value.startswith("+") and not spf_value.endswith("all"):
                            spf_value = spf_value.replace("+", "")
                        if str(spf_value).endswith("all"):
                            spf1["All"] = str(spf_value).replace("all", "")
                        elif str(spf_value).startswith("ip4") or str(spf_value).startswith("+ip4"):
                            spf1["IP4"].append(str(spf_value).split(":")[1])
                        elif str(spf_value).startswith("ip6") or str(spf_value).startswith("+ip6"):
                            spf1["IP6"].append(str(spf_value[spf_value.index("ip6:"):]).replace("ip6:", ""))
                        elif str(spf_value).startswith("a"):
                            try:
                                if len(spf_value) == 1:
                                    a_records = dns.resolver.query(domain, 'A')
                                    for a_record in a_records:
                                        spf1["A"].append({"Domain": domain, "IP": a_record.address})
                                else:
                                    new_a_domain = spf_value.split(":")[1]
                                    a_records = dns.resolver.query(new_a_domain, 'A')
                                    for a_record in a_records:
                                        spf1["A"].append({"Domain": new_a_domain, "IP": a_record.address})
                            except dns.resolver.NXDOMAIN:
                                pass
                            except dns.resolver.NoAnswer:
                                pass
                            except dns.resolver.Timeout:
                                pass
                            except Exception as ex:
                                pp.pprint(type(ex))
                        elif str(spf_value).startswith("mx"):
                            try:
                                if len(spf_value) == 2:
                                    mx_records = dns.resolver.query(domain, 'MX')
                                    for mx_record in mx_records:
                                        spf1["MX"].append(str(mx_record))
                                else:
                                    new_mx_domain = spf_value.split(":")[1]
                                    mx_records = dns.resolver.query(new_mx_domain, 'MX')
                                    for mx_record in mx_records:
                                        spf1["MX"].append(str(mx_record))
                            except dns.resolver.NXDOMAIN:
                                pass
                            except dns.resolver.NoAnswer:
                                pass
                            except dns.resolver.Timeout:
                                pass
                            except Exception as ex:
                                pp.pprint(type(ex))
                        elif str(spf_value).startswith("ptr"):
                            pass
                        elif str(spf_value).startswith("exists"):
                            pass
                        elif str(spf_value).startswith("include"):
                            include_domain = str(spf_value).split(":")[1]
                            spf1["INCLUDE"].append(spf_check(None, include_domain))
                        elif str(spf_value).startswith("redirect"):
                            redirect_domain = str(spf_value).split("=")[1]
                            spf1["REDIRECT"].append(spf_check(None, redirect_domain))
                        elif str(spf_value).startswith("exp"):
                            pass
                        else:
                            if is_valid_ipv4_address(spf_value):
                                spf1["IP4"].append(str(spf_value))
                            elif is_valid_ipv6_address(spf_value):
                                spf1["IP6"].append(str(spf_value))
                            else:
                                pp.pprint(spf_value)
                    ret["SPF"].append({"Version": 1, "SPF": result, "Detail": spf1})
                # endregion

                # region SPF2
                elif result.startswith("spf2") or result.startswith("v=spf2"):
                    results_content = result.split(" ")[1:]
                    for spf_value in results_content:
                        if spf_value is "" or spf_value is " ":
                            continue
                        spf_value = spf_value.lower()
                        if spf_value.startswith("+") and not spf_value.endswith("all"):
                            spf_value = spf_value.replace("+", "")
                        if str(spf_value).endswith("all"):
                            spf2["All"] = str(spf_value).replace("all", "")
                        elif str(spf_value).startswith("ip4") or str(spf_value).startswith("+ip4"):
                            spf2["IP4"].append(str(spf_value).split(":")[1])
                        elif str(spf_value).startswith("ip6") or str(spf_value).startswith("+ip6"):
                            spf2["IP6"].append(str(spf_value[spf_value.index("ip6:"):]).replace("ip6:", ""))
                        elif str(spf_value).startswith("a"):
                            try:
                                if len(spf_value) == 1:
                                    a_records = dns.resolver.query(domain, 'A')
                                    for a_record in a_records:
                                        spf2["A"].append({"Domain": domain, "IP": a_record.address})
                                else:
                                    new_a_domain = spf_value.split(":")[1]
                                    a_records = dns.resolver.query(new_a_domain, 'A')
                                    for a_record in a_records:
                                        spf2["A"].append({"Domain": new_a_domain, "IP": a_record.address})
                            except dns.resolver.NXDOMAIN:
                                pass
                            except dns.resolver.NoAnswer:
                                pass
                            except dns.resolver.Timeout:
                                pass
                            except Exception as ex:
                                pp.pprint(type(ex))
                        elif str(spf_value).startswith("mx"):
                            try:
                                if len(spf_value) == 2:
                                    mx_records = dns.resolver.query(domain, 'MX')
                                    for mx_record in mx_records:
                                        spf2["MX"].append(str(mx_record))
                                else:
                                    new_mx_domain = spf_value.split(":")[1]
                                    mx_records = dns.resolver.query(new_mx_domain, 'MX')
                                    for mx_record in mx_records:
                                        spf2["MX"].append(str(mx_record))
                            except dns.resolver.NXDOMAIN:
                                pass
                            except dns.resolver.NoAnswer:
                                pass
                            except dns.resolver.Timeout:
                                pass
                            except Exception as ex:
                                pp.pprint(type(ex))
                        elif str(spf_value).startswith("ptr"):
                            pass
                        elif str(spf_value).startswith("exists"):
                            pass
                        elif str(spf_value).startswith("include"):
                            include_domain = str(spf_value).split(":")[1]
                            spf2["INCLUDE"].append(spf_check(None, include_domain))
                        elif str(spf_value).startswith("redirect"):
                            redirect_domain = str(spf_value).split("=")[1]
                            spf2["REDIRECT"].append(spf_check(None, redirect_domain))
                        elif str(spf_value).startswith("exp"):
                            pass
                        else:
                            if is_valid_ipv4_address(spf_value):
                                spf2["IP4"].append(str(spf_value))
                            elif is_valid_ipv6_address(spf_value):
                                spf2["IP6"].append(str(spf_value))
                            else:
                                pp.pprint(spf_value)
                    ret["SPF"].append({"Version 2": spf2})
                # endregion
                # region Other TXT Recorgs
                else:
                    ret["TXT"].append(result)
                    # target.write("%s;%s\n" % (domain, result))
                    # endregion
    except dns.resolver.NoAnswer as ex:
        errrors.write("%s: %s\n" % (domain, type(ex)))
    except dns.resolver.NXDOMAIN as ex:
        errrors.write("%s: %s\n" % (domain, type(ex)))
    except Exception as ex:
        pp.pprint(type(ex))
    finally:
        return ret


def new_spf_check(reputation, domain):
    if reputation is not None:
        ret = "%s;%s;" % (reputation, domain)
    else:
        ret = ""
    try:
        for answer in dns.resolver.query(domain, 'TXT'):
            for result in answer.strings:
                if result.startswith("spf1") or result.startswith("v=spf1") or result.startswith("spf2") or result.startswith("v=spf1"):
                    ret += "%s " % result
                    results_content = result.split(" ")[1:]
                    for spf_value in results_content:
                        spf_value = spf_value.lower()
                        if str(spf_value).startswith("include"):
                            include_domain = str(spf_value).split(":")[1]
                            ret += "%s " % new_spf_check(None, include_domain)
                        elif str(spf_value).startswith("redirect"):
                            redirect_domain = str(spf_value).split("=")[1]
                            ret += "%s " % new_spf_check(None, redirect_domain)
                        else:
                            continue
    except dns.resolver.NoAnswer:
        if reputation is not None:
            ret += "None"
    except dns.resolver.NXDOMAIN:
        if reputation is not None:
            ret += "None"
    except Exception as ex:
        if reputation is not None:
            ret += "None"
        pp.pprint(type(ex))
    finally:
        if ret.endswith(";"):
            ret += "None"
        return ret.strip()


def print_spf_to_file(resultat):
    reputation = resultat["Reputation"]
    domain = resultat["Domain"]
    text = ""
    spf = resultat["SPF"]
    if len(spf) == 0:
        if reputation:
            text = "None"
        else:
            pass
    else:
        for s in spf:
            if "SPF" in s.keys():
                text += "%s " % s["SPF"]
                for detail in s["Detail"]["INCLUDE"]:
                    text += "%s " % print_spf_to_file(detail)
                for detail in s["Detail"]["REDIRECT"]:
                    text += "%s " % print_spf_to_file(detail)
    if reputation:
        target = open("RECURSIVE_RESULTS.txt", 'a')
        target.write("%s;%s;%s\n" % (reputation, domain, text))
        target.close()
    else:
        return text


@app.task(name='spf_check_task', bind=True)
def spf_check_task(self, reputation, domain):
    try:
        result = new_spf_check(reputation, domain)
        return result
    except Exception as exc:
        self.retry(exc=exc, max_retries=20, countdown=1)
