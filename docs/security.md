# 🔐 Security & Observability Overview

This document outlines the security controls and observability measures implemented for the **Chocolate Factory QA Post-Add Platform (MVP)**.

The system is intentionally deployed as a **public demo environment** using fictitious data, while applying real-world safeguards to protect backend services and ensure auditability.

---

## 🎯 Security Design Goals
- Enable public access for recruiter review and portfolio demonstration
- Prevent abuse or accidental overload
- Ensure no sensitive data or credentials are exposed
- Provide monitoring, traceability, and audit visibility
- Clearly document planned security enhancements

---

## 🌐 Frontend Security (S3 Static Website)

- Hosted using **Amazon S3 static website hosting**
- Public **read-only access** to frontend assets (`index.html`, `app.js`, `styles.css`)
- No secrets, credentials, IAM roles, or account numbers stored in client-side code
- API communication strictly over **HTTPS**

### Acceptable Public Exposure
- API Gateway invoke URLs
- REST endpoint paths for demo functionality

These exposures are standard for public single-page applications.

---

## 🔌 API Gateway Protections

### Request Throttling
To prevent abuse and protect downstream services:
- **Rate limit:** 5 requests per second
- **Burst limit:** 10 requests

These limits are appropriate for a demo environment and significantly reduce risk from automated or malicious traffic.

### Transport Security
- HTTPS enforced for all endpoints
- No client certificates required (MVP scope)

---

## 📊 Logging & Monitoring

### CloudWatch Integration
- Configured an **account-level IAM role** allowing API Gateway to publish logs to Amazon CloudWatch
- Enabled **CloudWatch Logs** for the `Prod` stage
- Enabled **detailed metrics** for request tracking and error visibility

This provides:
- Audit trail for QA submissions
- Operational visibility into API behavior
- Diagnostics for failures and performance issues

---

## 🔐 IAM & Least Privilege

- API Gateway and Lambda functions operate under **least-privilege IAM roles**
- Logging permissions scoped specifically to CloudWatch
- No broad or wildcard permissions granted

---

## 🧪 Backend Validation Controls

- All input validation enforced **server-side** in AWS Lambda
- Strict type and range checks for QA measurements (temperature, viscosity, etc.)
- Invalid or malformed requests rejected before persistence

---

## 🔒 Authentication (Planned)

Authentication is intentionally **not enforced in the MVP** to avoid friction during demonstration.

### Planned Enhancements
- User authentication via **Amazon Cognito**
- Role-based access controls for QA technicians vs. analysts
- Optional API authorization enforcement

These enhancements are scheduled for a future sprint and documented in the project roadmap.

---

## 🧠 Security Philosophy

This project demonstrates a **balanced approach**:
- Public accessibility for learning and evaluation
- Backend protections to prevent misuse
- Clear documentation of current controls and future improvements

This mirrors real-world practices for exposing non-production systems safely.

---

## 📌 Summary of Controls

| Area | Control |
|------|--------|
| Frontend | No secrets, HTTPS only |
| API Gateway | Throttling, logging, metrics |
| Backend | Server-side validation |
| IAM | Least privilege |
| Monitoring | CloudWatch logs & metrics |
| Auth | Planned (Cognito) |

---

## 🚧 Future Security Enhancements
- Amazon Cognito authentication
- SNS alerts for critical QA failures
- CloudWatch alarms for error thresholds
- Optional CloudFront + AWS WAF
