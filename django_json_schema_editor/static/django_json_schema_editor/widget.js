window.__djse_foreignKeys = {}

document.addEventListener("DOMContentLoaded", () => {
  const editors = document.querySelectorAll(".django_json_schema_editor")
  for (const el of editors) {
    const textarea = el.querySelector("textarea")
    if (textarea && !textarea.id.includes("__prefix__")) {
      initEditor(el)
    }
  }
})

document.addEventListener("DOMContentLoaded", () => {
  django.jQuery(document).on("formset:added", (event) => {
    const editors = event.target.querySelectorAll(".django_json_schema_editor")
    for (const el of editors) {
      initEditor(el)
    }
  })
})

const initEditor = (el) => {
  if (el.dataset.foreignKey) {
    Object.assign(window.__djse_foreignKeys, JSON.parse(el.dataset.foreignKey))
  }

  const input = el.querySelector("textarea")
  const config = JSON.parse(el.dataset.editorConfig)
  const editor = new JSONEditor(el, config)

  editor.on("ready", () => {
    const data = input.value ? JSON.parse(input.value) : null
    if (data) {
      editor.setValue(data)
    }
  })

  editor.on("change", () => {
    input.value = JSON.stringify(editor.getValue())
  })
}
