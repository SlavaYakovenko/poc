package com.example.worker;

import io.camunda.zeebe.client.api.response.ActivatedJob;
import io.camunda.zeebe.spring.client.annotation.JobWorker;
import org.springframework.stereotype.Component;
import java.util.Map;

@Component
public class OrderValidator {
    
    @JobWorker(type = "validate-order")
    public Map<String, Object> validateOrder(final ActivatedJob job) {
        
        Map<String, Object> variables = job.getVariablesAsMap();
        
        String customerId = (String) variables.get("customerId");
        Double amount = (Double) variables.get("amount");
        String productId = (String) variables.get("productId");
        
        System.out.println("🔍 Validating order for customer: " + customerId + 
                          ", product: " + productId + ", amount: " + amount);
        
        boolean isValid = customerId != null && !customerId.isEmpty() &&
                         amount != null && amount > 0 && 
                         productId != null && !productId.isEmpty();
        
        System.out.println("✅ Order validation result: " + isValid);
        
        return Map.of("orderValid", isValid);
    }
}