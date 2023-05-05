from demo_project.data_loaders.models import Ticket, Customer


class Utils(object):
    def __init__(self, api):
        self._api = api

    def list_agents(self, **kwargs):
        url = "agents?"
        page = kwargs.get("page", 1)
        per_page = kwargs.get("per_page", 100)
        agents = []
        while True:
            this_page = self._api.call_api(method="GET",
                                           url=self._api._api_prefix + url + "page=%d&per_page=%d" % (page, per_page))
            agents += this_page
            if len(this_page) < per_page or "page" in kwargs:
                break
            page += 1
        return agents

    def list_tickets(self, **kwargs):
        filter_name = None
        if "filter_name" in kwargs:
            filter_name = kwargs["filter_name"]
            del kwargs["filter_name"]
        ticket_url = "tickets"
        if filter_name is not None:
            ticket_url += "?filter=%s&" % filter_name
        else:
            ticket_url += "?"

        if "updated_since" in kwargs:
            ticket_url += "updated_since=%s&" % kwargs["updated_since"]

        page = kwargs.get("page", 1)
        per_page = kwargs.get("per_page", 100)

        tickets = []
        while True:
            this_page = self._api.call_api(method="GET",
                                           url=self._api._api_prefix + ticket_url + "page=%d&per_page=%d" % (
                                           page, per_page))
            tickets += this_page
            if len(this_page) < per_page or "page" in kwargs:
                break
            page += 1

        return [Ticket(**t).transformed_output() for t in tickets]

    def list_contacts(self, **kwargs):
        list_contacts_url = "contacts?"
        page = kwargs.get("page", 1)
        per_page = kwargs.get("per_page", 100)
        contacts = []

        while True:
            this_page = self._api.call_api(method="GET",
                                           url=self._api._api_prefix + list_contacts_url + "page=%d&per_page=%d" % (
                                               page, per_page))
            contacts += this_page
            if len(this_page) < per_page or "page" in kwargs:
                break
            page += 1

        return contacts

    def list_groups(self, **kwargs):
        list_groups_url = "groups?"
        page = kwargs.get("page", 1)
        per_page = kwargs.get("per_page", 100)

        groups = []
        while True:
            this_page = self._api.call_api(method="GET",
                                           url=self._api._api_prefix + list_groups_url + "page=%d&per_page=%d" % (
                                               page, per_page))
            groups += this_page
            if len(this_page) < per_page or "page" in kwargs:
                break
            page += 1

        return groups

    def list_companies(self, **kwargs):
        list_companies_url = "companies?"
        page = kwargs.get("page", 1)
        per_page = kwargs.get("per_page", 100)
        companies = []
        while True:
            this_page = self._api.call_api(method="GET",
                                           url=self._api._api_prefix + list_companies_url + "page=%d&per_page=%d" % (
                                               page, per_page))
            companies += this_page
            if len(this_page) < per_page or "page" in kwargs:
                break

            page += 1

        return companies

    def get_customer(self, company_id):
        get_cust_url = "customers/%s" % company_id
        resp = self._api.call_api(method="GET", url=self._api._api_prefix + get_cust_url)
        return Customer(**resp)
