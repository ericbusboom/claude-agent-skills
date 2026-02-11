---
status: done
sprint: '005'
---
# TODO Frontmatter and Traceability

TODO files should have YAML frontmatter tracking their lifecycle state and
where they end up when consumed.

## Frontmatter for TODOs

When a TODO file is created (or split by `todo-split`), give it frontmatter:

```yaml
---
status: pending
---
```

When a TODO is consumed into a sprint, `move_todo_to_done` should update
the frontmatter before moving:

```yaml
---
status: done
sprint: "004"
tickets: ["003", "005"]
---
```

This creates traceability — you can look at any done TODO and see which
sprint and tickets addressed it.

## Changes needed

1. `todo-split` should add `status: pending` frontmatter to each split file.
2. `move_todo_to_done` should accept sprint ID and ticket IDs as parameters,
   write them into the frontmatter, then move the file.
3. `list_todos` should return the status from frontmatter.
