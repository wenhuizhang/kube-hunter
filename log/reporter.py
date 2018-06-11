import logging
from prettytable import PrettyTable
from src.core.events import handler
from src.core.events.types import Vulnerability, Information, Service

services = list()
vulnerabilities = list()

EVIDENCE_PREVIEW = 40

@handler.subscribe(Vulnerability)
class VulnerabilityReport(object):
    def __init__(self, event):
        self.vulnerability = event

    def execute(self):
        logging.info("[VULNERABILITY - {name}] {desc}".format(
            name=self.vulnerability.get_name(),
            desc=self.vulnerability.explain(),
        ))
        vulnerabilities.append(self.vulnerability)
        # TODO: Add ActiveHunter replacement by id, when a vulnerability comes from active hunter, it replaces it's predecessor 

@handler.subscribe(Service)
class OpenServiceReport(object):
    def __init__(self, event):
        self.service = event

    def execute(self):
        logging.info("[OPEN SERVICE - {name}] IP:{host} PORT:{port}".format(
            name=self.service.name, 
            desc=self.service.desc, 
            host=self.service.host,
            port=self.service.port
        ))
        services.append(self.service)

def print_results(active):
    services_table = PrettyTable(["Service", "Location", "Description"])    
    for service in services:
        services_table.add_row([service.get_name(), "{}:{}{}".format(service.host, service.port, service.get_path()), service.explain()])
    
    column_names = ["Location", "Category", "Vulnerability", "Description"]
    if active: column_names.append("Evidence")

    vuln_table = PrettyTable(column_names)
    for vuln in vulnerabilities:
        row = ["{}:{}".format(vuln.host, vuln.port), vuln.component.name, vuln.get_name(), vuln.explain()]
        if active: 
            evidence = vuln.evidence[:EVIDENCE_PREVIEW] + "..." if len(vuln.evidence) > EVIDENCE_PREVIEW else vuln.evidence
            row.append(evidence)
        vuln_table.add_row(row)
        
    print "\nOpen Services:"
    print services_table
    print "\nVulnerabilities:"
    print vuln_table
    