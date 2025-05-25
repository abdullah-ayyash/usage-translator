from transformer import clean_account_guid, transform_rows

def test_clean_account_guid_basic():
    assert clean_account_guid("abc123") == "abc123"

def test_clean_account_guid_with_special_chars():
    assert clean_account_guid("abc-123-!!") == "abc123"

def test_transform_rows_valid_data():
    rows = [{
        "PartnerID": "1001",
        "PartNumber": "P123",
        "accountGuid": "abc-123",
        "itemCount": "1000",
        "domains": "example.com",
        "plan": "Standard"
    }]
    typemap = {"P123": "core.service"}
    skip_partners = set()
    unit_factors = {"P123": 1000}

    chargeable, domains, totals, errors = transform_rows(rows, typemap, skip_partners, unit_factors)

    assert len(chargeable) == 1
    assert chargeable[0]["usage"] == 1
    assert domains == {("abc123", "example.com")}
    assert not errors

def test_transform_rows_skips_missing_part_number():
    rows = [{
        "PartnerID": "1001",
        "PartNumber": "",
        "accountGuid": "abc123",
        "itemCount": "5",
        "domains": "example.com",
        "plan": "Standard"
    }]
    typemap = {}
    skip_partners = set()
    unit_factors = {}

    chargeable, domains, totals, errors = transform_rows(rows, typemap, skip_partners, unit_factors)

    assert len(chargeable) == 0
    assert len(errors) == 1
    assert "Missing PartNumber" in errors[0]

def test_transform_rows_applies_unit_factor():
    rows = [{
        "PartnerID": "1001",
        "PartNumber": "P5000",
        "accountGuid": "abc123",
        "itemCount": "10000",
        "domains": "example.com",
        "plan": "Standard"
    }]
    typemap = {"P5000": "bulk.plan"}
    skip_partners = set()
    unit_factors = {"P5000": 5000}

    chargeable, domains, totals, errors = transform_rows(rows, typemap, skip_partners, unit_factors)

    assert len(chargeable) == 1
    assert chargeable[0]["usage"] == 2
    assert not errors
