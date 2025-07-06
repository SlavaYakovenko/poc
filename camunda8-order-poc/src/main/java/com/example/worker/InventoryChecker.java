package com.example.worker;

import io.camunda.zeebe.client.api.response.ActivatedJob;
import io.camunda.zeebe.spring.client.annotation.JobWorker;
import org.springframework.stereotype.Component;
import java.util.Map;

@Component
public class InventoryChecker {
    
    @JobWorker(type = "check-inventory")
    public Map<String, Object> checkInventory(final ActivatedJob job) {
        
        Map<String, Object> variables = job.getVariablesAsMap();
        String productId = (String) variables.get("productId");
        Integer quantity = (Integer) variables.get("quantity");
        
        System.out.println("📦 Checking inventory for product: " + productId + 
                          ", quantity: " + quantity);
        
        // Имитируем проверку склада
        boolean inStock = Math.random() > 0.2; // 80% шанс что есть в наличии
        int availableQuantity = inStock ? (quantity + 10) : (quantity - 1);
        
        System.out.println("📊 Inventory check result - In stock: " + inStock + 
                          ", Available: " + availableQuantity);
        
        return Map.of(
            "inStock", inStock,
            "availableQuantity", availableQuantity
        );
    }
}