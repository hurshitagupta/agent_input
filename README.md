# Implementing Input

## Task 1 — Input Schema

### Objective

This task implements a clear input schema for user requests. The purpose is to ensure that the application accepts only the expected input structure and rejects invalid or protected fields.

### Implementation

The input schema is implemented using a Python `dataclass`:

```python
@dataclass
class InputRequest:
    text: str
```

The `parse_input()` function:

- Checks that the input is a dictionary.
- Checks that `text` is a string.
- Removes leading and trailing spaces from the text.
- Rejects empty text.
- Rejects protected fields supplied directly by the user.

The following fields are treated as protected:

- `tenant`
- `user`
- `locale`
- `policy`

These fields will later be added from trusted application context instead of being controlled by user input.

### Success Case

Example valid input:

```python
{
    "text": "Plan a report"
}
```

Expected result:

```text
InputRequest(text='Plan a report')
```

### Rejection Case

Example invalid input:

```python
{
    "text": "Plan a report", "tenant": "fake-tenant"
}
```

Expected result:

```text
Rejected: Protected fields cannot be supplied by user
```

This prevents the user from overriding protected application context.

### Run Command

Run the implementation using:

```powershell
python input_schema.py
```

### Automated Tests

Run the tests using:

```powershell
pytest tests/test_input_schema.py -v
```

The automated tests cover:

- Valid input is successfully parsed.
- Protected fields are rejected.
- Empty text is rejected.

### Evidence

Implementation output:

```text
outputs/input_schema.txt
```

Automated test output:

```text
outputs/test_input_schema.txt
```

### Guardrails

The following safeguards are implemented in this task:

- **Validation:** Input type, text type, and required text are checked.
- **Protected fields:** User input cannot directly set `tenant`, `user`, `locale`, or `policy`.
- **Safe failure:** Invalid input raises a clear `ValueError`.
- **Secret hygiene:** No credentials or secrets are stored in the source code.

Step limits, retry, and timeout are not required for the local schema parser because it performs a single synchronous operation without loops, external services, or transient failures.

---

## Task 2 — Normalization

### Objective

This task implements input normalization so that user text is converted into a consistent and clean format before further validation or processing.

### Implementation

The normalization logic is implemented in `normalization.py`.

The task reuses the `InputRequest` schema from Task 1 and applies the following normalization steps:

- Normalizes Unicode text into a consistent form.
- Removes leading and trailing spaces.
- Replaces repeated spaces with a single space.
- Converts tabs and newlines into normal spacing.
- Rejects input that becomes empty after normalization.

The existing `InputRequest` schema is reused instead of creating another input structure.

### Example

Raw input:

```text
"   Plan    a
report     for   sales   "
```

Normalized result:

```text
"Plan a report for sales"
```

The text content is preserved while unnecessary whitespace is removed.

### Success Case

Example input:

```python
InputRequest(
    text="   Plan    a\nreport\tfor   sales   "
)
```

Expected normalized result:

```text
InputRequest(text='Plan a report for sales')
```

### Rejection Case

Whitespace-only input is rejected because it contains no usable text after normalization.

Expected result:

```text
Rejected: text is empty after normalization
```

### Run Command

Run the implementation using:

```powershell
python normalization.py
```

### Automated Tests

Run the tests using:

```powershell
pytest tests/test_normalization.py -v
```

The tests cover:

- Text with repeated whitespace is normalized correctly.
- Already clean text remains unchanged.
- Whitespace-only text is rejected.

### Evidence

Implementation output:

```text
outputs/normalization.txt
```

Automated test output:

```text
outputs/test_normalization.txt
```

### Guardrails

The following safeguards are demonstrated in this task:

- **Validation:** Normalization only accepts string input.
- **Empty input protection:** Text that becomes empty after normalization is rejected.
- **Safe normalization:** Text content is preserved while unnecessary whitespace and inconsistent Unicode formatting are normalized.
- **Failure handling:** Invalid normalized input raises a clear `ValueError`.
- **Secret hygiene:** No credentials or secrets are stored in the source code.

Step limits, timeout, and retry are not applicable to this task because normalization is a single local string-processing operation with no loops, external services, or transient failures.

---

## Task 3 — Validation

### Objective

This task implements validation rules for the normalized input. The goal is to ensure that only valid input within the allowed limits continues to later processing.

### Implementation

The validation logic is implemented in `validation.py`.

