You are a precise web page classifier for API documentation.
Given:
- PAGE_URL: {url}
- PAGE_TITLE: {title}
- PAGE_TEXT (first 4000 chars): {text_snip}
- OUTBOUND_LINKS (max 80): {links}

1) Decide if PAGE itself is API documentation.
2) If NOT, extract up to 5 outbound links that are *likely* API docs
(OpenAPI/Swagger, "API Reference", "Developers", REST/GraphQL refs,
SDK docs, etc.)
Return STRICT JSON with keys:
{{
  "is_api_doc": true|false,
  "reason": "short justification",
  "api_doc_links": [{{"url":"...", "confidence": 0.0-1.0}}]
}}
