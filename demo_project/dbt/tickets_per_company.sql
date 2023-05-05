with tickets as (
    select * from {{ source("fd_source","tickets") }}
),
companies as (
    select "company_id", "name" as "company_name" from {{ source("fd_source","companies") }}
),
agg_tickets as (
    select "company_id", count(*) as "ticket_count" from tickets group by "company_id"
),
final as (
    select "company_name","ticket_count" from agg_tickets t
    inner join companies c
    on t."company_id" = c."company_id"
)
select * from final