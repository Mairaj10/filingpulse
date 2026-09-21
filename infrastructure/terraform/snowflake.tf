resource "snowflake_database" "filingpulse" {
  name    = "FILINGPULSE_DEV"
  comment = "Development database for FilingPulse"
}

resource "snowflake_schema" "raw" {
  database = snowflake_database.filingpulse.name
  name     = "RAW"
  comment  = "Raw ingestion schema for FilingPulse"
}

resource "snowflake_warehouse" "ingest" {
  name                = "FILINGPULSE_INGEST_WH"
  warehouse_size      = "XSMALL"
  auto_suspend        = 60
  auto_resume         = true
  initially_suspended = true

  comment = "Compute warehouse for FilingPulse ingestion"
}

resource "snowflake_account_role" "ingest" {
  name    = "FILINGPULSE_INGEST_ROLE"
  comment = "Least-privilege role for FilingPulse ingestion"
}

resource "snowflake_grant_privileges_to_account_role" "ingest_warehouse_usage" {
  privileges        = ["USAGE"]
  account_role_name = snowflake_account_role.ingest.name

  on_account_object {
    object_type = "WAREHOUSE"
    object_name = snowflake_warehouse.ingest.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "ingest_database_usage" {
  privileges        = ["USAGE"]
  account_role_name = snowflake_account_role.ingest.name

  on_account_object {
    object_type = "DATABASE"
    object_name = snowflake_database.filingpulse.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "ingest_schema_usage" {
  privileges        = ["USAGE"]
  account_role_name = snowflake_account_role.ingest.name

  on_schema {
    schema_name = snowflake_schema.raw.fully_qualified_name
  }
}

resource "snowflake_grant_privileges_to_account_role" "ingest_schema_create_table" {
  privileges        = ["CREATE TABLE"]
  account_role_name = snowflake_account_role.ingest.name

  on_schema {
    schema_name = snowflake_schema.raw.fully_qualified_name
  }
}

resource "snowflake_service_user" "dlt" {
  name              = "FILINGPULSE_DLT"
  login_name        = "FILINGPULSE_DLT"
  default_role      = snowflake_account_role.ingest.name
  default_warehouse = snowflake_warehouse.ingest.name

  rsa_public_key = replace(
    replace(
      replace(
        file(pathexpand("~/.snowflake/filingpulse/dlt/rsa_key.pub")),
        "-----BEGIN PUBLIC KEY-----",
        ""
      ),
      "-----END PUBLIC KEY-----",
      ""
    ),
    "\n",
    ""
  )

  comment = "Service user for FilingPulse dlt ingestion"
}

resource "snowflake_grant_account_role" "ingest_role_to_dlt" {
  role_name = snowflake_account_role.ingest.name
  user_name = snowflake_service_user.dlt.name
}

resource "snowflake_schema" "raw_staging" {
  database = snowflake_database.filingpulse.name
  name     = "RAW_STAGING"
  comment  = "Temporary staging schema for FilingPulse dlt merge operations"
}

resource "snowflake_grant_privileges_to_account_role" "ingest_staging_schema_usage" {
  privileges        = ["USAGE"]
  account_role_name = snowflake_account_role.ingest.name

  on_schema {
    schema_name = snowflake_schema.raw_staging.fully_qualified_name
  }
}

resource "snowflake_grant_privileges_to_account_role" "ingest_staging_schema_create_table" {
  privileges        = ["CREATE TABLE"]
  account_role_name = snowflake_account_role.ingest.name

  on_schema {
    schema_name = snowflake_schema.raw_staging.fully_qualified_name
  }
}

resource "snowflake_grant_account_role" "ingest_role_to_mairaj" {
  role_name = snowflake_account_role.ingest.name
  user_name = "MAIRAJ10"
}

