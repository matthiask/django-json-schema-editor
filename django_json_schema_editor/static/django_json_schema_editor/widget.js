/* global django, JSONEditor */
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".django_json_schema_editor").forEach((el) => {
    let textarea = el.querySelector("textarea")
    if (textarea && !textarea.id.includes("__prefix__")) {
      initEditor(el)
    }
  })
})

document.addEventListener("DOMContentLoaded", () => {
  django.jQuery(document).on("formset:added", (event) => {
    event.target
      .querySelectorAll(".django_json_schema_editor")
      .forEach((el) => {
        initEditor(el)
      })
  })
})

const initEditor = (el) => {
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
