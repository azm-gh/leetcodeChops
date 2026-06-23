# System Design — High Domain Overview

Source: [LeetCode Discuss](https://leetcode.com/discuss/post/6144179-system-design-questions-with-brief-answe-5gjj/)

---

## Core Infrastructure

### 1. URL Shortening Service (Bitly)

Use a hash function (Base62 encoding) to generate short codes. Store mappings in a key-value store (Redis) with a database as the source of truth.

**Key concepts:** consistent hashing, ID generation (Snowflake), read-heavy optimization.

**Resources:**
- [System Design — URL Shortening](https://systemdesign.one/url-shortening-system-design/)
- [Bitly distributed architecture (High Scalability)](https://highscalability.com/bitly-lessons-learned-building-a-distributed-system-that-han/)

---

### 3. LRU Cache

Hash map + doubly linked list. HashMap → O(1) lookup; linked list → O(1) eviction. On access, move node to head; on eviction, remove from tail.

**Key concepts:** eviction policies (LRU, LFU), write-through vs write-around.

**Resources:**
- [Design an LRU Cache (InterviewReady)](https://interviewready.io/blog/design-lru-cache)
- [Redis LRU eviction docs](https://redis.io/docs/reference/eviction/)

---

### 10. Rate Limiter

Use **token bucket** or **sliding window counter** stored in Redis per user/IP. Token bucket allows bursts; sliding window is more accurate.

**Key concepts:** throttling, distributed rate limiting, `X-RateLimit-Remaining` headers.

**Resources:**
- [Stripe rate limiters](https://stripe.com/blog/rate-limiters)
- [AWS API Gateway throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)

---

### 12. Microservices Architecture

Decompose into bounded contexts (DDD). Communicate via REST/gRPC or message queues. Use Docker + Kubernetes for orchestration. API gateway for routing and auth.

**Key concepts:** service discovery, circuit breakers, saga pattern, distributed tracing.

**Resources:**
- [Microservices patterns (Chris Richardson)](https://microservices.io/patterns/index.html)
- [Uber's microservice architecture](https://www.uber.com/blog/microservice-architecture/)

---

### 13. Distributed Job Scheduler

Use a message queue (RabbitMQ, Kafka) as the job buffer. Workers consume jobs. Store state in a database. Retry with exponential backoff and dead-letter queues.

**Key concepts:** cron triggers, priority queues, idempotent workers.

**Resources:**
- [Amazon SQS distributed job queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- [Apache Airflow architecture](https://airflow.apache.org/docs/apache-airflow/stable/concepts/overview.html)

---

### 15. Search Engine

Build an **inverted index** (term → document IDs). Use TF-IDF or BM25 for ranking. Partition across shards. Scatter-gather for queries.

**Key concepts:** inverted index, indexing pipeline, PageRank, query parsing.

**Resources:**
- [Elasticsearch architecture](https://www.elastic.co/guide/en/elasticsearch/reference/current/_basic_concepts.html)
- [How Google Search works](https://www.google.com/search/howsearchworks/)

---

### 22. Notification System

Message queue decouples generation from delivery. Fan-out to push (FCM/APNs), email (SES), SMS (Twilio), in-app (WebSockets). Store preferences and delivery logs.

**Key concepts:** fan-out, delivery guarantees, deduplication.

**Resources:**
- [Uber's push notification system](https://www.uber.com/blog/engineering/push-notifications/)
- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)

---

### 26. Job Queue System

Producer → queue → workers. Redis Lists for simple, RabbitMQ/Kafka for complex. Retry + dead-letter queues + visibility timeouts.

**Key concepts:** FIFO vs priority, at-least-once, backpressure.

**Resources:**
- [RabbitMQ vs Kafka comparison](https://www.cloudamqp.com/blog/part1-rabbitmq-best-practice.html)
- [Celery docs](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)

---

### 27. Email Sending System

Use SendGrid, SES, or Mailgun for deliverability and SPF/DKIM/DMARC. Queue emails with state tracking.

**Key concepts:** SMTP relay, email reputation, rate limiting sends.

**Resources:**
- [SendGrid sending guide](https://docs.sendgrid.com/for-developers/sending-email)
- [Email deliverability guide (SendGrid)](https://sendgrid.com/blog/what-is-email-deliverability/)

---

### 30. Server Monitoring System

Collect metrics via agents (Prometheus node_exporter). Store in time-series DB (Prometheus, InfluxDB). Alert on thresholds. Visualize with Grafana.

**Key concepts:** pull vs push, cardinality, distributed tracing.

**Resources:**
- [Google SRE Book — Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Prometheus overview](https://prometheus.io/docs/introduction/overview/)

---

## Data Storage & Databases

### 14. Highly Available Database

Primary-replica replication + sharding + consistent hashing. Quorum-based reads/writes. Automatic failover.

**Key concepts:** CAP theorem, Raft consensus, eventual consistency.

**Resources:**
- [DynamoDB design patterns](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [Cassandra architecture](https://www.datastax.com/resources/whitepaper/cassandra-architecture)

---

### 23. URL Redirection Service

Key-value store for short path → target URL. 301 for permanent, 302 for analytics tracking. Add analytics middleware.

**Key concepts:** HTTP redirects, TTL caching, analytics pipeline.

---

### 25. File Sharing Service

Blob storage (S3) + metadata database. Signed URLs for temporary access. Multi-part upload for large files.

**Key concepts:** encryption at rest, virus scanning, versioning.

**Resources:**
- [LAN sync performance (Dropbox tech)](https://dropbox.tech/infrastructure/inside-lan-sync)

---

## Real-time & Communication

### 6. Real-time Messaging (WhatsApp)

WebSockets for persistent connections. Distributed DB (Cassandra) for messages. Pub/sub delivery. Offline buffering via message queue.

**Key concepts:** chat architecture, end-to-end encryption, read receipts.

**Resources:**
- [WhatsApp engineering posts (Meta)](https://engineering.fb.com/tag/whatsapp/)
- [Building a chat system](https://www.youtube.com/watch?v=UzLMh68g4yg)

---

### 17. Payment Gateway

Integrate with Stripe/PayPal. Use idempotency keys. Encrypt sensitive data (PCI-DSS). Webhooks for async confirmation.

**Key concepts:** idempotency, 3D Secure, fraud detection, reconciliation.

**Resources:**
- [Stripe API design](https://stripe.com/docs/api)
- [Stripe's payment architecture](https://stripe.com/blog/payment-api-design)

---

### 19. Real-time Collaboration (Google Docs)

WebSockets + CRDTs or OT for conflict resolution. Event sourcing for document history.

**Key concepts:** CRDT vs OT, operational log, cursor sync.

**Resources:**
- [How Google Docs works](https://www.youtube.com/watch?v=3h1R6iE1hJs)
- [CRDTs (Martin Kleppmann — arXiv)](https://arxiv.org/abs/1909.04980)

---

### 20. Video Conferencing (Zoom)

WebRTC for P2P audio/video. SFU/MCU for group calls. TURN servers for NAT traversal. Adaptive bitrate.

**Key concepts:** codecs, jitter buffer, simulcast.

**Resources:**
- [Zoom architecture](https://zoom.us/docs/en-us/architecture.html)
- [WebRTC fundamentals (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)

---

### 24. Voting System

Relational DB for votes. Unique constraint (user + election) for dedup. Separate identity from ballot for anonymity.

**Key concepts:** audit trail, verifiability, live aggregation.

**Resources:**
- [ElectionGuard](https://www.electionguard.vote/)
- [Estonia e-voting](https://e-estonia.com/solutions/e-governance/)

---

## Media & Content Delivery

### 7. Video Streaming (YouTube)

Blob storage for uploads. Transcoding pipeline (multiple resolutions). CDN for delivery. HLS/DASH for adaptive bitrate.

**Key concepts:** encoding pipeline, CDN caching, hot vs cold content.

**Resources:**
- [YouTube architecture (High Scalability)](https://www.highscalability.com/youtube-architecture/)
- [Netflix content delivery](https://netflixtechblog.com/netflix-content-engineering-2-0-f87a87f7e51c)

---

### 8. Content Delivery Network (CDN)

Edge servers globally. Cache static content by TTL. DNS-based nearest-server routing. Origin pull vs push.

**Key concepts:** cache hit ratio, cache invalidation, geo-routing, DDoS protection.

**Resources:**
- [CloudFront architecture (AWS)](https://aws.amazon.com/cloudfront/)
- [Cloudflare edge network](https://www.cloudflare.com/network/)

---

### 29. File Compression Service

Upload → background job → compression (gzip, zstd) → store result. Task queue for async processing.

**Key concepts:** lossless vs lossy, streaming compression.

**Resources:**
- [Facebook's zstd](https://engineering.fb.com/2016/08/31/core-data/smaller-and-faster-data-compression-with-zstandard/)
- [Brotli compression (GitHub)](https://github.com/google/brotli)

---

## Social & Collaboration

### 4. Social Media Platform (Instagram)

NoSQL for user data. Blob storage for media. Feed service: fan-out on write for celebs, fan-out on read for regular users. WebSockets for notifications.

**Key concepts:** news feed generation (push vs pull), timeline merging, content moderation.

**Resources:**
- [Instagram engineering](https://engineering.instagram.com/)
- [Designing Instagram](https://www.youtube.com/watch?v=QmX2NPqr4Eo)

---

### 18. Location-based Service (Uber)

Geospatial indexing (QuadTree, Geohash, H3) for nearby queries. Real-time GPS streaming. Dispatcher matches rider to nearest driver.

**Key concepts:** geo-hashing, supply-demand matching, surge pricing.

**Resources:**
- [Uber's H3 geospatial index](https://www.uber.com/blog/h3/)
- [Uber dispatch architecture](https://www.uber.com/blog/engineering/real-time-dispatching/)

---

### 21. Blogging Platform

NoSQL for posts. Relational for relationships (follows, tags). Redis for hot content. CDN for images. Elasticsearch for search.

**Key concepts:** content caching, cursor-based pagination, full-text search.

**Resources:**
- [Medium engineering archive](https://blog.medium.com/)
- [Ghost architecture](https://ghost.org/docs/)

---

## E-commerce & Transactions

### 5. E-commerce Checkout

ACID transactions for orders. Idempotent payment integration. Inventory reservation with timeout. Message queue for fulfillment.

**Key concepts:** saga pattern, inventory locking, abandoned cart recovery.

**Resources:**
- [Challenges with distributed systems (AWS)](https://aws.amazon.com/builders-library/challenges-with-distributed-systems/)
- [Shopify engineering](https://shopify.engineering/)

---

### 16. Ticket Booking System

Relational DB with row-level locking. Optimistic locking for concurrent bookings. Queue for payment. Timeout-based seat release.

**Key concepts:** pessimistic vs optimistic locking, concurrency control, waitlist.

**Resources:**
- [Ticketmaster systems](https://www.ticketmaster.com/)
- [Designing a ticket system](https://www.youtube.com/watch?v=oZj6_0oJiS4)

---

### 28. Cloud Analytics Dashboard

Data → Kafka → Flink/Spark → time-series DB (ClickHouse, Druid) → dashboard UI (Grafana). Pre-compute rollups for historical data.

**Key concepts:** real-time vs batch, pre-aggregation, OLAP.

**Resources:**
- [Uber analytics dashboard](https://www.uber.com/blog/engineering/analytics-dashboard/)
- [ClickHouse architecture](https://clickhouse.com/docs/en/development/architecture)

---

## Analytics & Monitoring

### 11. Real-time Analytics System

Kafka for ingestion → Flink/Spark Streaming for aggregation → time-series DB or Redis for fast queries.

**Key concepts:** stream vs batch, windowing (tumbling, sliding), data freshness vs accuracy.

**Resources:**
- [Kafka + Flink at Netflix](https://netflixtechblog.com/keystone-real-time-stream-processing-platform-a3ee651812a)
- [Stream processing (Confluent)](https://www.confluent.io/learn/stream-processing/)

---

### 2. File Storage (Google Drive)

Blob storage partitioned by user. Metadata DB. Delta sync (upload changed chunks). Background workers for virus scanning and thumbnails.

**Key concepts:** chunking, deduplication, offline conflict resolution, ACLs.

**Resources:**
- [Google Drive infrastructure](https://cloud.google.com/blog/products/storage-data-transfer/google-drive-infrastructure)
- [Streaming file sync (Dropbox tech)](https://dropbox.tech/infrastructure/streaming-file-synchronization)
