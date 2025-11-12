import logfire, os
# Configure Logfire
logger = logfire.configure(
    token=os.getenv("LOGFIRE_API_TOKEN"),
    environment=os.getenv("LOGFIRE_ENVIRONMENT","DEVELOPMENT"),
    service_name=os.getenv("LOGFIRE_SERVICE_NAME","Atlantis"),
)
# Instrument Pydantic
logger.instrument_pydantic()