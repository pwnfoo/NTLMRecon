from termcolor import colored


def print_banner():
    print(colored("""
         _   _ _____ _     ___  _________                     
        | \ | |_   _| |    |  \/  || ___ \                    
        |  \| | | | | |    | .  . || |_/ /___  ___ ___  _ __  
        | . ` | | | | |    | |\/| ||    // _ \/ __/ _ \| '_ \ 
        | |\  | | | | |____| |  | || |\ \  __/ (_| (_) | | | |
        \_| \_/ \_/ \_____/\_|  |_/\_| \_\___|\___\___/|_| |_| - @pwnfoo

             """ + colored("""v.0.4 beta - Y'all still exposing NTLM endpoints?
""", 'green') + colored("""
 Bug Reports, Feature Requests : https://git.io/JIR5z

""", "cyan"), 'red'))


INTERNAL_WORDLIST = [
    "/abs",
    "/adfs/services/trust/2005/windowstransport",
    "/adfs/ls/wia",
    "/aspnet_client/",
    "/Autodiscover",
    "/Autodiscover/AutodiscoverService.svc/root",
    "/Autodiscover/Autodiscover.xml",
    "/AutoUpdate/",
    "/CertEnroll/",
    "/CertProv",
    "/CertSrv/",
    "/Conf/",
    "/debug/",
    "/deviceupdatefiles_ext/",
    "/deviceupdatefiles_int/",
    "/dialin",
    "/ecp/",
    "/Etc/",
    "/EWS/",
    "/Exchange/",
    "/Exchweb/",
    "/GroupExpansion/",
    "/HybridConfig",
    "/iwa/authenticated.aspx",
    "/iwa/iwa_test.aspx",
    "/mcx",
    "/meet",
    "/Microsoft-Server-ActiveSync/",
    "/OAB/",
    "/ocsp/",
    "/owa/",
    "/PersistentChat",
    "/PhoneConferencing/",
    "/PowerShell/",
    "/Public/",
    "/Reach/sip.svc",
    "/RequestHandler/",
    "/RequestHandlerExt",
    "/RequestHandlerExt/",
    "/Rgs/",
    "/RgsClients",
    "/Rpc/",
    "/RpcWithCert/",
    "/scheduler",
    "/Ucwa",
    "/UnifiedMessaging/",
    "/WebTicket",
    "/WebTicket/WebTicketService.svc",
    "_windows/default.aspx?ReturnUrl=/",
]
