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
                        if ":" in str(spf_value):
                            if str(spf_value).split(":")[0].endswith("include"):
                                include_domain = str(spf_value).split(":")[1]
                                ret += "%s " % new_spf_check(None, include_domain)
                            elif str(spf_value).split(":")[0].endswith("redirect"):
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


@app.task(name='spf_check_task', bind=True)
def spf_check_task(self, reputation, domain):
    try:
        result = spf_check(reputation, domain)
        return result
    except Exception:
        return "Error"
