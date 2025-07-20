# Image Processing Platform - Architecture Documentation

## Overview

This document outlines the architecture of a cloud-native microservice system designed for image upload, feature
extraction, and similarity search. The system supports asynchronous workflows and is optimized for modularity,
observability, and scalability.

---

## Components

### 1. **API Service (FastAPI)**

Handles client-facing HTTP endpoints for image upload, metadata retrieval, and similarity search.

**Endpoints:**

* `POST /images/upload`: Upload an image and initiate processing
* `GET /images/{image_id}`: Retrieve image metadata and extracted features
* `GET /images/{image_id}/similar`: Return visually similar images
* `GET /health`: Health check

**Responsibilities:**

* Accept image uploads and store them in the object store
* Notify the Coordinator to begin processing
* Forward user queries (e.g. similarity) to backend services

---

### 2. **Coordinator Service (Custom Async Service)**

Acts as the orchestrator for all image processing workflows.

**Responsibilities:**

* Maintain and update job state in the Workflow DB
* Fetch image objects from the object store
* Query the Config Service for pipeline configuration
* Send image data to the Embedding Service
* Store resulting feature vectors in the Vector DB

**Endpoints:**

* `GET /health`: Health check

**Note:** This service is designed to be a candidate for replacement by Temporal or another workflow engine in the
future.

---

### 3. Embedding Service

Processes images into vector embeddings using a pretrained CLIP model.

**Responsibilities:**

* Accept image bytes via HTTP
* Return a feature vector embedding

**Endpoints:**

* `POST /encode`&#x20;
* `GET /health`: Health check

---

### 4. **Config Service**

Manages runtime configuration parameters for the Coordinator and API Service.

**Responsibilities:**

* Provide runtime configurable parameters for services

**Internal DB:** `Config DB`&#x20;

**Endpoints:**

* `GET /config`: Return current config
* `GET /health`: Health check

---

### 5. Object Store

Stores uploaded image files.

**Responsibilities:**

* Provide reliable object storage
* Support pre-signed URL access or direct fetches

---

### 6. Vector DB

Stores and indexes embedding vectors for similarity search.

**Responsibilities:**

* Store embedding vectors with associated image IDs
* Serve similarity search queries

---

### 7. Workflow DB

Tracks the state of image processing jobs.

**Responsibilities:**

* Maintain per-image state (pending, processing, embedded, indexed, done, error)
* Support user-facing status queries

---

## Flow Summary

1. **Upload:** Client uploads image to API → stored in Object Store
2. **Trigger:** API calls Coordinator to process the image
3. **Orchestration:** Coordinator fetches image → queries config → sends to Embedder
4. **Embedding:** Embedding Service returns vector → Coordinator inserts into Vector DB
5. **Status Tracking:** Coordinator updates Workflow DB throughout the process
6. **Query:** API handles similarity search and metadata retrieval for client

---

## Design Principles

* **Separation of concerns:** API, coordination, processing, and storage are isolated
* **Stateless services:** All components are horizontally scalable
* **Cloud-native readiness:** Health checks, env-based config, persistent storage
* **Future extensibility:** Designed to support Temporal, new ML models, and pipeline steps

---

## Health Check Standard

All services implement `GET /health` and return HTTP 200 OK when alive.

---

## Strengths and Weaknesses

### Strengths

* **Centralized orchestration:** The Coordinator manages all workflow logic, making the system easy to extend and debug.
* **Stateless, scalable services:** Each component is independently deployable and horizontally scalable.
* **Separation of concerns:** The API, embedding logic, and orchestration are clearly decoupled.
* **Cloud-native design:** Services implement health checks, are environment-driven, and compatible with container
  orchestration.
* **Async and modular pipeline:** Enables non-blocking image processing with room for additional processing steps in the
  future.
* **ML model abstraction:** Embedding logic is isolated, making it easy to swap or upgrade ML models.

### Weaknesses

* **Coordinator as single point of failure:** The system heavily depends on the Coordinator. If it fails, the entire
  processing pipeline halts.
* **Image transfer overhead:** The Coordinator pulls full image files from object storage, which may introduce network
  or latency bottlenecks.
* **Limited real-time capabilities:** The system is not yet optimized for streaming or real-time processing (
  batch-centric design).

---

## Planned Improvements

* Add monitoring and logging (e.g., Prometheus + Grafana, Loki)
* Add metadata processing or moderation stages via pipeline extension
