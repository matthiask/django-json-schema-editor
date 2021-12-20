/* global django, JSONEditor */
document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelectorAll(".inline-related:not(.empty-form) .jsoneditorwidget")
    .forEach((el) => {
      DjangoJSONEditorWidget.initWidget(el)
    })
})

document.addEventListener("DOMContentLoaded", () => {
  django.jQuery(document).on("formset:added", (event, $row, _formsetName) => {
    $row.get().forEach((el) => {
      el.querySelectorAll(".jsoneditorwidget").forEach((el) =>
        DjangoJSONEditorWidget.initWidget(el)
      )
    })
  })
})

const DjangoJSONEditorWidget = {
  initWidget: (el) => {
    DjangoJSONEditorWidget.initEditor(el)
    DjangoJSONEditorWidget.initDatafieldToggle(el)
  },
  initEditor: (el) => {
    const container = el.querySelector(".editor")
    const input = el.querySelector("textarea")
    const config = JSON.parse(el.dataset["editorConfig"])
    const editor = new JSONEditor(container, config)

    const data = input.value ? JSON.parse(input.value) : null
    if (data) {
      editor.setValue(data)
    }

    editor.on("change", () => {
      input.value = JSON.stringify(editor.getValue())
    })
  },
  initDatafieldToggle: (el) => {
    const toggle = el.querySelector(".datafield-toggle")
    const showText = toggle.dataset["showText"]
    const hideText = toggle.dataset["hideText"]
    const wrapper = el.querySelector(".datafield-wrapper")

    toggle.text = showText
    wrapper.classList.add("hidden")

    toggle.addEventListener("click", (e) => {
      e.preventDefault()

      if (wrapper.classList.contains("hidden")) {
        // show
        wrapper.classList.remove("hidden")
        toggle.text = hideText
      } else {
        // hide
        wrapper.classList.add("hidden")
        toggle.text = showText
      }
    })
  },
}