The task reuses the `InputRequest` object from Task 1 and works with normalized input from Task 2.

The following validation rules are applied:

- `text` must be a string.
- `text` cannot be empty.
- `text` must not exceed 2000 characters.

The maximum length is defined as:

```python
MAX_TEXT_LENGTH = 2000
```

A `ValidationResult` object is returned for valid input and includes:

- validation status,
- text length,
- validation message.

### Success Case

Example valid input:

```text
Plan a monthly sales report
```

Expected result:

```text
Valid: True
Message: Input passed validation
```

The actual text length is also recorded as part of the result.

### Boundary Case

An input containing exactly:

```text
2000 characters
```

is accepted.

This verifies that the configured limit itself is valid.

### Rejection Case

An input containing more than 2000 words is rejected.

Expected result:

```text
Rejected: text must be <= 2000 characters
```

Empty text is also rejected with:

```text
text is required
```

### Run Command

Run the implementation using:

```powershell
python validation.py
```

### Automated Tests

Run the tests using:

```powershell
pytest tests/test_validation.py -v
```

The tests cover:

- Normal valid input passes validation.
- Input with exactly 2000 characters is accepted.
- Input with more than 2000 characters is rejected.
- Empty text is rejected.

### Evidence

Implementation output:

```text
outputs/validation.txt
```

Automated test output:

```text
outputs/test_validation.txt
```

### Measurement

The validation result records the actual input character count.

This provides measurable evidence for the configured input-size limit.

Example:

```text
Text length: 27
Valid: True
```

For a rejected request:

```text
Text length: 2001
Rejected: text must be <= 2000 characters
```
---

## Task 4 — Context Enrichment

### Objective

This task enriches validated user input with trusted application context.

The protected context includes:

- `tenant`
- `user`
- `locale`
- `request_id`
- `policy`

These values are not taken from user input. They are added from trusted application context so the user cannot override protected fields.

### Implementation

The context enrichment logic is implemented in `context_enrichment.py`.

A separate `TrustedContext` object is used for protected application values:

```python
@dataclass
class TrustedContext:
    tenant: str
    user: str
    locale: str
    policy: str
```

The final enriched input contains both the user request and trusted context:

```python
@dataclass
class EnrichedInput:
    request_id: str
    text: str
    tenant: str
    user: str
    locale: str
    policy: str
    provenance: dict[str, str]
```

Before enrichment, the input is validated using the validation logic from Task 3.

A unique request ID is generated by the system using `uuid4()`.

### Protected Context

The following values come from trusted sources:

```text
tenant      -> trusted_context
user        -> trusted_context
locale      -> trusted_context
policy      -> trusted_context
request_id  -> system_generated
```

The user-provided text remains:

```text
text -> user_input
```

This prevents the user from overriding protected application context.

### Provenance

The source of every field is recorded in a provenance dictionary.

Example:

```python
{
    "text": "user_input",
    "request_id": "system_generated",
    "tenant": "trusted_context",
    "user": "trusted_context",
    "locale": "trusted_context",
    "policy": "trusted_context"
}
```

This keeps the origin of each value visible and traceable.

### Success Case

Example trusted context:

```python
TrustedContext(
    tenant="demo-tenant",
    user="user-101",
    locale="en-IN",
    policy="standard-policy"
)
```

The provenance of each field is also displayed.

### Rejection Case

If required trusted context is missing, the request is rejected.

### Run Command

Run the implementation using:

```powershell
python context_enrichment.py
```

### Automated Tests

Run the tests using:

```powershell
pytest tests/test_context_enrichment.py -v
```

The tests cover:

- Trusted context is added successfully.
- A request ID is generated.
- Provenance is recorded correctly.
- Missing trusted tenant is rejected.

### Evidence

Implementation output:

```text
outputs/context_enrichment.txt
```

Automated test output:

```text
outputs/test_context_enrichment.txt
```

### Traceability

The task keeps the source of each field visible.

This provides traceable evidence showing which values came from the user and which came from trusted application context.

### Guardrails

The following safeguards are implemented:

- **Validation:** Input is validated before context enrichment.
- **Protected fields:** Tenant, user, locale, policy, and request ID are not controlled by the user.
- **Trusted context validation:** Required trusted fields cannot be empty.
- **Provenance:** The source of each field is recorded.
- **Failure handling:** Missing trusted context raises a clear `ValueError`.
- **Secret hygiene:** No credentials or secrets are stored in source code.


