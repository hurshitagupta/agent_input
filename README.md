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
