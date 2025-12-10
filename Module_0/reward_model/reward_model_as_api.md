# Reward Model API – Example Requests

A collection of example HTTP requests (method, endpoint, and body) for the Reward Model API.
This README is formatted in Markdown and includes **general**, **healthcare**, **finance**, and **e-commerce** domain examples.
You can copy-paste these examples directly into Postman, curl, or any HTTP client.

---

## Table of Contents

1. [General Examples](#general-examples)
2. [Healthcare Domain](#healthcare-domain)
3. [Finance Domain](#finance-domain)
4. [E-commerce Domain](#e-commerce-domain)
5. [Health Check](#health-check)
6. [Usage Notes](#usage-notes)

---

## General Examples

### SET 1 — Score Single Response
**Method:** `POST`  
**Endpoint:** `/score`  
**Body (JSON):**
```json
{
  "prompt": "How do I learn Python programming?",
  "response": "Start with basic tutorials, practice daily, and build small projects."
}
```

---

### SET 2 — Score Single Response
**Method:** `POST`  
**Endpoint:** `/score`  
**Body (JSON):**
```json
{
  "prompt": "What is 2+2?",
  "response": "2+2 equals 4."
}
```

---

### SET 3 — Rank Multiple Responses
**Method:** `POST`  
**Endpoint:** `/rank`  
**Body (JSON):**
```json
{
  "prompt": "Explain what machine learning is.",
  "responses": [
    "Machine learning allows systems to learn patterns from data without explicit programming.",
    "It is something related to machines working.",
    "ML includes supervised, unsupervised, and reinforcement learning techniques.",
    "I don't know."
  ]
}
```

---

### SET 4 — Batch Score
**Method:** `POST`  
**Endpoint:** `/batch/score`  
**Body (JSON):**
```json
{
  "items": [
    {
      "prompt": "What is cloud computing?",
      "response": "Cloud computing delivers computing services over the internet."
    },
    {
      "prompt": "What is virtualization?",
      "response": "Virtualization creates virtual versions of hardware or software resources."
    }
  ]
}
```

---

## Healthcare Domain

### SET 5 — Score Response (Healthcare)
**Method:** `POST`  
**Endpoint:** `/score`  
**Body (JSON):**
```json
{
  "prompt": "What are the symptoms of diabetes?",
  "response": "Increased thirst, frequent urination, fatigue, and blurred vision are common symptoms."
}
```

---

### SET 6 — Score Response (Healthcare)
**Method:** `POST`  
**Endpoint:** `/score`  
**Body (JSON):**
```json
{
  "prompt": "How to reduce high cholesterol?",
  "response": "Eat a low-fat diet, exercise regularly, quit smoking, and follow doctor-prescribed medication."
}
```

---

### SET 7 — Rank Responses (Healthcare)
**Method:** `POST`  
**Endpoint:** `/rank`  
**Body (JSON):**
```json
{
  "prompt": "Explain what hypertension is.",
  "responses": [
    "Hypertension is high blood pressure that increases risk of heart disease.",
    "Hypertension is when you feel stressed.",
    "It means your blood pressure is consistently above normal levels.",
    "No idea."
  ]
}
```

---

### SET 8 — Batch Score (Healthcare)
**Method:** `POST`  
**Endpoint:** `/batch/score`  
**Body (JSON):**
```json
{
  "items": [
    {
      "prompt": "What is an MRI scan?",
      "response": "An MRI uses magnetic fields to generate detailed images of internal organs."
    },
    {
      "prompt": "What is a common treatment for flu?",
      "response": "Rest, hydration, and antiviral medications if prescribed."
    }
  ]
}
```

---

## Finance Domain

### SET 9 — Score Response (Finance)
**Method:** `POST`  
**Endpoint:** `/score`  
**Body (JSON):**
```json
{
  "prompt": "What is a mutual fund?",
  "response": "A mutual fund pools money from investors to buy a diversified portfolio of securities."
}
```

---

### SET 10 — Score Response (Finance)
**Method:** `POST`  
**Endpoint:** `/score`  
**Body (JSON):**
```json
{
  "prompt": "Explain compound interest.",
  "response": "Compound interest is interest earned on both the principal and previously accumulated interest."
}
```

---

### SET 11 — Rank Responses (Finance)
**Method:** `POST`  
**Endpoint:** `/rank`  
**Body (JSON):**
```json
{
  "prompt": "What is a credit score?",
  "responses": [
    "A credit score is a number that represents your creditworthiness.",
    "It is your bank balance.",
    "A financial indicator used by lenders to decide loan eligibility.",
    "I think it's something about credit cards."
  ]
}
```

---

### SET 12 — Batch Score (Finance)
**Method:** `POST`  
**Endpoint:** `/batch/score`  
**Body (JSON):**
```json
{
  "items": [
    {
      "prompt": "Define inflation.",
      "response": "Inflation is the rate at which general price levels rise over time."
    },
    {
      "prompt": "What is a bond?",
      "response": "A bond is a fixed-income investment where investors lend money to entities for interest returns."
    }
  ]
}
```

---

## E-commerce Domain

### SET 13 — Score Response (E-commerce)
**Method:** `POST`  
**Endpoint:** `/score`  
**Body (JSON):**
```json
{
  "prompt": "How can e-commerce businesses improve customer retention?",
  "response": "By offering personalized recommendations, fast delivery, loyalty programs, and great support."
}
```

---

### SET 14 — Rank Responses (E-commerce)
**Method:** `POST`  
**Endpoint:** `/rank`  
**Body (JSON):**
```json
{
  "prompt": "What causes shopping cart abandonment?",
  "responses": [
    "High shipping costs and complicated checkout processes.",
    "Customers get bored.",
    "Lack of payment options or unexpected fees.",
    "Not sure."
  ]
}
```

---

### SET 15 — Batch Score (E-commerce)
**Method:** `POST`  
**Endpoint:** `/batch/score`  
**Body (JSON):**
```json
{
  "items": [
    {
      "prompt": "What is dropshipping?",
      "response": "Dropshipping is a retail model where sellers don’t store inventory; suppliers ship products directly to customers."
    },
    {
      "prompt": "How can I increase product conversions?",
      "response": "Use high-quality images, clear descriptions, social proof, and competitive pricing."
    }
  ]
}
```

---

## Health Check

### SET 16 — Health Check
**Method:** `GET`  
**Endpoint:** `/health`  
**Body:**  
```
(no body required)
```

---

## Usage Notes

- Content-type for POST requests: `application/json`
- The `/batch/score` endpoint typically accepts up to 100 items per request (confirm with your server).
- Use `curl` or Postman to test these examples; replace `BASE_URL` as needed (e.g., `http://localhost:8000`).
- For ranking responses, results are typically returned as an array of objects with `response`, `score`, and `rank` fields.

---

## License & Attribution

Generated examples — adapt freely for testing and documentation.

