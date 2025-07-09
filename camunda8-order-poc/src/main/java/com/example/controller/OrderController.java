package com.example.controller;

import io.camunda.zeebe.client.ZeebeClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/api/orders")
public class OrderController {
    
    @Autowired
    private ZeebeClient zeebeClient;
    
    @PostMapping("/create")
    public Map<String, Object> createOrder(@RequestBody OrderRequest request) {
        
        System.out.println("🚀 Starting process for order: " + request.getOrderId());
        
        var processInstance = zeebeClient.newCreateInstanceCommand()
                .bpmnProcessId("order-process")
                .latestVersion()
                .variables(Map.of(
                    "orderId", request.getOrderId(),
                    "customerId", request.getCustomerId(),
                    "productId", request.getProductId(),
                    "amount", request.getAmount(),
                    "quantity", request.getQuantity()
                ))
                .send()
                .join();
        
        System.out.println("✅ Process started with key: " + processInstance.getProcessInstanceKey());
        
        return Map.of(
            "orderId", request.getOrderId(),
            "processInstanceKey", processInstance.getProcessInstanceKey(),
            "status", "Process started"
        );
    }
    
    @GetMapping("/status")
    public Map<String, Object> getStatus() {
        return Map.of(
            "zeebeStatus", "Connected",
            "gateway", "localhost:26500"
        );
    }
}