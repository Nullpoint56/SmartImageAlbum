# Tooling Justification for Image Processing Platform

This document outlines and justifies the selection of deployable services used in the Image Processing Platform. The
choices reflect the system's requirements for scalability, cloud-native architecture, and maintainability, as detailed
in the [Architecture Documentation](./architecture_documentation.md) and project requirements.

---

## 1. Vector Store: **Qdrant**

### ✅ Justification

* **Purpose**: Stores high-dimensional vector embeddings and supports similarity search queries.
* **Selected Tool**: [Qdrant](https://qdrant.tech)

### 🔍 Why Qdrant?

* **Performance**: Optimized for dense vector search with support for ANN (Approximate Nearest Neighbor) techniques.
* **API Support**: Provides both REST and gRPC APIs for flexible integration.
* **Filtering Support**: Can store metadata alongside vectors and filter search results based on attributes.
* **Ease of Use**: Actively maintained with a strong Python SDK.
* **Scalability**: Horizontally scalable and container-friendly for Kubernetes or Docker environments.

### 🔄 Alternatives Considered

* **PostgreSQL + pgvector**: Simpler integration, but limited performance and scalability + harder to set up
* **Weaviate**: Powerful, but heavier and less flexible in self-hosted environments.

---

## 2. Object Store: **MinIO**

### ✅ Justification

* **Purpose**: Stores raw image files and supports efficient retrieval via the Coordinator.
* **Selected Tool**: [MinIO](https://min.io)

### 🔍 Why MinIO?

* **S3 Compatibility**: Fully S3-compatible, allowing seamless migration to AWS if needed.
* **Self-hosted Option**: Ideal for development, testing, and privacy-aware production setups.
* **Scalability**: Supports distributed mode for high availability.
* **Simplicity**: Lightweight, easy to deploy, and integrates well with Python (`boto3` or `minio` clients).

### 🔄 Alternatives Considered

* **AWS S3 / GCP Storage / Azure Blob**: Suitable for production, but incur vendor lock-in and external dependency.

---

## 3. Embedding Service: **Custom FastAPI Service using Hugging Face Transformers**

### ✅ Justification

* **Purpose**: Transforms images into high-dimensional embeddings using pretrained vision models.
* **Selected Tool**: Custom FastAPI service using the [Hugging Face
  `transformers`](https://huggingface.co/docs/transformers) library.

### 🔍 Why Hugging Face Transformers?

* **Model Flexibility**: Supports a wide range of vision models including OpenCLIP, DINOv2, SigLIP, and more.
* **Unified Interface**: Consistent API for encoding images across different model types.
* **Self-Hosted**: Fully open-source and Dockerizable for private or cloud deployment.
* **Production-Ready**: Integrates easily with FastAPI for lightweight embedding-as-a-service.
* **Extensibility**: Future support for additional models and embedding tasks.

### 🔄 Alternatives Considered

* **CLIP-as-a-Service (Jina)**: Too heavy and unmaintained; designed for multimodal search and dataset indexing.
* **Custom OpenCLIP-only Service**: Viable but limited to CLIP models alone.

---

## Conclusion

The selected tools—**Qdrant**, **MinIO**, and a **custom Hugging Face Transformers-based Embedding Service**—align with
our architecture's goals of modularity, async-first processing, and cloud-native deployment. They enable scalable,
containerized development with clean service boundaries and strong observability potential.

Future improvements, such as switching to managed services or integrating a workflow engine like Temporal, can be easily
introduced due to the system's decoupled and service-oriented design.
