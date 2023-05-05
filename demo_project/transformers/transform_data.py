from pandas import DataFrame
from itsdangerous import URLSafeSerializer

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd

s = URLSafeSerializer('secret-key')  # Read the secret key from key vault
table_column_mappings = {
    "tickets": "ticket_id,source,subject,priority,created_at,updated_at,due_by,status,company_id,requester_id,responder_id,spam,group_id,is_escalated,environment,platform,product_type",
    "contacts": "contact_id,name,email,job_title,mobile,phone,time_zone,description,address,created_at,updated_at,facebook_id,twitter_id,csat_rating,preferred_source,company_id",
    "agents": "agent_id,agent_level_id,name,email,mobile,job_title,active,time_zone,created_at,updated_at,last_active_at,available_since,type,available,occasional",
    "groups": "group_id,name,description,escalate_to,unassigned_for,business_hour_id,group_type,created_at,updated_at,auto_ticket_assign,agent_availability_status",
    "companies": "company_id,name,description,note,domains,created_at,updated_at,health_score,account_tier,renewal_date,industry"}


def modify_dataframe(df: DataFrame, table_name) -> DataFrame:
    if table_name == "tickets":
        df.rename(columns={'id': 'ticket_id'}, inplace=True)
        df['environment'] = df["custom_fields"].apply(lambda x: x.get('cf_environment', None))
        df['platform'] = df["custom_fields"].apply(lambda x: x.get('cf_platform', None))
        df['product_type'] = df["custom_fields"].apply(lambda x: x.get('product_type', None))
    elif table_name == "contacts":
        df.rename(columns={'id': 'contact_id'}, inplace=True)
        df = df.drop(['custom_fields'], axis=1)
    elif table_name == "groups":
        df.rename(columns={'id': 'group_id'}, inplace=True)
    elif table_name == "companies":
        df.rename(columns={'id': 'company_id'}, inplace=True)
    elif table_name == "agents":
        df.rename(columns={'id': 'agent_id'}, inplace=True)
        df['name'] = df["contact"].apply(lambda x: x.get('name', None))
        df['email'] = df["contact"].apply(lambda x: x.get('email', None))
        df['mobile'] = df["contact"].apply(lambda x: s.dumps(x) if not x.get('mobile', None) else None)
        df['job_title'] = df["contact"].apply(lambda x: x.get('job_title', None))
        df['active'] = df["contact"].apply(lambda x: x.get('active', False))
        df['time_zone'] = df["contact"].apply(lambda x: x.get('time_zone', False))

    columns = table_column_mappings.get(table_name).split(",")
    return df[columns]


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    return_items = {}
    # Specify your transformation logic here
    for key, value in data.items():
        inp_df = pd.DataFrame.from_dict(value)
        temp_df = modify_dataframe(inp_df, key)
        return_items[key] = temp_df.to_dict(orient="dict")

    return return_items


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
