# Self-Healing Infrastructure Demo

This project demonstrates a **self-healing infrastructure** using **Prometheus**, **Alertmanager**, **Ansible**, and **Flask**.  
It automatically detects service failures (NGINX) and recovers them using alerts and automation.

---

## **📌 Objective**

- Deploy a sample service (NGINX)
- Monitor its uptime and metrics with Prometheus
- Trigger alerts when service is down or unhealthy using Alertmanager
- Automatically recover the service using Ansible playbook via a webhook

---

## **🛠️ Tools Used**

| Tool            | Purpose                                           |
|-----------------|-------------------------------------------------|
| NGINX           | Sample service to monitor and recover          |
| Prometheus      | Monitors service uptime and metrics             |
| Alertmanager    | Triggers alerts based on Prometheus conditions |
| Ansible         | Automates service recovery                       |
| Flask (Python)  | Webhook server to trigger Ansible playbook      |
| Docker          | Containerization of all services for easy setup |

---

## **📁 Project Structure**

```text
self-healing-demo/
├── prometheus.yml          # Prometheus main config
├── alert_rules.yml         # Prometheus alert rules
├── alertmanager.yml        # Alertmanager config
├── restart-nginx.yml       # Ansible playbook to restart NGINX
├── webhook_server.py       # Flask webhook listener
└── README.md

---

## **⚙️ Setup Instructions**

### **Step 1: Deploy NGINX**

```bash
docker run -d --name nginx-demo -p 8080:80 nginx
curl http://localhost:8080  # Should return NGINX welcome page
```

### **Step 2: Configure Prometheus**

Create `prometheus.yml`

### **Step 3: Define Alert Rules**

`alert_rules.yml`

---

### **Step 4: Run NGINX Exporter**

Expose metrics for Prometheus:

```bash
docker run -d --name nginx-exporter -p 9113:9113 nginx/nginx-prometheus-exporter:latest -nginx.scrape-uri http://host.docker.internal:8080/stub_status
```

---

### **Step 5: Setup Alertmanager**

`alertmanager.yml`

---

### **Step 6: Run Prometheus & Alertmanager**

```bash
docker run -d --name alertmanager -p 9093:9093 \
  -v $(pwd)/alertmanager.yml:/etc/alertmanager/alertmanager.yml \
  prom/alertmanager

docker run -d --name prometheus -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v $(pwd)/alert_rules.yml:/etc/prometheus/alert_rules.yml \
  prom/prometheus
```

---

### **Step 7: Setup Webhook Listener**

`webhook_server.py`

Run:

```bash
pip install flask
python3 webhook_server.py
```

---

### **Step 8: Create Ansible Playbook**

`restart-nginx.yml`

Test manually:

```bash
ansible-playbook restart-nginx.yml
```

---

### **Step 9: Simulate Failure**

Stop NGINX to test auto-healing:

```bash
docker stop nginx-demo
```

**Expected workflow:**

1. Prometheus detects “NginxDown”
2. Alertmanager fires alert → webhook
3. Flask receives POST → triggers Ansible
4. NGINX container is automatically restarted

---

## **📸 Screenshots / Logs to Capture**

1. **Prometheus Target (UP/DOWN)**

   * [ ] Screenshot when NGINX is UP
     (<img width="1366" height="768" alt="Screenshot (482)" src="https://github.com/user-attachments/assets/662793d8-b726-43b3-ae2c-1fe4c1b792b9" />)
   * [ ] Screenshot when NGINX is DOWN
     (<img width="1366" height="768" alt="Screenshot (483)" src="https://github.com/user-attachments/assets/082c216e-686d-4da9-98d6-9ec3c8574c78" />)

2. **Alertmanager Alert**

   * [ ] Screenshot showing “NginxDown” firing alert
     (<img width="1366" height="768" alt="Screenshot (484)" src="https://github.com/user-attachments/assets/8b5192e3-255b-470b-8c00-2b38bbae313d" />)

3. **Webhook Trigger**

   * [ ] Screenshot of Flask logs receiving POST
     (<img width="1366" height="768" alt="Screenshot (485)" src="https://github.com/user-attachments/assets/d5ea82d2-e15a-482e-a10e-e4f2af14d64e" />)

4. **NGINX Auto-Restart**

   * [ ] Screenshot of Ansible playbook running OR `docker ps` showing container UP
     (<img width="1366" height="768" alt="Screenshot (487)" src="https://github.com/user-attachments/assets/e19aa5cd-f016-44fe-b7e1-0aac771a57b3" />)

---

## **📖 Observations**

* The system automatically detects service failure.
* Alerts are triggered within ~15 seconds.
* Ansible playbook recovers the service without manual intervention.
* Can be extended for multiple services, CPU/memory thresholds, or cloud VMs.

---

## **⚡ Future Improvements**

* Integrate Slack/Email notifications in Alertmanager.
* Extend to multiple services or nodes.
* Add advanced metrics like CPU, memory usage.
* Implement retry logic in Ansible for failed recoveries.

---

## **🔗 References**

* [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
* [Alertmanager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
* [Ansible Documentation](https://docs.ansible.com/)
* [NGINX Prometheus Exporter](https://github.com/nginxinc/nginx-prometheus-exporter)

```

