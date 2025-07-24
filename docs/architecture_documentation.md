# Image Processing Platform - Architecture Documentation

## Overview

This document outlines the architecture of a cloud-native microservice system designed for image upload, feature extraction, and similarity search. The system supports asynchronous workflows and is optimized for modularity, observability, and scalability.

---

## Components

### 1. **API Service (FastAPI)**

Handles client-facing HTTP endpoints for image upload, metadata retrieval, and similarity search.

**Endpoints:**

* `POST /images/upload`: Upload an image and initiate processing
* `GET /images/{id}`: Retrieve image metadata and extracted features
* `GET /images/{id}/similar`: Return visually similar images
* `GET /health`: Health check

**Responsibilities:**

* Accept image uploads and store them in the object store
* Submit image processing jobs to the Redis-backed Arq queue
* Query the Backend DB for image metadata and job status
* Perform similarity search using the Vector DB

---

### 2. **Worker Service (Arq)**

Handles asynchronous image processing workflows as background tasks.

**Responsibilities:**

* Poll Redis for new image processing jobs
* Fetch image objects from the object store
* Send image data to the Embedding Service
* Store resulting feature vectors in the Vector DB
* Maintain and update job state in the Backend DB

**Note:** This service is horizontally scalable and can be deployed independently from the API. It replaces the need for a custom Coordinator Service, and can be replaced with a workflow engine like Temporal in the future if needed.

---

### 3. **Embedding Service (FastAPI)**

Processes images into vector embeddings using a pretrained CLIP model.

**Responsibilities:**

* Accept image bytes or URLs via HTTP
* Return a feature vector embedding
* Optionally cache or persist embeddings for deduplication or recovery

**Endpoints:**

* `POST /encode`: Send an image and receive the embedding of it
* `GET /health`: Health check

---

### 4. **Object Store (MinIO)**

Stores uploaded image files.

**Responsibilities:**

* Provide reliable object storage
* Support pre-signed URL access or direct fetches

---

### 5. **Vector DB (Qdrant)**

Stores and indexes embedding vectors for similarity search.

**Responsibilities:**

* Store embedding vectors with associated image IDs
* Serve similarity search queries

---

### 6. **Backend DB (PostgreSQL)**

Tracks the state of image processing jobs.

**Responsibilities:**

* Maintain per-image state (created, pending, embedding, indexing, done, error)
* Track job metadata including vector insertion and retrieval
* Support user-facing status and metadata queries

---

## Flow Summary

1. **Upload:** Client uploads image to API → stored in Object Store
2. **Job Submission:** API pushes job to Redis queue
3. **Processing:** Arq Worker pulls job → fetches image → sends to Embedder
4. **Embedding:** Embedding Service returns vector → Worker inserts into Vector DB
5. **Tracking:** Worker updates Backend DB with job state transitions
6. **Query:** API handles similarity search and metadata/status retrieval for client

---

## Design Principles

* **Separation of concerns:** API, processing, and embedding logic are decoupled
* **Stateless services:** All components are horizontally scalable
* **Cloud-native readiness:** Health checks, env-based config, persistent storage
* **Future extensibility:** Designed to support Temporal, new ML models, and additional pipeline steps

---

## Health Check Standard

All services implement `GET /health` and return HTTP 200 OK when alive.

---

## Strengths and Weaknesses

### Strengths

* **Stateless, scalable services:** Each component is independently deployable and horizontally scalable.
* **Separation of concerns:** The API, embedding logic, and orchestration are clearly decoupled.
* **Cloud-native design:** Services implement health checks, are environment-driven, and compatible with container orchestration.
* **Async and modular pipeline:** Enables non-blocking image processing with room for additional processing steps in the future.
* **ML model abstraction:** Embedding logic is isolated, making it easy to swap or upgrade ML models.

### Weaknesses

* **Queue coordination dependency:** The system depends on Arq and Redis. If Redis fails, no new jobs are processed.
* **Embedding recomputation risk:** Without embedding cache, reuploads can lead to duplicate embedding computation.
* **Limited real-time capabilities:** The system is not yet optimized for streaming or real-time processing (batch-centric design).

---

## Planned Improvements

* Add monitoring and logging (e.g., Prometheus + Grafana, Loki)
* Add metadata processing or moderation stages via pipeline extension
* Add optional embedding cache to reduce recomputation
