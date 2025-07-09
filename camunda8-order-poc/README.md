# Camunda 8 Order Processing POC

## Overview
This is a Proof of Concept (POC) demonstrating order processing workflow using Camunda Platform 8, Spring Boot, and BPMN.

## Architecture
- **Camunda Platform 8**: Process orchestration (Zeebe, Operate, Tasklist, Elasticsearch)
- **Spring Boot**: Application framework with Zeebe integration
- **BPMN Process**: Automated order validation, inventory check, manual approval, and notifications

## Process Flow
```
[Order Received] → [Validate Order] → [Valid?] 
                                         ↓ Valid
                                   [Check Inventory] → [Approve Order] → [Send Notification] → [Order Processed]
                                         ↓ Invalid
                                   [Order Rejected]
```

## Prerequisites
- Docker & Docker Compose
- Java 17+
- Gradle (using wrapper)

## Quick Start

### 1. Start Camunda Platform 8
```bash
docker-compose -f docker-compose-camunda8.yml up -d
```

**Wait 2-3 minutes** for all services to start.

**Verify services:**
```bash
docker ps | grep camunda
```

### 2. Start the Application
```bash
./gradlew bootRun
```

**Expected output:**
```
🚀 Process deployed with key: [number]
📋 Process: order-process version: 1
```

### 3. Verify Process Deployment

**Operate (Process Monitoring):** http://localhost:8081
- **Login:** demo / demo
- **Navigate to:** Processes → "Order Processing" (id: `order-process`)

### 4. Test Valid Order Flow

#### Send a Valid Order:
```bash
curl -X POST http://localhost:8090/api/orders/create \
  -H "Content-Type: application/json" \
  -d '{
    "orderId": "ORD-001",
    "customerId": "CUST-123",
    "productId": "PROD-456",
    "amount": 99.99,
    "quantity": 2
  }'
```

**Expected response:**
```json
{
  "orderId": "ORD-001",
  "processInstanceKey": [number],
  "status": "Process started"
}
```

#### Approve the Order in Tasklist:
**Tasklist (User Tasks):** http://localhost:8082
- **Login:** demo / demo
- **Find task:** "Approve Order" for ORD-001
- **Add variable:** `orderApproved` = `true`
- **Complete task**

**Result:** Process completes successfully with notification sent.

### 5. Test Invalid Order Flow

#### Send an Invalid Order:
```bash
curl -X POST http://localhost:8090/api/orders/create \
  -H "Content-Type: application/json" \
  -d '{
    "orderId": "ORD-002",
    "customerId": "",
    "productId": "PROD-789",
    "amount": -10.0,
    "quantity": 1
  }'
```

**Result:** Process automatically rejects the order at validation step.

## Monitoring & Debugging

### Application Logs
Watch console output for:
- 🔍 Order validation
- 📦 Inventory checks  
- 📧 Notifications
- ✅/❌ Process results

### Operate Dashboard
- **Active Processes:** Running order instances
- **Process History:** Completed/failed orders
- **Incidents:** Process errors and failures

### API Health Check
```bash
curl http://localhost:8090/api/orders/status
```

## Architecture Components

### BPMN Elements
- **Service Tasks:** `validate-order`, `check-inventory`, `send-notification`
- **User Task:** `approve-order` (assigned to `demo`)
- **Gateway:** Conditional routing based on validation result
- **Process ID:** `order-process` (links BPMN to code)

### Java Components
- **Workers:** Process service tasks (`@JobWorker` annotations)
- **Controller:** REST API for order creation
- **ProcessDeployer:** Auto-deploys BPMN on startup

### Docker Services
- **Zeebe** (`:26500`): Process engine
- **Operate** (`:8081`): Process monitoring
- **Tasklist** (`:8082`): User task management  
- **Elasticsearch** (`:9200`): Data storage

## Troubleshooting

### Services Not Starting
```bash
# Check container status
docker-compose -f docker-compose-camunda8.yml ps

# View logs
docker-compose -f docker-compose-camunda8.yml logs zeebe
```

### Process Not Deploying
- Check BPMN file in `src/main/resources/order-process.bpmn`
- Verify process ID matches code: `order-process`
- Look for deployment errors in application logs

### API Not Responding
- Verify application started on port `:8090`
- Check Zeebe connection in logs
- Test status endpoint: `curl localhost:8090/api/orders/status`

## Development Notes

### Modifying the Process
1. **Edit BPMN:** Use Camunda Desktop Modeler
2. **Update Process ID:** In Properties Panel → Process → Id
3. **Update Code:** Change `.bpmnProcessId("order-process")` if ID changed
4. **Redeploy:** Restart application (auto-deploys on startup)

### Adding New Service Tasks
1. **Create Worker:** `@JobWorker(type = "new-task-type")`
2. **Update BPMN:** Add Service Task with matching type
3. **Deploy:** Restart application

## Cleanup
```bash
# Stop application
Ctrl+C

# Stop Docker services
docker-compose -f docker-compose-camunda8.yml down

# Remove volumes (optional)
docker-compose -f docker-compose-camunda8.yml down -v
```