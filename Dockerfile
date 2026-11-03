# syntax=docker/dockerfile:1
FROM gcr.io/distroless/python3-debian13:nonroot
ARG VERSION=dev
ENV APP_VERSION=${VERSION} PYTHONUNBUFFERED=1
WORKDIR /app
COPY app.py .
# Numeric UID so Kubernetes can verify runAsNonRoot
USER 65532:65532
EXPOSE 8080
CMD ["/app/app.py"]
