from sql_writer import build_sql_statements


def test_build_sql_statements_basic():
    chargeable_rows = [{
        "partnerID": 1001,
        "product": "core.product",
        "partnerPurchasedPlanID": "ABC123",
        "plan": "Standard",
        "usage": 5
    }]
    domain_pairs = {("ABC123", "example.com")}

    chargeable_sql, domains_sql = build_sql_statements(chargeable_rows, domain_pairs)

    assert "INSERT INTO chargeable" in chargeable_sql
    assert "'core.product'" in chargeable_sql
    assert "'ABC123'" in chargeable_sql
    assert "'Standard'" in chargeable_sql
    assert "5" in chargeable_sql

    assert "INSERT INTO domains" in domains_sql
    assert "'example.com'" in domains_sql

def test_escaping_single_quotes():
    chargeable_rows = [{
        "partnerID": 2002,
        "product": "plan'with'quote",
        "partnerPurchasedPlanID": "GUID'123",
        "plan": "Standard'Plan",
        "usage": 10
    }]
    domain_pairs = {("GUID'123", "domain'quoted.com")}

    chargeable_sql, domains_sql = build_sql_statements(chargeable_rows, domain_pairs)

    assert "plan''with''quote" in chargeable_sql
    assert "GUID''123" in chargeable_sql
    assert "Standard''Plan" in chargeable_sql
    assert "domain''quoted.com" in domains_sql
