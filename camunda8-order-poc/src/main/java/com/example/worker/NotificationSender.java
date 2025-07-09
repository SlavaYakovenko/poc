package com.example.worker;

import io.camunda.zeebe.client.api.response.ActivatedJob;
import io.camunda.zeebe.spring.client.annotation.JobWorker;
import org.springframework.stereotype.Component;
import java.util.Map;

@Component
public class NotificationSender {
    
    @JobWorker(type = "send-notification")
    public Map<String, Object> sendNotification(final ActivatedJob job) {
        
        Map<String, Object> variables = job.getVariablesAsMap();
        String customerId = (String) variables.get("customerId");
        String productId = (String) variables.get("productId");
        Boolean approved = (Boolean) variables.get("orderApproved");
        
        System.out.println("📧 Sending notification to customer: " + customerId);
        
        if (approved != null && approved) {
            System.out.println("✅ Order APPROVED notification sent for product: " + productId);
        } else {
            System.out.println("❌ Order REJECTED notification sent for product: " + productId);
        }
        
        return Map.of("notificationSent", true);
    }
}