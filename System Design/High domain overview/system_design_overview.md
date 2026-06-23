# System Design — High Domain Overview

A curated collection of common system design questions with enriched answers and references to authoritative tech blogs, papers, and architecture deep-dives.

Source: [LeetCode Discuss](https://leetcode.com/discuss/post/6144179/system-design-questions-with-brief-answe-5gjj/)

---

## Core Infrastructure

### 1. Design a URL shortening service like Bitly

Use a hash function (e.g., Base62 encoding of a unique ID) to generate short codes and store the mapping in a fast key-value store (e.g., Redis) with a relational or NoSQL database as the source of truth for persistence. Redirection is a simple 301/302 lookup.

**Key concepts:** consistent hashing, ID generation (snowflake, ZooKeeper seq), read-heavy optimization.

**Resources:**
- [System Design — URL Shortening](https://systemdesign.one/url-shortening-system-design/)
- [TinyURL design (High Scalability)](https://www.highscalability.com/tinyurl-design/)

---

### 3. Design a cache system (e.g., LRU cache)

Implement with a hash map (O(1) lookup) and a doubly linked list (O(1) insertion/removal for eviction). The hash map points to linked-list nodes; on access, move the node to the head; on eviction, remove from the tail. This maps to any distributed cache (Redis, Memcached) with an LRU eviction policy.

**Key concepts:** eviction policies (LRU, LFU, FIFO), cache invalidation, write-through vs write-around.

**Resources:**
- [Design an LRU Cache (InterviewReady)](https://interviewready.io/blog/design-lru-cache)
- [Redis LRU eviction docs](https://redis.io/docs/reference/eviction/)

---

### 10. Design a rate limiter system

Use the **token bucket** algorithm (burst-friendly) or **leaky bucket** (smooths traffic). Store counters per user/IP in Redis with a TTL. Sliding window log is more accurate but memory-heavy; sliding window counters are a good trade-off.

**Key concepts:** throttling strategies, distributed rate limiting (Redis Cluster), HTTP headers (`X-RateLimit-Remaining`).

**Resources:**
- [Stripe rate limiting design](https://stripe.com/blog/rate-limiters)
- [AWS API Gateway throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)

---

### 12. Design a microservices architecture for a large application

Decompose the monolith into bounded contexts (Domain-Driven Design). Services communicate via REST/gRPC (synchronous) or message queues (asynchronous). Use Docker for containerization, Kubernetes for orchestration, and an API gateway (e.g., Kong, NGINX) for routing, auth, and rate limiting.

**Key concepts:** service discovery, circuit breakers, distributed tracing, eventual consistency, saga pattern.

**Resources:**
- [Microservices patterns (Chris Richardson)](https://microservices.io/patterns/index.html)
- [Uber's microservice architecture](https://www.uber.com/blog/microservice-architecture/)

---

### 13. Design a distributed job scheduler

Use a distributed message queue (RabbitMQ, Kafka, SQS) as the job buffer. Worker nodes consume jobs and process them. Use a database to store job state (pending, running, completed, failed). Handle retries with exponential backoff and dead-letter queues.

**Key concepts:** cron triggers, priority queues, idempotent workers, leader election for coordination.

**Resources:**
- [Building a distributed job scheduler (Engineering at Quora)](https://quorablog.quora.com/Building-a-distributed-job-scheduler)
- [Apache Airflow architecture](https://airflow.apache.org/docs/apache-airflow/stable/concepts/overview.html)

---

### 15. Design a search engine

Crawl web pages, tokenize content, and build an **inverted index** (term → list of document IDs + positions). Use TF-IDF or BM25 for ranking. Partition the index across shards (document-based) and replicate for fault tolerance. Serve queries with a scatter-gather pattern across shards.

**Key concepts:** inverted index, indexing vs querying, PageRank, search query parsing (tokenization, stemming).

**Resources:**
- [Elasticsearch architecture overview](https://www.elastic.co/guide/en/elasticsearch/reference/current/_basic_concepts.html)
- [How Google Search works](https://www.google.com/search/howsearchworks/)

---

### 22. Design a notification system

Use a message queue (Kafka, RabbitMQ) to decouple notification generation from delivery. Fan out to channels: push (FCM/APNs), email (SES/SendGrid), SMS (Twilio), and in-app (WebSockets). Store notification preferences and delivery logs in a database.

**Key concepts:** fan-out, delivery guarantees (at-least-once), batching, deduplication.

**Resources:**
- [Uber's push notification system](https://www.uber.com/blog/engineering/push-notifications/)
- [Firebase Cloud Messaging architecture](https://firebase.google.com/docs/cloud-messaging)

---

### 26. Design a job queue system

Similar to #13 — a producer adds jobs to a queue, workers pull and process them. Use Redis Lists (BLPOP) for simple queues or RabbitMQ/Kafka for complex routing. Implement retries with dead-letter queues and visibility timeouts.

**Key concepts:** FIFO vs priority queues, at-least-once vs exactly-once, backpressure.

**Resources:**
- [RabbitMQ vs Kafka (Confluent)](https://www.confluent.io/blog/apache-kafka-vs-rabbitmq/)
- [Celery architecture docs](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)

---

### 27. Design a system for sending emails

Use a dedicated email service (SendGrid, AWS SES, Mailgun) to handle deliverability, SPF/DKIM/DMARC authentication, and bounce handling. Queue emails in a database with state tracking. Use templates for consistency and tracking pixels for open/click rates.

**Key concepts:** SMTP relay, email reputation, deliverability, rate limiting (sending too fast triggers spam filters).

**Resources:**
- [SendGrid email delivery guide](https://docs.sendgrid.com/for-developers/sending-email)
- [How Gmail handles email infrastructure](https://workspace.google.com/learn-more/email/)

---

### 30. Design a monitoring system for server health

Collect metrics (CPU, memory, latency, error rate) via agents (e.g., Prometheus node_exporter) running on each server. Store in a time-series database (Prometheus, InfluxDB, TimescaleDB). Set up alerting rules based on thresholds. Visualize with Grafana.

**Key concepts:** pull vs push metrics collection, cardinality, alert fatigue, distributed tracing for request-level visibility.

**Resources:**
- [Google SRE Book — Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Prometheus architecture overview](https://prometheus.io/docs/introduction/overview/)

---

## Data Storage & Databases

### 14. Design a highly available database system

Use **primary-replica replication** for high availability and read scaling. **Shard** (horizontal partitioning) across nodes using consistent hashing to distribute write load. Use **quorum-based reads/writes** (e.g., R=2, W=2 for a 3-node cluster) for strong consistency. Handle node failures with automatic failover.

**Key concepts:** CAP theorem, Raft/Paxos consensus, eventual consistency, read replicas, partitioning.

**Resources:**
- [DynamoDB design patterns (AWS)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [Cassandra architecture (DataStax)](https://www.datastax.com/resources/whitepaper/cassandra-architecture)

---

### 23. Design a URL redirection service (e.g., 301 redirect)

Simpler than #1 — a key-value store mapping short paths → target URLs. Use 301 (permanent) for SEO and 302 (temporary) for analytics tracking. Add analytics middleware to count redirects.

**Key concepts:** HTTP redirects, TTL-based caching for hot keys, analytics pipeline.

---

### 25. Design a file sharing service

Store files in blob storage (S3, GCS). Store metadata (user, filename, size, permissions, shared-with) in a relational or NoSQL database. Use signed URLs for temporary access without authentication.

**Key concepts:** multi-part upload for large files, virus scanning, encryption at rest and in transit, versioning.

**Resources:**
- [Dropbox infrastructure (High Scalability)](https://www.highscalability.com/dropbox-architecture/)
- [How WeTransfer handles large files](https://wetransfer.com/engineering)

---

## Real-time & Communication

### 6. Design a real-time messaging system (e.g., WhatsApp)

Use **WebSockets** for persistent bidirectional communication. Messages are stored in a distributed database (Cassandra for write-heavy workload) and delivered via a **publish/subscribe** model. Use a message queue to buffer messages if the recipient is offline.

**Key concepts:** chat architecture (one-on-one vs group), last-seen, read receipts, end-to-end encryption, delivery guarantees.

**Resources:**
- [WhatsApp architecture (Meta Engineering)](https://engineering.fb.com/2012/09/17/data-infrastructure/facebook-and-whatsapp/)
- [Building a chat system (System Design Interview)](https://www.youtube.com/watch?v=UzLMh68g4yg)

---

### 17. Design a payment gateway system

Integrate with external payment processors (Stripe, PayPal, Adyen). Use **idempotency keys** to prevent duplicate charges. Encrypt sensitive data (PCI-DSS compliance). Store transaction logs in a database with status tracking (pending, success, failed, refunded). Implement webhooks for async payment confirmation.

**Key concepts:** idempotency, 3D Secure, fraud detection, reconciliation, PCI compliance.

**Resources:**
- [Stripe's payment API design](https://stripe.com/docs/api)
- [Building reliable payment systems (Adyen)](https://www.adyen.com/blog/payment-architecture)

---

### 19. Design a real-time collaboration platform (e.g., Google Docs)

Use **WebSockets** for live updates. Implement **CRDTs** (Conflict-Free Replicated Data Types) or OT (Operational Transformation) to resolve concurrent edits without conflicts. Store document history as a sequence of operations (event sourcing) rather than periodic snapshots.

**Key concepts:** OT vs CRDT, operational log, cursor synchronization, undo/redo in collaborative context.

**Resources:**
- [Google Docs architecture (How Google Docs works)](https://www.youtube.com/watch?v=3h1R6iE1hJs)
- [CRDTs explained (Martin Kleppmann)](https://martin.kleppmann.com/papers/crdt-papoc.pdf)

---

### 20. Design a video conferencing system (e.g., Zoom)

Use **WebRTC** for peer-to-peer audio/video streaming. For group calls, use a **SFU** (Selective Forwarding Unit) or **MCU** (Multipoint Control Unit) server to relay streams. Use TURN servers for NAT traversal. Optimize with adaptive bitrate based on network conditions.

**Key concepts:** codecs (H.264, VP9), jitter buffer, simulcast, noise suppression, screen sharing.

**Resources:**
- [Zoom architecture (Zoom Engineering)](https://zoom.us/docs/en-us/architecture.html)
- [WebRTC fundamentals (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)

---

### 24. Design a voting system (e.g., elections)

Use a relational database for vote recording. Implement duplicate detection via user ID + election ID unique constraint. Anonymize votes by separating identity from vote data (two-table approach). Use idempotent submission to prevent double-counting on retry.

**Key concepts:** audit trail, end-to-end verifiability, separation of identity from ballot, live result aggregation.

**Resources:**
- [Building reliable voting systems (ElectionGuard)](https://www.electionguard.vote/)
- [How Estonia's e-voting works](https://e-estonia.com/solutions/e-governance/e-voting/)

---

## Media & Content Delivery

### 7. Design a video streaming service (e.g., YouTube)

Store raw videos in cloud blob storage. Transcode into multiple resolutions (360p, 720p, 1080p) using a distributed encoding pipeline. Use a **CDN** (Content Delivery Network) for geo-distributed content delivery. Store metadata (title, description, comments) in a database.

**Key concepts:** adaptive bitrate streaming (HLS/DASH), encoding pipeline, CDN caching, hot vs cold content.

**Resources:**
- [YouTube architecture (High Scalability)](https://www.highscalability.com/youtube-architecture/)
- [Netflix's content delivery architecture](https://netflixtechblog.com/netflix-content-engineering-2-0-f87a87f7e51c)

---

### 8. Design a content delivery network (CDN)

Deploy **edge servers** in multiple geographic locations. Cache static content (images, CSS, JS, videos) at the edge based on cache-control headers and TTL. Use **DNS-based routing** to direct users to the nearest edge server. Implement origin pull vs push for cache population.

**Key concepts:** cache hit ratio, cache invalidation, geo-routing, DDoS protection (origin shielding).

**Resources:**
- [CloudFront architecture (AWS)](https://aws.amazon.com/cloudfront/)
- [Cloudflare's edge network](https://www.cloudflare.com/network/)

---

### 29. Design a file compression service

Accept uploads, run compression (gzip, zstd, brotli) in a background job queue, return the compressed file. Use a task queue (Celery, SQS) for async processing. Store original and compressed files in cloud storage with metadata about compression ratio.

**Key concepts:** lossless vs lossy compression, streaming compression for large files, cost vs speed trade-offs.

**Resources:**
- [Facebook's zstd compression](https://engineering.fb.com/2016/08/31/core-data/smaller-and-faster-data-compression-with-zstandard/)
- [How Google uses brotli for web performance](https://www.igvita.com/2015/08/18/brotli-compression-for-web/)

---

## Social & Collaboration

### 4. Design a simple social media platform (e.g., Instagram)

Store user profiles and posts in a NoSQL database (Cassandra for write-heavy workloads). Store images/videos in cloud blob storage. Use a **feed service** that builds a personalized timeline by merging posts from followed users (fan-out on write for celebrities, fan-out on read for regular users). Use WebSockets for real-time notifications.

**Key concepts:** news feed generation (push vs pull), timeline merging, media optimization (thumbnails, lazy loading), content moderation.

**Resources:**
- [Instagram architecture (Engineering at Meta)](https://engineering.instagram.com/)
- [Designing Instagram (System Design Interview)](https://www.youtube.com/watch?v=QmX2NPqr4Eo)

---

### 18. Design a location-based service (e.g., Uber)

Use **geospatial indexing** (QuadTree, S2, Geohash) to efficiently query nearby drivers. Drivers continuously update their GPS coordinates. A **dispatcher service** matches riders to the nearest available driver. Use a distributed database for trip data.

**Key concepts:** real-time location streaming, geo-hashing, supply-demand matching, surge pricing algorithm.

**Resources:**
- [Uber's geospatial index (H3)](https://www.uber.com/blog/h3/)
- [Uber's dispatch architecture](https://www.uber.com/blog/engineering/real-time-dispatching/)

---

### 21. Design a blogging platform

Use a NoSQL database for posts (document-oriented like MongoDB fits well). Use a relational database for relationships (follows, tags). Implement a caching layer (Redis) for hot posts. Use a CDN for images. Support markdown rendering, comments, and RSS feeds.

**Key concepts:** content caching, pagination (cursor-based vs offset-based), full-text search (Elasticsearch), WYSIWYG editors.

**Resources:**
- [Medium engineering blog](https://medium.engineering/)
- [Ghost architecture](https://ghost.org/docs/)

---

## E-commerce & Transactions

### 5. Design an e-commerce checkout system

Use a **relational database** with transactions (ACID) for orders. Integrate with a payment gateway via idempotent API calls. Implement inventory reservation with a timeout (hold stock for N minutes). Use a message queue for order processing (fulfillment, email notifications).

**Key concepts:** distributed transactions (Saga pattern), inventory locking strategies, abandoned cart recovery.

**Resources:**
- [Amazon's checkout architecture](https://www.amazon.science/publications/amazon-checkout)
- [Shopify engineering blog](https://shopify.engineering/)

---

### 16. Design an online ticket booking system

Use a relational database for seat reservations with row-level locking to prevent double-booking. Implement **two-phase commit** or **optimistic locking** for concurrent bookings. Use a queue for payment processing. Release held seats after a timeout if payment fails.

**Key concepts:** concurrency control (pessimistic vs optimistic locking), seat selection UX, waitlist handling.

**Resources:**
- [Ticketmaster's scalable systems](https://www.ticketmaster.com/)
- [Designing a ticket booking system](https://www.youtube.com/watch?v=oZj6_0oJiS4)

---

### 28. Design a cloud-based analytics dashboard

Data flows from sources → stream processor (Kafka + Flink/Spark) → time-series database (ClickHouse, Druid) → dashboard UI (React/Grafana). Aggregate metrics in real-time for recent data and pre-compute rollups for historical data. Support drill-down by time range, dimension, and filters.

**Key concepts:** real-time vs batch processing, pre-aggregation, OLAP vs OLTP, query performance tuning.

**Resources:**
- [Building dashboards at scale (Uber)](https://www.uber.com/blog/engineering/analytics-dashboard/)
- [ClickHouse architecture](https://clickhouse.com/docs/en/development/architecture)

---

## Analytics & Monitoring

### 11. Design a real-time analytics system

Use **Apache Kafka** as the ingestion layer for event streams (page views, clicks). Use **Apache Flink** or **Spark Streaming** for real-time aggregation (counts, sums, top-K). Store results in a time-series database (InfluxDB, TimescaleDB) or a key-value store (Redis) for fast querying.

**Key concepts:** stream vs batch processing, windowing (tumbling, sliding, session), data freshness vs accuracy.

**Resources:**
- [Kafka + Flink at Netflix](https://netflixtechblog.com/keystone-real-time-stream-processing-platform-a3ee651812a)
- [Stream processing fundamentals (Confluent)](https://www.confluent.io/learn/stream-processing/)

---

### 2. Design a file storage system like Google Drive

Store files in cloud object storage (S3, GCS) partitioned by user ID. Use a relational database for metadata (file name, parent folder, owner, permissions, version history). Implement **delta sync** — upload only changed chunks of a file rather than the full file. Use a background worker for virus scanning and thumbnail generation.

**Key concepts:** chunking for large files, deduplication, offline sync conflict resolution, access control lists.

**Resources:**
- [Google Drive infrastructure](https://cloud.google.com/blog/products/storage-data-transfer/google-drive-infrastructure)
- [Dropbox sync architecture](https://dropbox.tech/infrastructure/file-synchronization)
