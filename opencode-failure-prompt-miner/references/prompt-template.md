# Failure Guardrail Template

把以下區塊貼到需要的 system prompt、skill 規則、或工作提示中：

```text
<failure_guardrails>
- Before any read or edit, verify the exact path exists and prefer glob/search over guessing file paths.
- Before patching, reread the current file and anchor edits on live surrounding context instead of assuming earlier text still matches.
- Do not issue no-op edits. Compare the intended replacement first and only patch when the new content is actually different.
- If a tool aborts, inspect the exact failure, reduce the step size, and choose a deterministic fallback instead of retrying blindly.
- When the user is asking for explanation, analysis, or review, stay in analysis mode and do not edit unless they explicitly ask for changes.
- Treat 'do not change' and 'ignore this source' instructions as hard constraints and repeat them back before acting if there is any ambiguity.
</failure_guardrails>
```

## Usage Notes

- 這是基礎模板，建議仍用 helper script 依最近 session 資料重新產生
- 若某條 guardrail 長期沒有命中，可以考慮移除，避免提示膨脹
- 若新錯誤類型反覆出現，應回頭擴充 `mine_failures.py` 的 `LESSON_RULES`
