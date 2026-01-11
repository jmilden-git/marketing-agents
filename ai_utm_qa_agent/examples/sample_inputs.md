# Sample Inputs for AI UTM and Tag QA Agent

This file contains example URLs and parameter blocks to exercise the UTM QA agent.

Use these samples to verify parsing, validation, suggested corrections, and LLM summaries.

---

## 1. Valid and Near Valid URLs

### A1. Fully compliant email onboarding URL
```
https://example.com/welcome?utm_source=email&utm_medium=email&utm_campaign=fy25_onboarding_series
```

### A2. Paid search brand campaign
```
https://example.com/pricing?utm_source=paid_search&utm_medium=cpc&utm_campaign=fy25_brand_search
```

### A3. Paid social retargeting campaign
```
https://example.com/demo?utm_source=paid_social&utm_medium=social&utm_campaign=fy25_retarg_demo
```

---

## 2. Common Issues and Corrections

### B1. Missing medium and campaign
```
https://example.com/welcome?utm_source=email
```

### B2. Medium mismatch for email
```
https://example.com/welcome?utm_source=email&utm_medium=cpc&utm_campaign=fy25_onboarding_series
```

### B3. Invalid source value
```
https://example.com/demo?utm_source=newsletter&utm_medium=email&utm_campaign=q1_launch
```

### B4. Missing source, partially valid campaign
```
https://example.com/demo?utm_medium=email&utm_campaign=q1_launch
```

### B5. Non standard campaign naming
```
https://example.com/product?utm_source=paid_search&utm_medium=cpc&utm_campaign=spring_sales_push
```

---

## 3. Raw Query String Blocks

### C1. Clean email parameters
```
utm_source=email&utm_medium=email&utm_campaign=fy25_welcome_series
```

### C2. Paid search with missing campaign
```
utm_source=paid_search&utm_medium=cpc
```

### C3. Mixed casing and spacing
```
utm_source=Email&utm_medium=Email&utm_campaign=FY25_Welcome_Series
```

---

## 4. Edge Cases

### D1. URL with additional query parameters
```
https://example.com/welcome?page=1&ref=homepage&utm_source=email&utm_medium=email&utm_campaign=fy25_onboarding_series
```

### D2. UTM parameters in the fragment
```
https://example.com/welcome#utm_source=email&utm_medium=email&utm_campaign=fy25_onboarding_series
```

### D3. Duplicate UTM parameters
```
https://example.com/welcome?utm_source=email&utm_medium=email&utm_campaign=fy25_onboarding_series&utm_campaign=fy25_onboarding_series_v2
```

### D4. Completely missing UTM parameters
```
https://example.com/welcome
```

### D5. Non UTF-8 characters or encoding oddities
```
https://example.com/welcome?utm_source=email&utm_medium=email&utm_campaign=fy25_welc%C3%B6me
```
