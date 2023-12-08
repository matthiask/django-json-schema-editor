/* global django, JSONEditor */
document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelectorAll(
      ".inline-related:not(.empty-form) .django_json_schema_editor",
    )
    .forEach((el) => {
      initEditor(el)
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
  const container = el.querySelector(".editor")
  const input = el.querySelector("textarea")
  const config = JSON.parse(el.dataset.editorConfig)
  console.debug(container, config)
  const editor = new JSONEditor(container, config)

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
