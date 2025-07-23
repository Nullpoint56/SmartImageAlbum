WORKDIR /app
COPY coordinator_service ./coordinator_service
CMD ["uvicorn", "coordinator_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
