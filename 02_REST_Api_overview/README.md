

### 🔹 What is REST API?

REST (Representational State Transfer) is not a **protocol** or **tool**, it's a **style** to design web APIs that communicate over HTTP. It makes things **simple, scalable, and reliable** by following a few rules (called constraints).

---

### 🔹 Core REST Rules (Constraints)

1. **Client-Server**:

   * Frontend (user) and backend (server) are separate.
   * They can be updated independently.

2. **Stateless**:

   * Server doesn’t remember anything about past requests.
   * Every request must include all required information (like login token).

3. **Cacheable**:

   * Server tells if the response can be stored and reused.
   * Saves time and reduces server load.

4. **Layered System**:

   * API may use middle services like load balancers or gateways.
   * User doesn’t need to know.

5. **Code on Demand (optional)**:

   * Server can send code (e.g., JavaScript) to the client to run.

6. **Uniform Interface**:

   * Everything in the API follows a standard way:

     * Use **URIs** to identify resources (like `/users/1`)
     * Use **HTTP verbs** (GET, POST, PUT, DELETE)
     * Send and receive **data formats** like JSON or XML
     * Support **HATEOAS** (server gives useful links in response)

---

### 🔹 REST API Key Concepts

| Concept            | Meaning                                                                             |
| ------------------ | ----------------------------------------------------------------------------------- |
| **Resources**      | Anything like users, posts, products (each with a unique URI)                       |
| **Representation** | JSON/XML copy of a resource                                                         |
| **HTTP Methods**   | `GET` (read), `POST` (create), `PUT` (replace), `PATCH` (update), `DELETE` (remove) |
| **Status Codes**   | `200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`, etc.                   |
| **Idempotence**    | Same request multiple times = same result (e.g., `DELETE`)                          |
| **Media Types**    | `application/json`, `text/html`, etc. via `Content-Type` and `Accept` headers       |

---

### 🔹 Best Practices

✅ Use **nouns** in URLs, not verbs
✅ Use **standard HTTP methods**
✅ Provide **clear status codes**
✅ Support **pagination**, **filtering**, **sorting**
✅ Use **versioning** (e.g., `/v1/users`)
✅ Return **useful error messages**
✅ Secure with **HTTPS**, **auth tokens**
✅ Write **good documentation** (like Swagger/OpenAPI)

---

### 🔹 Example

🟢 **GET** `/users/123`
→ Returns user data in JSON format

🟢 **POST** `/users`
→ Sends user data to create a new one

🟢 Response includes **HATEOAS** links:

```json
"_links": {
  "self": {"href": "/users/123"},
  "update": {"href": "/users/123", "method": "PATCH"},
  "delete": {"href": "/users/123", "method": "DELETE"}
}
```

---

### 🔹 REST in Python (Client Side)

Use `requests` library to call REST APIs:

```python
import requests

# GET request
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(response.json())

# POST request
data = {"title": "My Post", "body": "Post body", "userId": 1}
response = requests.post("https://jsonplaceholder.typicode.com/posts", json=data)
print(response.json())
```

---

### 🔹 REST vs Other Styles

| REST           | SOAP           | GraphQL                | gRPC                            |
| -------------- | -------------- | ---------------------- | ------------------------------- |
| Easy, flexible | Strict, XML    | Exact data, 1 endpoint | Fast, binary, for microservices |
| JSON & HTTP    | XML & WSDL     | JSON query             | Protocol Buffers                |
| Very common    | Enterprise use | More dynamic           | High performance                |

---

### 🔹 REST for Agentic AI (DACA Systems)

In smart agent systems, REST APIs can:

* Manage agents: `GET /agents/{id}`
* Assign tasks: `POST /agents/{id}/tasks`
* Get status: `GET /agents/{id}/status`
* Interact with tools, storage, and dashboards

---

### 🔹 REST Strengths 👍

* Simple to use
* Scalable
* Flexible with formats (JSON, XML)
* Works with web standards
* Widely supported in all languages

### 🔹 REST Weaknesses 👎

* May return too much or too little data
* Multiple requests for complex data
* No real-time support (needs WebSockets)
* Different APIs can implement it differently

---

## Use Cases in Agentic AI Systems (DACA Context)

RESTful APIs are a cornerstone for building modular and interoperable agentic AI systems like those envisioned by the DACA pattern:

- **Core Agent Functionality API**: Exposing an agent's capabilities, status, and configuration via REST endpoints.
  - `GET /agents/{agent_id}/status`
  - `POST /agents/{agent_id}/tasks` (to assign a new task)
  - `GET /agents/{agent_id}/tasks/{task_id}`
- **Tool Integration**: Agents can interact with external tools, services, or data sources that expose REST APIs (e.g., weather APIs, knowledge bases, search engines).
- **Data Exchange and Persistence**: Agents can retrieve data from or store data to databases, vector stores, or other storage services through RESTful interfaces.
- **Inter-Agent Communication**: For simpler, request-response style communication between agents, REST can be a straightforward choice, especially if agents are developed as independent microservices.
- **Management and Orchestration APIs**: The DACA infrastructure itself (e.g., for deploying, monitoring, scaling, and configuring agents) can be managed via REST APIs.
- **Human-in-the-Loop (HITL) Interfaces**: Web-based dashboards or control panels for human oversight and intervention would typically interact with the backend agent systems via REST APIs.
- **Model Serving**: While specialized model serving solutions exist (like TensorFlow Serving, TorchServe), simpler models or custom inference logic can be exposed as REST endpoints.
  - `POST /models/{model_id}/predict`
- **Logging and Monitoring**: Agents can send logs or metrics to a central logging/monitoring service via REST.

In DACA, REST APIs provide a standardized, well-understood way to ensure that different components of the agentic system (agents, tools, data stores, UIs) can communicate effectively and be developed/scaled independently.

---
Click this link to read more about REST Api.
["Panaversity Rest Theory"](https://github.com/panaversity/learn-agentic-ai/tree/main/03_ai_protocols/01_mcp/02_rest)
