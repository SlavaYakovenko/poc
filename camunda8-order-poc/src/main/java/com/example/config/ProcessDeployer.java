package com.example.config;

import io.camunda.zeebe.client.ZeebeClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class ProcessDeployer implements CommandLineRunner {
    
    @Autowired
    private ZeebeClient zeebeClient;
    
    @Override
    public void run(String... args) throws Exception {
        
        var deployment = zeebeClient.newDeployResourceCommand()
                .addResourceFromClasspath("order-process.bpmn")
                .send()
                .join();
        
        System.out.println("🚀 Process deployed with key: " + deployment.getKey());
        deployment.getProcesses().forEach(process -> 
            System.out.println("📋 Process: " + process.getBpmnProcessId() + 
                             " version: " + process.getVersion())
        );
    }
}