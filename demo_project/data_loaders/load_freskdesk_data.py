if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from demo_project.data_loaders.freshdesk_client import FreshdeskClient


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    fd = FreshdeskClient(freshdesk_domain="<domain>.freshdesk.com", api_key="")
    agents_data = fd.utils.list_agents()
    contacts_data = fd.utils.list_contacts()
    tickets_data = fd.utils.list_tickets()
    groups_data = fd.utils.list_groups()
    companies_data = fd.utils.list_companies()
    return {"agents": agents_data, "contacts": contacts_data, "tickets": tickets_data,
            "groups": groups_data, "companies": companies_data}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
