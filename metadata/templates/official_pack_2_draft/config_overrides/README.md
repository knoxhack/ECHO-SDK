# Official Pack #2 Draft Config Notes

Pack #2 does not ship hard config overrides yet.

- Use `tech_normal` for ordinary internal MVP validation.
- Use `low_end_performance` for performance smoke checks.
- Keep future Pack #2 overrides namespaced in this template/profile, not in generic module defaults.
- DataCore persistence is not required in 1.0.0 because Pack #2 stores no Pack-specific save state yet.
- RuntimeGuard budget notes are advisory until heavier automation, route simulation, or world systems are added.
- Optional-module warnings should explain missing surfaces without leaking Pack #2 assumptions into reusable configs.
