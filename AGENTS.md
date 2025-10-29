# Coding Rules

## Core Principles

### 1. Minimal Code Approach
- Write only the **minimum code necessary** to achieve functionality
- Remove all defensive programming and validation unless absolutely critical
- Fail fast - let errors bubble up naturally instead of catching and wrapping them
- No unnecessary abstractions or layers

### 2. Comments Policy
- **No "what" comments** - the code should be self-explanatory
- **Minimal "why" comments** - only when reading the code alone is insufficient to understand the reasoning
- Prefer clear variable/function names over comments
- If you need many comments, the code is probably too complex

### 3. Error Handling
- Don't wrap every operation in try/catch
- Let exceptions propagate unless you have a specific recovery strategy
- Prefer `raise` over returning error objects when possible
- Only handle errors at the appropriate boundary level

### 4. Code Structure
- Direct execution over complex validation
- Simple conditionals over elaborate state machines
- Explicit over implicit behavior
- One responsibility per function/class

### 5. Examples

**Bad (defensive):**
```python
def process_data(data):
    if not data:
        return {"error": "No data provided", "success": False}
    try:
        result = complex_validation(data)
        if not result.is_valid():
            return {"error": "Validation failed", "success": False}
        processed = expensive_operation(result)
        return {"data": processed, "success": True}
    except Exception as e:
        return {"error": f"Processing failed: {e}", "success": False}
```

**Good (minimal):**
```python
def process_data(data):
    validated = validate(data)  # Raises if invalid
    return expensive_operation(validated)
```

### 6. When to Add Comments
- Complex business logic that isn't obvious
- Performance optimizations with non-obvious reasoning
- Workarounds for external system quirks
- Regulatory or compliance requirements

### 7. When NOT to Add Comments
- Explaining what a variable stores
- Describing obvious operations
- Documenting API signatures (use type hints instead)
- Explaining basic programming concepts

### 8. Object-Oriented Design
- **Single Responsibility**: Each class should have one clear purpose
- **Composition over Inheritance**: Prefer composition and delegation
- **Separation of Concerns**: Extract complex logic into separate classes/files
- **Avoid Over-Engineering**: Don't create methods with single-line implementations

### 9. Refactoring Guidelines
- **Extract when complex**: Move complex logic to separate classes
- **Keep it simple**: Prefer direct code over unnecessary abstractions
- **Organize by responsibility**: Separate files for different concerns
- **Test the refactor**: Ensure functionality remains the same

### 9.1 Minimal, Readability-First Refactors
- Favor fewer moving parts and fewer lines over feature breadth
- Prefer cohesive objects with clear data flow over granular helpers
- Keep state in a single, obvious place (e.g., one messages list for chat)
- Remove validations unless they unlock real recovery paths
- Ship only what is essential; delete dead code and comments

### 10. Python Naming Conventions
- **No get/set prefixes** - avoid Java-style `get_text()` or `set_value()`
- Use simple method names: `text()` instead of `get_text()`
- Use `@property` decorators for attribute-like access when appropriate
- Keep method names short and descriptive
- **No is/has prefixes for boolean attributes** - use direct names
  - ❌ `is_active`, `has_permission` (verbose)
  - ✅ `active`, `permitted` (Pythonic)
- **Use specific types, avoid `Any`** - import and use the actual type
  - ❌ `def create_client(self) -> Any:`
  - ✅ `def create_client(self) -> BaseChatModel:`

**Bad (Java-style):**
```python
class Response:
    def get_text(self):
        return self._text

    def set_text(self, value):
        self._text = value
```

**Good (Pythonic):**
```python
class Response:
    def text(self):
        return self._text

    # Or even better with property:
    @property
    def text(self):
        return self._text
```

### 11. Avoid Unpredictable Return Types
- Methods should return consistent, predictable types
- Avoid returning different types based on conditions (e.g., `dict | str | None`)
- If a method can fail, return `None` or raise an exception - don't return different types
- Use explicit control flow (if/else) instead of complex type unions

**Bad (unpredictable):**
```python
def parse_content(text: str) -> dict | str | bool:
    try:
        parsed = json.loads(text)
        return parsed, True  # Tuple sometimes
    except:
        return text  # String other times
```

**Good (predictable):**
```python
def try_parse_json(text: str) -> dict | None:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None

# Then use explicit control flow:
json_content = try_parse_json(text)
if json_content:
    # Handle structured content
    self.structured = True
else:
    # Handle plain text
    self.structured = False
```

### 12. Readability Through Steps
- Break complex logic into clear, sequential steps
- Each step should be obvious and self-documenting
- Prefer multiple simple lines over clever one-liners
- Let the flow of the code tell the story

**Bad (complex):**
```python
self._content, self.structured = self._parse(text) or (text, False)
```

**Good (clear steps):**
```python
json_content = self._try_parse_json(text)

if json_content:
    self._content = json_content
    self.structured = True
else:
    self._content = text
    self.structured = False
```

### 13. Git and Commits
- **NEVER suggest commits** unless explicitly asked
- Only commit when user explicitly requests it
- Don't propose commit messages or git operations
- Focus on code changes, not version control workflow
- **Never add "Generated with Claude Code" or similar AI signatures** to commit messages
  - Keep commit messages clean and professional
  - No "Co-Authored-By: Claude" or similar attribution
